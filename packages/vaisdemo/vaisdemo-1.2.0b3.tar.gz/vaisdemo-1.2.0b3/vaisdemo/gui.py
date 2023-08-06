#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Truong Do <truongdq54@gmail.com>
#
from __future__ import print_function
import os
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
from vaisdemo.EvaluateTruecaser import evaluateTrueCaser, load_model

import vaisdemo.capture as capture

import wave
import time

import sys
import vaisdemo.vais as vais
import threading
from kivy.lang import Builder



Window.clearcolor = (1, 1, float(204) / 255, 1)
root_dir = os.path.dirname(os.path.abspath(__file__))
Builder.load_file(os.path.join(root_dir, "ui.kv"))
max_vol = 32768
device_info = capture.DeviceInfo()

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class LoadDialog_MIC(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class LoadDialog_API_INPUT(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

class DataItem(object):
    def __init__(self, text='', is_selected=False):
        self.text = text
        self.is_selected = is_selected
        self.mark = False

list_item_args_converter = lambda row_index, obj: {'text': obj.text if not obj.mark else '[b]' + obj.text + '[/b]',
                                                   'size_hint_y': None,
                                                   'markup': True,
                                                   'height': 25}

class Controller(FloatLayout):
    '''Create a controller that receives a custom widget from the kv lang file.

    Add an action to be called from the kv lang file.
    '''
    asr_result = StringProperty()
    conn_status = StringProperty()
    btn_start = ObjectProperty()
    btn_change_api_key = ObjectProperty()
    list_view_mic = ObjectProperty()
    api_input = ObjectProperty()
    label_result = ObjectProperty()
    btn_load_audio_file = ObjectProperty()
    btn_stop = ObjectProperty()
    asr_thread = None
    graph_mic = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super(Controller, self).__init__(*args, **kwargs)
        Clock.schedule_interval(self.get_mic_volume, 0.1)
        Clock.schedule_interval(self.check_data_queue, 0.5)
        self.selected_mic = None
        self.vais_engine = None
        self.api_key_path = os.path.join(root_dir, "apikey.dat")
        self.init()
        self.n_slow = 0
        self.n_good = 0
        self.n_unstable = 0
        self.prev_warn = ""
        self.done_loading_model = False
        t = threading.Thread(target=self.load_truecaser_model)
        t.start()

    def load_truecaser_model(self):
        self.asr_result = "Preparing ..."
        try:
            load_model()
            self.done_loading_model = True
        except Exception as e:
            print(e)
        self.asr_result = "Ready!"

    def init(self):
        if self.btn_start: self.btn_start.on_press = self.start
        if self.btn_stop: self.btn_stop.on_press = self.stop
        if self.btn_load_audio_file: self.btn_load_audio_file.on_press = self.show_dialog
        if self.btn_change_api_key: self.btn_change_api_key.on_press = self.show_api_dialog
        if self.btn_stop:
            self.btn_stop.disabled = True
            self.btn_stop.color = (0, 0, 0, 1)
        self.conn_status = "[color=000000]...[/color]"

    def check_data_queue(self, dt):
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

    def show_mic_dialog(self):
        devices = [DataItem(x) for x in device_info.get_device_list(input_only=True)]
        devices.reverse()
        for d in devices:
            if self.selected_mic and self.selected_mic == d.text:
                d.mark = True
            else:
                d.mark = False

        class CustomListItemButton(ListItemButton):
            selected_color = (0, 0, 1, 1)
            deselected_color = (0, 0, 0, 1)

        list_adapter = ListAdapter(data=devices,
                                   args_converter=list_item_args_converter,
                                   propagate_selection_to_data=True,
                                   cls=CustomListItemButton)
        list_adapter.bind(on_selection_change=self.set_mic)
        content = LoadDialog_MIC(load=self.set_mic, cancel=self.dismiss_popup)
        content.list_view_mic.adapter = list_adapter
        self._popup = Popup(title="Select an input audio device", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load_api_key(self, api_key):
        open(self.api_key_path, "w").write(api_key)
        self.dismiss_popup()

    def show_api_dialog(self):
        content = LoadDialog_API_INPUT(load=self.load_api_key)
        cur_api_key = ""
        if os.path.exists(self.api_key_path):
            cur_api_key = open(self.api_key_path).readline().strip()
        content.api_input.text = cur_api_key
        self._popup = Popup(title="Nhập mã API key của bạn", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def show_dialog(self):
        content = LoadDialog(load=self.load_file, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def dismiss_popup(self):
        self._popup.dismiss()

    def set_mic(self, adapter):
        self.dismiss_popup()
        for device in adapter.data:
            if device.is_selected:
                print("Selected mic:", device.text)
                self.selected_mic = device.text

    def load_file(self, path, filename):
        if not filename:
            return
        full_path = os.path.join(path, filename[0])
        self._popup.dismiss()
        sound = SoundLoader.load(full_path)
        if sound:
            sound.play()
            self.asr_result = "ASR started"
            if self.asr_thread:
                self.vais_engine.capture._interrupt = True
            self.asr_thread = threading.Thread(target=self.run_asr,kwargs={'filename': full_path})
            self.asr_thread.start()
        else:
            self.asr_result = "Cannot decode audio file. Only 16Khz, mono audio is accepted!"

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

    def run_asr(self, filename=None):
        final_text = []
        self.label_result.text_size = (None, None)
        def on_result(output, is_final):
            if output:
                output = output.replace("<SPOKEN_NOISE>", "").strip()
                if self.done_loading_model:
                    output = evaluateTrueCaser(output)
                words = output.split()
                if len(words) > 15:
                    e = 0
                    new_words = []
                    for s in range(0, len(words), 15):
                        e = s + 15
                        new_words.append(" ".join(words[s:e]))
                    output = "\n".join(new_words)
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
        self.btn_start.disabled = True
        # self.btn_load_audio_file.disabled = True
        self.btn_stop.disabled = False
        self.btn_start.color = (0, 0, 0, 1)
        # self.btn_load_audio_file.color = (0, 0, 0, 1)
        self.btn_stop.color = (1, 1, 1, 1)
        cur_api_key = open(self.api_key_path).readline().strip()
        try:
            with vais.VaisService(cur_api_key, mic_name=self.selected_mic) as self.vais_engine:
                self.vais_engine.asr_callback = on_result
                self.vais_engine.asr(filename=filename)
        except Exception as e:
            print(e)
            self.asr_result = e.message
        if self.asr_thread:
            self.vais_engine.capture._interrupt = True
        e_time = time.time()
        if (e_time - s_time < 1) and (not final_text):
            self.asr_result = "Lỗi kết nối, có thể mã API của bạn đã hết hiệu lực. \nXin vui lòng liên hệ với chúng tôi qua địa chỉ email [color=000000]support@vais.vn[/color] \nđể được hỗ trợ!"

        self.asr_result += ". Done!"
        self.btn_start.disabled = False
        self.btn_stop.disabled = True
        self.btn_start.color = (1, 1, 1, 1)
        # self.btn_load_audio_file.color = (1, 1, 1, 1)
        self.btn_stop.color = (0, 0, 0, 1)

    def start(self):
        s_time = time.time()
        if not os.path.exists(self.api_key_path):
            self.show_api_dialog()
            return
        cur_api_key = open(self.api_key_path).readline().strip()
        if not cur_api_key:
            self.show_api_dialog()
            return
        self.asr_result = "ASR started"
        if self.asr_thread and self.vais_engine:
            self.vais_engine.capture._interrupt = True
        self.asr_thread = threading.Thread(target=self.run_asr)
        self.asr_thread.start()

    def stop(self):
        if self.asr_thread:
            if self.vais_engine:
                self.vais_engine.capture._interrupt = True
        self.btn_start.disabled = False
        self.btn_stop.disabled = True
        # self.btn_load_audio_file.disabled = False
        self.btn_start.color = (1, 1, 1, 1)
        # self.btn_load_audio_file.color = (1, 1, 1, 1)
        self.btn_stop.color = (0, 0, 0, 1)



class ControllerApp(App):

    def build(self):
        return Controller(asr_result='Demo nhận dạng tiếng nói tiếng Việt của VAIS!')

Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)

def main():
    ControllerApp().run()

if __name__ == '__main__':
    main()
