from vaisdemo.Truecaser import*
import pickle
import os
import time
import string
class MyTrueCaser():
 def __init__(f):
  f.uniDist=None
  f.backwardBiDist=None
  f.forwardBiDist=None
  f.trigramDist=None
  f.wordCasingLookup=None
 def evaluateTrueCaser(f,sentence):
  if not f.uniDist:
   print("TrueCaser model is not loaded. Skip!")
   return sentence
  P=0
  q=0
  N=sentence.lower().split()
  k=[token for token in N]
  M=getTrueCase(k,'title',f.wordCasingLookup,f.uniDist,f.backwardBiDist,f.forwardBiDist,f.trigramDist)
  return " ".join(M)
 def load_model(f):
  time.sleep(5)
  C=os.path.dirname(os.path.abspath(__file__))
  R=os.path.join(C,'distributions.obj')
  if os.path.exists(R):
   f=open(R,'rb')
   f.wordCasingLookup=pickle.load(f)
   f.uniDist=pickle.load(f)
   f.backwardBiDist=pickle.load(f)
   f.forwardBiDist=pickle.load(f)
   f.close()

