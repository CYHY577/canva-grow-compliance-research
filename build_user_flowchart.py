from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"C:\Users\pc\Desktop\canva测试")
OUT = ROOT / "output" / "Canva_AI_海报文字合规审核_用户流程图.png"
OUT.parent.mkdir(parents=True, exist_ok=True)

W, H = 2400, 1800
im = Image.new("RGB", (W, H), "#FFFFFF")
d = ImageDraw.Draw(im)
reg = r"C:\Windows\Fonts\msyh.ttc"
bold = r"C:\Windows\Fonts\msyhbd.ttc"
FT = ImageFont.truetype(bold, 55)
FS = ImageFont.truetype(reg, 25)
FN = ImageFont.truetype(bold, 28)
FB = ImageFont.truetype(reg, 23)
FL = ImageFont.truetype(bold, 22)

INK="#25212B"; MUTED="#6E6875"; PURPLE="#7D2AE8"; PBG="#F5EEFF"
BLUE="#2B6DE5"; BBG="#EDF4FF"; GREEN="#17865A"; GBG="#EAF8F2"
RED="#BF3F30"; RBG="#FFF0ED"; AMBER="#A56D00"; ABG="#FFF4D6"
GRAY="#68636D"; XBG="#F0EFF2"; BORDER="#DDD7E3"


def text_center(rect, lines, font=FN, color=INK, gap=7):
    if isinstance(lines,str): lines=lines.split("\n")
    hs=[d.textbbox((0,0),t,font=font)[3] for t in lines]
    yy=rect[1]+(rect[3]-rect[1]-(sum(hs)+gap*(len(lines)-1)))/2
    for t,h in zip(lines,hs):
        bb=d.textbbox((0,0),t,font=font)
        d.text((rect[0]+(rect[2]-rect[0]-(bb[2]-bb[0]))/2,yy),t,font=font,fill=color)
        yy+=h+gap


def box(x,y,w,h,text,fill="#FFFFFF",stroke=PURPLE,font=FN,radius=22):
    r=(x,y,x+w,y+h); d.rounded_rectangle(r,radius=radius,fill=fill,outline=stroke,width=4); text_center(r,text,font); return r


def status(x,y,w,title,desc,fill,stroke):
    h=138; r=(x,y,x+w,y+h); d.rounded_rectangle(r,radius=22,fill=fill,outline=stroke,width=4)
    d.text((x+25,y+20),title,font=FN,fill=stroke); d.text((x+25,y+72),desc,font=FB,fill=INK); return r


