"""Compact HUD, pause settings and Don Mugron's visible volley / rage charge."""
from pathlib import Path
import runpy, xml.etree.ElementTree as E, zipfile
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
m=runpy.run_path(str(ROOT/'tools/build_readable.py'))
project,layout,sheet,events=[m[k] for k in ['project','layout','sheet','events']]
a,c,el,png,canvas,box,text,save,button,card,ident=[m[k] for k in ['a','c','el','png','canvas','box','text','save','button','card','ident']]
def sv(n,v):return a('System',-9,n,v)
def cv(n,v,op=0):return c('System',-14,n,v,op)
def ev(cs,actions):
    e=el(events,'event-block',sid=ident());cc=el(e,'conditions');cc.extend(cs);aa=el(e,'actions');aa.extend(actions);return e
def world(ins,**values):
    for k,v in values.items():ins.find('world/'+k).text=str(v)
def instance(name):return layout.find(f".//instance[@type='{name}']")

# The whole lower panel is gone. Only game state, one pause button and a small
# contextual card occupy the play view; settings are on the paused layer.
im,d=canvas();box(d,(0,0,1280,62),'#fffbed');text(d,24,19,'ECOGAME',23,bold=True)
for x,label in [(410,'PUNTOS'),(590,'RESIDUOS'),(785,'TIEMPO'),(965,'VIDAS')]:text(d,x,8,label,12,bold=True)
button(d,(1176,9,1262,53),'II')
card(d,(16,78,370,211));text(d,30,90,'CONSEJO',13,bold=True)
card(d,(16,634,348,696));text(d,76,643,'MOCHILA',11,bold=True);save(im,'Hud')
for name,x,w in [('ScoreText',410,150),('CleanText',590,170),('TimeText',785,150),('LivesText',965,160)]:world(instance(name),x=x,y=26,width=w,height=31)
world(instance('Progress'),x=590,y=58)
world(instance('TipText'),x=30,y=114,width=326,height=90);instance('TipText').find('properties/font').text='Arial,-21'
world(instance('HeldIcon'),x=47,y=665,width=45,height=45)
world(instance('CarryText'),x=76,y=663,width=265,height=28);instance('CarryText').find('properties/font').text='Arial,-20'
world(instance('BossPanel'),x=1029,y=111,width=410,height=64)
world(instance('BossText'),x=830,y=89,width=396,height=34)
world(instance('BossBar'),x=1029,y=125)
world(instance('ActionText'),x=-1000,y=-1000)
for ins in layout.findall(".//instance[@type='Hit']"):
    cmd=int(ins.findtext('instance-variables/Command'))
    world(ins,x=1219 if cmd==2 else -1000,y=31 if cmd==2 else -1000,width=86 if cmd==2 else 1,height=44 if cmd==2 else 1)
sound=instance('SoundText');owner=next(n for n in layout.findall('.//instances') if sound in list(n));owner.remove(sound);layout.find("layers/layer[@name='Pantallas']/instances").append(sound)
world(sound,x=433,y=465,width=220,height=30);sound.find('properties/font').text='Arial,-22';sound.find('properties/color').text='255,255,255'

im,d=canvas(color=(19,43,36,185));card(d,(264,64,1008,598));text(d,636,112,'PAUSA · CONTROLES Y AJUSTES',19,bold=True,anchor='mm')
text(d,636,177,'Un respiro en el parque',36,bold=True,anchor='mm')
for y,t in [(244,'WASD o flechas: caminar'),(292,'Pasa sobre un residuo para recogerlo'),(340,'E o espacio: entregar / disparar'),(388,'P o Esc: pausar / continuar · M: música')]:text(d,636,y,t,23,anchor='mm')
button(d,(392,451,650,499));button(d,(676,451,884,499),'GUÍA [H]');button(d,(403,516,877,574),'CONTINUAR');save(im,'Overlay',1)
# Keep the main confirm button and add separately gated pause settings targets.
for name,x,w in [('PauseMusic',521,258),('PauseGuide',780,208)]:
    m['add_sprite'](name,1,'Confirm');png(Image.new('RGBA',(8,8)),name)
    m['add_instance'](name,'Confirm','Pantallas',x,475,w,48)
    ev([c('Touch',3,name),cv('State',2)],[sv('Cmd',6 if name=='PauseMusic' else 3)])

