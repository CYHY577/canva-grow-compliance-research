from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(r"C:\Users\pc\Desktop\canva测试")
OUT=ROOT/"output"/"Canva_Grow_合规层_产品全流程泳道图.png"
OUT.parent.mkdir(parents=True,exist_ok=True)
W,H=3200,2400
im=Image.new("RGB",(W,H),"#FFFFFF"); d=ImageDraw.Draw(im)
reg=r"C:\Windows\Fonts\msyh.ttc"; bold=r"C:\Windows\Fonts\msyhbd.ttc"
FT=ImageFont.truetype(bold,62); FS=ImageFont.truetype(reg,26); FH=ImageFont.truetype(bold,31); FL=ImageFont.truetype(bold,29); FN=ImageFont.truetype(bold,25); FB=ImageFont.truetype(reg,21); FNUM=ImageFont.truetype(bold,21); FE=ImageFont.truetype(bold,20)
INK="#20242D"; MUTED="#636B78"; BLUE="#1768CC"; BLUE_BG="#F1F6FE"; PURPLE="#7D2AE8"; PURPLE_BG="#F7F1FF"; TEAL="#078B80"; TEAL_BG="#EFFAF8"; GREEN="#178B4D"; GREEN_BG="#F1FAF4"; GRID="#D7DFE9"; BORDER="#AFC0D5"; RED="#C24132"; AMBER="#A46C00"; GRAY="#67636D"

def center(r,text,font=FN,color=INK,gap=5):
    lines=text.split("\n"); hs=[d.textbbox((0,0),t,font=font)[3] for t in lines]; y=r[1]+(r[3]-r[1]-sum(hs)-gap*(len(lines)-1))/2
    for t,h in zip(lines,hs):
        bb=d.textbbox((0,0),t,font=font); d.text((r[0]+(r[2]-r[0]-(bb[2]-bb[0]))/2,y),t,font=font,fill=color); y+=h+gap

