#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import sys
if sys.executable.endswith("pythonw.exe"):
 sys.stdout=open(os.devnull,"w");
 sys.stderr=open(os.path.join(os.getenv("TEMP"),"stderr-"+os.path.basename(sys.argv[0])),"w")
else:
 import logmatic
 import logging
 I=logging.getLogger()
 X=logging.StreamHandler()
 I.addHandler(X)
 I.setLevel(logging.DEBUG)
import traceback
import codecs
from kivy import Config
Config.set('graphics','multisamples','0')
import kivy
from kivy.core.audio import SoundLoader
kivy.require('1.0.6') 
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.properties import ObjectProperty,StringProperty
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.graphics import Color,Rectangle
from kivy.uix.listview import ListView
from kivy.uix.label import Label
from kivy.uix.listview import ListItemButton
from kivy.adapters.listadapter import ListAdapter
from vaisdemo.EvaluateTruecaser import MyTrueCaser
from vaisdemo.async_gui.engine import Task,MultiProcessTask
from vaisdemo.async_gui.toolkits.kivy import KivyEngine
import rollbar
import operator
from vaisdemo.custom_dialog import LoadDialog,LoadDialog_MIC,LoadDialog_API_INPUT,SaveDialog,DataItem
from vaisdemo.info import info
from vaisdemo.audio_token import audio_token
import wave
import time
import vaisdemo.vais as vais
import threading
from kivy.lang import Builder
l=KivyEngine()
rollbar.init('a24f6683ad064d768538cbf9b0e20930','production') 
Window.clearcolor=(1,1,float(204)/255,1)
j=os.path.dirname(os.path.abspath(__file__))
w=""
if os.name!="posix":
 from win32com.shell import shellcon,shell
 w="{}\\".format(shell.SHGetFolderPath(0,shellcon.CSIDL_APPDATA,0,0))
else:
 w="{}/".format(os.path.expanduser("~"))
Builder.load_file(os.path.join(j,"ui.kv"))
O=32768
S=lambda row_index,obj:{'text':obj.text if not obj.mark else '[b]'+obj.text+'[/b]','size_hint_y':None,'markup':True,'height':25}
def internet_on():
 import urllib
 Y="https://google.com"
 try:
  urllib.request.urlopen(Y,timeout=1)
  return True
 except urllib.request.URLError:
  return False