# Sprite sheets for actual flying cans and dirt clods, with light edge outlines.
m['add_sprite']('EnemyShot',2,'Bolt')
shotdef=project.find("object-folder/object-type[@name='EnemyShot']")
vs=el(shotdef,'instance-variables');el(vs,'instance-variable',name='Spread',type='number')
can=Image.open(ROOT/'Animations/Trash/Default/003.png').convert('RGBA')
# Draw the can independently of its pickup backplate.
im,d=canvas(48,48);box(d,(12,8,35,39),'#b9c9c6',7,'#354c48',2);box(d,(11,7,36,13),'#e8eece',4,'#354c48',2);box(d,(16,18,31,31),'#d17146',3);text(d,24,25,'X',12,'#fffbed',True,'mm');save(im,'EnemyShot',0)
im,d=canvas(48,48)
for xy in [(8,16,35,42),(16,8,41,34),(5,19,24,36)]:d.ellipse(tuple(v*2 for v in xy),fill='#8a6241',outline='#483c2e',width=3)
for x,y in [(15,25),(29,16),(33,31),(22,36)]:d.ellipse((x*2,y*2,(x+4)*2,(y+3)*2),fill='#b99161')
save(im,'EnemyShot',1)
m['add_instance']('EnemyShot','Bolt','Parque',-100,-100,48,48)
base=instance('EnemyShot');el(base,'instance-variables');el(base.find('instance-variables'),'Spread',0)
for spread in [-58,58]:
    ins=E.fromstring(E.tostring(base));ins.set('uid',ident());ins.find('instance-variables/Spread').text=str(spread);layout.find("layers/layer[@name='Parque']/instances").append(ins)
m['add_sprite']('ChargeTrail',1,'Halo');im,d=canvas(256,36);box(d,(0,6,255,30),(222,72,43,90),10,'#ffbd68',2)
for x in range(18,244,40):d.polygon([(x*2,9*2),((x+18)*2,18*2),(x*2,27*2)],fill='#ffdc96')
save(im,'ChargeTrail');m['add_instance']('ChargeTrail','Halo','Parque',-100,-100,100,36)

wind='(BossHP<=3 ? 0.75 : 1.35)';impact=f'({wind}+0.45)';opening='(BossHP<=3 ? 3.2 : 1.8)'
# Adapt the existing fight in place. The charge is protected, then the duck
# returns and exposes its shield; ammo still cannot be wasted outside openings.
for e in events.findall('.//event-block'):
    for z in e.findall('conditions/condition')+e.findall('actions/action'):
        typ,idx=z.get('type'),z.get('id')
        for p in z.findall('param'):
            if p.text:
                p.text=p.text.replace('(BossHP<=3 ? 0.9 : 1.35)',wind).replace('(BossHP<=3 ? 1.35 : 1.8)',opening).replace('(BossHP<=3 ? 4.4 : 6)','(BossHP<=3 ? 4.4 : 6)')
        # Old computed opening was (windup+0.45) in shoot and impact events.
        if typ=='System' and idx=='-8' and z.findtext("param[@id='0']")=='BossClock':
            p=z.find("param[@id='2']")
            if p is not None and p.text==f'({wind}+0.45)' and z.findtext("param[@id='1']")=='5':p.text=opening
        if typ=='BossBar' and idx=='-3':z.find("param[@id='0']").text='842+BossHP/6*187';z.find("param[@id='1']").text='125'
        if typ=='Warning' and idx=='-16':z.find('param').text=f'BossClock<{impact} ? 100 : 0'
        if typ=='BossText' and idx=='0':z.find('param').text='"DON MUGRÓN " & BossHP & "/6 · " & (BossHP<=3 ? (BossClock<1.2 ? "LLUVIA" : (BossClock<1.95 ? "¡EMBESTIDA!" : (BossClock<3.2 ? "¡CORRE!" : "ATACA"))) : (BossClock<1.8 ? "¡ESQUIVA!" : "ATACA"))'
        if typ=='CarryText' and idx=='0':z.find('param').text='Stage=0 ? (Carry=0 ? "Vacía" : ItemName) : ("Cargas: " & (Shield=1 ? "VERDE" : (Shield=2 ? "AMARILLO" : "AZUL")))'
        if typ=='TipText' and idx=='0':z.find('param').text=f'TipTime>0 ? Tip : (Stage=0 ? (Carry=0 ? "Busca un residuo en el parque." : "Sigue la flecha hasta su contenedor.") : (BossHP<=3 & BossClock>=1.2 & BossClock<3.2 ? "¡Embestida! Apártate de la trayectoria naranja." : (BossClock<{opening} ? "Esquiva las latas y la tierra." : "¡Abertura! Dispara desde el contenedor señalado.")))'
        if typ=='BossPanel' and idx=='-15':z.find('param').text='1'

