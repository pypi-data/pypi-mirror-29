from __future__ import print_function
import logging
import time
import threading
import os
import sys
if sys.version_info[0]<3:
 import Queue
else:
 import queue as Queue
os.environ["PA_ALSA_PLUGHW"]="1"
import pyaudio 
g=logging.getLogger(__name__)
class ConfigurationException(Exception):
 pass
class f(object):
 b=None
 def __init__(V):
  V._pa=pyaudio.PyAudio()
 def get_device_list(V,input_only=False):
  z=[]
  for i in range(V._pa.get_device_count()):
   if(not input_only)or(input_only and V._pa.get_device_info_by_index(i)['maxInputChannels']>0):
    z.append(V._pa.get_device_info_by_index(i)['name'])
  return z
 def get_device_index(V,name):
  if not name:
   return None
  return V.get_device_list().index(name)
 def get_device_name(V,idx):
  if idx is None:
   return None
  return V.get_device_list()[idx]
 def __del__(V):
  V._pa.terminate()
class Capture(object):
 C=120
 J=16000
 l=20
 v=int((J/1000)*l)
 D=1000
 x=10
 b=None
 B=False
 L=None
 G=None
 Y=None
 A=None
 h=None
 W=None
 O=None
 N=None
 E=None
 r=None
 q=False
 s=None
 def __init__(V,y,U):
  V._config=y
  V._tmp_path=U
  if not os.path.exists(U):
   os.makedirs(U)
  V._pa=pyaudio.PyAudio()
  V._queue=Queue.Queue()
  V._device_info=f()
  V._recording_lock_inverted=threading.Event()
  V._recording_lock_inverted.set()
  if('input_device' not in y['sound'])and('input_device_name' not in y['sound']):
   raise Exception("Device must be set")
  V.validate_config()
 def validate_config(V):
  u=V._config['sound']['input_device']
  j=V._device_info.get_device_list(False)
  if u and(u not in j):
   raise ConfigurationException("Your input_device '"+u+"' is invalid. Use one of the following:\n"+'\n'.join(j))
 def setup(V,t):
  V._state_callback=t
 def cleanup(V):
  g.debug("Cleaning up capture")
  if not V._recording_lock_inverted.isSet():
   V._interrupt=True
   V._recording_lock_inverted.wait()
  V._pa.terminate()
 def handle_init(V,rate,m):
  V._handle=V._pa.open(input=True,input_device_index=V._device_info.get_device_index(V._config['sound']['input_device']),format=pyaudio.paInt16,channels=1,rate=rate,frames_per_buffer=m)
  V._handle_chunk_size=m
 def handle_read(V):
  return V._handle.read(V._handle_chunk_size,exception_on_overflow=V._pa_exception_on_overflow)
 def handle_release(V):
  V._handle.close()
 def _callback(V,k,frame_count,time_info,status): 
  o=logging.getLogger('alexapi').getEffectiveLevel()==logging.DEBUG
  p=False
  if p and(V._callback_data['frames']<V._callback_data['throwaway_frames']):
   V._callback_data['frames']+=1
  elif(V._callback_data['force_record']and V._callback_data['force_record'][0]()) or(p and(V._callback_data['thresholdSilenceMet']is False)and((time.time()-V._callback_data['start'])<V.MAX_RECORDING_LENGTH)):
   if p:
    if int(len(k)/2)==V.VAD_PERIOD:
     F=V._vad.is_speech(k,V.VAD_SAMPLERATE)
     if not F:
      V._callback_data['silenceRun']+=1
     else:
      V._callback_data['silenceRun']=0
      V._callback_data['numSilenceRuns']+=1
    if(V._callback_data['numSilenceRuns']!=0) and((V._callback_data['silenceRun']*V.VAD_FRAME_MS)>V.VAD_SILENCE_TIMEOUT):
     V._callback_data['thresholdSilenceMet']=True
  V._queue.put(k)
  if o:
   V._callback_data['audio']+=k
  return None,pyaudio.paContinue
 def silence_listener(V,throwaway_frames=None,force_record=None):
  g.debug("Recording: Setting up")
  V._recording_lock_inverted.clear()
  o=logging.getLogger('alexapi').getEffectiveLevel()==logging.DEBUG
  if V._state_callback:
   V._state_callback()
  V._queue.queue.clear()
  V._callback_data={'start':time.time(),'thresholdSilenceMet':False,'frames':0,'throwaway_frames':throwaway_frames or V.VAD_THROWAWAY_FRAMES,'numSilenceRuns':0,'silenceRun':0,'force_record':force_record,'audio':b'' if o else False,}
  d=V._pa.open(input=True,input_device_index=V._device_info.get_device_index(V._config['sound']['input_device']),format=pyaudio.paInt16,channels=1,rate=V.VAD_SAMPLERATE,frames_per_buffer=V.VAD_PERIOD,stream_callback=V._callback,start=False)
  g.debug("Recording: Start")
  d.start_stream()
  def _listen():
   while True:
    try:
     w=V._queue.get(block=True,timeout=2)
     if not w or V._interrupt:
      break
     yield w
    except Queue.Empty:
     break
   d.stop_stream()
   g.debug("Recording: End")
   d.close()
   if V._state_callback:
    V._state_callback(False)
   if o:
    with open(V._tmp_path+'/recording.wav','wb')as rf:
     rf.write(V._callback_data['audio'])
   V._recording_lock_inverted.set()
  return _listen()

