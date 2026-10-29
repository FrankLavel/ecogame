"""Build original artwork, audio and editable Construct 2 project. No third party assets."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import xml.etree.ElementTree as E
import math, random, wave, struct, subprocess, zipfile, shutil

ROOT=Path(__file__).resolve().parents[1]
random.seed(17)
S=2
INK='#244c42'; GREEN='#277b58'; CREAM='#fff9e9'; GOLD='#efbe62'
def font(n,bold=False):
    return ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if bold else 'arial.ttf'),n*S)
def canvas(w,h,color=(0,0,0,0)):
    im=Image.new('RGBA',(w*S,h*S),color); return im,ImageDraw.Draw(im)
def box(d,xy,fill,r=0,outline=None,width=1):
    xy=tuple(round(a*S) for a in xy)
    if r:d.rounded_rectangle(xy,r*S,fill,outline,width*S)
    else:d.rectangle(xy,fill,outline,width*S)
def ellipse(d,xy,fill,outline=None,width=1):d.ellipse(tuple(round(a*S) for a in xy),fill,outline,width*S)
def line(d,xy,fill,width=2):d.line([(round(x*S),round(y*S)) for x,y in xy],fill,width*S)
def text(d,xy,t,n=18,c=INK,b=False,anchor=None):d.text(tuple(round(a*S) for a in xy),t,font=font(n,b),fill=c,anchor=anchor)
def save(im,p):
    p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);im.resize((im.width//S,im.height//S),Image.Resampling.LANCZOS).save(p)
def tree(d,x,y,s=1):
    ellipse(d,(x-42*s,y+30*s,x+58*s,y+58*s),'#86ae6c')
    box(d,(x-7*s,y,x+8*s,y+44*s),'#98724c',4)
    for a,b,r,c in [(-21,0,28,'#397956'),(19,-3,32,'#397956'),(0,-26,37,'#4b9160'),(-17,-27,25,'#64a26a'),(10,-42,24,'#75ae72')]:
        ellipse(d,(x+(a-r)*s,y+(b-r)*s,x+(a+r)*s,y+(b+r)*s),c)
    ellipse(d,(x-25*s,y-52*s,x-8*s,y-42*s),'#95c482')
def flower(d,x,y,c='#fff8d6'):
    for a in range(0,360,72):
        dx=3*math.cos(math.radians(a));dy=3*math.sin(math.radians(a));ellipse(d,(x+dx-2,y+dy-2,x+dx+2,y+dy+2),c)
    ellipse(d,(x-1,y-1,x+1,y+1),'#dfae53')

# A hand-built illustrated park: one screen, matching the collision geometry.
im,d=canvas(1280,720,'#acd18a')
for y in range(96,610,6):
    color=(170+int(5*math.sin(y/90)),205+int(5*math.sin(y/90)),139,255)
    box(d,(0,y,1280,y+6),color)
for i in range(650):
    x=random.randint(40,1240);y=random.randint(110,600)
    line(d,[(x-2,y+3),(x,y),(x+2,y+3)],random.choice(['#97c17e','#b9d995','#a1c780']),1)
# Paths
line(d,[(120,438),(1160,438)],'#c7b184',104)
line(d,[(120,432),(1160,432)],'#e9d4a3',96)
line(d,[(640,180),(640,610)],'#c7b184',106)
line(d,[(640,180),(640,610)],'#e9d4a3',98)
box(d,(395,150,885,258),'#c7b184',34);box(d,(400,145,880,252),'#e9d4a3',30)
for i in range(165):
    x=random.randint(110,1170);y=random.randint(390,471)
    ellipse(d,(x,y,x+2,y+1),'#d7c18f')
# Pond at left, collision = ellipse approximated by inset rectangle
ellipse(d,(95,205,334,368),'#8eaf76');ellipse(d,(92,196,330,354),'#f1dfa9')
ellipse(d,(104,205,318,343),'#5dada7');ellipse(d,(113,212,310,330),'#79c6bc')
for x,y in [(142,235),(211,278),(165,314),(259,237)]:line(d,[(x,y),(x+31,y)],'#b7e7d5',3)
for x,y in [(139,280),(273,287),(202,223)]:
    ellipse(d,(x-12,y-5,x+12,y+5),'#559a6a');line(d,[(x,y),(x+11,y-6)],'#79c6bc',2)
# Benches and planter
for x,y in [(1020,280),(200,515)]:
    for a in [0,12,24]:box(d,(x-47,y+a,x+47,y+a+8),'#ac7e50',3)
    for a in [-32,32]:box(d,(x+a-3,y+28,x+a+3,y+42),'#426457',2)
for x,y in [(90,160),(350,164),(965,159),(1170,170),(1168,340),(1150,555),(930,563),(370,568),(70,562)]:tree(d,x,y,.85)
for x in range(32,1280,62):
    if x<570 or x>710:tree(d,x,108,.63)
for x,y in [(365,300),(890,300),(420,525),(855,515),(1090,370),(70,390)]:
    for dx,dy in [(-14,3),(0,-4),(16,6)]:ellipse(d,(x+dx-13,y+dy-10,x+dx+13,y+dy+10),'#6a9d64')
    flower(d,x,y,'#ffe5a8')
for i in range(50):
    x=random.randint(60,1210);y=random.randint(130,590)
    if not (380<x<900 and y<270) and not(85<x<340 and 190<y<365):flower(d,x,y)
box(d,(990,490,1093,528),'#e5ca8f',6);text(d,(1041,509),'PARQUE ALBA',11,INK,True,'mm')
save(im,Path('Animations/Park/Default/000.png'))

# Ranger with walking cycle (native Sprite frames)
for frame in range(4):
    im,d=canvas(64,84);step=[0,4,0,-4][frame]
    ellipse(d,(9,69,56,81),(39,70,51,55))
    box(d,(18,52,29,75+step),'#34584f',5);box(d,(35,52,46,75-step),'#34584f',5)
    box(d,(14,71+step,30,79+step),'#293f39',4);box(d,(34,71-step,50,79-step),'#293f39',4)
    box(d,(12,32,52,61),'#e3bc68',10);box(d,(16,34,48,58),'#3b8460',8)
    box(d,(8,38+step,17,59+step),'#ecc29a',4);box(d,(48,38-step,57,59-step),'#ecc29a',4)
    ellipse(d,(16,11,49,43),'#e9bb90');ellipse(d,(12,24,20,34),'#e9bb90');ellipse(d,(45,24,53,34),'#e9bb90')
    ellipse(d,(23,25,26,30),INK);ellipse(d,(39,25,42,30),INK)
    line(d,[(29,35),(34,37),(38,34)],'#a96e52',2)
    box(d,(13,8,51,23),'#5b9470',8);ellipse(d,(7,16,58,27),'#3d7359')
    ellipse(d,(27,9,38,19),'#f7e8a5');line(d,[(30,16),(35,12)],GREEN,2)
    save(im,Path(f'Animations/Player/Default/{frame:03}.png'))

# Six distinct, legible waste icons; two examples per category.
for k in range(6):
    im,d=canvas(56,56);ellipse(d,(3,37,53,52),(60,88,57,40))
    ellipse(d,(2,2,54,54),(255,250,225,180))
    if k==0:
        d.arc((12*S,4*S,45*S,40*S),15,170,fill='#e6b345',width=10*S)
        d.arc((11*S,3*S,43*S,35*S),20,165,fill='#ffe39a',width=6*S)
        line(d,[(12,25),(9,21)],'#8d7553',4);line(d,[(43,15),(45,11)],'#8d7553',3)
    elif k==1:
        ellipse(d,(13,20,30,43),'#d97a57');ellipse(d,(25,20,43,43),'#e48b64');line(d,[(28,23),(29,11)],'#82664a',3);ellipse(d,(30,10,43,18),'#51885b')
    elif k==2:
        box(d,(22,8,35,16),'#397c9b',3);box(d,(18,17,39,45),'#82c6d0',7, '#397c9b',2);box(d,(19,27,38,37),'#f5f5df',2);line(d,[(24,21),(24,25)],'#c7eee2',3)
    elif k==3:
        box(d,(16,13,39,44),'#d1dde0',7,'#67858b',2);ellipse(d,(16,11,39,20),'#9eafb3');line(d,[(23,15),(31,15)],'#526e77',3);box(d,(17,25,38,35),'#e3b85c',2)
    elif k==4:
        box(d,(14,9,40,45),'#fffbe6',3,'#b6a984',2)
        for y in [20,26,32,38]:line(d,[(20,y),(34,y)],'#91b1ad',2)
    else:
        box(d,(11,17,44,42),'#c59562',3,'#9a704a',2);box(d,(24,17,30,42),'#ead4a0');line(d,[(11,17),(21,10),(49,12),(44,19)],'#9a704a',2)
    save(im,Path(f'Animations/Trash/Default/{k:03}.png'))

for k,(name,sub,col) in enumerate([('ORGÁNICOS','Fruta y restos','#43825b'),('ENVASES','PET y latas','#d5a23c'),('PAPEL','Papel y cartón','#528caa')]):
    im,d=canvas(140,110);ellipse(d,(25,83,119,105),(50,80,52,45))
    box(d,(35,22,106,87),col,9);box(d,(29,16,112,29),col,5)
    box(d,(46,31,96,38),'#264c44',4);box(d,(62,48,80,68),CREAM,6)
    text(d,(71,57),str(k+1),17,col,True,'mm')
    box(d,(4,84,137,109),CREAM,9);text(d,(70,96),name,13,INK,True,'mm')
    save(im,Path(f'Animations/Bin/Default/{k:03}.png'))

# HUD panels, with enough dedicated space for all dynamic labels.
im,d=canvas(1280,720)
box(d,(0,0,1280,91),CREAM);box(d,(0,89,1280,94),'#d9dfbc')
ellipse(d,(22,22,70,70),GREEN);text(d,(46,46),'E',30,CREAM,True,'mm')
text(d,(84,21),'ECOGAME',24,INK,True);text(d,(85,52),'GUARDIANES DEL PARQUE',10,GREEN,True)
for x,w,l in [(330,150,'PUNTAJE'),(492,170,'PARQUE LIMPIO'),(676,110,'TIEMPO'),(802,140,'VIDAS')]:
    box(d,(x,13,x+w,77),'#edf0d8',12);text(d,(x+14,20),l,10,GREEN,True)
for x,l in [(984,'II'),(1060,'?'),(1136,'♪')]:
    box(d,(x,21,x+58,70),'#e2e9cd',13);text(d,(x+29,45),l,24,INK,True,'mm')
text(d,(1213,45),'01',23,GREEN,True,'mm')
box(d,(0,611,1280,720),CREAM);box(d,(0,608,1280,612),'#d9dfbc')
text(d,(225,630),'TU MOCHILA',11,GREEN,True)
box(d,(216,668,986,671),'#d9dfbc')
# compact touch movement pad
for x,y,label in [(78,625,'↑'),(78,682,'↓'),(22,682,'←'),(134,682,'→')]:
    box(d,(x-22,y-20,x+22,y+20),'#e2e9cd',10);text(d,(x,y),label,24,GREEN,True,'mm')
box(d,(1025,635,1238,694),GREEN,18);text(d,(1131,657),'E  /  ENTREGAR',19,CREAM,True,'mm');text(d,(1131,681),'junto a un contenedor',11,'#d4e8ca',False,'mm')
save(im,Path('Animations/Hud/Default/000.png'))

# Overlay artwork: title, pause, guide, win, defeat. Click target is shared.
for frame in range(5):
    im,d=canvas(1280,720,(22,51,43,185))
    box(d,(271,74,1009,605),'#1f483b',34)
    box(d,(267,66,1005,597),CREAM,34)
    text(d,(640,101),'E C O G A M E   /   PARQUE ALBA',12,GREEN,True,'mm')
    if frame==0:
        text(d,(640,168),'Pequeñas acciones.',39,INK,True,'mm');text(d,(640,216),'Un parque lleno de vida.',39,INK,True,'mm')
        text(d,(640,268),'Hoy tú eres el guardián. ¿Nos ayudas a recuperarlo?',18,'#6b7c68',False,'mm')
        for i,(a,b) in enumerate([('01  EXPLORA','Muévete con WASD o flechas.'),('02  RECOGE','Toca los 12 residuos del parque.'),('03  SEPARA','Acércate al contenedor y pulsa E.')]):
            y=320+i*57;box(d,(322,y-8,950,y+40),'#edf0db',12);text(d,(340,y+2),a,15,GREEN,True);text(d,(525,y+2),b,16)
        label='COMENZAR A CUIDAR';hint='3 vidas · 3 minutos · 1 parque por transformar'
    elif frame==1:
        text(d,(640,190),'Respira. El parque espera.',33,INK,True,'mm')
        text(d,(640,257),'La partida y el reloj están en pausa.',20,'#6b7c68',False,'mm')
        for y,t in [(323,'WASD / flechas: caminar'),(365,'E: entregar cerca de un contenedor'),(407,'H: guía de residuos   ·   M: sonido')]:text(d,(640,y),t,20,INK,False,'mm')
        label='VOLVER AL PARQUE';hint='P o Esc para continuar'
    elif frame==2:
        text(d,(640,166),'Cada residuo tiene su lugar.',32,INK,True,'mm')
        for i,(a,b,c) in enumerate([('1   ORGÁNICOS','Cáscaras de plátano y corazones de manzana.','#43825b'),('2   ENVASES','Botellas PET y latas vacías.','#b08832'),('3   PAPEL','Hojas limpias y cajas de cartón secas.','#528caa')]):
            y=224+i*81;box(d,(320,y,951,y+70),'#edf0db',14);text(d,(340,y+10),a,18,c,True);text(d,(340,y+39),b,16)
        text(d,(640,488),'Colores de este juego; consulta las reglas de tu localidad.',13,'#6b7c68',False,'mm')
        label='ENTENDIDO, ¡A CUIDAR!';hint='La guía detiene el reloj. H también la abre.'
    elif frame==3:
        text(d,(640,182),'¡El parque vuelve a respirar!',34,INK,True,'mm')
        text(d,(640,240),'Separaste los 12 residuos. Cada acción cuenta.',20,GREEN,False,'mm')
        for x in [562,640,718]:
            pts=[(x+25*math.cos(math.pi/5*a-math.pi/2)*(1 if a%2==0 else .45),338+25*math.sin(math.pi/5*a-math.pi/2)*(1 if a%2==0 else .45)) for a in range(10)]
            d.polygon([(int(x*S),int(y*S)) for x,y in pts],fill=GOLD)
        text(d,(640,405),'Reutiliza lo que puedas. Separa lo que ya no uses.',17,'#6b7c68',False,'mm')
        label='CUIDARLO OTRA VEZ';hint='Enter para volver a jugar'
    else:
        text(d,(640,183),'Todo guardián aprende.',36,INK,True,'mm')
        text(d,(640,246),'El intento terminó, pero tu próxima acción cuenta.',19,'#6b7c68',False,'mm')
        text(d,(640,332),'Consulta la guía con H y fíjate en las etiquetas.',19,GREEN,True,'mm')
        text(d,(640,383),'Un residuo a la vez. Sin prisa, con propósito.',18,INK,False,'mm')
        label='VOLVER A INTENTAR';hint='Enter para reiniciar'
    box(d,(403,516,877,573),GREEN,18);text(d,(640,545),label,20,CREAM,True,'mm');text(d,(640,633),hint,15,'#fff5d8',False,'mm')
    save(im,Path(f'Animations/Overlay/Default/{frame:03}.png'))

# Small objects: transparent hit area, pond collision, progress bar, held icon glow.
for name,col in [('Hit',(255,255,255,0)),('Obstacle',(255,255,255,0)),('Progress','#5d9b61')]:
    im,d=canvas(16,16,col);save(im,Path(f'Animations/{name}/Default/000.png'))

# Original synthesized sound palette, converted with Construct's bundled encoder.
for folder in ['Sounds','Music']: (ROOT/folder).mkdir(exist_ok=True)
def audio(name,notes,step=.13,music=False):
    sr=22050;length=len(notes)*step;buf=[]
    for i in range(int(length*sr)):
        t=i/sr;j=min(int(t/step),len(notes)-1);u=t-j*step;freq=notes[j]
        env=min(1,u/.012)*max(0,1-u/step)**2
        val=0 if not freq else (math.sin(2*math.pi*freq*u)+.22*math.sin(4*math.pi*freq*u))*env*.2
        if music:val*=.55
        buf.append(int(max(-1,min(1,val))*32767))
    wav=ROOT/'AudioSource'/f'{name}.wav'
    with wave.open(str(wav),'wb') as w:w.setparams((1,2,sr,0,'NONE','not compressed'));w.writeframes(struct.pack('<'+'h'*len(buf),*buf))
    dest=ROOT/('Music' if music else 'Sounds')/f'{name}.ogg'
    subprocess.run(['C:/Program Files/Construct 2/tools/audio/oggenc2.exe','-Q','-q','3','-o',str(dest),str(wav)],check=True,capture_output=True)
    shutil.copyfile(dest,ROOT/'Files'/dest.name)
audio('recoger',[660,880],.09);audio('correcto',[523.25,659.25,783.99],.12)
audio('error',[220,174.61],.16);audio('victoria',[523,659,784,1046,784,1046],.18);audio('fin',[392,330,261,196],.22)
audio('parque',[261.63,0,329.63,392,0,329.63,293.66,0,261.63,329.63,392,523.25,440,392,329.63,0,220,261.63,329.63,0,293.66,349.23,440,0,196,261.63,293.66,392,329.63,293.66,261.63,0],.32,True)

# Construct 2 XML helpers. IDs come from installed Scirra plugins and examples.
sid=100000
def el(p,tag,value=None,**attrs):
    v=E.SubElement(p,tag,{k.replace('_','-'):str(v) for k,v in attrs.items()})
    if value is not None:v.text=str(value)
    return v
def ident():
    global sid;sid+=1;return str(sid)
def write(root,path):
    E.indent(root,space='    ');E.ElementTree(root).write(ROOT/path,encoding='utf-8',xml_declaration=True)
project=E.parse(ROOT/'New project.caproj').getroot()
project.find('unique-id').text='ecogameparquealba2026'
for tag in ['used-plugins','used-behaviors','object-folder','global-instances','sounds-folder','music-folder']:
    project.find(tag).clear()
for tag,v in [('name','EcoGame - Guardianes del parque'),('description','Videojuego educativo 2D: restaura el Parque Alba separando residuos. Arte y audio originales.'),('version','1.0.0.0'),('app-id','com.ecogame.parquealba')]:project.find(tag).text=v
project.find('window-size/width').text='1280';project.find('window-size/height').text='720'
for p in project.findall('configuration-settings/prop'):
    if p.get('name')=='Orientations':p.text='Landscape'
plugins=project.find('used-plugins')
for p in ['Sprite','Text','Keyboard','Touch','Audio']:el(plugins,'plugin',p,author='Scirra',id=p,version='1')
behs=project.find('used-behaviors')
for p,name in [('EightDir','8 Direction'),('solid','Solid')]:el(behs,'behavior',name,author='Scirra',id=p,version='1')
objects=project.find('object-folder')
defs={}
def obj(name,plugin='Sprite',frames=1,variables=None,behaviors=None):
    o=el(objects,'object-type',name=name);el(o,'plugin',id=plugin);defs[name]=plugin
    if variables:
        vs=el(o,'instance-variables')
        for n,t in variables.items():el(vs,'instance-variable',name=n,type='string' if t=='text' else t)
    if behaviors:
        bs=el(o,'behaviors')
        for n,b in behaviors.items():el(el(bs,'behavior-type',name=n),'behavior',id=b)
    if plugin=='Sprite':
        a=el(el(o,'animation-folder'),'animation',name='Default',framecount=frames,speed=0,loop=1,pingpong=0,repeatcount=1,repeatto=0,sid=ident())
        for i in range(frames):
            f=el(a,'frame',duration=1,hotspotX=.5,hotspotY=.5)
            poly=el(f,'collision-poly')
            coords=[(.22,.55),(.78,.55),(.78,.95),(.22,.95)] if name=='Player' else [(0,0),(1,0),(1,1),(0,1)]
            for x,y in coords:el(poly,'point',x=x,y=y)
    return o
for name,frames in [('Park',1),('Hud',1),('Overlay',5),('Player',4),('Trash',6),('Bin',3),('Hit',1),('Obstacle',1),('Progress',1)]:
    vars={'Kind':'number','Label':'text'} if name=='Trash' else {'Kind':'number'} if name=='Bin' else {'Command':'number'} if name=='Hit' else None
    obj(name,frames=frames,variables=vars,behaviors={'Walk':'EightDir'} if name=='Player' else {'Solid':'solid'} if name=='Obstacle' else None)
for n in ['ScoreText','CleanText','TimeText','LivesText','CarryText','TipText','EndText','SoundText']:obj(n,'Text')
for n in ['Keyboard','Touch','Audio']:obj(n,n)
for n in ['Keyboard','Touch','Audio']:
    g=el(project.find('global-instances'),'global-instance',type=n)
    if n=='Touch':el(el(g,'properties'),'use-mouse-input','Yes')
    if n=='Audio':
        props=el(g,'properties')
        for k,v in {'timescale-audio':'Off','panning-model':'HRTF','distance-model':'Inverse','listener-z-height':600,'reference-distance':600,'maximum-distance':10000,'roll-off-factor':1}.items():el(props,k,v)
for folder,tag in [('Sounds','sounds-folder'),('Music','music-folder')]:
    for f in (ROOT/folder).glob('*.ogg'):el(project.find(tag),'file',name=f.name)

layout=E.Element('c2layout');el(layout,'name','Layout 1');el(layout,'sid',ident());el(layout,'event-sheet','Event sheet 1')
sz=el(layout,'size');el(sz,'width',1280);el(sz,'height',720)
m=el(layout,'margins');el(m,'horizontal',500);el(m,'vertical',500);el(layout,'unbounded-scrolling',0)
layers=el(layout,'layers');ls={}
for n in ['Fondo','Parque','Interfaz','Pantallas']:
    l=el(layers,'layer',name=n,sid=ident());el(l,'initially-visible',1);el(l,'background-color','172,209,138');el(l,'transparent',int(n!='Fondo'))
    p=el(l,'parallax');el(p,'x',1);el(p,'y',1)
    for k,v in [('zoom-rate',1),('opacity',1),('force-own-texture',0),('global',0),('use-render-cells',0),('blend-mode',0),('effect-fallback',0)]:el(l,k,v)
    ls[n]=el(l,'instances');el(l,'effects')
def instance(n,x,y,w,h,layer='Parque',frame=0,vs=None,txt='',size=18,color='36,76,66',align='Left'):
    ins=el(ls[layer],'instance',type=n,uid=ident());p=el(ins,'properties')
    if defs[n]=='Sprite':
        for k,v in [('initial-visibility','Visible'),('initial-animation','Default'),('initial-frame',frame),('collisions','Enabled')]:el(p,k,v)
    else:
        for k,v in [('text',txt),('initial-visibility','Visible'),('font',f'Arial,-{size}'),('color',color),('horizontal-alignment',align),('vertical-alignment','Top'),('hotspot','Top-left'),('wrapping','Word'),('line-height',0),('blend-mode','Normal')]:el(p,k,v)
    if vs:
        v=el(ins,'instance-variables')
        for k,val in vs.items():el(v,k,val)
    if n=='Player':
        b=el(el(ins,'behavior-instances'),'behavior-instance',type='Walk');p=el(b,'properties')
        for k,v in [('max-speed',240),('acceleration',1400),('deceleration',1800),('directions','8 directions'),('set-angle','No'),('default-controls','No'),('initial-state','Enabled')]:el(p,k,v)
    if n=='Obstacle':el(el(el(ins,'behavior-instances'),'behavior-instance',type='Solid'),'properties')
    el(ins,'blend-mode',0);el(ins,'effect-fallback',0);p=el(ins,'world')
    for k,v in [('x',x),('y',y),('z',0),('width',w),('height',h),('depth',0),('hotspotX',.5 if defs[n]=='Sprite' else 0),('hotspotY',.5 if defs[n]=='Sprite' else 0),('angle',0),('opacity',1)]:el(p,k,v)
    return ins
instance('Park',640,360,1280,720,'Fondo');instance('Hud',640,360,1280,720,'Interfaz')
for x,k in [(470,1),(640,2),(810,3)]:instance('Bin',x,190,140,110,frame=k-1,vs={'Kind':k})
items=[(396,315,0),(537,338,2),(748,325,4),(922,368,1),(1070,427,3),(824,455,5),(1020,557,2),(760,562,0),(520,548,4),(375,460,1),(126,419,5),(477,474,3)]
names=['Cáscara de plátano','Corazón de manzana','Botella PET','Lata vacía','Hoja de papel','Caja de cartón']
for x,y,k in items:instance('Trash',x,y,48,48,frame=k,vs={'Kind':k//2+1,'Label':names[k]})
instance('Player',640,490,56,74)
for x,y,w,h in [(211,273,184,99),(1020,304,96,60),(200,537,96,60),(640,109,1280,35),(640,607,1280,20),(28,360,45,550),(1250,360,45,550)]:instance('Obstacle',x,y,w,h)
instance('Progress',507,70,1,4,'Interfaz')
for n,x,y,w,h,txt,size in [('ScoreText',344,39,130,30,'0000',24),('CleanText',506,39,150,27,'0 / 12',24),('TimeText',690,39,100,30,'3:00',24),('LivesText',815,39,130,30,'3 / 3',24),('CarryText',225,648,750,26,'Mochila vacía',19),('TipText',225,680,760,25,'',13),('SoundText',1137,74,65,15,'SONIDO',9)]:instance(n,x,y,w,h,'Interfaz',txt=txt,size=size)
for x,y,w,h,cmd in [(1013,46,58,49,2),(1089,46,58,49,3),(1165,46,58,49,6),(1131,663,213,59,5),(78,625,44,40,10),(78,682,44,40,11),(22,682,44,40,12),(134,682,44,40,13)]:instance('Hit',x,y,w,h,'Interfaz',vs={'Command':cmd})
instance('Overlay',640,360,1280,720,'Pantallas')
instance('EndText',350,447,580,35,'Pantallas',txt='',size=23,align='Center')
# The main button has its own type so no hidden HUD target can intercept overlay taps.
obj('Confirm',frames=1);p=ROOT/'Animations/Confirm/Default';p.mkdir(parents=True,exist_ok=True);shutil.copy(ROOT/'Animations/Hit/Default/000.png',p/'000.png')
instance('Confirm',640,545,474,57,'Pantallas')
el(layout,'nonworld-instances');el(layout,'effects')

sheet=E.Element('c2eventsheet');el(sheet,'name','Event sheet 1');events=el(sheet,'events')
for n,t,v in [('State','number',0),('Previous','number',0),('Cmd','number',0),('Carry','number',0),('ItemName','text',''),('Score','number',0),('Clean','number',0),('Lives','number',3),('TimeLeft','number',180),('Tip','text','¡Bienvenido! Toca un residuo para recogerlo.'),('TipTime','number',0),('Combo','number',0),('Muted','number',0)]:el(events,'variable',v,name=n,type=t,constant=0,static=0,sid=ident())
def node(tag,typ,id,params=(),**kw):
    a=E.Element(tag,{'type':typ,'id':str(id),'sid':ident(),**kw})
    for i,v in enumerate(params):el(a,'param',v,id=i,name=f'Parameter {i}')
    return a
def c(t,i,*p,**kw):return node('condition',t,i,p,**kw)
def a(t,i,*p,**kw):return node('action',t,i,p,**kw)
def ev(cs,acts,parent=events):
    e=el(parent,'event-block',sid=ident());co=el(e,'conditions');ac=el(e,'actions')
    for z in cs:co.append(z)
    for z in acts:ac.append(z)
    return e
def cv(n,v,cmp=0):return c('System',-14,n,cmp,v)
def sv(n,v):return a('System',-9,n,v)
def say(v):return a('TipText',0,v)
def layer(v):return a('System',-4,'"Pantallas"',v)
def frame(v):return a('Overlay',5,v)
def sound(n,music=0,loop=0,vol=-9):
    # Play by name: parameter IDs are not positional in the editor API.
    r=a('Audio',7);r.extend([E.Element('param',{'id':str(i),'name':n}) for i,n in []])
    for i,v in [(0,music),(1,f'"{n}"'),(3,loop),(4,vol),(2,'"music"' if music else '"fx"')]:el(r,'param',v,id=i,name='Audio')
    return r
el(events,'comment','ESTADOS: 0 inicio, 1 juego, 2 pausa, 3 guía, 4 victoria, 5 derrota. Comandos consumidos para evitar dobles transiciones.')
ev([c('System',-2)],[sv('State',0),sv('Previous',0),sv('Cmd',0),sv('Carry',0),sv('Score',0),sv('Clean',0),sv('Lives',3),sv('TimeLeft',180),sv('Combo',0),sv('Muted',0),sv('Tip','"¡Vamos! Recoge un residuo y llévalo al contenedor correcto."'),a('Audio',8,1),a('Player',8,0,behavior='Walk'),frame(0),layer(1)])
el(events,'comment','ENTRADAS. Touch usa también el ratón: botones funcionales en escritorio y pantalla táctil.')
for key,cmd in [(13,4),(27,2),(80,2),(72,3),(69,5),(32,5),(77,6)]:ev([c('Keyboard',0,f'{key}')],[sv('Cmd',cmd)])
ev([c('Touch',3,'Confirm')],[sv('Cmd',4)])
ev([c('Touch',3,'Hit')],[sv('Cmd','Hit.Command')])
for cmd,state,acts in [(4,0,[sv('State',1),layer(0),sound('parque',1,1,-14)]),(4,2,[sv('State',1),layer(0)]),(4,3,[sv('State','Previous'),layer(0)]),(2,1,[sv('State',2),frame(1),layer(1)]),(2,2,[sv('State',1),layer(0)]),(3,0,[sv('Previous',0),sv('State',3),frame(2),layer(1)]),(3,1,[sv('Previous',1),sv('State',3),frame(2),layer(1)]),(3,2,[sv('Previous',2),sv('State',3),frame(2),layer(1)]),(3,3,[sv('State','Previous'),layer(0)])]:
    ev([cv('Cmd',cmd),cv('State',state)],[sv('Cmd',0)]+acts)
# Restore the correct overlay when closing guide to menu/pause.
ev([cv('State',0)],[frame(0),layer(1)])
ev([cv('State',2)],[frame(1),layer(1)])
ev([cv('Cmd',4),cv('State',4,5)],[a('Audio',6,'"music"'),a('System',-26)])
ev([cv('Cmd',6)],[sv('Muted','1-Muted'),a('Audio',8,2)])
ev([cv('Muted',1)],[a('SoundText',0,'"MUDO"')]);ev([cv('Muted',0)],[a('SoundText',0,'"SONIDO"')])
el(events,'comment','MOVIMIENTO. Ocho direcciones, colisión Solid y animación propia. La pausa congela movimiento y reloj.')
ev([cv('State',1)],[a('Player',8,1,behavior='Walk'),sv('TimeLeft','max(0,TimeLeft-dt)'),a('Player',-3,'clamp(Player.X,55,1225)','clamp(Player.Y,145,570)')])
ev([cv('State',1,1)],[a('Player',8,0,behavior='Walk')])
for keys,control in [([65,37],0),([68,39],1),([87,38],2),([83,40],3)]:
    for k in keys:ev([c('Keyboard',2,str(k)),cv('State',1)],[a('Player',7,control,behavior='Walk')])
for cmd,control in [(10,2),(11,3),(12,0),(13,1)]:ev([c('Touch',4,'Hit'),c('Hit',-7,'Command',0,cmd),cv('State',1)],[a('Player',7,control,behavior='Walk')])
ev([cv('State',1),c('Player',0,behavior='Walk')],[a('Player',5,'floor(time*9)%4')])
ev([cv('State',1),c('Player',0,behavior='Walk',inverted='1')],[a('Player',5,0)])
el(events,'comment','RECOLECCIÓN. Colisión con un residuo, mochila de capacidad uno; categoría y nombre se conservan.')
ev([cv('State',1),cv('Carry',0),c('Player',1,'Trash')],[sv('Carry','Trash.Kind'),sv('ItemName','Trash.Label'),sv('Tip','"Llevas: " & ItemName & ". Busca su contenedor y pulsa E."'),a('Trash',-9),sound('recoger')])
el(events,'comment','ENTREGA. E o botón táctil. Solo se evalúa el contenedor más cercano y dentro del radio indicado.')
near=[c('Bin',-15,0,'Player.X','Player.Y'),c('System',-8,'distance(Player.X,Player.Y,Bin.X,Bin.Y)',2,105)]
deliver=ev([cv('Cmd',5),cv('State',1),cv('Carry',0,4)]+near,[sv('Cmd',0)])
sub=el(deliver,'sub-events')
ev([c('Bin',-7,'Kind',0,'Carry')],[sv('Score','Score+100+Combo*10'),sv('Combo','Combo+1'),sv('Clean','Clean+1'),sv('Carry',0),sv('Tip','"¡Correcto! +" & (100+(Combo-1)*10) & " puntos. Sigue cuidando el parque."'),sound('correcto')],sub)
ev([c('System',-22)],[sv('Lives','Lives-1'),sv('Combo',0),sv('Tip','"Va en " & (Carry=1 ? "ORGÁNICOS (verde)" : (Carry=2 ? "ENVASES (amarillo)" : "PAPEL (azul)")) & ". Conservas el residuo; inténtalo de nuevo."'),sound('error')],sub)
ev([cv('Cmd',5),cv('State',1),cv('Carry',0)],[sv('Tip','"Tu mochila está vacía. Camina sobre un residuo para recogerlo."')])
ev([cv('Cmd',5),cv('State',1),cv('Carry',0,4)],[sv('Tip','"Acércate más a un contenedor antes de entregar."')])
el(events,'comment','HUD Y CIERRE. Victoria por doce entregas, derrota por vidas o tiempo. Reinicio completo de variables.')
ev([c('System',-1)],[a('ScoreText',0,'zeropad(Score,4)'),a('CleanText',0,'Clean & " / 12"'),a('TimeText',0,'floor(ceil(TimeLeft)/60) & ":" & zeropad(ceil(TimeLeft)%60,2)'),a('LivesText',0,'Lives & " / 3"'),a('CarryText',0,'Carry=0 ? "Mochila vacía · encuentra un residuo" : ItemName'),a('TipText',0,'Tip'),a('Progress',-5,'max(1,Clean/12*138)')])
ev([cv('State',1),cv('Clean',12)],[sv('State',4),sv('Score','Score+floor(TimeLeft)*2+Lives*50'),frame(3),layer(1),a('EndText',0,'Score & " puntos   ·   " & Lives & " vidas   ·   100% limpio"'),a('Audio',6,'"music"'),sound('victoria')])
for var in ['Lives','TimeLeft']:ev([cv('State',1),cv(var,0,3)],[sv('State',5),frame(4),layer(1),a('EndText',0,'Clean & " / 12 separados   ·   " & Score & " puntos"'),a('Audio',6,'"music"'),sound('fin')])
ev([c('System',-1)],[sv('Cmd',0)])
write(project,Path('EcoGame.caproj'));write(layout,Path('Layouts/Layout 1.xml'));write(sheet,Path('Event sheets/Event sheet 1.xml'))
# Keep the original entry point usable; both open the same assets, layouts and events.
write(project,Path('New project.caproj'))
with zipfile.ZipFile(ROOT/'EcoGame.capx','w',zipfile.ZIP_DEFLATED) as z:
    z.write(ROOT/'EcoGame.caproj','EcoGame.caproj')
    for folder in ['Animations','Layouts','Event sheets','Files','Sounds','Music']:
        for f in (ROOT/folder).rglob('*'):
            if f.is_file() and '.uistate.' not in f.name:z.write(f,f.relative_to(ROOT))
print('Built EcoGame.caproj and EcoGame.capx:',len(events.findall('.//event-block')),'events,',len(objects),'object types.')