# Projectile flight is clock driven, so pausing freezes every trajectory.
# Side shots only become dangerous in rage; the warning locks their destination.
t=f'clamp(BossClock/{wind},0,1)'
active=[cv('State',1),cv('Stage',1)]
ev([c('System',-1)],[a('SoundText',-16,'State=2 ? 100 : 0'),a('BossPanel',-16,'Stage=1 ? 100 : 0'),a('BossText',-16,'Stage=1 ? 100 : 0'),a('EnemyShot',-16,f'Stage=1 & State=1 & BossClock<{wind} ? (BossHP<=3 ? 100 : (EnemyShot.Spread=0 ? 100 : 0)) : 0'),a('ChargeTrail',-16,'Stage=1 & State=1 & BossHP<=3 & BossClock>=1.2 & BossClock<2.55 ? 80 : 0')])
ev(active,[a('EnemyShot',-15,1),a('EnemyShot',5,'EnemyShot.Spread=0 ? 0 : 1'),a('EnemyShot',-3,f'1045+(Warning.X+EnemyShot.Spread-1045)*{t}',f'300+(Warning.Y-300)*{t}-sin({t}*180)*145'),a('EnemyShot',-22,'EnemyShot.X+cos(BossClock*660+EnemyShot.Spread)*100','EnemyShot.Y+sin(BossClock*660+EnemyShot.Spread)*100'),a('ChargeTrail',-15,1),a('ChargeTrail',-3,'(1045+Warning.X)/2','(325+Warning.Y)/2'),a('ChargeTrail',-5,'distance(1045,325,Warning.X,Warning.Y)'),a('ChargeTrail',-22,'Warning.X','Warning.Y')])
ev(active+[c('EnemyShot',1,'Player'),cv('Invuln',0),c('System',-8,'BossClock',4,f'{wind}*0.55'),c('System',-8,'BossClock',2,wind),c('System',-8,'EnemyShot.Opacity',4,50)],[sv('Lives','Lives-1'),sv('Invuln',1.1),sv('Tip','"¡Te alcanzó la basura! Sigue moviéndote."'),sv('TipTime',2)])
q='(BossClock<2.55 ? clamp((BossClock-1.95)/0.6,0,1) : (1-clamp((BossClock-2.55)/0.65,0,1)))'
charge=ev(active+[cv('BossHP',3,3),c('System',-8,'BossClock',5,1.2),c('System',-8,'BossClock',2,3.2)],[a('Boss',-3,f'1045+(Warning.X-1045)*{q}',f'325+(Warning.Y-325)*{q}'),a('Boss',5,'BossClock<1.95 ? 2 : 3'),a('Halo',-3,'Boss.X','Boss.Y')])
# Evaluate charging position before the existing body-contact damage check.
events.remove(charge);body=next(e for e in events.findall('event-block') if any(z.get('type')=='Player' and z.findtext('param')=='Boss' for z in e.findall('conditions/condition')));events.insert(list(events).index(body),charge)
project.find('version').text='4.0.0.0';project.find('description').text='Vista despejada, ajustes en pausa, consejos en esquina y Don Mugrón con lluvia de basura y embestida furiosa.'
# Normalize SID uniqueness after cloning references and preserve native resources.
for r in [project,layout,sheet]:
    for n in r.iter():
        if 'sid' in n.attrib:n.set('sid',ident())
for p in ['EcoGame.caproj','New project.caproj']:m['write'](project,p)
m['write'](layout,'Layouts/Layout 1.xml');m['write'](sheet,'Event sheets/Event sheet 1.xml')
count=len(events.findall('.//event-block'))+len(events.findall('variable'));assert count<=100,count
with zipfile.ZipFile(ROOT/'EcoGame.capx','w',zipfile.ZIP_DEFLATED) as z:
    z.write(ROOT/'EcoGame.caproj','EcoGame.caproj')
    for folder in ['Animations','Layouts','Event sheets','Files','Sounds','Music']:
        for f in (ROOT/folder).rglob('*'):
            if f.is_file() and '.uistate.' not in f.name:z.write(f,f.relative_to(ROOT))
print('V4:',len(project.findall('object-folder/object-type')),'types;',count,'event budget')
