import string
import math
def getScore(g,o,R,wordCasingLookup,M,h,v,u):
 Y=5.0
 s=0
 V=M[o]+Y
 K=0
 for B in wordCasingLookup[o.lower()]:
  K+=M[B]+Y
 H=V/K
 s=math.log(H)
 a=1
 if h:
  if g!=None:
   V=h[g+'_'+o]+Y
   K=0
   for B in wordCasingLookup[o.lower()]:
    K+=h[g+'_'+B]+Y
   a=V/K
  s+=math.log(a)
 t=1
 if v:
  if R!=None:
   R=R.lower()
   V=v[o+"_"+R]+Y
   K=0
   for B in wordCasingLookup[o.lower()]:
    K+=v[B+"_"+R]+Y
   t=V/K
  s+=math.log(t)
 S=1
 if u:
  if g!=None and R!=None:
   R=R.lower()
   V=u[g+"_"+o+"_"+R]+Y
   K=0
   for B in wordCasingLookup[o.lower()]:
    K+=u[g+"_"+B+"_"+R]+Y
   S=V/K
  s+=math.log(S)
 return s
def getTrueCase(tokens,outOfVocabularyTokenOption,wordCasingLookup,M,h,v,u):
 D=[]
 for z in range(len(tokens)):
  q=tokens[z]
  if q in string.punctuation or q.isdigit():
   D.append(q)
  else:
   if q in wordCasingLookup:
    if len(wordCasingLookup[q])==1:
     D.append(list(wordCasingLookup[q])[0])
    else:
     g=D[z-1]if z>0 else None
     R=tokens[z+1]if z<len(tokens)-1 else None
     L=None
     f=float("-inf")
     for o in wordCasingLookup[q]:
      G=getScore(g,o,R,wordCasingLookup,M,h,v,u)
      if G>f:
       L=o
       f=G
     D.append(L)
    if z==0:
     D[0]=D[0].title();
   else:
    if outOfVocabularyTokenOption=='title':
     D.append(q.title())
    elif outOfVocabularyTokenOption=='lower':
     D.append(q.lower())
    else:
     D.append(q)
 return D

