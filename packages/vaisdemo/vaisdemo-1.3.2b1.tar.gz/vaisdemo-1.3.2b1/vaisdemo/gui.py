#! /usr/bin/env python
# -*- coding: utf-8 -*-
Ω=open
ߜ=float
ﯕ=None
씼=True
𢦬=False
𥭫=super
𞤊=Exception
𐛚=sorted
ﱘ=print
ﰰ=len
ݼ=range
ꝕ=hasattr
from __future__ import print_function
import os
𐦲=os.name
𤡳=os.getenv
乬=os.path
𞺘=os.devnull
import sys
𠲷=sys.argv
𪜼=sys.stderr
瀋=sys.stdout
玜=sys.executable
if 玜.endswith("pythonw.exe"):
 瀋=Ω(𞺘,"w");
 𪜼=Ω(乬.join(𤡳("TEMP"),"stderr-"+乬.basename(𠲷[0])),"w")
else:
 import logmatic
 import logging
 ﶮ=logging.getLogger()
 𬡓=logging.StreamHandler()
 ﶮ.addHandler(𬡓)
 ﶮ.setLevel(logging.DEBUG)
import traceback
𐣦=traceback.print_exc
import codecs
𧝘=codecs.Ω
from kivy import Config
𦂊=Config.set
𦂊('graphics','multisamples','0')
import kivy
𞺓=kivy.metrics
𐩲=kivy.lang
𞠆=kivy.adapters
ﺪ=kivy.graphics
𐬎=kivy.clock
ﶬ=kivy.factory
𧠙=kivy.properties
ߞ=kivy.app
𑚠=kivy.uix
𐔙=kivy.require
ᦇ=kivy.core
from ᦇ.audio import SoundLoader
𐔙('1.0.6') 
from 𑚠.floatlayout import FloatLayout
from ߞ import App
from 𧠙 import ObjectProperty,StringProperty
from ᦇ.window import Window
ﵗ=Window.clearcolor
from ﶬ import Factory
럖=Factory.register
from 𑚠.popup import Popup
from 𐬎 import Clock
䳫=Clock.schedule_interval
from ﺪ import Color,Rectangle
from 𑚠.listview import ListView
from 𑚠.label import Label
from 𑚠.listview import ListItemButton
from 𞠆.listadapter import ListAdapter
from vaisdemo.EvaluateTruecaser import MyTrueCaser
from vaisdemo.async_gui.engine import Task,MultiProcessTask
from vaisdemo.async_gui.toolkits.kivy import KivyEngine
import rollbar
ὐ=rollbar.report_exc_info
𣮷=rollbar.init
import operator
䴷=operator.itemgetter
from vaisdemo.custom_dialog import LoadDialog,LoadDialog_MIC,LoadDialog_API_INPUT,SaveDialog,DataItem
from vaisdemo.info import info
ڎ=info.get_system_info
from vaisdemo.audio_token import audio_token
ㄏ=audio_token.segment_audio
import wave
import time
刯=time.time
import vaisdemo.vais as vais
import threading
𞺆=threading.Thread
from 𐩲 import Builder
囉=Builder.load_file
𣦤=KivyEngine()
𣮷('a24f6683ad064d768538cbf9b0e20930','production') 
ﵗ=(1,1,ߜ(204)/255,1)
𡙆=乬.dirname(乬.abspath(__file__))
𐦔=""
if 𐦲!="posix":
 from win32com.shell import shellcon,shell
 𐦔="{}\\".format(shell.SHGetFolderPath(0,shellcon.CSIDL_APPDATA,0,0))
else:
 𐦔="{}/".format(乬.expanduser("~"))
囉(乬.join(𡙆,"ui.kv"))
𐲑=32768
ݠ=lambda row_index,obj:{'text':obj.text if not obj.mark else '[b]'+obj.text+'[/b]','size_hint_y':ﯕ,'markup':씼,'height':25}
def ᬘ():
 import urllib
 𞢭="https://google.com"
 try:
  urllib.request.urlopen(𞢭,timeout=1)
  return 씼
 except urllib.request.URLError:
  return 𢦬
