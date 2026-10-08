from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(r"C:\Users\pc\Desktop\canva测试")
OUT=ROOT/"output"/"Canva_AI_海报文字合规审核_用户流程泳道图_参考样式.png"
OUT.parent.mkdir(parents=True,exist_ok=True)
W,H=3000,2200
im=Image.new("RGB",(W,H),"#FFFFFF"); d=ImageDraw.Draw(im)
reg=r"C:\Windows\Fonts\msyh.ttc"; bold=r"C:\Windows\Fonts\msyhbd.ttc"
FT=ImageFont.truetype(bold,62); FS=ImageFont.truetype(reg,26); FH=ImageFont.truetype(bold,31); FL=ImageFont.truetype(bold,30); FN=ImageFont.truetype(bold,27); FB=ImageFont.truetype(reg,23); FXS=ImageFont.truetype(reg,20); FNUM=ImageFont.truetype(bold,22); FE=ImageFont.truetype(bold,21)
INK="#1F2430"; MUTED="#606979"; BLUE="#0A5ACD"; BLUE2="#1D73E8"; BLUE_BG="#F2F7FF"; ORANGE="#F26722"; ORANGE_BG="#FFF6EF"; GREEN="#16934A"; GREEN_BG="#F2FBF5"; BORDER="#C8D4E5"; GRID="#D6DFEB"; PURPLE="#7D2AE8"

def center(rect,text,font=FN,color=INK,gap=6):
    lines=text.split("\n"); hs=[d.textbbox((0,0),t,font=font)[3] for t in lines]; y=rect[1]+(rect[3]-rect[1]-sum(hs)-gap*(len(lines)-1))/2
    for t,h in zip(lines,hs):
        bb=d.textbbox((0,0),t,font=font); d.text((rect[0]+(rect[2]-rect[0]-(bb[2]-bb[0]))/2,y),t,font=font,fill=color); y+=h+gap

