"""Pixel edition: original coherent low-resolution art and native frame animation."""
from pathlib import Path
import runpy, xml.etree.ElementTree as E, zipfile, math
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
m=runpy.run_path(str(ROOT/'tools/build_v2.py'))
project,layout,sheet=m['project'],m['layout'],m['sheet']
events=sheet.find('events');src=ROOT/'art-source/v3'
el,obj,instance,c,a,cv,sv=[m[k] for k in ['el','obj','instance','c','a','cv','sv']]
def ev(cs,acts):return m['ev'](cs,acts,parent=events)
ident=m['g']['ident']
def png(im,name,i=0):
    path=ROOT/f'Animations/{name}/Default/{i:03}.png';path.parent.mkdir(parents=True,exist_ok=True);im.save(path)
def palette(im,n):return im.convert('RGB').resize((256,256),Image.Resampling.NEAREST).quantize(colors=n,dither=Image.Dither.NONE)
def world_palette():
    # Reserved water tones prevent the foliage from dominating automatic quantization.
    colors=['#172f2e','#234638','#31563a','#3d6b3b','#4a7e39','#5f913c','#75a344','#8fb84b','#a8c658','#c2d26b',
            '#ded87d','#efdf9a','#fff0ba','#ffffff','#a9aaa0','#858e83','#636f66','#485955',
            '#543b2c','#705034','#8a633b','#a67a43','#bc914e','#d2a660','#e2ba72','#f0cc86','#f7db9e',
            '#246b78','#2e8991','#38a49f','#4abead','#77d0ba','#a5e3cc',
            '#c17443','#995637','#d9ad61','#dcc59c','#d8e8b5','#d2886a','#ab5144','#703e37',
            '#466c63','#6c8e75','#9cb28b','#b6c6a0','#343e35','#dfbb50','#f7e68f']
    pal=Image.new('P',(1,1));flat=[]
    for color in colors:flat.extend(bytes.fromhex(color[1:]))
    pal.putpalette(flat+[0]*(768-len(flat)));return pal
def pixel(im,size,pal=None):
    im=im.convert('RGBA').resize(size,Image.Resampling.NEAREST)
    alpha=im.getchannel('A').point(lambda n:255 if n>=110 else 0)
    rgb=im.convert('RGB').quantize(palette=pal,dither=Image.Dither.NONE).convert('RGBA') if pal else im.convert('RGB').quantize(colors=48,dither=Image.Dither.NONE).convert('RGBA')
    rgb.putalpha(alpha);return rgb
