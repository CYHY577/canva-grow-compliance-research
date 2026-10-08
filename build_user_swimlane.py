from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(r"C:\Users\pc\Desktop\canva测试")
OUT=ROOT/"output"/"Canva_AI_海报文字合规审核_用户流程泳道图.png"
OUT.parent.mkdir(parents=True,exist_ok=True)
W,H=2600,1700
im=Image.new("RGB",(W,H),"#FFFFFF"); d=ImageDraw.Draw(im)
reg=r"C:\Windows\Fonts\msyh.ttc"; bold=r"C:\Windows\Fonts\msyhbd.ttc"
FT=ImageFont.truetype(bold,54); FS=ImageFont.truetype(reg,24); FL=ImageFont.truetype(bold,28); FN=ImageFont.truetype(bold,25); FB=ImageFont.truetype(reg,21); FE=ImageFont.truetype(bold,20)
INK="#25212B"; MUTED="#6E6875"; PURPLE="#7D2AE8"; PBG="#F5EEFF"; BLUE="#2B6DE5"; BBG="#EDF4FF"; GREEN="#17865A"; GBG="#EAF8F2"; RED="#BF3F30"; RBG="#FFF0ED"; AMBER="#A56D00"; ABG="#FFF4D6"; GRAY="#68636D"; XBG="#F0EFF2"; BORDER="#DCD6E2"

def center(rect,text,font=FN,color=INK,gap=5):
    lines=text.split("\n"); hs=[d.textbbox((0,0),t,font=font)[3] for t in lines]; y=rect[1]+(rect[3]-rect[1]-sum(hs)-gap*(len(lines)-1))/2
    for t,h in zip(lines,hs):
        bb=d.textbbox((0,0),t,font=font); d.text((rect[0]+(rect[2]-rect[0]-(bb[2]-bb[0]))/2,y),t,font=font,fill=color); y+=h+gap

def box(x,y,w,h,text,fill="#FFFFFF",stroke=PURPLE,font=FN,radius=20):
    r=(x,y,x+w,y+h); d.rounded_rectangle(r,radius=radius,fill=fill,outline=stroke,width=4); center(r,text,font); return r

def arrow(points,color=PURPLE,label=None,pos=None,dashed=False):
    if dashed:
        for i in range(len(points)-1):
            a,b=points[i],points[i+1]; dist=max(abs(b[0]-a[0]),abs(b[1]-a[1])); n=max(1,int(dist/18))
            for s in range(0,n,2):
                t1=s/n; t2=min((s+1)/n,1); d.line((a[0]+(b[0]-a[0])*t1,a[1]+(b[1]-a[1])*t1,a[0]+(b[0]-a[0])*t2,a[1]+(b[1]-a[1])*t2),fill=color,width=5)
    else: d.line(points,fill=color,width=6,joint="curve")
    a,b=points[-2],points[-1]
    if abs(b[0]-a[0])>=abs(b[1]-a[1]): tri=[(b[0],b[1]),(b[0]-18 if b[0]>a[0] else b[0]+18,b[1]-11),(b[0]-18 if b[0]>a[0] else b[0]+18,b[1]+11)]
    else: tri=[(b[0],b[1]),(b[0]-11,b[1]-18 if b[1]>a[1] else b[1]+18),(b[0]+11,b[1]-18 if b[1]>a[1] else b[1]+18)]
    d.polygon(tri,fill=color)
    if label and pos:
        d.rounded_rectangle((pos[0]-7,pos[1]-4,pos[0]+d.textbbox((0,0),label,font=FE)[2]+7,pos[1]+27),radius=6,fill="#FFFFFF"); d.text(pos,label,font=FE,fill=color)

d.text((80,48),"Canva AI 海报文字合规审核：用户流程泳道图",font=FT,fill=INK)
d.text((82,118),"审核在海报生成完成后自动触发；Prompt 只用于生成，合规判断读取最终海报中的可见文字。",font=FS,fill=MUTED)

x0,y0=60,180; labelw=270; laneh=430
lanes=[("用户","#FAF8FC"),("Canva AI","#F6F0FD"),("Compliance\nLayer","#EEF5FF")]
for i,(name,fill) in enumerate(lanes):
    y=y0+i*laneh; d.rounded_rectangle((x0,y,W-60,y+laneh-10),radius=24,fill=fill,outline=BORDER,width=3); d.rounded_rectangle((x0,y,x0+labelw,y+laneh-10),radius=24,fill="#FFFFFF",outline=BORDER,width=3)
    lines=name.split("\n"); yy=y+165-(len(lines)-1)*22
    for line in lines:
        bb=d.textbbox((0,0),line,font=FL); d.text((x0+(labelw-(bb[2]-bb[0]))/2,yy),line,font=FL,fill="#5B20B5"); yy+=42

