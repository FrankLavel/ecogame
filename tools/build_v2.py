"""EcoGame 2: generated detailed art and a native Construct boss encounter."""
from pathlib import Path
import runpy, zipfile, math
import xml.etree.ElementTree as E
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
g=runpy.run_path(str(ROOT/'tools/build_game.py'))
el,obj,instance,ev,c,a,cv,sv,frame,layer,sound=[g[k] for k in ['el','obj','instance','ev','c','a','cv','sv','frame','layer','sound']]
project,layout,sheet,events=[g[k] for k in ['project','layout','sheet','events']]
canvas,box,ellipse,line,text,save=[g[k] for k in ['canvas','box','ellipse','line','text','save']]
INK,CREAM,GREEN,GOLD=[g[k] for k in ['INK','CREAM','GREEN','GOLD']]
src=ROOT/'art-source/v2'
def fit(image,size,padding=0):
    im=Image.open(image).convert('RGBA') if isinstance(image,Path) else image.convert('RGBA')
    out=Image.new('RGBA',size);im.thumbnail((size[0]-padding*2,size[1]-padding*2),Image.Resampling.LANCZOS)
    out.alpha_composite(im,((size[0]-im.width)//2,size[1]-im.height-padding));return out
def png(im,name,index=0):
    dest=ROOT/f'Animations/{name}/Default/{index:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);im.save(dest)
park=Image.open(src/'park.png').convert('RGBA').resize((1280,720),Image.Resampling.LANCZOS)
png(park,'Park')
duck=Image.open(src/'duck.png').convert('RGBA');duck=duck.crop(duck.getbbox())
png(fit(duck,(320,320),8),'Boss')

# Slice generated atlases without altering their art.
if (src/'ranger.png').exists():
    im=Image.open(src/'ranger.png').convert('RGBA');cw,ch=im.width//2,im.height//2
    cells=[im.crop((i%2*cw,i//2*ch,(i%2+1)*cw,(i//2+1)*ch)) for i in range(4)]
    # Ignore near-transparent atlas margins when fitting each full-body pose.
    for i,p in enumerate(cells):
        bounds=p.getchannel('A').point(lambda alpha:255 if alpha>96 else 0).getbbox()
        png(fit(p.crop(bounds),(80,104),3),'Player',i)
if (src/'waste.png').exists():
    im=Image.open(src/'waste.png').convert('RGBA');cw,ch=im.width//3,im.height//2
    for i in range(6):
        p=im.crop((i%3*cw,i//3*ch,(i%3+1)*cw,(i//3+1)*ch));png(fit(p.crop(p.getbbox()),(80,80),5),'Trash',i)
if (src/'bins.png').exists():
    im=Image.open(src/'bins.png').convert('RGBA');cw=im.width//3
    for i,label in enumerate(['1  ORGÁNICOS','2  ENVASES','3  PAPEL']):
        p=im.crop((i*cw,0,(i+1)*cw,im.height));p=fit(p.crop(p.getbbox()),(280,220),28)
        d=ImageDraw.Draw(p);box(d,(3,88,137,109),CREAM,8);text(d,(70,99),label,12,INK,True,'mm');png(p.resize((140,110),Image.Resampling.LANCZOS),'Bin',i)

# Boss markers and projectiles are vector HUD graphics, kept crisp and readable.
colors=['#4cda8d','#ffd260','#68c8ff']
for i,col in enumerate(colors):
    im,d=canvas(240,240)
    ellipse(d,(8,8,232,232),(20,35,28,25));ellipse(d,(18,18,222,222),None,col,7)
    for ang in range(0,360,45):
        x=120+106*math.cos(math.radians(ang));y=120+106*math.sin(math.radians(ang));ellipse(d,(x-4,y-4,x+4,y+4),CREAM)
    save(im,Path(f'Animations/Halo/Default/{i:03}.png'))
    im,d=canvas(40,40);ellipse(d,(1,1,39,39),(250,240,170,40));ellipse(d,(6,6,34,34),col);ellipse(d,(10,10,30,30),CREAM);text(d,(20,21),str(i+1),15,INK,True,'mm');save(im,Path(f'Animations/Bolt/Default/{i:03}.png'))
for i in range(2):
    im,d=canvas(200,200)
    ellipse(d,(5,5,195,195),(217,70,43,40 if i==0 else 145), '#ef7449',3)
    if i==0:
        for ang in range(0,360,30):
            x=100+88*math.cos(math.radians(ang));y=100+88*math.sin(math.radians(ang));ellipse(d,(x-4,y-4,x+4,y+4),'#ffe3a1')
        text(d,(100,100),'!',60,'#fff3ce',True,'mm')
    else:
        for x,y,r in [(80,100,42),(124,102,37),(95,65,34),(103,135,30)]:ellipse(d,(x-r,y-r,x+r,y+r),'#795347')
        for x,y in [(68,78),(120,124),(127,73)]:ellipse(d,(x-7,y-7,x+7,y+7),'#b59662')
    save(im,Path(f'Animations/Warning/Default/{i:03}.png'))
im,d=canvas(410,61);box(d,(0,0,410,61),(24,48,42,235),17);box(d,(18,39,392,49),'#573d33',5);save(im,Path('Animations/BossPanel/Default/000.png'))
im,d=canvas(16,16,'#eea851');save(im,Path('Animations/BossBar/Default/000.png'))

# Extend the native object model after the 21 v1 object types (stable QA indices).
for name,frames in [('Halo',3),('Boss',1),('Warning',2),('Bolt',3),('BossPanel',1),('BossBar',1)]:obj(name,frames=frames,variables={'Flying':'number'} if name=='Bolt' else None)
obj('BossText','Text')
bin_def=project.find("object-folder/object-type[@name='Bin']/instance-variables")
el(bin_def,'instance-variable',name='Stock',type='number')
for ins in layout.findall(".//instance[@type='Bin']"):el(ins.find('instance-variables'),'Stock',0)
instance('Halo',1050,330,230,230)
instance('Boss',1050,315,220,220)
instance('Warning',640,500,150,150)
instance('Bolt',-100,-100,32,32,vs={'Flying':0})
instance('BossPanel',640,127,410,61,'Interfaz')
instance('BossBar',640,141,374,10,'Interfaz')
instance('BossText',442,105,396,34,'Interfaz',txt='',size=20,color='255,248,225',align='Center')
for ins in layout.findall(".//instance[@type='TipText']"):ins.find('properties/font').text='Arial,-16'
for ins in layout.findall(".//instance[@type='Player']"):
    ins.find('world/width').text='62';ins.find('world/height').text='81'
for ins in layout.findall(".//instance[@type='Trash']"):
    ins.find('world/width').text='54';ins.find('world/height').text='54'
for name in ['Halo','Boss','Warning','Bolt','BossPanel','BossBar','BossText']:
    for ins in layout.findall(f".//instance[@type='{name}']"):ins.find('properties/initial-visibility').text='Invisible'

# Six overlays retain the common button bounds while explaining both phases.
for f in project.findall("object-folder/object-type[@name='Overlay']/animation-folder/animation"):
    f.set('framecount','6');new=E.fromstring(E.tostring(f.find('frame')));f.append(new)
for i in range(6):
    im,d=canvas(1280,720,(17,38,36,195))
    box(d,(269,73,1009,608),'#173c32',34);box(d,(265,65,1005,597),CREAM,34)
    box(d,(301,87,969,90),'#dab76e',1);text(d,(635,111),'E C O G A M E   /   CAPÍTULO II',12,GREEN,True,'mm')
    if i==0:
        text(d,(635,178),'Guardianes del parque',38,INK,True,'mm');text(d,(635,222),'El ataque de Don Mugrón',29,GREEN,True,'mm')
        text(d,(635,274),'Recoge. Separa. Prepara la defensa.',20,'#6b7c68',False,'mm')
        rows=[('01  RECUPERA','Separa los 12 residuos antes de 3 minutos.'),('02  PREPÁRATE','Cada entrega carga un contenedor.'),('03  DEFIENDE','Esquiva al pato y devuelve sus ataques.')]
        for j,(h,b) in enumerate(rows):
            y=318+j*57;box(d,(318,y-8,952,y+40),'#edf0db',12);text(d,(337,y+3),h,15,GREEN,True);text(d,(525,y+3),b,15)
        button='COMENZAR LA AVENTURA';hint='Un parque. Dos desafíos. Un pato con muy malas ideas.'
    elif i==1:
        text(d,(635,188),'Un respiro para el guardián.',33,INK,True,'mm');text(d,(635,248),'La partida, los ataques y el reloj están en pausa.',18,'#6b7c68',False,'mm')
        for y,t in [(315,'WASD / flechas / cruceta: caminar'),(359,'E / espacio: entregar o disparar desde un contenedor'),(403,'H: guía   ·   M: sonido   ·   P / Esc: pausa')]:text(d,(635,y),t,18,INK,False,'mm')
        button='VOLVER AL PARQUE';hint='Los proyectiles también esperan a que vuelvas.'
    elif i==2:
        text(d,(635,166),'La separación es tu superpoder.',30,INK,True,'mm')
        for j,(h,b,col) in enumerate([('1  ORGÁNICOS','Cáscaras y corazones de fruta.','#43825b'),('2  ENVASES','Botellas PET y latas vacías.','#b08832'),('3  PAPEL','Hojas limpias y cartón seco.','#528caa')]):
            y=211+j*74;box(d,(320,y,950,y+64),'#edf0db',12);text(d,(339,y+9),h,17,col,True);text(d,(339,y+35),b,16)
        text(d,(635,452),'JEFE: esquiva el rojo, espera la abertura y usa su color.',16,GREEN,True,'mm')
        text(d,(635,482),'Los colores del juego pueden variar de los de tu localidad.',12,'#6b7c68',False,'mm')
        button='ENTENDIDO, ¡A CUIDAR!';hint='La guía detiene el reloj y todos los ataques.'
    elif i==3:
        text(d,(635,184),'¡Don Mugrón se retira!',36,INK,True,'mm');text(d,(635,243),'El parque está limpio. Y esta vez, también a salvo.',20,GREEN,False,'mm')
        for x in [557,635,713]:
            pts=[(x+25*math.cos(math.pi/5*a-math.pi/2)*(1 if a%2==0 else .45),335+25*math.sin(math.pi/5*a-math.pi/2)*(1 if a%2==0 else .45)) for a in range(10)]
            d.polygon([(int(x*2),int(y*2)) for x,y in pts],fill=GOLD)
        text(d,(635,401),'Tu mejor defensa fue aprender a separar.',20,'#6b7c68',False,'mm');button='DEFENDERLO OTRA VEZ';hint='Victoria: parque recuperado y jefe derrotado.'
    elif i==4:
        text(d,(635,183),'Todo guardián aprende.',36,INK,True,'mm');text(d,(635,248),'El intento terminó. La próxima acción cuenta.',20,'#6b7c68',False,'mm')
        text(d,(635,326),'Al pato: muévete cuando aparezca la zona roja.',18,GREEN,True,'mm');text(d,(635,377),'Espera la abertura y usa un contenedor de su color.',18,INK,False,'mm')
        button='VOLVER A INTENTAR';hint='Enter para volver al comienzo.'
    else:
        text(d,(635,171),'¡DON MUGRÓN HA LLEGADO!',30,INK,True,'mm')
        portrait=fit(duck,(350,410),0);im.alpha_composite(portrait,(1600,370))
        for y,t in [(234,'¡Cuac! Quiere volver a ensuciar el parque.'),(281,'1. Sal de las zonas rojas antes del impacto.'),(322,'2. Espera a que anuncie una ABERTURA.'),(363,'3. Pulsa E junto al contenedor de su color.'),(410,'Tus 12 entregas son 4 cargas por contenedor.'),(452,'6 aciertos para vencer. Recuperas 3 vidas.')]:text(d,(316,y),t,15,INK,y in [234,452])
        button='¡A DEFENDER EL PARQUE!';hint='90 segundos · al perder media vida, el pato acelera.'
    box(d,(403,516,877,573),GREEN,18);text(d,(640,545),button,19,CREAM,True,'mm');text(d,(640,636),hint,14,'#fff5d8',False,'mm')
    save(im,Path(f'Animations/Overlay/Default/{i:03}.png'))

# Version and orientation: desktop browsers do not need orientation-lock requests.
project.find('version').text='2.0.0.0'
project.find('description').text='Recupera el Parque Alba y defiéndelo de Don Mugrón con contenedores cargados. Arte detallado y dos fases.'
for p in project.findall('configuration-settings/prop'):
    if p.get('name')=='Orientations':p.text='Any'
for n,v in [('Stage',0),('BossHP',6),('Shield',1),('BossClock',0),('Cooldown',0),('Invuln',0)]:el(events,'variable',v,name=n,type='number',constant=0,static=0,sid=g['ident']())

def vis(n,v):return a(n,-15,v)
def isvar(cond,n):return cond.get('type')=='System' and cond.get('id')=='-14' and cond.findtext('param')==n
base=list(events.findall('event-block'));clear=base[-1];events.remove(clear)
start=base[0].find('actions')
for n,v in [('Stage',0),('BossHP',6),('Shield',1),('BossClock',0),('Cooldown',0),('Invuln',0)]:start.append(sv(n,v))
for n in ['Halo','Boss','Warning','Bolt','BossPanel','BossBar','BossText']:start.append(vis(n,0))
start.append(a('Player',-16,100))
for e in base:
    cs=e.find('conditions');ac=e.find('actions')
    if any(isvar(z,'Carry') for z in cs) or any(z.get('type')=='Trash' for z in cs):cs.append(cv('Stage',0))
    if any(z.get('type')=='Player' and z.get('id')=='1' for z in cs):
        if not any(isvar(z,'Stage') for z in cs):cs.append(cv('Stage',0))
    if any(isvar(z,'State') and z.findtext("param[@id='1']")=='5' for z in cs):cs.append(cv('State',6,1))
    if any(isvar(z,'Clean') for z in cs):
        cs.append(cv('Stage',0));ac.clear()
        for z in [sv('State',6),sv('Stage',1),sv('BossHP',6),sv('Shield',1),sv('BossClock',0),sv('Cooldown',0),sv('Invuln',0),sv('Lives',3),sv('TimeLeft',90),sv('Carry',0),frame(5),layer(1),a('Audio',6,'"music"'),sound('aviso')]:ac.append(z)
        for n in ['Halo','Boss','Warning','BossPanel','BossBar','BossText']:ac.append(vis(n,1))
        ac.append(a('Warning',-16,0))
    for z in list(ac):
        if z.get('type')=='CleanText' and z.get('id')=='0':z.find('param').text='Stage=0 ? (Clean & " / 12") : ("JEFE " & BossHP & "/6")'
        if z.get('type')=='CarryText' and z.get('id')=='0':z.find('param').text='Stage=0 ? (Carry=0 ? "Mochila vacía · encuentra un residuo" : ItemName) : ("Escudo: " & (Shield=1 ? "VERDE" : (Shield=2 ? "AMARILLO" : "AZUL")) & " · E junto al contenedor del mismo color")'
    if any(z.get('type')=='System' and z.get('id')=='-1' for z in cs) and any(z.get('type')=='ScoreText' for z in ac):
        ac.append(a('Player',-16,'Invuln>0 & floor(time*12)%2=0 ? 35 : 100'))
# Deposits charge the selected bin. A correct release consumes a charge only on launch.
correct=next(e for e in events.findall('.//event-block') if any(z.get('type')=='Bin' and z.get('id')=='-7' for z in e.find('conditions')))
correct.find('actions').append(a('Bin',-10,'Stock','Bin.Stock+1'))

g['audio']('aviso',[147,147,220,196,147],.19)
g['audio']('lanzar',[420,660,980],.055)
g['audio']('golpe',[196,294,392,587],.06)
g['audio']('batalla',[146.83,220,293.66,220,146.83,220,349.23,293.66,130.81,196,261.63,196,130.81,196,329.63,261.63,123.47,185,246.94,293.66,123.47,185,293.66,246.94,110,165,220,329.63,293.66,220,185,165],.19,True)
for folder,tag in [('Sounds','sounds-folder'),('Music','music-folder')]:
    project.find(tag).clear()
    for p in (ROOT/folder).glob('*.ogg'):el(project.find(tag),'file',name=p.name)

el(events,'comment','JEFE: el reciclaje carga los tres contenedores. El pato marca zonas, ataca y baja su escudo. Fase rápida a media vida.')
windup='(BossHP<=3 ? 0.9 : 1.35)';end=f'({windup}+0.45)';period='(BossHP<=3 ? 4.4 : 6)'
active=[cv('State',1),cv('Stage',1)]
ev([cv('Cmd',4),cv('State',6)],[sv('Cmd',0),sv('State',1),layer(0),a('Warning',-3,'Player.X','Player.Y+20'),sv('Tip','"¡Muévete cuando veas el rojo! Después busca el color de su escudo."'),sound('batalla',1,1,-12)])
ev(active,[sv('BossClock','BossClock+dt'),sv('Cooldown','max(0,Cooldown-dt)'),sv('Invuln','max(0,Invuln-dt)'),a('Boss',-3,'1045+sin(BossClock*90)*28','325+cos(BossClock*170)*8'),a('Halo',-3,'Boss.X','Boss.Y'),a('Halo',5,'Shield-1'),a('Warning',-16,f'BossClock<{end} ? 100 : 0'),a('Warning',5,f'BossClock<{windup} ? 0 : 1'),a('Warning',-5,'BossHP<=3 ? 190 : 145'),a('Warning',-6,'BossHP<=3 ? 190 : 145'),a('BossBar',-5,'max(1,BossHP/6*374)'),a('BossBar',-3,'453+BossHP/6*187',141),a('BossText',0,f'"DON MUGRÓN · " & (BossClock<{end} ? "¡ESQUIVA!" : "¡ABERTURA!") & " · " & BossHP & "/6"')])
ev(active+[c('System',-8,'BossClock',4,period)],[sv('BossClock',0),a('Warning',-3,'clamp(Player.X,100,1180)','clamp(Player.Y+20,190,555)'),sound('aviso',vol=-15)])
ev(active+[c('System',-8,'BossClock',5,windup),c('System',-8,'BossClock',2,end),cv('Invuln',0),c('System',-8,'distance(Player.X,Player.Y+20,Warning.X,Warning.Y)',2,'BossHP<=3 ? 86 : 63')],[sv('Lives','Lives-1'),sv('Invuln',1.4),sv('Tip','"¡Sal de la zona roja antes del impacto! Parpadeas mientras te recuperas."'),sound('error')])
ev(active+[c('Player',1,'Boss'),cv('Invuln',0)],[sv('Lives','Lives-1'),sv('Invuln',1.4),sv('Tip','"¡Ese pato es enorme! Mantén tu distancia y usa los contenedores."'),sound('error')])
near=[c('Bin',-15,0,'Player.X','Player.Y'),c('System',-8,'distance(Player.X,Player.Y,Bin.X,Bin.Y)',2,105)]
shoot=ev([cv('Cmd',5)]+active+near+[cv('Cooldown',0),c('Bolt',-7,'Flying',0,0)],[sv('Cmd',0)])
subs=el(shoot,'sub-events')
ev([c('Bin',-7,'Kind',0,'Shield'),c('Bin',-7,'Stock',4,0),c('System',-8,'BossClock',5,end)],[a('Bin',-10,'Stock','Bin.Stock-1'),a('Bolt',-10,'Flying',1),a('Bolt',-3,'Bin.X','Bin.Y+20'),a('Bolt',5,'Bin.Kind-1'),vis('Bolt',1),sv('Cooldown',1),sv('Tip','"¡Carga reciclada en camino! Quedan " & Bin.Stock & " en este contenedor."'),sound('lanzar')],subs)
ev([c('System',-22)],[sv('Cooldown',.35),sv('Tip','"No gastaste cargas. Espera la ABERTURA y usa " & (Shield=1 ? "VERDE" : (Shield=2 ? "AMARILLO" : "AZUL")) & "."')],subs)
ev(active+[c('Bolt',-7,'Flying',0,1)],[a('Bolt',-22,'Boss.X','Boss.Y'),a('Bolt',-3,'Bolt.X+cos(Bolt.Angle)*850*dt','Bolt.Y+sin(Bolt.Angle)*850*dt')])
ev(active+[c('Bolt',-7,'Flying',0,1),c('Bolt',1,'Boss')],[a('Bolt',-10,'Flying',0),vis('Bolt',0),sv('BossHP','max(0,BossHP-1)'),sv('Shield','1+(6-BossHP)%3'),sv('Score','Score+250'),sv('Tip','BossHP<=3 ? "¡Mugrón está furioso! Sus avisos son más cortos. ¡Sigue esquivando!" : "¡Impacto! Cambió de escudo: busca el siguiente color."'),sound('golpe')])
ev(active+[cv('BossHP',0)],[sv('State',4),sv('Score','Score+floor(TimeLeft)*2+Lives*50+500'),frame(3),layer(1),vis('Warning',0),vis('Bolt',0),a('EndText',0,'Score & " puntos · pato derrotado · parque a salvo"'),a('Audio',6,'"music"'),sound('victoria')])
events.append(clear)

# Native HUD wording supports cleanup and the boss phase.
hud=Image.open(ROOT/'Animations/Hud/Default/000.png').convert('RGBA').resize((2560,1440),Image.Resampling.LANCZOS);d=ImageDraw.Draw(hud)
box(d,(222,624,500,645),CREAM);text(d,(225,630),'MOCHILA / DEFENSA',11,GREEN,True)
box(d,(1025,635,1238,694),GREEN,18);text(d,(1131,657),'E  /  ACCIÓN',19,CREAM,True,'mm');text(d,(1131,681),'entregar · disparar',11,'#d4e8ca',False,'mm');save(hud,Path('Animations/Hud/Default/000.png'))
for p in ['EcoGame.caproj','New project.caproj']:g['write'](project,Path(p))
sheet=E.fromstring(E.tostring(sheet))
for element in sheet.iter():
    if 'sid' in element.attrib:element.set('sid',g['ident']())
g['write'](layout,Path('Layouts/Layout 1.xml'));g['write'](sheet,Path('Event sheets/Event sheet 1.xml'))
count=len(events.findall('.//event-block'))+len(events.findall('variable'))
assert count<=100,f'Free edition event budget exceeded: {count}'
with zipfile.ZipFile(ROOT/'EcoGame.capx','w',zipfile.ZIP_DEFLATED) as z:
    z.write(ROOT/'EcoGame.caproj','EcoGame.caproj')
    for folder in ['Animations','Layouts','Event sheets','Files','Sounds','Music']:
        for f in (ROOT/folder).rglob('*'):
            if f.is_file() and '.uistate.' not in f.name:z.write(f,f.relative_to(ROOT))
print('V2 built:',len(project.findall('object-folder/object-type')),'types;',count,'event budget; two phases; generated assets imported.')

