#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Truong Do <truongdq54@gmail.com>
#
from __future__ import print_function
import os
import sys


if sys.executable.endswith("pythonw.exe"):
    sys.stdout = open(os.devnull, "w");
    sys.stderr = open(os.path.join(os.getenv("TEMP"), "stderr-"+os.path.basename(sys.argv[0])), "w")
else:
    import logmatic
    import logging
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
import traceback
import codecs
# add the following 2 lines to solve OpenGL 2.0 bug
from kivy import Config
Config.set('graphics', 'multisamples', '0')
import kivy
from kivy.core.audio import SoundLoader

kivy.require('1.0.6')  # replace with your current kivy version !

from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.listview import ListView
from kivy.uix.label import Label
from kivy.uix.listview import ListItemButton
from kivy.adapters.listadapter import ListAdapter
from vaisdemo.EvaluateTruecaser import MyTrueCaser
from vaisdemo.async_gui.engine import Task, MultiProcessTask
from vaisdemo.async_gui.toolkits.kivy import KivyEngine
import rollbar
import operator

from vaisdemo.custom_dialog import LoadDialog, LoadDialog_MIC, LoadDialog_API_INPUT, SaveDialog, DataItem
from vaisdemo.info import info
from vaisdemo.audio_token import audio_token

import wave
import time

import vaisdemo.vais as vais
import threading
from kivy.lang import Builder


engine = KivyEngine()
rollbar.init('a24f6683ad064d768538cbf9b0e20930', 'production')  # access_token, environment
Window.clearcolor = (1, 1, float(204) / 255, 1)

root_dir = os.path.dirname(os.path.abspath(__file__))
home_dir = ""
if os.name != "posix":
    from win32com.shell import shellcon, shell
    home_dir = "{}\\".format(shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0))
else:
    home_dir = "{}/".format(os.path.expanduser("~"))
Builder.load_file(os.path.join(root_dir, "ui.kv"))
max_vol = 32768

list_item_args_converter = lambda row_index, obj: {'text': obj.text if not obj.mark else '[b]' + obj.text + '[/b]',
                                                   'size_hint_y': None,
                                                   'markup': True,
                                                   'height': 25}


def internet_on():
    import urllib
    reference = "https://google.com"
    try:
        urllib.request.urlopen(reference, timeout=1)
        return True
    except urllib.request.URLError:
        return False