class ﴃ(FloatLayout):
 ﮌ=StringProperty()
 ﲿ=StringProperty()
 ﻰ=ObjectProperty()
 ﶉ=ObjectProperty()
 댊=ObjectProperty()
 麜=ObjectProperty()
 슕=ObjectProperty()
 𐰊=ObjectProperty()
 ﰇ=ﯕ
 ࡄ=ObjectProperty()
 def __init__(𞺔,*args,**𑀖):
  𥭫(ﴃ,𞺔).__init__()
  𞺔.selected_mic=ﯕ
  𞺔.vais_engine=ﯕ
  𞺔.config=𑀖["config"]
  𞺔.file_path=ﯕ 
  𞺔.tokenizer=ﯕ
  𞺔.observer=ﯕ
  𞺔.缜()
  𞺔.true_caser=𝞝()
  𞺔.prev_warn=""
  𞺔.done_loading_model=𢦬
  䳫(𞺔.ﱼ,0.1)
  䳫(𞺔.뿚,0.5)
 @𣦤.async
 def ﱥ(𞺔):
  𞺔.asr_result="Preparing ..."
  try:
   yield 罖(𞺔.true_caser.load_model)
   𞺔.done_loading_model=씼
  except 𞤊 as 㵩:
   ὐ()
  𞺔.asr_result="Ready!"
  if 𞺔.config.get("user","report")=="yes" and 𞺔.config.get("user","apikey")!="":
   ڻ=𞺔.config.get("user","apikey")
   ڎ(ڻ)
   𞺔.config.set("user","report","no")
 def 缜(𞺔):
  if 𞺔.btn_start:𞺔.btn_start.on_press=𞺔.𬯇
  if 𞺔.btn_stop:𞺔.btn_stop.on_press=𞺔.멱
  if 𞺔.btn_stop:
   𞺔.btn_stop.disabled=씼
   𞺔.btn_stop.color=(0,0,0,1)
  𞺔.conn_status="[color=000000]...[/color]"
 def 𪴉(𞺔):
  if 𞺔.file_path:
   𞺔.ᮐ(𞺔.file_path)
   return
  톑=LoadDialog(load=𞺔.𐬔,cancel=𞺔.𞢯)
  𞺔._popup=𧷠(title="Load file",content=톑,size_hint=(0.9,0.9))
  𞺔._popup.Ω()
 def 𞢯(𞺔):
  𞺔._popup.dismiss()
 def 𞹲(𞺔,𪫪,text=ﯕ,is_finished=𢦬):
  if 𪫪==-1:
   𞺔.asr_result=text
   𞺔.멱()
   return
  if 𞺔.progress_result:
   𞺔.progress_result.value=𪫪
  if text:
   𞺔.asr_result=text
  if is_finished:
   𞺔.ߜ()
   if 𞺔.output_csv:
    with 𧝘(𞺔.output_csv,'w',"utf-8")as f:
     import csv
     𐭩=['start','end','text']
     ﳯ=csv.DictWriter(f,fieldnames=𐭩)
     ﳯ.writeheader()
     䢟=𐛚(𞺔.observer.results.items(),key=䴷(0))
     for 綝,(end_time,text)in 䢟:
      text=𞺔.true_caser.evaluateTrueCaser(text)
      ﳯ.writerow({'start':綝,'end':end_time,'text':text})
    𞺔.output_csv=ﯕ
   𞺔.ߜ()
 def 𞺱(𞺔):
  𞺔.btn_start.disabled=씼
  𞺔.btn_stop.disabled=𢦬
  𞺔.btn_start.color=(0,0,0,1)
  𞺔.btn_stop.color=(1,1,1,1)
 def ߜ(𞺔):
  𞺔.btn_start.disabled=𢦬
  𞺔.btn_stop.disabled=씼
  𞺔.btn_stop.text="Stop"
  𞺔.btn_start.text="Start"
  𞺔.btn_start.color=(1,1,1,1)
  𞺔.btn_stop.color=(0,0,0,1)
 def 𐬔(𞺔,path,filename):
  if not filename:
   return
  𞺔.progress_result.value=0
  𞺔.asr_result="Started!"
  𐫞=乬.join(path,filename[0])
  𞺔._popup.dismiss()
  𞺔.ᮐ(𐫞)
 def 𫀹(𞺔):
  𞠤=𞺔.config.get("user","apikey")
  if not 𞠤:
   𞺔.asr_result="API key không tồn tại, ấn F1 để nhập mã API key!"
  return 𞠤
 @𣦤.async
 def ᮐ(𞺔,𐫞):
  if 𞺔.progress_result:
   𞺔.progress_result.value=0
  𞠤=𞺔.𫀹()
  if not 𞠤:
   return
  ﴞ=乬.splitext(乬.basename(𐫞))[0]
  𞺔.output_csv=乬.join(乬.dirname(𐫞),ﴞ+".csv")
  𞺔.𞺱()
  𞺔.tokenizer,𞺔.observer=yield 罖(ㄏ,𐫞,𞠤,callback=𞺔.𞹲)
  if 𞺔.tokenizer and 𞺔.observer:
   𞺔.observer.start()
   𞺔.asr_result="Audio segmentation ..."
   𞺔.tokenizer.start()
 def 퇄(𞺔):
  ﱘ("Started")
  𞸍=[]
  𞺔.label_result.text_size=(ﯕ,ﯕ)
  def 𤋉(𞸝,is_final):
   if 𞸝:
    𞸝=𞸝.replace("<SPOKEN_NOISE>","").strip()
    if 𞺔.done_loading_model:
     𞸝=𞺔.true_caser.evaluateTrueCaser(𞸝)
    ࡀ=𞸝.split()
    if ﰰ(ࡀ)>15:
     㵩=0
     ܣ=[]
     for s in ݼ(0,ﰰ(ࡀ),15):
      㵩=s+15
      ܣ.append(" ".join(ࡀ[s:㵩]))
     𞸝="\n".join(ܣ)
   if 𞸝:
    𞡻=[]
    if not is_final:
     𞡻=𞸍+[𞸝]
    else:
     𞸍.append(𞸝)
     𞡻=𞸍
    𞺔.asr_result="\n".join(𞡻)
    ﳠ=ﰰ(𞺔.asr_result.split())
    if ﳠ>180 or ﰰ(𞡻)>10:
     𞺔.label_result.text_size=(ﯕ,𞺔.label_result.height)
  𞺔.𞺱()
  𞠤=𞺔.config.get("user","apikey")
  𐡠=刯()
  try:
   with vais.VaisService(𞠤,mic_name=self.selected_mic)as 𞺔.vais_engine:
    𞺔.vais_engine.asr_callback=𤋉
    𞺔.vais_engine.asr()
  except 𞤊 as 㵩:
   ὐ()
   𞺔.asr_result=㵩.message
  if 𞺔.asr_thread:
   𞺔.vais_engine.capture._interrupt=씼
  𨪤=刯()
  if(𨪤-𐡠<1)and(not 𞸍):
   𞺔.asr_result="Lỗi kết nối, có thể mã API của bạn đã hết hiệu lực. \nXin vui lòng liên hệ với chúng tôi qua địa chỉ email [color=000000]support@vais.vn[/color] \nđể được hỗ trợ!"
  𞺔.asr_result+=". Done!"
  𞺔.btn_start.disabled=𢦬
  𞺔.btn_stop.disabled=씼
  𞺔.btn_start.color=(1,1,1,1)
  𞺔.btn_stop.color=(0,0,0,1)
 def 𡢉(𞺔):
  𞺔.btn_stop.text="Stopping"
  if 𞺔.tokenizer is not ﯕ:
   ﱘ("Stopping tokenizer")
   𞺔.tokenizer.stop()
  if 𞺔.observer is not ﯕ:
   ﱘ("Stopping observer")
   𞺔.observer.stop()
  𞺔.tokenizer=ﯕ
  𞺔.observer=ﯕ
  𞺔.ߜ()
 @𣦤.async
 def 𬯇(𞺔):
  𞠤=𞺔.𫀹()
  if not 𞠤:
   return
  if not ᬘ():
   𞺔.asr_result="Couldn't connect to the Internet!"
   return
  犾=𞺔.config.get("user","long_audio")
  if 犾 and 犾 not in["0","False"]:
   𞺔.𪴉()
  else:
   yield 罖(𞺔.퇄)
 def 멱(𞺔):
  𝒵=𞺆(target=𞺔.𡢉)
  𝒵.𬯇()
  if 𞺔.vais_engine:
   𞺔.vais_engine.capture._interrupt=씼
 def ﱼ(𞺔,dt):
  if ꝕ(𞺔,"vais_engine"):
   if 𞺔.vais_engine:
    if 𞺔.graph_mic:
     𞺔.graph_mic.canvas.after.clear()
     with 𞺔.graph_mic.canvas.after:
      ﰳ=𞺔.graph_mic.size[0]
      騜=𞺔.vais_engine.volume
      𐢝=騜*ﰳ/𐲑
      ﻧ(pos=𞺔.graph_mic.pos,size=(𐢝,10))
 def 뿚(𞺔,dt):
  if 𞺔.vais_engine:
   if 𞺔.vais_engine.capture._queue:
    𧊖=𞺔.vais_engine.capture._queue.qsize()
    if 𧊖>50:
     𞺔.n_slow+=1
     𞺔.n_unstable+=1
    elif 𧊖>15:
     𞺔.n_slow=0
     𞺔.n_unstable+=1
    else:
     𞺔.n_unstable=0
     𞺔.n_slow=0
    if 𞺔.n_slow>5:
     𧄝=" [color=c10000][b]Slow[/b][/color]"
    elif 𞺔.n_unstable>5:
     𧄝="[color=a34c00][b]Unstable[/b][/color]"
    else:
     𧄝="[color=000000]OK[/color]"
    if 𞺔.prev_warn!=𧄝:
     𞺔.prev_warn=𧄝
     𞺔.conn_status=𧄝
 def 𨟩(𞺔):
  𞺔.𡢉()