class Io(FloatLayout):
 W=StringProperty()
 C=StringProperty()
 o=ObjectProperty()
 G=ObjectProperty()
 D=ObjectProperty()
 u=ObjectProperty()
 B=ObjectProperty()
 s=ObjectProperty()
 p=None
 R=ObjectProperty()
 def __init__(v,*args,**Q):
  super(Io,v).__init__()
  v.selected_mic=None
  v.vais_engine=None
  v.config=Q["config"]
  v.file_path=None 
  v.tokenizer=None
  v.observer=None
  v.init()
  v.true_caser=d()
  v.prev_warn=""
  v.done_loading_model=False
  Clock.schedule_interval(v.get_mic_volume,0.1)
  Clock.schedule_interval(v.check_connection_status,0.5)
 @l.async
 def init_params(v):
  v.asr_result="Preparing ..."
  try:
   yield H(v.true_caser.load_model)
   v.done_loading_model=True
  except Exception as e:
   rollbar.report_exc_info()
  v.asr_result="Ready!"
  if v.config.get("user","report")=="yes" and v.config.get("user","apikey")!="":
   i=v.config.get("user","apikey")
   info.get_system_info(i)
   v.config.set("user","report","no")
 def init(v):
  if v.btn_start:v.btn_start.on_press=v.start
  if v.btn_stop:v.btn_stop.on_press=v.stop
  if v.btn_stop:
   v.btn_stop.disabled=True
   v.btn_stop.color=(0,0,0,1)
  v.conn_status="[color=000000]...[/color]"
 def select_file_dialog(v):
  if v.file_path:
   v.run_asr_on_file(v.file_path)
   return
  U=LoadDialog(load=v.load_file,cancel=v.dismiss_popup)
  v._popup=r(title="Load file",content=U,size_hint=(0.9,0.9))
  v._popup.open()
 def dismiss_popup(v):
  v._popup.dismiss()
 def progress(v,x,text=None,is_finished=False):
  if x==-1:
   v.asr_result=text
   v.stop()
   return
  if v.progress_result:
   v.progress_result.value=x
  if text:
   v.asr_result=text
  if is_finished:
   v.enable_start_btn()
   if v.output_csv:
    with codecs.open(v.output_csv,'w',"utf-8")as f:
     import csv
     T=['start','end','text']
     E=csv.DictWriter(f,fieldnames=T)
     E.writeheader()
     F=sorted(v.observer.results.items(),key=operator.itemgetter(0))
     for q,(end_time,text)in F:
      text=v.true_caser.evaluateTrueCaser(text)
      E.writerow({'start':q,'end':end_time,'text':text})
    v.output_csv=None
   v.enable_start_btn()
 def disable_start_btn(v):
  v.btn_start.disabled=True
  v.btn_stop.disabled=False
  v.btn_start.color=(0,0,0,1)
  v.btn_stop.color=(1,1,1,1)
 def enable_start_btn(v):
  v.btn_start.disabled=False
  v.btn_stop.disabled=True
  v.btn_stop.text="Stop"
  v.btn_start.text="Start"
  v.btn_start.color=(1,1,1,1)
  v.btn_stop.color=(0,0,0,1)
 def load_file(v,path,filename):
  if not filename:
   return
  v.progress_result.value=0
  v.asr_result="Started!"
  M=os.path.join(path,filename[0])
  v._popup.dismiss()
  v.run_asr_on_file(M)
 def check_api_key(v):
  V=v.config.get("user","apikey")
  if not V:
   v.asr_result="API key không tồn tại, ấn F1 để nhập mã API key!"
  return V
 @l.async
 def run_asr_on_file(v,M):
  if v.progress_result:
   v.progress_result.value=0
  V=v.check_api_key()
  if not V:
   return
  y=os.path.splitext(os.path.basename(M))[0]
  v.output_csv=os.path.join(os.path.dirname(M),y+".csv")
  v.disable_start_btn()
  v.tokenizer,v.observer=yield H(audio_token.segment_audio,M,V,callback=v.progress)
  if v.tokenizer and v.observer:
   v.observer.start()
   v.asr_result="Audio segmentation ..."
   v.tokenizer.start()
 def from_mic(v):
  print("Started")
  L=[]
  v.label_result.text_size=(None,None)
  def on_result(b,is_final):
   if b:
    b=b.replace("<SPOKEN_NOISE>","").strip()
    if v.done_loading_model:
     b=v.true_caser.evaluateTrueCaser(b)
    A=b.split()
    if len(A)>15:
     e=0
     N=[]
     for s in range(0,len(A),15):
      e=s+15
      N.append(" ".join(A[s:e]))
     b="\n".join(N)
   if b:
    m=[]
    if not is_final:
     m=L+[b]
    else:
     L.append(b)
     m=L
    v.asr_result="\n".join(m)
    h=len(v.asr_result.split())
    if h>180 or len(m)>10:
     v.label_result.text_size=(None,v.label_result.height)
  v.disable_start_btn()
  V=v.config.get("user","apikey")
  f=time.time()
  try:
   with vais.VaisService(V,mic_name=self.selected_mic)as v.vais_engine:
    v.vais_engine.asr_callback=on_result
    v.vais_engine.asr()
  except Exception as e:
   rollbar.report_exc_info()
   v.asr_result=e.message
  if v.asr_thread:
   v.vais_engine.capture._interrupt=True
  e=time.time()
  if(e-f<1)and(not L):
   v.asr_result="Lỗi kết nối, có thể mã API của bạn đã hết hiệu lực. \nXin vui lòng liên hệ với chúng tôi qua địa chỉ email [color=000000]support@vais.vn[/color] \nđể được hỗ trợ!"
  v.asr_result+=". Done!"
  v.btn_start.disabled=False
  v.btn_stop.disabled=True
  v.btn_start.color=(1,1,1,1)
  v.btn_stop.color=(0,0,0,1)
 def stop_token(v):
  v.btn_stop.text="Stopping"
  if v.tokenizer is not None:
   print("Stopping tokenizer")
   v.tokenizer.stop()
  if v.observer is not None:
   print("Stopping observer")
   v.observer.stop()
  v.tokenizer=None
  v.observer=None
  v.enable_start_btn()
 @l.async
 def start(v):
  V=v.check_api_key()
  if not V:
   return
  if not internet_on():
   v.asr_result="Couldn't connect to the Internet!"
   return
  J=v.config.get("user","long_audio")
  if J and J not in["0","False"]:
   v.select_file_dialog()
  else:
   yield H(v.from_mic)
 def stop(v):
  t=threading.Thread(target=v.stop_token)
  t.start()
  if v.vais_engine:
   v.vais_engine.capture._interrupt=True
 def get_mic_volume(v,dt):
  if hasattr(v,"vais_engine"):
   if v.vais_engine:
    if v.graph_mic:
     v.graph_mic.canvas.after.clear()
     with v.graph_mic.canvas.after:
      K=v.graph_mic.size[0]
      n=v.vais_engine.volume
      z=n*K/O
      t(pos=v.graph_mic.pos,size=(z,10))
 def check_connection_status(v,dt):
  if v.vais_engine:
   if v.vais_engine.capture._queue:
    Il=v.vais_engine.capture._queue.qsize()
    if Il>50:
     v.n_slow+=1
     v.n_unstable+=1
    elif Il>15:
     v.n_slow=0
     v.n_unstable+=1
    else:
     v.n_unstable=0
     v.n_slow=0
    if v.n_slow>5:
     Ij=" [color=c10000][b]Slow[/b][/color]"
    elif v.n_unstable>5:
     Ij="[color=a34c00][b]Unstable[/b][/color]"
    else:
     Ij="[color=000000]OK[/color]"
    if v.prev_warn!=Ij:
     v.prev_warn=Ij
     v.conn_status=Ij
 def on_stop(v):
  v.stop_token()