def box(cx,cy,w,h,title,detail,stroke,fill="#FFFFFF"):
    r=(cx-w//2,cy-h//2,cx+w//2,cy+h//2); d.rounded_rectangle(r,radius=18,fill=fill,outline=stroke,width=3)
    bb=d.textbbox((0,0),title,font=FN); d.text((cx-(bb[2]-bb[0])/2,r[1]+24),title,font=FN,fill=stroke)
    yy=r[1]+76
    for line in detail.split("\n"):
        bb=d.textbbox((0,0),line,font=FB); d.text((cx-(bb[2]-bb[0])/2,yy),line,font=FB,fill=INK); yy+=31
    return r

def arrow(points,color="#161A22",width=4,dashed=False):
    if dashed:
        for i in range(len(points)-1):
            a,b=points[i],points[i+1]; dist=max(abs(b[0]-a[0]),abs(b[1]-a[1])); n=max(1,int(dist/15))
            for s in range(0,n,2):
                t1=s/n; t2=min((s+1)/n,1); d.line((a[0]+(b[0]-a[0])*t1,a[1]+(b[1]-a[1])*t1,a[0]+(b[0]-a[0])*t2,a[1]+(b[1]-a[1])*t2),fill=color,width=width)
    else: d.line(points,fill=color,width=width,joint="curve")
    a,b=points[-2],points[-1]
    if abs(b[0]-a[0])>=abs(b[1]-a[1]): tri=[(b[0],b[1]),(b[0]-16 if b[0]>a[0] else b[0]+16,b[1]-10),(b[0]-16 if b[0]>a[0] else b[0]+16,b[1]+10)]
    else: tri=[(b[0],b[1]),(b[0]-10,b[1]-16 if b[1]>a[1] else b[1]+16),(b[0]+10,b[1]-16 if b[1]>a[1] else b[1]+16)]
    d.polygon(tri,fill=color)

def icon_user(x,y,c): d.ellipse((x+10,y,x+34,y+24),fill=c); d.rounded_rectangle((x,y+29,x+44,y+66),radius=14,fill=c)
def icon_ai(x,y,c): d.rounded_rectangle((x,y+8,x+48,y+56),radius=10,outline=c,width=5); d.line((x+24,y,x+24,y+8),fill=c,width=4); d.ellipse((x+19,y-5,x+29,y+5),fill=c); d.ellipse((x+11,y+26,x+18,y+33),fill=c); d.ellipse((x+30,y+26,x+37,y+33),fill=c)
def icon_engine(x,y,c): d.ellipse((x,y,x+46,y+15),fill=c); d.rectangle((x,y+7,x+46,y+56),fill=c); d.ellipse((x,y+47,x+46,y+63),fill=c); d.ellipse((x+5,y+9,x+41,y+19),fill="#FFFFFF")
def icon_rules(x,y,c): d.rounded_rectangle((x,y,x+48,y+62),radius=7,outline=c,width=5); d.line((x+10,y+18,x+38,y+18),fill=c,width=4); d.line((x+10,y+31,x+38,y+31),fill=c,width=4); d.line((x+10,y+44,x+31,y+44),fill=c,width=4)

d.text((70,46),"Canva Grow 合规层产品全流程（泳道图）",font=FT,fill=INK)
d.text((72,124),"覆盖 Context、海报生成、自动触发、知识路由、四态决策、自动重检与发布前 Gate",font=FS,fill=MUTED)

x0,x1=55,3145; y0=215; head_h=110; label_w=285; col_w=(x1-x0-label_w)//5; lane_h=350; lane_top=y0+head_h
d.rounded_rectangle((x0,y0,x1,lane_top+lane_h*4),radius=24,fill="#FFFFFF",outline="#155FC4",width=4)
d.rectangle((x0,y0,x0+label_w,lane_top),fill="#0D4FB5"); center((x0,y0,x0+label_w,lane_top),"阶段",FH,"#FFFFFF")
phases=["1. Context 准备","2. 生成海报","3. 自动触发","4. 判断与处理","5. 发布与沉淀"]
colors=["#0F51B9","#145FCA","#176CD9","#247AE8","#1457BE"]
for i,(t,c) in enumerate(zip(phases,colors)):
    xa=x0+label_w+i*col_w; xb=xa+col_w; pts=[(xa,y0),(xb-23,y0),(xb,lane_top-head_h//2),(xb-23,lane_top),(xa,lane_top),(xa+23,lane_top-head_h//2)] if i else [(xa,y0),(xb-23,y0),(xb,lane_top-head_h//2),(xb-23,lane_top),(xa,lane_top)]
    d.polygon(pts,fill=c); center((xa+15,y0,xb-25,lane_top),t,FH,"#FFFFFF")

lanes=[("营销创作者",BLUE,BLUE_BG,icon_user),("Canva AI",PURPLE,PURPLE_BG,icon_ai),("Compliance Engine",TEAL,TEAL_BG,icon_engine),("知识与规则服务",GREEN,GREEN_BG,icon_rules)]
for i,(name,c,fill,ic) in enumerate(lanes):
    yt=lane_top+i*lane_h; yb=yt+lane_h; d.rectangle((x0,yt,x1,yb),fill=fill); d.rectangle((x0,yt,x0+label_w,yb),fill="#FFFFFF",outline=GRID,width=2); ic(x0+32,yt+140,c)
    lines=name.split(" ") if name=="Compliance Engine" else [name]; yy=yt+146-(len(lines)-1)*20
    for line in lines: d.text((x0+98,yy),line,font=FL,fill=c); yy+=40
    for j in range(6):
        xx=x0+label_w+j*col_w; d.line((xx,yt,xx,yb),fill=GRID,width=2)
    d.line((x0,yt,x1,yt),fill=GRID,width=2)

centers=[x0+label_w+i*col_w+col_w//2 for i in range(5)]; ys=[lane_top+lane_h//2+i*lane_h for i in range(4)]; bw,bh=455,185

# User
u1=box(centers[0],ys[0],bw,bh,"确认产品信息","国家 / 行业 / 产品类型\n监管身份可选择“不确定”",BLUE)
u2=box(centers[1],ys[0],bw,bh,"输入并查看海报","输入生成需求\n确认最终画面与可见文字",BLUE)
u3=box(centers[2],ys[0],bw,bh,"查看自动检查","状态随生成结果出现\n用户无需手动发起",BLUE)
u4=box(centers[3],ys[0],bw,bh,"选择下一步","继续 / 修改 / 补充信息\n或查看覆盖范围",BLUE)
u5=box(centers[4],ys[0],bw,bh,"完成使用","有效“可以发布”时\n下载、发布或继续",BLUE)

# Canva
a1=box(centers[0],ys[1],bw,bh,"记录 Context","保存本次生成与审核所需\n六个基础字段",PURPLE,"#FFFDFF")
a2=box(centers[1],ys[1],bw,bh,"生成可用海报","背景图 + 可编辑文字层\n组合为营销内容",PURPLE,"#FFFDFF")
a3=box(centers[2],ys[1],bw,bh,"挂载合规入口","渲染完成后展示状态条\n或右侧辅助抽屉",PURPLE,"#FFFDFF")
a4=box(centers[3],ys[1],bw,bh,"展示结果并写回","显示问题、建议与覆盖\n接收编辑或补充信息",PURPLE,"#FFFDFF")
a5=box(centers[4],ys[1],bw,bh,"执行关键操作","允许或阻止下载、发布\n不阻断继续编辑",PURPLE,"#FFFDFF")

# Engine
c1=box(centers[0],ys[2],bw,bh,"校验 Context 与范围","信息不足进入需要补充\n组合不支持则不在范围",TEAL,"#FCFFFE")
c2=box(centers[1],ys[2],bw,bh,"建立内容版本","等待可用海报形成\n记录 Content Hash",TEAL,"#FCFFFE")
c3=box(centers[2],ys[2],bw,bh,"提取海报文字","文字图层优先\n扁平图片使用 OCR",TEAL,"#FCFFFE")
c4=box(centers[3],ys[2],bw,bh,"合规判断与建议","规则处理强制义务\n模型定位、解释与改写",TEAL,"#FCFFFE")
c5=box(centers[4],ys[2],bw,bh,"Pre-use Gate","检查结果、内容与规则版本\n有效后才允许继续",TEAL,"#FCFFFE")

# Knowledge
k1=box(centers[0],ys[3],bw,bh,"匹配知识包","Country × Industry × Product\nRegulation × Format",GREEN,"#FCFFFD")
k2=box(centers[1],ys[3],bw,bh,"返回发布版本","规则版本、有效期\n覆盖范围与回滚点",GREEN,"#FCFFFD")
k3=box(centers[2],ys[3],bw,bh,"提供受控规则","强制声明 / 证据依赖\n监管边界与例外",GREEN,"#FCFFFD")
k4=box(centers[3],ys[3],bw,bh,"返回可追溯依据","可能适用的规则\n来源、版本与 trace_id",GREEN,"#FCFFFD")
k5=box(centers[4],ys[3],bw,bh,"版本监控与回滚","规则过期立即失效\n触发重检或停止使用",GREEN,"#FCFFFD")

# Main cross-lane flow
arrow([((u1[0]+u1[2])//2,u1[3]),((a1[0]+a1[2])//2,a1[1])]); arrow([((a1[0]+a1[2])//2,a1[3]),((c1[0]+c1[2])//2,c1[1])]); arrow([((c1[0]+c1[2])//2,c1[3]),((k1[0]+k1[2])//2,k1[1])])
arrow([(a1[2],ys[1]),(a2[0],ys[1])]); arrow([(k1[2],ys[3]),(k2[0],ys[3])],color=GREEN); arrow([(c1[2],ys[2]),(c2[0],ys[2])],color=TEAL)
arrow([((a2[0]+a2[2])//2,a2[1]),((u2[0]+u2[2])//2,u2[3])]); arrow([(u2[2],ys[0]),(u3[0],ys[0])]); arrow([(a2[2],ys[1]),(a3[0],ys[1])])
arrow([((a3[0]+a3[2])//2,a3[3]),((c3[0]+c3[2])//2,c3[1])]); arrow([(c2[2],ys[2]),(c3[0],ys[2])]); arrow([((c3[0]+c3[2])//2,c3[3]),((k3[0]+k3[2])//2,k3[1])])
arrow([(k2[2],ys[3]),(k3[0],ys[3])],color=GREEN); arrow([(k3[2],ys[3]),(k4[0],ys[3])],color=GREEN); arrow([((k4[0]+k4[2])//2,k4[1]),((c4[0]+c4[2])//2,c4[3])],color=GREEN)
arrow([((c4[0]+c4[2])//2,c4[1]),((a4[0]+a4[2])//2,a4[3])]); arrow([((a4[0]+a4[2])//2,a4[1]),((u4[0]+u4[2])//2,u4[3])]); arrow([(u3[2],ys[0]),(u4[0],ys[0])])
arrow([(c4[2],ys[2]),(c5[0],ys[2])]); arrow([(k4[2],ys[3]),(k5[0],ys[3])],color=GREEN); arrow([((k5[0]+k5[2])//2,k5[1]),((c5[0]+c5[2])//2,c5[3])],color=GREEN)
arrow([((c5[0]+c5[2])//2,c5[1]),((a5[0]+a5[2])//2,a5[3])]); arrow([((a5[0]+a5[2])//2,a5[1]),((u5[0]+u5[2])//2,u5[3])])

# Recheck loop from updates back to extraction
loop_y=lane_top+lane_h*4-18
arrow([(a4[2],ys[1]),(x1-16,ys[1]),(x1-16,loop_y),(centers[2],loop_y),(centers[2],c3[3])],color=PURPLE,dashed=True)
d.text((centers[3]-85,loop_y-33),"内容 / Context 变化后自动重检",font=FE,fill=PURPLE)

# Status strip
sy=lane_top+lane_h*4+45
chips=[("可以发布","#EAF8F2",GREEN),("发布前需修改","#FFF0ED",RED),("需要补充信息","#FFF4D6",AMBER),("不在覆盖范围","#F0EFF2",GRAY)]
cw=520; start=(W-(cw*4+30*3))//2
for i,(t,fill,stroke) in enumerate(chips):
    r=(start+i*(cw+30),sy,start+i*(cw+30)+cw,sy+70); d.rounded_rectangle(r,radius=18,fill=fill,outline=stroke,width=3); center(r,t,FN,stroke)

# Exception section
ey=sy+135; title="异常与兜底（安全流程）"; bb=d.textbbox((0,0),title,font=FL); d.line((950,ey+10,1270,ey+10),fill=INK,width=3); d.text(((W-(bb[2]-bb[0]))/2,ey-18),title,font=FL,fill=INK); d.line((1930,ey+10,2250,ey+10),fill=INK,width=3)
d.rounded_rectangle((55,ey+62,3145,2325),radius=20,fill="#FBFCFE",outline="#9EB2CC",width=2)
items=[("1","Context 缺失"),("2","当前组合\n不在范围"),("3","OCR 低置信\n或无可识别文字"),("4","知识包缺失\n或过期"),("5","缺少强制声明\n或明确问题"),("6","Supporting evidence\n缺失或不匹配"),("7","模型 / 规则服务\n执行失败"),("8","内容或版本变化\n原结果失效")]
gap=22; ew=(3090-gap*9)//8; xx=55+gap
for num,label in items:
    r=(xx,ey+100,xx+ew,ey+285); d.rounded_rectangle(r,radius=15,fill="#FFFFFF",outline="#A9BBD2",width=2); d.ellipse((xx+ew//2-23,ey+117,xx+ew//2+23,ey+163),fill="#0C5DC8"); nb=d.textbbox((0,0),num,font=FNUM); d.text((xx+ew//2-(nb[2]-nb[0])/2,ey+123),num,font=FNUM,fill="#FFFFFF"); center((xx+10,ey+170,xx+ew-10,ey+275),label,FB,INK); xx+=ew+gap

im.save(OUT,quality=95)
print(OUT)
