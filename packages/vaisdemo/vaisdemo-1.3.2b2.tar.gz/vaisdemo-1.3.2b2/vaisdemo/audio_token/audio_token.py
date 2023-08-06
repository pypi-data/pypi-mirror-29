from auditok import ADSFactory,AudioEnergyValidator,StreamTokenizer,player_for,dataset
from auditok.io import PyAudioSource,BufferAudioSource,StdinAudioSource,player_for
import operator
import os
from collections import OrderedDict
from pydub import AudioSegment
import sys
from threading import Thread
import threading
import time
from queue import Queue,Empty
import vaisdemo.vais as vais
import logging
import site
for h in site.getsitepackages():
 y=os.path.dirname(sys.executable)
 print("Setting path")
 os.environ["PATH"]+=os.pathsep+y
 os.environ["PATH"]+=os.pathsep+os.path.join(y,"Scripts")
 os.system("ffmpeg")
def file_to_audio_source(filename,filetype=None,**g):
 v=filename.lower()
 r=False
 if filetype is not None:
  filetype=filetype.lower()
 if filetype=="raw" or(filetype is None and v.endswith(".raw")):
  n=g.pop("sampling_rate",None)
  if n is None:
   n=g.pop("sr",None)
  J=g.pop("sample_width",None)
  if J is None:
   J=g.pop("sw",None)
  ch=g.pop("channels",None)
  if ch is None:
   ch=g.pop("ch",None)
  if None in(J,n,ch):
   raise Exception("All audio parameters are required for raw data")
  w=open(filename).read()
  r=True
 p=g.pop("use_channel",None)
 if p is None:
  p=g.pop("uc",None)
 if p is None:
  p=1
 else:
  try:
   p=int(p)
  except ValueError:
   pass
 if not isinstance(p,(int))and not p.lower()in["left","right","mix"]:
  raise ValueError("channel must be an integer or one of 'left', 'right' or 'mix'")
 i=None
 if r:
  i=AudioSegment(w,sample_width=J,frame_rate=n,channels=ch)
 if filetype in("wave","wav")or(filetype is None and v.endswith(".wav")):
  i=AudioSegment.from_wav(filename)
 elif filetype=="mp3" or(filetype is None and v.endswith(".mp3")):
  i=AudioSegment.from_mp3(filename)
 elif filetype=="ogg" or(filetype is None and v.endswith(".ogg")):
  i=AudioSegment.from_ogg(filename)
 elif filetype=="flv" or(filetype is None and v.endswith(".flv")):
  i=AudioSegment.from_flv(filename)
 else:
  i=AudioSegment.from_file(filename)
 if i.channels>1:
  if isinstance(p,int):
   if p>i.channels:
    raise ValueError("Can not use channel '{0}', audio file has only {1} channels".format(p,i.channels))
   else:
    i=i.split_to_mono()[p-1]
  else:
   N=p.lower()
   if N=="mix":
    i=i.set_channels(1)
   elif p.lower()=="left":
    i=i.split_to_mono()[0]
   elif p.lower()=="right":
    i=i.split_to_mono()[1]
 if i.frame_rate<16000:
  raise Exception("Audio frame_rate is %d which is below 16000"%(i.frame_rate))
 if i.frame_rate>16000:
  print("Downsampling from %d to 16000"%(i.frame_rate))
  i=i.set_frame_rate(16000)
 if i.sample_width!=2:
  print("Convert sample with from %d to 2"%(i.sample_width))
  i=i.set_sample_width(2)
 t=len(i)/float(60000)
 if t>4.5:
  print("Audio length: ",t)
  raise Exception("Audio too long")
 return V(data_buffer=i._data,sampling_rate=i.frame_rate,sample_width=i.sample_width,channels=i.channels)
class W(Thread):
 def __init__(k,timeout=0.2):
  k.timeout=timeout
  k.logger=None
  if sys.executable.endswith("pythonw.exe"):
   sys.stdout=open(os.devnull,"w");
   sys.stderr=open(os.path.join(os.getenv("TEMP"),"stderr-"+os.path.basename(sys.argv[0])),"w")
  else:
   k.logger=logging.getLogger(__name__)
  k._inbox=q()
  k._stop_request=q()
  Thread.__init__(k)
 def debug_message(k,L):
  if k.logger:
   k.logger.debug(L)
 def _stop_requested(k):
  try:
   L=k._stop_request.get_nowait()
   if L=="stop":
    return True
  except Empty:
   return False
 def stop(k):
  k._stop_request.put("stop")
  if k.isAlive():
   k.join()
 def send(k,L):
  k._inbox.put(L)
 def _get_message(k):
  try:
   L=k._inbox.get(timeout=k.timeout)
   return L
  except Empty:
   return None