def diamond(cx,cy,w,h,text):
    pts=[(cx,cy-h//2),(cx+w//2,cy),(cx,cy+h//2),(cx-w//2,cy)]
    d.polygon(pts,fill="#FFFFFF"); d.line(pts+[pts[0]],fill=PURPLE,width=5,joint="curve")
    text_center((cx-w//2+45,cy-h//2+30,cx+w//2-45,cy+h//2-30),text,FN)
    return (cx-w//2,cy-h//2,cx+w//2,cy+h//2)


def arrow(points,color=PURPLE,label=None,label_pos=None,dashed=False):
    if dashed:
        for i in range(len(points)-1):
            a,b=points[i],points[i+1]; dist=max(abs(b[0]-a[0]),abs(b[1]-a[1])); n=max(1,int(dist/18))
            for s in range(0,n,2):
                t1=s/n; t2=min((s+1)/n,1)
                d.line((a[0]+(b[0]-a[0])*t1,a[1]+(b[1]-a[1])*t1,a[0]+(b[0]-a[0])*t2,a[1]+(b[1]-a[1])*t2),fill=color,width=5)
    else: d.line(points,fill=color,width=6,joint="curve")
    a,b=points[-2],points[-1]
    if abs(b[0]-a[0])>=abs(b[1]-a[1]):
        tri=[(b[0],b[1]),(b[0]-18 if b[0]>a[0] else b[0]+18,b[1]-11),(b[0]-18 if b[0]>a[0] else b[0]+18,b[1]+11)]
    else:
        tri=[(b[0],b[1]),(b[0]-11,b[1]-18 if b[1]>a[1] else b[1]+18),(b[0]+11,b[1]-18 if b[1]>a[1] else b[1]+18)]
    d.polygon(tri,fill=color)
    if label and label_pos:
        bb=d.textbbox((0,0),label,font=FL); d.rounded_rectangle((label_pos[0]-8,label_pos[1]-4,label_pos[0]+bb[2]+8,label_pos[1]+30),radius=7,fill="#FFFFFF")
        d.text(label_pos,label,font=FL,fill=color)


# Title
d.text((85,50),"Canva AI 海报文字合规审核：用户流程图",font=FT,fill=INK)
d.text((88,124),"只展示用户能看到和执行的路径；审核在海报生成完成后自动开始，不检查用户 Prompt。",font=FS,fill=MUTED)

# Phase labels
phases=[("1  生成海报",90,690),("2  自动检查",720,1320),("3  用户决策",1350,2310)]
for title,x1,x2 in phases:
    d.rounded_rectangle((x1,185,x2,235),radius=16,fill=PBG)
    d.text((x1+20,194),title,font=FL,fill=PURPLE)

# Main horizontal journey
open_ai=box(95,300,360,112,"进入 Canva AI")
prompt=box(515,300,430,112,"输入海报生成需求")
poster=box(1005,290,460,132,"查看生成的\n广告图片/海报",fill=PBG)
auto=box(1525,290,430,132,"生成完成\n自动检查海报文字",fill=BBG,stroke=BLUE)
state=diamond(2190,356,330,190,"查看\n检查状态")
for a,b in [(open_ai,prompt),(prompt,poster),(poster,auto)]: arrow([(a[2],(a[1]+a[3])//2),(b[0],(b[1]+b[3])//2)])
arrow([(auto[2],356),(state[0],356)])

# Status columns
xs=[90,660,1230,1800]; widths=[480]*4; y=610
ready=status(xs[0],y,widths[0],"可以发布","在已检查范围内未发现问题",GBG,GREEN)
fix=status(xs[1],y,widths[1],"发布前需修改","有明确问题需要先处理",RBG,RED)
need=status(xs[2],y,widths[2],"需要补充信息","还缺信息才能完成判断",ABG,AMBER)
outside=status(xs[3],y,widths[3],"不在覆盖范围","当前组合尚未覆盖",XBG,GRAY)

# Branches from state hub routed above cards
hub=(2190,state[3]); split_y=535
d.line([(2190,state[3]),(2190,split_y)],fill=PURPLE,width=6)
for target,label,color in [(ready,"Ready",GREEN),(fix,"Fix",RED),(need,"Need input",AMBER),(outside,"Outside",GRAY)]:
    tx=(target[0]+target[2])//2
    arrow([(2190,split_y),(tx,split_y),(tx,target[1])],color=color,label=label,label_pos=(tx-55,550))

# Actions
ready_detail=box(140,820,380,100,"查看详情（可选）",stroke=GREEN,font=FB)
ready_go=box(140,970,380,110,"继续 / 下载 / 发布",fill=GBG,stroke=GREEN,font=FN)
ready_end=box(195,1130,270,74,"完成",fill=GBG,stroke=GREEN,font=FN,radius=37)

fix_detail=box(710,820,380,100,"查看标记文字与原因",stroke=RED,font=FB)
fix_edit=box(710,970,380,110,"编辑或应用建议",fill=RBG,stroke=RED,font=FN)

need_detail=box(1280,820,380,100,"查看缺失信息",stroke=AMBER,font=FB)
need_add=box(1280,970,380,110,"补充监管身份或证据",fill=ABG,stroke=AMBER,font=FN)

outside_detail=box(1850,820,380,100,"查看覆盖范围",stroke=GRAY,font=FB)
outside_next=box(1850,970,380,110,"修改 Context 或转人工",fill=XBG,stroke=GRAY,font=FN)

for a,b,color in [(ready,ready_detail,GREEN),(ready_detail,ready_go,GREEN),(ready_go,ready_end,GREEN),(fix,fix_detail,RED),(fix_detail,fix_edit,RED),(need,need_detail,AMBER),(need_detail,need_add,AMBER),(outside,outside_detail,GRAY),(outside_detail,outside_next,GRAY)]:
    arrow([((a[0]+a[2])//2,a[3]),((b[0]+b[2])//2,b[1])],color=color)

# Shared recheck path
recheck=box(850,1325,700,120,"内容或信息更新后自动重新检查",fill=BBG,stroke=BLUE,font=FN)
for a,color in [(fix_edit,RED),(need_add,AMBER),(outside_next,GRAY)]:
    ax=(a[0]+a[2])//2
    arrow([(ax,a[3]),(ax,1245),(1200,1245),(1200,recheck[1])],color=color)

# Loop back to state
arrow([(recheck[2],1385),(2310,1385),(2310,480),(2190,480),(2190,state[3])],color=PURPLE,dashed=True,label="返回新状态",label_pos=(2150,1340))

# User-facing principles
d.rounded_rectangle((90,1525,2310,1695),radius=24,fill="#FAF8FC",outline=BORDER,width=3)
d.text((125,1550),"用户体验原则",font=FN,fill=PURPLE)
principles=[
    "系统自动出现，但不打断用户继续对话和编辑",
    "后三种状态只阻止下载、发布或继续使用",
    "每次结果都展示已检查 / 未检查范围",
    "应用建议后必须重检，修改动作本身不代表通过",
]
for i,t in enumerate(principles):
    xx=125+(i%2)*1080; yy=1602+(i//2)*48
    d.ellipse((xx,yy+7,xx+14,yy+21),fill=PURPLE); d.text((xx+28,yy),t,font=FB,fill=INK)

d.rounded_rectangle((90,1725,2310,1772),radius=15,fill=PBG)
d.text((125,1735),"失效规则：用户修改海报文字或 Context 后，旧结果立即失效，系统自动重新检查。",font=FL,fill=PURPLE)

im.save(OUT,quality=95)
print(OUT)