# 用户泳道
open_ai=box(350,315,290,100,"进入 Canva AI")
input_brief=box(700,315,350,100,"输入海报生成需求")
view_poster=box(1120,315,350,100,"查看生成海报")
view_status=box(1870,305,300,120,"查看审核状态",fill=PBG)

# Canva AI 泳道
generate=box(700,740,350,112,"生成背景图\n与文字图层",fill=PBG)
compose=box(1120,740,350,112,"组合并展示\n可用营销海报",fill=PBG)
update=box(2170,740,330,112,"更新文字或 Context",fill="#FFFFFF")

# Compliance 泳道
trigger=box(1120,1165,320,112,"渲染完成\n自动触发",fill=BBG,stroke=BLUE)
extract=box(1490,1165,320,112,"读取文字图层\nOCR 兜底",fill=BBG,stroke=BLUE)
judge=box(1860,1165,320,112,"校验 Context\n规则协同判断",fill=BBG,stroke=BLUE)
return_state=box(2230,1165,300,112,"返回四态结果",fill=PBG,stroke=PURPLE)

# 主路径
arrow([(open_ai[2],365),(input_brief[0],365)])
arrow([((input_brief[0]+input_brief[2])//2,input_brief[3]),((generate[0]+generate[2])//2,generate[1])],label="生成",pos=(895,545))
arrow([(generate[2],796),(compose[0],796)])
arrow([((compose[0]+compose[2])//2,compose[1]),((view_poster[0]+view_poster[2])//2,view_poster[3])],label="展示",pos=(1310,535))
arrow([((compose[0]+compose[2])//2,compose[3]),((trigger[0]+trigger[2])//2,trigger[1])],label="完成事件",pos=(1310,970))
arrow([(trigger[2],1221),(extract[0],1221)])
arrow([(extract[2],1221),(judge[0],1221)])
arrow([(judge[2],1221),(return_state[0],1221)])
arrow([((return_state[0]+return_state[2])//2,return_state[1]),(2380,1000),(2020,1000),((view_status[0]+view_status[2])//2,view_status[3])],label="呈现",pos=(2045,960))

# 四态与用户动作
sx=2210; sw=330; sh=72; ys=[205,293,381,469]
states=[("可以发布","继续 / 下载 / 发布",GBG,GREEN),("发布前需修改","编辑或应用建议",RBG,RED),("需要补充信息","补监管身份或证据",ABG,AMBER),("不在覆盖范围","查看覆盖 / 调 Context",XBG,GRAY)]
state_rects=[]
for y,(title,action,fill,stroke) in zip(ys,states):
    r=(sx,y,sx+sw,y+sh); d.rounded_rectangle(r,radius=16,fill=fill,outline=stroke,width=4); d.text((sx+17,y+10),title,font=FE,fill=stroke); d.text((sx+17,y+39),action,font=FB,fill=INK); state_rects.append(r)

# 状态分流：由查看状态连到四个选项
d.line([(view_status[2],365),(2190,365)],fill=PURPLE,width=6)
d.line([(2190,241),(2190,505)],fill=PURPLE,width=6)
for r,(_,_,_,stroke) in zip(state_rects,states): arrow([(2190,(r[1]+r[3])//2),(r[0],(r[1]+r[3])//2)],color=stroke)

# 需要处理的三态写回并重检
for r,(_,_,_,stroke) in zip(state_rects[1:],states[1:]):
    sy=(r[1]+r[3])//2
    arrow([(r[2],sy),(2560,sy),(2560,690),(2335,690),(2335,update[1])],color=stroke,dashed=True)
arrow([((update[0]+update[2])//2,update[3]),(2335,1420),(1020,1420),(1020,1110),((trigger[0]+trigger[2])//2,trigger[1])],color=PURPLE,dashed=True,label="自动重检",pos=(1580,1380))

# Ready 的结束提示
d.rounded_rectangle((2210,570,2540,628),radius=29,fill=GBG,outline=GREEN,width=4); center((2210,570,2540,628),"完成",font=FN,color=GREEN)
arrow([((state_rects[0][0]+state_rects[0][2])//2,state_rects[0][3]),(2375,570)],color=GREEN)

# 底部产品原则
d.rounded_rectangle((80,1495,2520,1645),radius=22,fill="#FAF8FC",outline=BORDER,width=3)
d.text((112,1518),"用户侧规则",font=FN,fill=PURPLE)
rules=["后三种状态只阻止发布，不阻断继续对话和编辑","每次结果均展示已检查 / 未检查范围","应用建议后必须重检，修改本身不等于通过","文字或 Context 改变后，旧结果立即失效"]
for i,t in enumerate(rules):
    xx=112+(i%2)*1190; yy=1565+(i//2)*42; d.ellipse((xx,yy+7,xx+13,yy+20),fill=PURPLE); d.text((xx+26,yy),t,font=FB,fill=INK)

im.save(OUT,quality=95)
print(OUT)