def action_box(cx,cy,w,h,title,detail,stroke,fill="#FFFFFF"):
    r=(cx-w//2,cy-h//2,cx+w//2,cy+h//2); d.rounded_rectangle(r,radius=20,fill=fill,outline=stroke,width=3)
    tb=d.textbbox((0,0),title,font=FN); d.text((cx-(tb[2]-tb[0])/2,r[1]+30),title,font=FN,fill=stroke)
    lines=detail.split("\n"); yy=r[1]+87
    for line in lines:
        bb=d.textbbox((0,0),line,font=FB); d.text((cx-(bb[2]-bb[0])/2,yy),line,font=FB,fill=INK); yy+=34
    return r

def arrow(points,color="#151922",width=4,dashed=False):
    if dashed:
        for i in range(len(points)-1):
            a,b=points[i],points[i+1]; dist=max(abs(b[0]-a[0]),abs(b[1]-a[1])); n=max(1,int(dist/16))
            for s in range(0,n,2):
                t1=s/n; t2=min((s+1)/n,1); d.line((a[0]+(b[0]-a[0])*t1,a[1]+(b[1]-a[1])*t1,a[0]+(b[0]-a[0])*t2,a[1]+(b[1]-a[1])*t2),fill=color,width=width)
    else: d.line(points,fill=color,width=width,joint="curve")
    a,b=points[-2],points[-1]
    if abs(b[0]-a[0])>=abs(b[1]-a[1]): tri=[(b[0],b[1]),(b[0]-16 if b[0]>a[0] else b[0]+16,b[1]-10),(b[0]-16 if b[0]>a[0] else b[0]+16,b[1]+10)]
    else: tri=[(b[0],b[1]),(b[0]-10,b[1]-16 if b[1]>a[1] else b[1]+16),(b[0]+10,b[1]-16 if b[1]>a[1] else b[1]+16)]
    d.polygon(tri,fill=color)

def user_icon(x,y,color):
    d.ellipse((x+8,y,x+32,y+24),fill=color); d.rounded_rectangle((x,y+28,x+40,y+64),radius=14,fill=color)

def bot_icon(x,y,color):
    d.rounded_rectangle((x,y+10,x+45,y+55),radius=10,outline=color,width=5); d.line((x+22,y,x+22,y+10),fill=color,width=4); d.ellipse((x+18,y-5,x+27,y+4),fill=color); d.ellipse((x+10,y+26,x+17,y+33),fill=color); d.ellipse((x+28,y+26,x+35,y+33),fill=color)

def db_icon(x,y,color):
    d.ellipse((x,y,x+44,y+16),fill=color); d.rectangle((x,y+8,x+44,y+52),fill=color); d.ellipse((x,y+44,x+44,y+60),fill=color); d.ellipse((x+5,y+10,x+39,y+20),fill="#FFFFFF")

# Title
d.text((75,48),"用户流程图（泳道图）",font=FT,fill=INK)
d.text((78,126),"从营销用户视角，展示生成海报、查看自动审核结果、处理问题并完成发布的完整路径（单轮任务）",font=FS,fill=MUTED)

# Main canvas geometry
x0,x1=70,2930; y_header=225; header_h=118; lane_top=y_header+header_h; lane_h=390; label_w=270; col_w=(x1-x0-label_w)//5
d.rounded_rectangle((x0,y_header,x1,lane_top+lane_h*3),radius=24,fill="#FFFFFF",outline=BLUE,width=4)

# Header phase cells with chevrons
phase_colors=["#104FB9","#0E5CCB","#0C68D9","#1777E7","#0D4FBA"]
d.rectangle((x0,y_header,x0+label_w,y_header+header_h),fill="#0A4EB5")
center((x0,y_header,x0+label_w,y_header+header_h),"阶段",FH,"#FFFFFF")
phases=["1. 唤醒与进入","2. 表达需求 / 生成","3. 结果反馈","4. 查看结果 / 处理","5. 任务完成 / 结束"]
for i,(title,color) in enumerate(zip(phases,phase_colors)):
    xa=x0+label_w+i*col_w; xb=xa+col_w
    pts=[(xa,y_header),(xb-24,y_header),(xb,y_header+header_h//2),(xb-24,y_header+header_h),(xa,y_header+header_h),(xa+24,y_header+header_h//2)] if i>0 else [(xa,y_header),(xb-24,y_header),(xb,y_header+header_h//2),(xb-24,y_header+header_h),(xa,y_header+header_h)]
    d.polygon(pts,fill=color); center((xa+18,y_header,xb-25,y_header+header_h),title,FH,"#FFFFFF")

# Lanes and grid
lane_specs=[("营销用户",BLUE,BLUE_BG,user_icon),("Canva AI",ORANGE,ORANGE_BG,bot_icon),("Compliance Layer",GREEN,GREEN_BG,db_icon)]
for i,(name,color,fill,icon) in enumerate(lane_specs):
    yt=lane_top+i*lane_h; yb=yt+lane_h
    d.rectangle((x0,yt,x1,yb),fill=fill); d.rectangle((x0,yt,x0+label_w,yb),fill="#FFFFFF",outline=GRID,width=2)
    icon(x0+35,yt+145,color)
    label_lines=name.split(" ") if name=="Compliance Layer" else [name]
    yy=yt+150
    for line in label_lines:
        d.text((x0+95,yy),line,font=FL,fill=color); yy+=42
    d.line((x0,yt,x1,yt),fill=GRID,width=2)
    for c in range(6):
        xx=x0+label_w+c*col_w; d.line((xx,yt,xx,yb),fill=GRID,width=2)
d.line((x0,lane_top+lane_h*3,x1,lane_top+lane_h*3),fill=GRID,width=2)

centers=[x0+label_w+i*col_w+col_w//2 for i in range(5)]
ys=[lane_top+lane_h//2,lane_top+lane_h+lane_h//2,lane_top+lane_h*2+lane_h//2]
bw,bh=410,205

# Row 1 user
u1=action_box(centers[0],ys[0],bw,bh,"打开 Canva AI","进入对话页\n确认产品与投放信息",BLUE)
u2=action_box(centers[1],ys[0],bw,bh,"描述海报需求","输入生成要求\n查看并确认生成海报",BLUE)
u3=action_box(centers[2],ys[0],bw,bh,"查看审核结果","审核提示自动出现\n确认状态与原因",BLUE)
u4=action_box(centers[3],ys[0],bw,bh,"处理审核结果","继续 / 修改 / 补信息\n或查看覆盖范围",BLUE)
u5=action_box(centers[4],ys[0],bw,bh,"完成任务","“可以发布”时下载、发布\n其他状态继续处理",BLUE)

# Row 2 Canva AI
a1=action_box(centers[0],ys[1],bw,bh,"进入对话界面","展示生成入口\n收集基础 Context",ORANGE,"#FFFDFC")
a2=action_box(centers[1],ys[1],bw,bh,"理解并生成海报","生成背景图与文字图层\n组合为可用营销海报",ORANGE,"#FFFDFC")
a3=action_box(centers[2],ys[1],bw,bh,"反馈状态与提示","在生成结果下沿展示\n四态结果与下一步",ORANGE,"#FFFDFC")
a4=action_box(centers[3],ys[1],bw,bh,"更新海报或 Context","应用改写 / 接收补充信息\n保持用户可继续编辑",ORANGE,"#FFFDFC")
a5=action_box(centers[4],ys[1],bw,bh,"结束本次交互","允许发布或阻止推进\n不阻断继续对话",ORANGE,"#FFFDFC")

# Row 3 Compliance
c1=action_box(centers[0],ys[2],bw,bh,"校验审核 Context","国家 / 行业 / 产品监管\n渠道 / 内容格式",GREEN,"#FCFFFD")
c2=action_box(centers[1],ys[2],bw,bh,"接收海报完成事件","海报生成完成后触发\n不审核用户 Prompt",GREEN,"#FCFFFD")
c3=action_box(centers[2],ys[2],bw,bh,"读取海报文字","文字图层优先 · OCR 兜底\n匹配适用知识包",GREEN,"#FCFFFD")
c4=action_box(centers[3],ys[2],bw,bh,"返回四态结果","可以发布 / 发布前需修改\n需要补充 / 不在范围",GREEN,"#FCFFFD")
c5=action_box(centers[4],ys[2],bw,bh,"发布前校验","结果、内容与规则版本有效\n内容变化后自动重检",GREEN,"#FCFFFD")

# Flow arrows
arrow([((u1[0]+u1[2])//2,u1[3]),((a1[0]+a1[2])//2,a1[1])])
arrow([(a1[2],ys[1]),(a2[0],ys[1])])
arrow([((a2[0]+a2[2])//2,a2[1]),((u2[0]+u2[2])//2,u2[3])])
# Context read in parallel
arrow([((a1[0]+a1[2])//2,a1[3]),((c1[0]+c1[2])//2,c1[1])],color=GREEN,dashed=True)
arrow([(c1[2],ys[2]),(c2[0],ys[2])],color=GREEN,dashed=True)
# Poster review to compliance via side of column 2
route_x=x0+label_w+2*col_w-35
arrow([((u2[0]+u2[2])//2,u2[3]),(route_x,u2[3]),(route_x,c2[1]-35),((c2[0]+c2[2])//2,c2[1]-35),((c2[0]+c2[2])//2,c2[1])])
arrow([(c2[2],ys[2]),(c3[0],ys[2])])
arrow([((c3[0]+c3[2])//2,c3[1]),((a3[0]+a3[2])//2,a3[3])])
arrow([((a3[0]+a3[2])//2,a3[1]),((u3[0]+u3[2])//2,u3[3])])
arrow([(u3[2],ys[0]),(u4[0],ys[0])])
arrow([((u4[0]+u4[2])//2,u4[3]),((a4[0]+a4[2])//2,a4[1])])
arrow([((a4[0]+a4[2])//2,a4[3]),((c4[0]+c4[2])//2,c4[1])])
arrow([(c4[2],ys[2]),(c5[0],ys[2])])
arrow([((c5[0]+c5[2])//2,c5[1]),((a5[0]+a5[2])//2,a5[3])])
arrow([((a5[0]+a5[2])//2,a5[1]),((u5[0]+u5[2])//2,u5[3])])

# Recheck loop from update to checking
loop_y=lane_top+lane_h*3-22
arrow([(a4[2],ys[1]),(x1-18,ys[1]),(x1-18,loop_y),(centers[2],loop_y),(centers[2],c3[3])],color=PURPLE,dashed=True)
d.text((centers[3]-100,loop_y-36),"修改后自动重检",font=FE,fill=PURPLE)

# Exception / fallback area
ey=lane_top+lane_h*3+80
d.line((1080,ey+5,1340,ey+5),fill="#1F2430",width=3); d.line((1660,ey+5,1920,ey+5),fill="#1F2430",width=3)
title="异常与兜底（安全流程）"; bb=d.textbbox((0,0),title,font=FL); d.text(((W-(bb[2]-bb[0]))/2,ey-20),title,font=FL,fill=INK)
d.rounded_rectangle((70,ey+55,2930,2110),radius=20,fill="#FBFCFE",outline="#91A9C9",width=2)
exceptions=[
    ("1","图片生成失败"),("2","无可识别文字\n或 OCR 低置信"),("3","必要 Context\n缺失"),("4","知识包缺失\n或已过期"),
    ("5","当前组合\n不在覆盖范围"),("6","缺少强制声明\n或明确问题"),("7","模型 / 规则服务\n执行失败"),("8","内容发生变化\n原结果已失效")]
gap=24; ew=(2860-gap*9)//8; ex=70+gap
for num,label in exceptions:
    r=(ex,ey+100,ex+ew,ey+330); d.rounded_rectangle(r,radius=16,fill="#FFFFFF",outline="#A8BAD2",width=2)
    d.ellipse((ex+ew//2-25,ey+122,ex+ew//2+25,ey+172),fill="#0B5BC7"); nb=d.textbbox((0,0),num,font=FNUM); d.text((ex+ew//2-(nb[2]-nb[0])/2,ey+130),num,font=FNUM,fill="#FFFFFF")
    center((ex+12,ey+180,ex+ew-12,ey+310),label,FB,INK)
    ex+=ew+gap

im.save(OUT,quality=95)
print(OUT)
