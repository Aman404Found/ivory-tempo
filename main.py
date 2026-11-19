import os,json,urllib.request
D=(1,-1,16,-16,15,-15,17,-17)
N=(14,-14,18,-18,31,-31,33,-33)
V=(0,100,315,332,503,930,24000)
S=range(120)
def sq(x):return ord(x[0])-97+16*(int(x[1])-1)
def choose(fen,legal):
 f,side,*_=fen.split();b=[0]*128
 for y,row in enumerate(f.split('/')):
  i=112-16*y
  for c in row:
   if c.isdigit():i+=int(c);continue
   b[i]=' pnbrqk'.index(c.lower())*(1 if c.isupper() else -1);i+=1
 t=1 if side=='w' else -1
 end=sum(abs(p)>1 for p in b)<9
 def pst(p,i):
  x=i%16;y=i//16 if p>0 else 7-i//16;c=7-abs(x*2-7)//2-abs(y*2-7)//2
  return V[abs(p)]+(0,y*y*2+c*2,c*9-12*(y==0),c*5-8*(y==0),y*2,c*2,(c*9 if end else -4*c-9*y))[abs(p)]
 P={p:[pst(p,i) for i in range(128)] for p in range(-6,7)}
 def moves(s,q):
  for i in S:
   p=b[i]*s
   if p<=0:continue
   if p==1:
    h=16*s;j=i+h
    if j&136:continue
    if not b[j] and (not q or j//16 in (0,7)):
     yield i,j
     if i//16==(1 if s==1 else 6) and not b[j+h]:yield i,j+h
    for j in (j-1,j+1):
     if not j&136 and b[j]*s<0:yield i,j
   else:
    for h in (N if p==2 else D[4:] if p==3 else D[:4] if p==4 else D):
     j=i+h
     while not j&136:
      v=b[j]*s
      if v<=0 and (v or not q):yield i,j
      if v or p in (2,6):break
      j+=h
 def apply(i,j,s):
  p=b[i];v=b[j];u=5*s if p==s and j//16 in (0,7) else p
  b[i]=0;b[j]=u
  return P[u][j]-P[p][i]+P[v][j],p,v
 count=0;table={};killer={}
 def attacked(k,s):
  for h in N:
   j=k+h
   if not j&136 and b[j]==2*s:return True
  for n,h in enumerate(D):
   j=k+h
   if j&136:continue
   v=b[j]*s
   if v==6 or v==1 and h in (-16*s-1,-16*s+1):return True
   while not b[j]:
    j+=h
    if j&136:break
   else:
    if b[j]*s in (5,3+(n<4)):return True
  return False
 def search(s,d,a,z,e,ply=1):
  nonlocal count
  count+=1
  if count>24000:raise OverflowError
  k=b.index(s*6);check=attacked(k,-s);q=d<=0 and not check
  if ply>18:return e
  if q:
   if e>=z or d<-4:return e
   a=max(a,e)
  key=(tuple(b),s) if d>0 else None;hit=table.get(key);hint=None;orig=a
  if hit:
   depth,val,flag,hint=hit
   if depth>=d and abs(val)<29000 and (flag==0 or flag==1 and val>=z or flag==-1 and val<=a):return val
  if d>=3 and not check and e>=z and not end and ply>1 and -search(-s,d-3,-z,1-z,-e,ply+1)>=z:return z
  kill=killer.get(ply)
  ms=list(moves(s,q));ms.sort(key=lambda m:50000*(m==hint)+16*V[abs(b[m[1]])]+400*(m==kill)+P[b[m[0]]][m[1]]-P[b[m[0]]][m[0]],reverse=True)
  n=0
  for i,j in ms:
   g,p,v=apply(i,j,s)
   if not attacked(j if i==k else k,-s):
    n+=1;red=d>=3 and n>4 and not(v or check)
    w=-search(-s,d-1-red,-z,-a,-e-g,ply+1)
    if red and w>a:w=-search(-s,d-1,-z,-a,-e-g,ply+1)
    if w>a:
     a=w
     hint=(i,j)
   b[i]=p;b[j]=v
   if a>=z:
    if not v:killer[ply]=(i,j)
    break
  if not n and not q:return ply-30000 if check else 0
  if key:table[key]=(d,a,1 if a>=z else -1 if a<=orig else 0,hint)
  return a
 e=sum((1 if p>0 else -1)*P[p][i] for i,p in enumerate(b) if p)*t
 order=sorted(legal);best=order[0]
 try:
  for d in range(1,8):
   ranks=[];a=-40000
   for m in order:
    i,j=sq(m),sq(m[2:]);g,p,v=apply(i,j,t);save=b[:];k=-1
    if abs(p)==6 and abs(i-j)==2:
     k=i+3 if j>i else i-4;b[(i+j)//2]=b[k];b[k]=0
    if abs(p)==1 and i%16!=j%16 and not v:k=j-16*t;b[k]=0;g+=100
    w=-search(-t,d-1,-40000,-a,-e-g);b[:]=save;b[i]=p;b[j]=v
    ranks.append((w,m));a=max(a,w)
   order=[m for w,m in sorted(ranks,key=lambda x:-x[0])];best=order[0]
 except OverflowError:pass
 return best

def post(path,obj):return json.load(urllib.request.urlopen(urllib.request.Request(os.environ['MAKEFUN_ENV_URL']+path,json.dumps(obj).encode(),{'Content-Type':'application/json'})))
if __name__=='__main__':
 while (g:=post('/game',{}))['status']!='done':
  while g['status']=='your_move':g=post('/move',{'game':g['game'],'move':choose(g['fen'],g['legal_moves'])})