class ID(App):
 Iw=False
 def build_config(v,IO):
  IO.setdefaults('user',{'apikey':'','report':'yes','long_audio':False})
 def build_settings(v,IY):
  IS="""[
    {"type": "string", "title": "API key", "desc": "Nhập API key của bạn vào đây", "section": "user", "key": "apikey" },
    {"type": "bool", "title": "Kích hoạt chức năng gỡ băng", "desc": "Chức năng gỡ băng", "section": "user", "key": "long_audio"}
    ]"""  
  IY.add_json_panel('VAIS Setting',v.config,data=IS)
  IY.interface.menu.width=kivy.metrics.dp(100)
 def _on_file_drop(v,window,IW):
  v.c.file_path=IW
  print("File selected ",IW)
  v.c.asr_result=IW
 def on_config_change(v,IO,section,key,value):
  if IO is v.config:
   IC=(section,key)
   pass
 def on_start(v):
  v.c.init_params()
 def get_application_config(v):
  return super(ID,v).get_application_config('~/.vais.ini')
 def build(v):
  v.icon=os.path.join(j,'icon.png')
  v.title='VAIS Demo'
  IO=v.config
  v.c=Io(asr_result='Demo nhận dạng tiếng nói tiếng Việt của VAIS!',config=IO)
  return v.c
Factory.register('LoadDialog',cls=LoadDialog)
Factory.register('SaveDialog',cls=SaveDialog)
def main():
 try:
  ID().run()
 except Exception as e:
  traceback.print_exc(file=sys.stdout)
  rollbar.report_exc_info()
if __name__=='__main__':
 main()