class TokenizerWorker(W):
 M="END_OF_PROCESSING"
 def __init__(k,o,m,C,Y):
  k.ads=o
  k.tokenizer=m
  k.analysis_window=C
  k.observer=Y
  k._inbox=q()
  k.count=0
  W.__init__(k)
 def run(k):
  def notify_observers(w,start,end):
   H=b''.join(w)
   k.count+=1
   U=start*k.analysis_window
   I=(end+1)*k.analysis_window
   s=(end-start+1)*k.analysis_window
   k.observer.notify({"id":k.count,"audio_data":H,"start":start,"end":end,"start_time":U,"end_time":I,"duration":s})
  k.ads.open()
  k.tokenizer.tokenize(data_source=self,callback=notify_observers)
  k.observer.notify(TokenizerWorker.END_OF_PROCESSING)
 def read(k):
  if k._stop_requested():
   return None
  else:
   return k.ads.read()
class TokenSaverWorker(W):
 def __init__(k,T,timeout=0.2,callback=None,**g):
  k.kwargs=g
  k.max_asr_thread=7
  k.total_data=0
  k.api_key=T
  k.callback=callback
  k.asr_queue=q()
  k.data_queue=q()
  k.results=O()
  k.stop_request=False
  W.__init__(k,timeout=timeout)
 def run_asr(k,X,E,H):
  def on_result(R,is_final):
   if is_final:
    if R:
     R=R.replace("<SPOKEN_NOISE>","").strip()
     if X not in k.results:
      k.results[X]=[E,[R]]
     else:
      k.results[X][1].append(R)
  with vais.VaisService(k.api_key,record=False)as P:
   P.asr_callback=on_result
   P.asr(audio_data=audio_data)
  if X in k.results:
   k.results[X][1]=" ".join(k.results[X][1])
 def do_the_work(k):
  B=[]
  try:
   while True:
    try:
     X,E,H=k.data_queue.get(timeout=1)
     if X is None:
      break
    except Empty:
     continue
    if k._stop_requested()or k.stop_request:
     k.debug_message({"status":"Got stop request"})
     k.stop_request=True
     break
    k.debug_message({"status":"queue new asr session","start_time":X})
    k.run_asr(X,E,H)
    k.data_queue.task_done()
    if k.callback:
     B=[]
     S=100*float(k.total_data-k.data_queue.qsize())/k.total_data
     for s,(e,R)in k.results.items():
      if isinstance(R,list):
       R=" ".join(R)
      B.append("--> %s ..."%(R[:40]))
     k.callback(S,"\n".join(B[-10:]))
  except Exception as e:
   k.debug_message({"status":e})
  k.asr_queue.task_done()
 def run(k):
  k.asr_queue=q()
  for i in range(k.max_asr_thread):
   t=Thread(target=k.do_the_work)
   t.daemon=True
   t.start()
   k.asr_queue.put(t)
  a=time.time()
  while True:
   if k._stop_requested():
    break
   L=k._get_message()
   if L is not None:
    if L==TokenizerWorker.END_OF_PROCESSING:
     break
    H=L.pop("audio_data",None)
    U=L.pop("start_time",None)
    I=L.pop("end_time",None)
    d=L.pop("id",None)
    k.debug_message({"status":"new segment %.2f %.2f"%(U,I)})
    k.data_queue.put((U,I,H))
  for i in range(k.max_asr_thread):
   k.data_queue.put((None,None,None))
  k.asr_queue.join()
  D=time.time()
  k.callback(100,"Done! Spent %.2fs"%(D-a),is_finished=True)
 def notify(k,L):
  k.total_data+=1
  k.send(L)
def segment_audio(fname,T,energy_threshold=50,min_duration=0.2,max_duration=20,max_silence=0.3,callback=None):
 F=None
 e=[]
 Y=TokenSaverWorker(T,callback=callback)
 C=0.01
 G=None
 try:
  G=file_to_audio_source(fname)
 except Exception as e:
  callback(-1,"File audio không được hỗ trợ, hoặc độ dài quá 4 phút!",False)
  return None,None
 o=ADSFactory.ads(audio_source=G,block_dur=C,max_time=None,record=False)
 z=AudioEnergyValidator(sample_width=G.get_sample_width(),energy_threshold=energy_threshold)
 A=0
 j=1./C
 m=StreamTokenizer(validator=z,min_length=min_duration*j,max_length=int(max_duration*j),max_continuous_silence=max_silence*j,mode=A)
 F=TokenizerWorker(o,m,C,Y)
 return F,Y
if __name__=="__main__":
 w=segment_audio("/home/truong-d/work/vais/vlsp18/wav/002192e360_4m.wav","demo","output.csv")