def atlas(path,cols,rows,size):
    im=Image.open(path).convert('RGBA');w,h=im.width//cols,im.height//rows
    return [im.crop((i%cols*w,i//cols*h,(i%cols+1)*w,(i//cols+1)*h)) for i in range(cols*rows)]
def fit_cell(im,size,pal,box=None):
    if box is None:box=im.getchannel('A').point(lambda n:255 if n>110 else 0).getbbox()
    crop=im.crop(box);scale=min((size[0]-2)/crop.width,(size[1]-2)/crop.height)
    fitted=pixel(crop,(max(1,round(crop.width*scale)),max(1,round(crop.height*scale))),pal)
    out=Image.new('RGBA',size);out.alpha_composite(fitted,((size[0]-fitted.width)//2,size[1]-fitted.height-1));return out
def set_frames(name,n):
    anim=project.find(f"object-folder/object-type[@name='{name}']/animation-folder/animation")
    frame=E.tostring(anim.find('frame'))
    for f in list(anim):anim.remove(f)
    anim.set('framecount',str(n));anim.set('speed','0')
    for _ in range(n):anim.append(E.fromstring(frame))
def size(name,w,h):
    for ins in layout.findall(f".//instance[@type='{name}']"):
        ins.find('world/width').text=str(w);ins.find('world/height').text=str(h)
def var(n,v):el(events,'variable',v,name=n,type='number',constant=0,static=0,sid=ident())

park=Image.open(src/'park.png').convert('RGBA');park=pixel(park,(320,180),world_palette());png(park,'Park')
heroes=atlas(src/'ranger.png',4,4,(16,24));pal=palette(Image.open(src/'ranger.png'),24)
set_frames('Player',16)
for i,im in enumerate(heroes):png(fit_cell(im,(16,24),pal),'Player',i)
bosses=atlas(src/'boss.png',3,2,(56,56));pal=palette(Image.open(src/'boss.png'),24)
# One shared logical crop keeps the actor's body size consistent across its poses.
bounds=[im.getchannel('A').point(lambda n:255 if n>110 else 0).getbbox() for im in bosses]
union=(min(b[0] for b in bounds),min(b[1] for b in bounds),max(b[2] for b in bounds),max(b[3] for b in bounds))
set_frames('Boss',6)
for i,im in enumerate(bosses):png(fit_cell(im,(56,56),pal,union),'Boss',i)
props_source=Image.open(src/'props.png').convert('RGBA');pal=palette(props_source,32)
# The generated bins are taller than the loose items; locate their three alpha bands.
mask=props_source.getchannel('A').point(lambda n:255 if n>110 else 0);runs=[]
for y in range(mask.height):
    if mask.crop((0,y,mask.width,y+1)).histogram()[255]>12:
        if not runs or y-runs[-1][-1]>8:runs.append([y])
        else:runs[-1].append(y)
bands=sorted(sorted(runs,key=len,reverse=True)[:3],key=lambda r:r[0]);assert len(bands)==3
cw=props_source.width//3
props=[props_source.crop((col*cw,max(0,band[0]-2),(col+1)*cw,min(props_source.height,band[-1]+3))) for band in bands for col in range(3)]
for i,im in enumerate(props[3:]):png(fit_cell(im,(12,12),pal),'Trash',i)
size('Player',64,96);size('Boss',224,224);size('Halo',240,240);size('Trash',48,48);size('Bin',140,112)

# UI is authored at half resolution using aliased bitmap-like glyphs and bevels.
BG='#f2dca2';INK='#473321';DARK='#35291e';WOOD='#a66d37';MID='#cd9455';LIGHT='#f0c785';GREEN='#426b3f';WHITE='#fff4ce'
def ui(w=1280,h=720,color=(0,0,0,0)):
    im=Image.new('RGBA',(w//2,h//2),color);d=ImageDraw.Draw(im);d.fontmode='1';return im,d
def rect(d,xy,col):d.rectangle(tuple(round(v/2) for v in xy),fill=col)
def txt(d,x,y,t,n=18,col=INK,bold=False,anchor=None):
    font=ImageFont.truetype('C:/Windows/Fonts/'+('consolab.ttf' if bold else 'consola.ttf'),max(5,round(n/2)))
    d.text((round(x/2),round(y/2)),t,font=font,fill=col,anchor=anchor)
def panel(d,xy,fill=BG):
    x1,y1,x2,y2=xy
    rect(d,(x1+4,y1,x2-4,y2),DARK);rect(d,(x1,y1+4,x2,y2-4),DARK)
    rect(d,(x1+4,y1+4,x2-4,y2-4),WOOD);rect(d,(x1+8,y1+8,x2-8,y2-8),LIGHT)
    rect(d,(x1+12,y1+12,x2-12,y2-12),fill)
    for x in [x1+6,x2-8]:
        for y in [y1+6,y2-8]:rect(d,(x,y,x+2,y+2),WHITE)
def button(d,xy,label,n=20):
    x1,y1,x2,y2=xy;panel(d,xy,GREEN);rect(d,(x1+14,y1+12,x2-14,y1+14),'#6f9854');txt(d,(x1+x2)/2,(y1+y2)/2,label,n,WHITE,True,'mm')
def badge(d,x,y,label):panel(d,(x-23,y-20,x+23,y+20),'#e8cb8c');txt(d,x,y,label,24,INK,True,'mm')

for i,name in enumerate(['1 ORGÁNICOS','2 ENVASES','3 PAPEL']):
    im,d=ui(140,112);small=fit_cell(props[i],(24,24),pal).resize((48,48),Image.Resampling.NEAREST)
    im.alpha_composite(small,(11,0));panel(d,(0,88,140,112));txt(d,70,100,name,12,INK,True,'mm');png(im,'Bin',i)

im,d=ui();panel(d,(0,0,1280,94));panel(d,(16,14,76,78),GREEN);txt(d,46,45,'E',34,WHITE,True,'mm')
txt(d,88,20,'ECOGAME',24,INK,True);txt(d,88,51,'GUARDIANES DEL PARQUE',11,GREEN,True)
for x,w,label in [(330,150,'PUNTAJE'),(492,170,'PARQUE LIMPIO'),(676,110,'TIEMPO'),(802,140,'VIDAS')]:
    panel(d,(x,12,x+w,80),'#f8e8bc');txt(d,x+14,20,label,11,GREEN,True)
for x,label in [(984,'II'),(1060,'?'),(1136,'M')]:button(d,(x,20,x+58,72),label,24)
txt(d,1214,46,'01',22,GREEN,True,'mm')
panel(d,(0,610,1280,720));txt(d,224,628,'MOCHILA / DEFENSA',12,GREEN,True)
rect(d,(220,670,990,672),'#b08a51')
for x,y,label in [(78,632,'↑'),(78,686,'↓'),(24,686,'←'),(132,686,'→')]:badge(d,x,y,label)
button(d,(1024,634,1240,696),'E / ACCIÓN',20);png(im,'Hud')

duck_portrait=Image.open(ROOT/'Animations/Boss/Default/000.png').resize((112,112),Image.Resampling.NEAREST)
for i in range(6):
    im,d=ui(color=(18,29,28,190));panel(d,(264,64,1008,598));panel(d,(304,88,968,128),'#e7c68b')
    txt(d,636,108,'ECOGAME / EDICIÓN PIXEL',15,INK,True,'mm')
    if i==0:
        txt(d,636,175,'GUARDIANES DEL PARQUE',34,INK,True,'mm');txt(d,636,220,'El ataque de Don Mugrón',26,GREEN,True,'mm');txt(d,636,272,'Recoge. Separa. Prepara la defensa.',18,INK,False,'mm')
        for j,(h,t) in enumerate([('01 RECUPERA','Separa los 12 residuos del parque.'),('02 PREPARA','Cada entrega carga un contenedor.'),('03 DEFIENDE','Esquiva al pato y usa su color.')]):
            y=316+j*56;panel(d,(316,y-8,956,y+40),'#e7cc91');txt(d,334,y+5,h,16,GREEN,True);txt(d,520,y+5,t,15)
        label='COMENZAR LA AVENTURA';hint='Un parque. Dos desafíos. Un pato con malas ideas.'
    elif i==1:
        txt(d,636,190,'UN RESPIRO PARA EL GUARDIÁN',28,INK,True,'mm');txt(d,636,250,'La partida y las animaciones están en pausa.',18,INK,False,'mm')
        for y,t in [(318,'WASD / flechas / cruceta: caminar'),(364,'E / espacio: entregar o disparar'),(410,'H: guía · M: sonido · P / Esc: pausa')]:txt(d,636,y,t,19,INK,False,'mm')
        label='VOLVER AL PARQUE';hint='El agua, los ataques y los proyectiles también esperan.'
    elif i==2:
        txt(d,636,166,'LA SEPARACIÓN ES TU SUPERPODER',26,INK,True,'mm')
        for j,(h,t,col) in enumerate([('1 ORGÁNICOS','Cáscaras y corazones de fruta.','#426b3f'),('2 ENVASES','Botellas PET y latas vacías.','#97702e'),('3 PAPEL','Hojas limpias y cartón seco.','#3a6a89')]):
            y=210+j*74;panel(d,(316,y,956,y+64),'#e7cc91');txt(d,336,y+12,h,18,col,True);txt(d,336,y+38,t,17)
        txt(d,636,454,'JEFE: esquiva el rojo y usa el color de su escudo.',15,GREEN,True,'mm');txt(d,636,482,'Los colores pueden variar de los de tu localidad.',13,INK,False,'mm')
        label='ENTENDIDO, ¡A CUIDAR!';hint='La guía también detiene el reloj.'
    elif i==3:
        txt(d,636,184,'¡DON MUGRÓN SE RETIRA!',32,INK,True,'mm');txt(d,636,244,'El parque está limpio. Y esta vez, a salvo.',19,GREEN,False,'mm')
        for x in [560,636,712]:
            pts=[(round((x+25*math.cos(math.pi/5*k-math.pi/2)*(1 if k%2==0 else .45))/2),round((335+25*math.sin(math.pi/5*k-math.pi/2)*(1 if k%2==0 else .45))/2)) for k in range(10)];d.polygon(pts,fill='#b67e2f')
        txt(d,636,401,'Tu mejor defensa fue aprender a separar.',18,INK,False,'mm');label='DEFENDERLO OTRA VEZ';hint='Victoria: parque recuperado y jefe derrotado.'
    elif i==4:
        txt(d,636,184,'TODO GUARDIÁN APRENDE',32,INK,True,'mm');txt(d,636,248,'El intento terminó. La próxima acción cuenta.',18,INK,False,'mm')
        txt(d,636,326,'Sal de las zonas rojas antes del impacto.',18,GREEN,True,'mm');txt(d,636,378,'Espera la abertura y usa un contenedor de su color.',16,INK,False,'mm');label='VOLVER A INTENTAR';hint='Enter para volver al comienzo.'
    else:
        txt(d,636,172,'¡DON MUGRÓN HA LLEGADO!',28,INK,True,'mm');im.alpha_composite(duck_portrait,(388,118))
        for y,t in [(232,'¡Cuac! Quiere volver a ensuciar el parque.'),(279,'1. Sal del rojo antes del impacto.'),(321,'2. Espera a que anuncie ABERTURA.'),(363,'3. E junto al contenedor de su color.'),(411,'Tienes 4 cargas en cada contenedor.'),(454,'6 aciertos. Recuperas 3 vidas.')]:txt(d,316,y,t,16,INK,y in [232,454])
        label='¡A DEFENDER EL PARQUE!';hint='90 segundos · a media vida, el pato acelera.'
    button(d,(402,516,878,574),label,20);txt(d,640,636,hint,16,WHITE,False,'mm');png(im,'Overlay',i)

# Crisp, low-resolution combat graphics share the world's four-pixel grid.
for i,col in enumerate(['#77b85c','#e8b551','#69a8bd']):
    im=Image.new('RGBA',(60,60));d=ImageDraw.Draw(im);d.ellipse((2,2,57,57),outline=col,width=1)
    for x,y in [(30,2),(2,30),(57,30),(30,57)]:d.rectangle((x-1,y-1,x+1,y+1),fill=WHITE)
    png(im,'Halo',i)
    im=Image.new('RGBA',(8,8));d=ImageDraw.Draw(im);d.rectangle((2,1,5,6),fill=col);d.rectangle((1,2,6,5),fill=col);d.rectangle((3,2,4,3),fill=WHITE);png(im,'Bolt',i)
set_frames('Warning',4)
for i in range(4):
    im=Image.new('RGBA',(48,48));d=ImageDraw.Draw(im);r=18 if i<2 else 23
    if i%2==0:
        d.ellipse((24-r,24-r,24+r,24+r),outline='#de6b42',width=1)
        for ang in range(0,360,45):
            x=round(24+(r-1)*math.cos(math.radians(ang)));y=round(24+(r-1)*math.sin(math.radians(ang)));d.rectangle((x,y,x+1,y+1),fill='#f5d48b')
        d.rectangle((23,15,24,26),fill=WHITE);d.rectangle((23,29,24,30),fill=WHITE)
    else:
        d.ellipse((25-r,25-r,23+r,23+r),fill='#684832',outline='#c7814a',width=1)
        for x,y in [(17,18),(27,29),(29,18)]:d.rectangle((x,y,x+2,y+2),fill='#a97847')
    png(im,'Warning',i)
size('Warning',192,192)
im,d=ui(410,64);panel(d,(0,0,410,64),'#3a4030');rect(d,(18,40,392,50),'#60402d');png(im,'BossPanel');size('BossPanel',410,64)
im=Image.new('RGBA',(4,4),'#e0b65c');png(im,'BossBar')

# Simple native particle tiles add movement without changing collision geometry.
obj('Water',frames=8)
obj('Leaves',frames=4,variables={'BaseX':'number','BaseY':'number','Seed':'number'})
obj('Spark',frames=4,variables={'Life':'number'})
instance('Water',210,275,224,144,'Parque')
for x,y,seed in [(356,256,0),(926,365,2),(1132,480,4),(116,405,6)]:instance('Leaves',x,y,32,32,'Parque',vs={'BaseX':x,'BaseY':y,'Seed':seed})
instance('Spark',-100,-100,64,64,'Parque',vs={'Life':0})
for i in range(8):
    im=Image.new('RGBA',(56,36));d=ImageDraw.Draw(im)
    for k,(x,y) in enumerate([(9,10),(28,8),(39,19),(17,27)]):
        phase=(i+k)%8;dx=phase//3;length=[3,5,7,5,3,2,0,0][phase]
        if length:d.line((x+dx,y,x+dx+length,y),fill='#b4e6ce' if k%2 else '#e5f2cf')
    png(im,'Water',i)
for i in range(4):
    im=Image.new('RGBA',(8,8));d=ImageDraw.Draw(im);d.polygon([(2,2),(5,1),(6,4),(3,6),(2,4)],fill='#a5bd55');d.line((2,6,5,2),fill='#557745');png(im.rotate(i*90,Image.Resampling.NEAREST),'Leaves',i)
    im=Image.new('RGBA',(16,16));d=ImageDraw.Draw(im);r=max(1,5-i)
    d.rectangle((7,8-r,8,8+r),fill='#ffe8a0');d.rectangle((8-r,7,8+r,8),fill='#ffe8a0')
    for x,y in [(3,3),(12,4),(4,12),(12,12)]:d.point((x,y),fill='#dba44b')
    png(im,'Spark',i)

for n,v in [('Facing',0),('AnimClock',0),('BossHurt',0)]:var(n,v)
start=events.findall('event-block')[0].find('actions')
for n in ['Facing','AnimClock','BossHurt']:start.append(sv(n,0))
for e in events.findall('.//event-block'):
    cs=e.find('conditions');ac=e.find('actions')
    # Pick a single overlapping item, including when two items are close together.
    if any(z.get('type')=='Player' and z.get('id')=='1' and z.findtext('param')=='Trash' for z in cs):
        cs.append(c('Trash',-15,0,'Player.X','Player.Y'))
        ac.extend([a('Spark',-3,'Trash.X','Trash.Y'),a('Spark',-10,'Life',.28)])
    for z in list(ac):
        typ=z.get('type');idx=z.get('id')
        if typ=='Player' and z.get('behavior')=='Walk' and idx=='7':
            control=int(z.findtext('param'));ac.append(sv('Facing',{0:4,1:8,2:12,3:0}[control]))
        if typ=='Player' and idx=='5':
            z.find('param').text='Facing+floor(AnimClock*8)%4' if 'floor' in z.findtext('param') else 'Facing'
        if typ=='System' and idx=='-9' and z.findtext('param')=='TimeLeft' and z.findtext("param[@id='1']")=='max(0,TimeLeft-dt)':
            ac.extend([sv('AnimClock','AnimClock+dt'),sv('BossHurt','max(0,BossHurt-dt)'),a('Spark',-10,'Life','max(0,Spark.Life-dt)')])
        if typ=='Warning' and idx in ['-5','-6']:z.find('param').text='192'
        if typ=='Warning' and idx=='5':z.find('param').text='(BossHP<=3 ? 2 : 0)+(BossClock<(BossHP<=3 ? 0.9 : 1.35) ? 0 : 1)'
        if typ=='System' and idx=='-9' and z.findtext('param')=='BossHP' and 'max' in (z.findtext("param[@id='1']") or ''):
            ac.extend([sv('BossHurt',.28),a('Spark',-10,'Life',.28),a('Spark',-3,'Boss.X','Boss.Y-20')])
ev([c('System',-1)],[a('Water',5,'floor(AnimClock*5)%8'),a('Leaves',5,'floor(AnimClock*4+Leaves.Seed)%4'),a('Leaves',-3,'Leaves.BaseX+sin(AnimClock*45+Leaves.Seed*40)*12','Leaves.BaseY+(AnimClock*13+Leaves.Seed*12)%70'),a('Spark',5,'min(3,floor((0.28-Spark.Life)*14))'),a('Spark',-16,'min(100,Spark.Life/0.08*100)')])
ev([cv('State',1),cv('Stage',1)],[a('Boss',5,'BossHurt>0 ? 5 : (BossClock<(BossHP<=3 ? 0.9 : 1.35) ? 2+floor(AnimClock*8)%2 : (BossClock<(BossHP<=3 ? 1.35 : 1.8) ? 3 : (floor(AnimClock*3)%2=0 ? 4 : 1)))')])

project.find('version').text='3.0.0.0'
project.find('description').text='Edición pixel: parque vivo, caminata en cuatro direcciones y Don Mugrón animado. Dos fases de juego en Construct.'
project.find('pixel-rounding').text='1'
for p in project.findall('configuration-settings/prop'):
    if p.get('name')=='Sampling':p.text='Point'
for ins in layout.findall('.//instance'):
    f=ins.find('properties/font')
    if f is not None:f.text=f.text.replace('Arial','Consolas')
# Materialize reused element references and give every condition/action a unique SID.
sheet=E.fromstring(E.tostring(sheet))
for elem in sheet.iter():
    if 'sid' in elem.attrib:elem.set('sid',ident())
for p in ['EcoGame.caproj','New project.caproj']:m['g']['write'](project,Path(p))
m['g']['write'](layout,Path('Layouts/Layout 1.xml'));m['g']['write'](sheet,Path('Event sheets/Event sheet 1.xml'))
count=len(sheet.findall('.//event-block'))+len(sheet.findall('events/variable'));assert count<=100,count
with zipfile.ZipFile(ROOT/'EcoGame.capx','w',zipfile.ZIP_DEFLATED) as z:
    z.write(ROOT/'EcoGame.caproj','EcoGame.caproj')
    for folder in ['Animations','Layouts','Event sheets','Files','Sounds','Music']:
        for f in (ROOT/folder).rglob('*'):
            if f.is_file() and '.uistate.' not in f.name:z.write(f,f.relative_to(ROOT))
print('PIXEL V3:',len(project.findall('object-folder/object-type')),'types;',count,'event budget; 16 walk frames, 6 boss poses, water, leaves and sparks.')
