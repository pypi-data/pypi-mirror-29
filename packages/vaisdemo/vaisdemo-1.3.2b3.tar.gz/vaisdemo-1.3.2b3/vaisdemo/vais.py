from __future__ import print_function
import uuid
import grpc
import json
import audioop
import shutil
import yaml
import vaisdemo.speech.v1.cloud_speech_pb2_grpc as cloud_speech_pb2_grpc
import vaisdemo.speech.v1.cloud_speech_pb2 as cloud_speech_pb2
import threading
import importlib
import vaisdemo.capture as capture
import wave
try:
 import pyaudio
except Exception as e:
 exit(1)
c=640
R=pyaudio.paInt16
q=1
V=16000
M=15
Q=threading.Lock()
class VaisService():
 def __init__(N,j,resources_path=None,silence=False,mic_name=None,record=True):
  N.api_key=j
  N.record=record
  N.url="service.grpc.vais.vn:50051"
  N.channel=grpc.insecure_channel(N.url)
  N.channel.subscribe(callback=N.connectivity_callback,try_to_connect=True)
  N.stop=False
  N.stub=cloud_speech_pb2_grpc.SpeechStub(N.channel)
  N.volume=0
  N.mic_name=mic_name
  if N.record:
   N.capture=capture.Capture({'sound':{'input_device':mic_name}},"/tmp/audio")
  N.asr_callback=None
  N.encoder=None
  try:
   from speex import WBEncoder
   N.encoder=f()
   N.encoder.quality=10
   k=N.encoder.frame_size
   c=k
  except Exception as e:
   pass
 def state_callback(*args):
  pass
 def __enter__(N):
  if N.record:
   N.capture.setup(N.state_callback)
  return N
 def __exit__(N,*args):
  if N.record:
   N.capture.cleanup()
  try:
   shutil.rmtree("/tmp/audio")
  except Exception as e:
   pass
 def connectivity_callback(N,c):
  pass
 def get_speech(N):
  try:
   g=N.capture.silence_listener()
   for T in g:
    N.volume=audioop.max(T,2)
    if N.encoder:
     with Q:
      T=N.encoder.encode(T)
    yield T
  except Exception as e:
   N.asr_callback(e.message,False)
 def load_audio(N,fname):
  S=wave.open(fname)
  B=S.getnframes()
  d=640
  p=0
  J=0
  while p<B:
   J+=1
   b=B-p
   a=d
   if d>b:
    a=b
   T=S.readframes(a)
   N.volume=audioop.max(T,2)
   if N.encoder:
    with Q:
     T=N.encoder.encode(T)
   p+=a
   yield T
 def load_audio_bin(N,all_data):
  B=len(all_data)
  d=640
  p=0
  J=0
  for i in range(0,B,d):
   w=i+d
   T=all_data[i:w]
   y=len(T)
   if y==d:
    if N.encoder:
     with Q:
      T=N.encoder.encode(T)
    yield T
 def generate_messages(N,filename=None,audio_data=None):
  o=cloud_speech_pb2.RecognitionConfig.SPEEX_WITH_HEADER_BYTE
  if N.encoder is None:
   o=cloud_speech_pb2.RecognitionConfig.LINEAR16
  I=cloud_speech_pb2.RecognitionConfig(encoding=o)
  s=cloud_speech_pb2.StreamingRecognitionConfig(config=I,single_utterance=False,interim_results=True)
  r=cloud_speech_pb2.StreamingRecognizeRequest(streaming_config=s)
  yield r
  H=None
  if(not filename)and(not audio_data):
   H=N.get_speech()
  elif not audio_data:
   H=N.load_audio(filename)
  else:
   H=N.load_audio_bin(audio_data)
  N.asr_callback("Ready!",False)
  for u in H:
   r=cloud_speech_pb2.StreamingRecognizeRequest(audio_content=u)
   yield r
 def asr(N,filename=None,audio_data=None):
  N.asr_callback("Connecting ...",False)
  F=[(b'api-key',N.api_key)]
  t=N.stub.StreamingRecognize(N.generate_messages(filename=filename,audio_data=audio_data),metadata=F)
  for L in t:
   if L.results:
    if L.results[0].alternatives:
     N.asr_callback(L.results[0].alternatives[0].transcript,L.results[0].is_final)

