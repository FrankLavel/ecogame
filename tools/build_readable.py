"""Readable retro edition: retain animation, restore detail and add clear guidance."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import xml.etree.ElementTree as E
import zipfile

ROOT=Path(__file__).resolve().parents[1]
project=E.parse(ROOT/'EcoGame.caproj').getroot();layout=E.parse(ROOT/'Layouts/Layout 1.xml').getroot();sheet=E.parse(ROOT/'Event sheets/Event sheet 1.xml').getroot();events=sheet.find('events')
sid=max(int(n.get(k)) for root in [project,layout,sheet] for n in root.iter() for k in ['sid','uid'] if n.get(k,'').isdigit())+1000
def ident():
    global sid;sid+=1;return str(sid)
def el(parent,tag,value=None,**attrs):
    node=E.SubElement(parent,tag,{k:str(v) for k,v in attrs.items()})
    if value is not None:node.text=str(value)
    return node
def node(tag,typ,idx,*params):
    n=E.Element(tag,{'type':typ,'id':str(idx),'sid':ident()})
    for i,value in enumerate(params):el(n,'param',value,id=i,name=f'Parameter {i}')
    return n
def a(t,i,*p):return node('action',t,i,*p)
def c(t,i,*p):return node('condition',t,i,*p)
def png(im,name,i=0):
    p=ROOT/f'Animations/{name}/Default/{i:03}.png';p.parent.mkdir(parents=True,exist_ok=True);im.save(p)
def fit(im,size):
    bounds=im.getchannel('A').point(lambda n:255 if n>96 else 0).getbbox();im=im.crop(bounds)
    im.thumbnail((size[0]-4,size[1]-4),Image.Resampling.LANCZOS)
    out=Image.new('RGBA',size);out.alpha_composite(im,((size[0]-im.width)//2,size[1]-im.height-2));return out
def cells(name,cols,rows):
    im=Image.open(ROOT/f'art-source/v3/{name}.png').convert('RGBA');w,h=im.width//cols,im.height//rows
    return [im.crop((i%cols*w,i//cols*h,(i%cols+1)*w,(i//cols+1)*h)) for i in range(cols*rows)]

# Use the original detailed map, without the aggressive 320x180/color reduction.
park=Image.open(ROOT/'art-source/v3/park.png').convert('RGBA').resize((1280,720),Image.Resampling.LANCZOS);png(park,'Park')
for i,im in enumerate(cells('ranger',4,4)):png(fit(im,(32,48)),'Player',i)
# Mirror the left walk cycle so both profiles share silhouette, scale and feet.
for i in range(4):
    with Image.open(ROOT/f'Animations/Player/Default/{i+4:03}.png') as left:
        png(left.transpose(Image.Transpose.FLIP_LEFT_RIGHT),'Player',i+8)
for i,im in enumerate(cells('boss',3,2)):png(fit(im,(112,112)),'Boss',i)

S=2;INK='#254b40';GREEN='#347453';CREAM='#fffbed'
def canvas(w=1280,h=720,color=(0,0,0,0)):
    im=Image.new('RGBA',(w*S,h*S),color);return im,ImageDraw.Draw(im)
def box(d,xy,color,r=0,outline=None,width=1):
    coords=tuple(round(v*S) for v in xy)
    if r:d.rounded_rectangle(coords,r*S,color,outline,width*S)
    else:d.rectangle(coords,color,outline,width*S)
def text(d,x,y,t,n=22,color=INK,bold=False,anchor=None):
    font=ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if bold else 'arial.ttf'),n*S)
    d.text((round(x*S),round(y*S)),t,font=font,fill=color,anchor=anchor)
def save(im,name,i=0):png(im.resize((im.width//S,im.height//S),Image.Resampling.LANCZOS),name,i)
def card(d,xy,fill=CREAM):box(d,xy,fill,16,'#d2b77d',2)
def button(d,xy,label=None):
    box(d,xy,GREEN,14)
    if label:text(d,(xy[0]+xy[2])/2,(xy[1]+xy[3])/2,label,24,'#ffffff',True,'mm')

props=Image.open(ROOT/'art-source/v3/props.png').convert('RGBA');cw=props.width//3;mask=props.getchannel('A').point(lambda n:255 if n>110 else 0);runs=[]
for y in range(mask.height):
    if mask.crop((0,y,mask.width,y+1)).histogram()[255]>12:
        if not runs or y-runs[-1][-1]>8:runs.append([y])
        else:runs[-1].append(y)
bands=sorted(sorted(runs,key=len,reverse=True)[:3],key=lambda r:r[0]);parts=[props.crop((col*cw,max(0,row[0]-2),(col+1)*cw,min(props.height,row[-1]+3))) for row in bands for col in range(3)]
for i,p in enumerate(parts[3:]):
    im,d=canvas(64,64);d.ellipse((2*S,2*S,62*S,62*S),fill='#fffbed',outline='#c8d6b8',width=2*S)
    item=fit(p,(50,50));im.alpha_composite(item.resize((100,100),Image.Resampling.LANCZOS),(14,12));save(im,'Trash',i)
for i,(name,col) in enumerate([('1 ORGÁNICOS','#4c875d'),('2 ENVASES','#bb8b2d'),('3 PAPEL','#487e9e')]):
    im,d=canvas(140,112);body=fit(parts[i],(78,82));im.alpha_composite(body.resize((156,164),Image.Resampling.LANCZOS),(62,0));box(d,(0,82,139,111),CREAM,7,col,2);text(d,70,97,name,17,col,True,'mm');save(im,'Bin',i)
for n,count,size in [('Water',8,(112,72)),('Leaves',4,(16,16)),('Spark',4,(32,32))]:
    for i in range(count):
        p=ROOT/f'Animations/{n}/Default/{i:03}.png';im=Image.open(p).convert('RGBA');png(im.resize(size,Image.Resampling.LANCZOS),n,i)

# Clean high-resolution UI; large type is separate from the retro world art.
im,d=canvas();box(d,(0,0,1280,94),CREAM);box(d,(0,90,1280,94),'#dce6cf')
box(d,(20,20,72,72),GREEN,14);text(d,46,46,'E',34,'#ffffff',True,'mm');text(d,88,20,'ECOGAME',26,INK,True);text(d,88,54,'GUARDIANES DEL PARQUE',12,GREEN,True)
for x,w,label in [(330,150,'PUNTOS'),(492,170,'RESIDUOS'),(676,110,'TIEMPO'),(802,140,'VIDAS')]:box(d,(x,12,x+w,80),'#edf2df',12);text(d,x+14,18,label,15,GREEN,True)
for x,label in [(984,'II'),(1060,'?'),(1136,'♪')]:box(d,(x,21,x+58,72),'#e1ebd1',12);text(d,x+29,47,label,26,INK,True,'mm')
text(d,1214,46,'01',24,GREEN,True,'mm')
box(d,(0,607,1280,720),CREAM);box(d,(0,606,1280,610),'#dce6cf');text(d,240,618,'TU MOCHILA',16,GREEN,True)
for x,y,label in [(78,625,'↑'),(78,682,'↓'),(22,682,'←'),(134,682,'→')]:box(d,(x-21,y-19,x+21,y+19),'#dfebd2',9);text(d,x,y,label,28,GREEN,True,'mm')
button(d,(1025,635,1238,694));text(d,1131,706,'cerca del contenedor',14,GREEN,False,'mm');save(im,'Hud')

portrait=Image.open(ROOT/'Animations/Boss/Default/000.png').resize((170,170),Image.Resampling.LANCZOS)
for i in range(6):
    im,d=canvas(color=(19,43,36,185));card(d,(264,64,1008,598));text(d,636,108,'ECOGAME · GUARDIANES DEL PARQUE',16,GREEN,True,'mm')
    if i==0:
        text(d,636,174,'Recupera el parque',40,INK,True,'mm');text(d,636,232,'Después, defiéndelo de Don Mugrón.',23,GREEN,False,'mm')
        for y,t in [(310,'1. Camina con WASD o las flechas.'),(372,'2. Pasa sobre un residuo para recogerlo.'),(434,'3. Llévalo al contenedor indicado y pulsa E.')]:text(d,636,y,t,23,INK,False,'mm')
        label='COMENZAR';hint='Recoge un residuo a la vez. La flecha te mostrará dónde llevarlo.'
    elif i==1:
        text(d,636,190,'Partida en pausa',38,INK,True,'mm');text(d,636,250,'El tiempo y los ataques están detenidos.',24,GREEN,False,'mm')
        for y,t in [(322,'WASD o flechas: caminar'),(374,'E o espacio: entregar / disparar'),(426,'H: guía · M: sonido · P o Esc: pausa')]:text(d,636,y,t,23,INK,False,'mm')
        label='CONTINUAR';hint='Puedes continuar también con P o Esc.'
    elif i==2:
        text(d,636,166,'¿Dónde va cada residuo?',34,INK,True,'mm')
        for j,(h,t,col) in enumerate([('VERDE · ORGÁNICOS','Cáscaras y restos de fruta.','#43805a'),('AMARILLO · ENVASES','Botellas PET y latas vacías.','#a47a27'),('AZUL · PAPEL','Papel limpio y cartón seco.','#467e9e')]):
            y=210+j*87;box(d,(316,y,956,y+76),'#edf2df',12);text(d,336,y+10,h,23,col,True);text(d,336,y+43,t,21)
        label='ENTENDIDO';hint='La flecha señala el contenedor correcto durante el juego.'
    elif i==3:
        text(d,636,184,'¡Parque limpio y a salvo!',36,INK,True,'mm');text(d,636,248,'Separaste los residuos y venciste a Don Mugrón.',23,GREEN,False,'mm')
        text(d,636,344,'¡Gracias por cuidarlo!',30,INK,True,'mm');text(d,636,405,'Tu puntaje final:',20,GREEN,False,'mm');label='JUGAR OTRA VEZ';hint='Cada residuo en su lugar hace la diferencia.'
    elif i==4:
        text(d,636,184,'Vamos de nuevo',38,INK,True,'mm');text(d,636,250,'Se acabó el tiempo o las vidas.',24,GREEN,False,'mm')
        text(d,636,332,'Recicla siguiendo la flecha del contenedor.',23,INK,False,'mm');text(d,636,390,'Contra el pato: esquiva el rojo y espera «ATACA».',22,INK,False,'mm');label='REINTENTAR';hint='La próxima acción cuenta.'
    else:
        text(d,636,172,'¡Llegó Don Mugrón!',38,INK,True,'mm');im.alpha_composite(portrait.resize((340,340),Image.Resampling.LANCZOS),(1590,454))
        for y,t in [(266,'1. Esquiva el círculo rojo.'),(322,'2. Espera la señal «ATACA».'),(378,'3. Ve al contenedor indicado'),(412,'y pulsa E para disparar.')]:text(d,316,y,t,24,INK,y in [266,322])
        text(d,636,476,'Necesitas 6 aciertos. Tienes 90 segundos.',21,GREEN,True,'mm');label='DEFENDER EL PARQUE';hint='La flecha te indica desde qué contenedor disparar.'
    button(d,(403,516,877,574),label);text(d,640,636,hint,18,'#fff9df',False,'mm');save(im,'Overlay',i)
im,d=canvas(410,64);box(d,(0,0,410,64),CREAM,12,'#d2b77d',2);box(d,(18,43,392,53),'#e2e7d3',5);save(im,'BossPanel')

def add_sprite(name,frames,reference):
    if project.find(f"object-folder/object-type[@name='{name}']") is None:
        obj=E.fromstring(E.tostring(project.find(f"object-folder/object-type[@name='{reference}']")));obj.set('name',name)
        for tag in ['instance-variables','behaviors']:
            old=obj.find(tag)
            if old is not None:obj.remove(old)
        anim=obj.find('animation-folder/animation');first=E.tostring(anim.find('frame'));anim.clear();anim.attrib.update({'name':'Default','framecount':str(frames),'speed':'0','loop':'1','pingpong':'0','repeatcount':'1','repeatto':'0','sid':ident()})
        for _ in range(frames):anim.append(E.fromstring(first))
        project.find('object-folder').append(obj)
def add_instance(name,reference,layer,x,y,w,h):
    if layout.find(f".//instance[@type='{name}']") is not None:return
    ins=E.fromstring(E.tostring(layout.find(f".//instance[@type='{reference}']")));ins.set('type',name);ins.set('uid',ident())
    ins.find('properties/initial-visibility').text='Visible'
    for tag in ['instance-variables','behavior-instances']:
        old=ins.find(tag)
        if old is not None:ins.remove(old)
    for key,val in [('x',x),('y',y),('width',w),('height',h),('opacity',0 if name!='ActionText' else 1)]:ins.find('world/'+key).text=str(val)
    layout.find(f"layers/layer[@name='{layer}']/instances").append(ins)
add_sprite('HeldIcon',6,'Trash');add_sprite('GuideMarker',3,'Halo')
for i in range(6):png(Image.open(ROOT/f'Animations/Trash/Default/{i:03}.png').convert('RGBA'),'HeldIcon',i)
for i,col in enumerate(['#4c875d','#d5a43f','#4b87ac']):
    im,d=canvas(172,164);box(d,(7,31,165,138),(255,251,230,12),15,col,4)
    pts=[(72,160),(100,160),(100,148),(110,148),(86,126),(62,148),(72,148)]
    d.polygon([(x*S,y*S) for x,y in pts],fill='#fffdf0',outline=col,width=3*S);save(im,'GuideMarker',i)
add_instance('HeldIcon','Trash','Interfaz',198,654,56,56);add_instance('GuideMarker','Halo','Parque',470,190,172,164)
if project.find("object-folder/object-type[@name='ActionText']") is None:
    obj=E.fromstring(E.tostring(project.find("object-folder/object-type[@name='CarryText']")));obj.set('name','ActionText');project.find('object-folder').append(obj)
add_instance('ActionText','CarryText','Interfaz',1030,650,203,30)
for ins in layout.findall('.//instance'):
    typ=ins.get('type');props=ins.find('properties');world=ins.find('world')
    if typ=='Trash':world.find('width').text='56';world.find('height').text='56'
    font=props.find('font')
    if font is not None:
        value=30 if typ in ['ScoreText','CleanText','TimeText','LivesText'] else 28 if typ=='CarryText' else 22 if typ=='TipText' else 26 if typ in ['BossText','ActionText'] else 24 if typ=='EndText' else 16
        font.text=f'Arial,-{value}'
    if typ=='CarryText':world.find('x').text='240';world.find('y').text='641';world.find('width').text='760';world.find('height').text='34'
    if typ=='TipText':world.find('x').text='240';world.find('y').text='680';world.find('width').text='760';world.find('height').text='38'
    if typ=='BossText':world.find('y').text='105';props.find('color').text='37,75,64'
    if typ=='ActionText':props.find('text').text='ENTREGAR [E]';props.find('color').text='255,255,255';props.find('horizontal-alignment').text='Center'

for event in events.findall('.//event-block'):
    actions=event.find('actions');conditions=event.find('conditions')
    if any(z.get('type')=='Player' and z.get('id')=='1' and z.findtext('param')=='Trash' for z in conditions):
        if not any(z.get('type')=='HeldIcon' for z in actions):actions.append(a('HeldIcon',5,'Trash.AnimationFrame'))
    writes_tip=any(z.get('type')=='System' and z.get('id')=='-9' and z.findtext('param')=='Tip' for z in actions)
    if writes_tip and not any(z.get('type')=='System' and z.findtext('param')=='TipTime' for z in actions):actions.append(a('System',-9,'TipTime',3))
    ticks_time=any(z.get('type')=='System' and z.get('id')=='-9' and z.findtext('param')=='TimeLeft' and 'max' in (z.findtext("param[@id='1']") or '') for z in actions)
    if ticks_time and not any(z.get('type')=='System' and z.findtext('param')=='TipTime' for z in actions):actions.append(a('System',-9,'TipTime','max(0,TipTime-dt)'))
old=events.find("event-block[@sid='910000']")
if old is not None:events.remove(old)
event=el(events,'event-block',sid='910000');cs=el(event,'conditions');cs.append(c('System',-1));ac=el(event,'actions')
color='(Shield=1 ? "VERDE" : (Shield=2 ? "AMARILLO" : "AZUL"))'
carrycolor='(Carry=1 ? "VERDE" : (Carry=2 ? "AMARILLO" : "AZUL"))'
end='(BossHP<=3 ? 1.35 : 1.8)'
for action in [a('BossPanel',-15,1),a('BossText',-15,1),a('BossText',0,f'Stage=0 ? (Carry=0 ? "1. Recoge un residuo" : "2. Sigue la flecha y entrega") : (BossClock<{end} ? "Esquiva el círculo rojo" : ("ATACA con el " & {color}))'),a('CarryText',0,'Stage=0 ? (Carry=0 ? "Mochila vacía" : ("Llevas: " & ItemName)) : ("Contenedor indicado: " & '+color+')'),a('TipText',0,f'TipTime>0 ? Tip : (Stage=0 ? (Carry=0 ? "Pasa sobre un residuo para recogerlo. Usa WASD o las flechas." : ("Llévalo al contenedor " & {carrycolor} & " y pulsa E.")) : (BossClock<{end} ? "Sal del círculo antes del golpe. Espera para disparar." : "Acércate al contenedor señalado y pulsa E para disparar."))'),a('HeldIcon',-16,'Stage=0 & Carry>0 ? 100 : 0'),a('GuideMarker',5,'(Stage=0 ? max(1,Carry) : Shield)-1'),a('GuideMarker',-3,'470+170*((Stage=0 ? max(1,Carry) : Shield)-1)',190),a('GuideMarker',-16,f'State=1 ? (Stage=0 ? (Carry>0 ? 90 : 0) : (BossClock>={end} ? 90 : 0)) : 0'),a('ActionText',0,'Stage=0 ? "ENTREGAR [E]" : "DISPARAR [E]"')]:ac.append(action)
project.find('version').text='3.1.0.0';project.find('description').text='Retro legible: animaciones conservadas, escenario detallado, texto grande, mochila visible y flechas de ayuda.'
for prop in project.findall('configuration-settings/prop'):
    if prop.get('name')=='Sampling':prop.text='Linear'
def write(root,path):E.indent(root,space='    ');E.ElementTree(root).write(ROOT/path,encoding='utf-8',xml_declaration=True)
for path in ['EcoGame.caproj','New project.caproj']:write(project,path)
write(layout,'Layouts/Layout 1.xml');write(sheet,'Event sheets/Event sheet 1.xml')
count=len(events.findall('.//event-block'))+len(events.findall('variable'));assert count<=100,count
with zipfile.ZipFile(ROOT/'EcoGame.capx','w',zipfile.ZIP_DEFLATED) as z:
    z.write(ROOT/'EcoGame.caproj','EcoGame.caproj')
    for folder in ['Animations','Layouts','Event sheets','Files','Sounds','Music']:
        for f in (ROOT/folder).rglob('*'):
            if f.is_file() and '.uistate.' not in f.name:z.write(f,f.relative_to(ROOT))
print('Readable 3.1:',len(project.findall('object-folder/object-type')),'types,',count,'events; large clean UI and container guidance.')