class 𘤠(App):
 ﲄ=𢦬
 def 𐡮(𞺔,ﴯ):
  ﴯ.setdefaults('user',{'apikey':'','report':'yes','long_audio':𢦬})
 def 𦄻(𞺔,㱘):
  𞡶="""[
    {"type": "string", "title": "API key", "desc": "Nhập API key của bạn vào đây", "section": "user", "key": "apikey" },
    {"type": "bool", "title": "Kích hoạt chức năng gỡ băng", "desc": "Chức năng gỡ băng", "section": "user", "key": "long_audio"}
    ]"""  
  㱘.add_json_panel('VAIS Setting',𞺔.config,data=𞡶)
  㱘.interface.menu.width=𞺓.dp(100)
 def 𐤸(𞺔,window,𪛕):
  𞺔.c.file_path=𪛕
  ﱘ("File selected ",𪛕)
  𞺔.c.asr_result=𪛕
 def 𐭡(𞺔,ﴯ,section,key,value):
  if ﴯ is 𞺔.config:
   𥸸=(section,key)
   pass
 def 𬒥(𞺔):
  𞺔.c.init_params()
 def 𫼶(𞺔):
  return 𥭫(𘤠,𞺔).get_application_config('~/.vais.ini')
 def ﺺ(𞺔):
  𞺔.icon=乬.join(𡙆,'icon.png')
  𞺔.title='VAIS Demo'
  ﴯ=𞺔.config
  𞺔.c=ﴃ(asr_result='Demo nhận dạng tiếng nói tiếng Việt của VAIS!',config=ﴯ)
  return 𞺔.c
럖('LoadDialog',cls=LoadDialog)
럖('SaveDialog',cls=SaveDialog)
def ﶒ():
 try:
  𘤠().run()
 except 𞤊 as 㵩:
  𐣦(file=瀋)
  ὐ()
if __name__=='__main__':
 ﶒ()