class Controller(FloatLayout):
    asr_result = StringProperty()
    conn_status = StringProperty()
    btn_start = ObjectProperty()
    api_input = ObjectProperty()
    label_result = ObjectProperty()
    progress_result = ObjectProperty()
    btn_load_audio_file = ObjectProperty()
    btn_stop = ObjectProperty()
    asr_thread = None
    graph_mic = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super(Controller, self).__init__()
        self.selected_mic = None
        self.vais_engine = None
        self.config = kwargs["config"]
        self.file_path = None # Audio filepath
        self.tokenizer = None
        self.observer = None
        self.init()
        self.true_caser = MyTrueCaser()
        self.prev_warn = ""
        self.done_loading_model = False
        Clock.schedule_interval(self.get_mic_volume, 0.1)
        Clock.schedule_interval(self.check_connection_status, 0.5)

    @engine.async
    def init_params(self):
        self.asr_result = "Preparing ..."
        try:
            yield Task(self.true_caser.load_model)
            self.done_loading_model = True
        except Exception as e:
            rollbar.report_exc_info()
        self.asr_result = "Ready!"

    @engine.async
    def write_info(self):
        api_key = self.config.get("user", "apikey")
        yield Task(info.get_system_info, api_key)

    def init(self):
        if self.btn_start: self.btn_start.on_press = self.start
        if self.btn_stop: self.btn_stop.on_press = self.stop
        if self.btn_stop:
            self.btn_stop.disabled = True
            self.btn_stop.color = (0, 0, 0, 1)
        self.conn_status = "[color=000000]...[/color]"

    def select_file_dialog(self):
        if self.file_path:
            self.run_asr_on_file(self.file_path)
            return
        content = LoadDialog(load=self.load_file, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def dismiss_popup(self):
        self._popup.dismiss()

    def progress(self, done_percentage, text=None, is_finished=False, confidence=None):
        if done_percentage == -1:
            # Something went wrong with loading audio
            self.asr_result = text
            self.stop()
            return
        if self.progress_result:
            self.progress_result.value = done_percentage
        if text:
            self.asr_result = text
        if is_finished:
            self.enable_start_btn()
            if self.output_csv:
                with codecs.open(self.output_csv, 'w', "utf-8") as f:
                    import csv
                    fieldnames = ['start', 'end', 'text']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    sorted_x = sorted(self.observer.results.items(), key=operator.itemgetter(0))
                    for start_time, (end_time, text) in sorted_x:
                        text = self.true_caser.evaluateTrueCaser(text)
                        writer.writerow({'start': start_time, 'end': end_time, 'text': text})
                self.output_csv = None
            self.enable_start_btn()

    def disable_start_btn(self):
        self.btn_start.disabled = True
        self.btn_stop.disabled = False
        self.btn_start.color = (0, 0, 0, 1)
        self.btn_stop.color = (1, 1, 1, 1)

    def enable_start_btn(self):
        self.btn_start.disabled = False
        self.btn_stop.disabled = True
        self.btn_stop.text = "Stop"
        self.btn_start.text = "Start"
        self.btn_start.color = (1, 1, 1, 1)
        self.btn_stop.color = (0, 0, 0, 1)

    def load_file(self, path, filename):
        if not filename:
            return
        self.progress_result.value = 0
        self.asr_result = "Started!"
        full_path = os.path.join(path, filename[0])
        self._popup.dismiss()
        self.run_asr_on_file(full_path)

    def check_api_key(self):
        cur_api_key = self.config.get("user", "apikey")
        if not cur_api_key:
            self.asr_result = "API key không tồn tại, ấn F1 để nhập mã API key!"
        return cur_api_key

    @engine.async
    def run_asr_on_file(self, full_path):
        if self.progress_result:
            self.progress_result.value = 0
        cur_api_key = self.check_api_key()
        if not cur_api_key:
            return
        list_file = []
        if os.path.isdir(full_path):
            for root, dirs, files in os.walk(full_path):
                for fname in files:
                    abs_fname = os.path.join(root, fname)
                    for audio_type in ["wav", "mp3", "mp4", "wma", "ogg"]:
                        if audio_type in os.path.splitext(os.path.basename(fname))[-1]:
                            list_file.append(abs_fname)
                break
        else:
            list_file.append(full_path)

        server_url = self.config.get("user", "server_url")
        for full_path in list_file[:4]:
            basename = os.path.splitext(os.path.basename(full_path))[0]
            self.output_csv = os.path.join(os.path.dirname(full_path), basename + ".csv")
            self.disable_start_btn()
            self.tokenizer, self.observer = yield Task(audio_token.segment_audio, full_path, cur_api_key, callback=self.progress, server_url=server_url)
            if self.tokenizer and self.observer:
                self.observer.start()
                self.asr_result = "Processing file " + basename
                self.tokenizer.start()
            break  # Only decode 1 file, we will have to comeup with a way to wait, otherwise it will start 4 x len(list_file) connection
            # has to wait here


    def from_mic(self):
        final_text = []
        self.label_result.text_size = (None, None)
        def on_result(output, is_final, confidence=None, **kwargs):
            if output:
                if self.done_loading_model:
                    output = self.true_caser.evaluateTrueCaser(output)
                words = output.split()
                if confidence:
                    for idx, (w, c) in enumerate(zip(words, confidence)):
                        if c < 0.6:
                            w = "[color=a06f1b]" + w + "[/color]"
                        words[idx] = w

                if len(words) > 15:
                    e = 0
                    new_words = []
                    for s in range(0, len(words), 15):
                        e = s + 15
                        new_words.append(" ".join(words[s:e]))
                    words = new_words
                    output = "\n".join(words)
                else:
                    output = " ".join(words)
            if output:
                print_text = []
                if not is_final:
                    print_text = final_text + [output]
                else:
                    final_text.append(output)
                    print_text = final_text
                self.asr_result = "\n".join(print_text)
                w_count = len(self.asr_result.split())
                if w_count > 180 or len(print_text) > 10:
                    self.label_result.text_size = (None, self.label_result.height)
        self.disable_start_btn()
        cur_api_key = self.config.get("user", "apikey")
        s_time = time.time()
        server_url = self.config.get("user", "server_url")
        try:
            with vais.VaisService(cur_api_key, mic_name=self.selected_mic, server_url=server_url) as self.vais_engine:
                self.vais_engine.asr_callback = on_result
                self.vais_engine.asr()
        except Exception as e:
            rollbar.report_exc_info()
            self.asr_result = "Cannot connect to the server!"
        if self.asr_thread:
            self.vais_engine.capture._interrupt = True
        e_time = time.time()
        if (e_time - s_time < 1) and (not final_text):
            self.asr_result = "Lỗi kết nối, có thể mã API của bạn đã hết hiệu lực. \nXin vui lòng liên hệ với chúng tôi qua địa chỉ email [color=000000]support@vais.vn[/color] \nđể được hỗ trợ!"

        self.asr_result += ". Done!"
        self.btn_start.disabled = False
        self.btn_stop.disabled = True
        self.btn_start.color = (1, 1, 1, 1)
        self.btn_stop.color = (0, 0, 0, 1)

    def stop_token(self):
        self.btn_stop.text = "Stopping"
        if self.tokenizer is not None:
            self.tokenizer.stop()
        if self.observer is not None:
            self.observer.stop()
        self.tokenizer = None
        self.observer = None
        self.enable_start_btn()

    @engine.async
    def start(self):
        cur_api_key = self.check_api_key()
        if not cur_api_key:
            return
        # self.asr_result = "Checking connection ..."
        if not internet_on():
            self.asr_result = "Couldn't connect to the Internet!"
            return
        long_audio = self.config.get("user", "long_audio")
        if long_audio and long_audio not in ["0", "False"]:
            self.select_file_dialog()
        else:
            yield Task(self.from_mic)
            # self.asr_thread = threading.Thread(target=self.from_mic)
            # self.asr_thread.start()

    def stop(self):
        t = threading.Thread(target=self.stop_token)
        t.start()
        if self.vais_engine:
            self.vais_engine.capture._interrupt = True

    def get_mic_volume(self, dt):
        if hasattr(self, "vais_engine"):
            if self.vais_engine:
                if self.graph_mic:
                    self.graph_mic.canvas.after.clear()
                    with self.graph_mic.canvas.after:
                        max_y = self.graph_mic.size[0]
                        raw_vol = self.vais_engine.volume
                        cur_vol = raw_vol * max_y / max_vol
                        Rectangle(pos=self.graph_mic.pos, size=(cur_vol, 10))

    def check_connection_status(self, dt):
        if self.vais_engine:
            if self.vais_engine.capture._queue:
                data_queue = self.vais_engine.capture._queue.qsize()
                if data_queue > 50:
                    self.n_slow += 1
                    self.n_unstable += 1
                elif data_queue > 15:
                    self.n_slow = 0
                    self.n_unstable += 1
                else:
                    self.n_unstable = 0
                    self.n_slow = 0
                if self.n_slow > 5:
                    message = " [color=c10000][b]Slow[/b][/color]"
                elif self.n_unstable > 5:
                    message = "[color=a34c00][b]Unstable[/b][/color]"
                else:
                    message = "[color=000000]OK[/color]"
                if self.prev_warn != message:
                    self.prev_warn = message
                    self.conn_status = message

    def on_stop(self):
        self.stop_token()

class VaisLongAudioApp(App):
    use_kivy_settings = False
    def build_config(self, config):
        config.setdefaults('user', {
            'apikey': '',
            'report': 'yes',
            'long_audio': False,
            'server_url': 'service.grpc.vais.vn:50051'
        })

    def build_settings(self, settings):
        jsondata = """[
    { "type": "string",
      "title": "API key",
      "desc": "Nhập API key của bạn vào đây",
      "section": "user",
      "key": "apikey" },
    { "type": "bool",
      "title": "Kích hoạt chức năng gỡ băng",
      "desc": "Chức năng gỡ băng",
      "section": "user",
      "key": "long_audio"}
    ]"""
        settings.add_json_panel('VAIS Setting', self.config, data=jsondata)
        settings.interface.menu.width = kivy.metrics.dp(100)

    def _on_file_drop(self, window, file_path):
        self.c.file_path = file_path
        self.c.asr_result = file_path

    def on_config_change(self, config, section, key, value):
        if config is self.config:
            token = (section, key)
            if token == ("user", "apikey"):
                print("API key change, update info")
                self.c.write_info()

    def on_start(self):
        self.c.init_params()

    def get_application_config(self):
        return super(VaisLongAudioApp, self).get_application_config(
                         '~/.vais.ini')
    def build(self):
        self.icon = os.path.join(root_dir, 'icon.png')
        self.title = 'VAIS Demo'
        config = self.config
        self.c = Controller(asr_result='Demo nhận dạng tiếng nói tiếng Việt của VAIS!', config=config)
        return self.c

Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)

def main():
    try:
        VaisLongAudioApp().run()
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        rollbar.report_exc_info()

if __name__ == '__main__':
    main()
