from pathlib import Path
from math import pi, cos, sin

from PIL import Image, ImageDraw, ImageFont
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor


ROOT = Path(r"C:\Users\pc\Desktop\canva测试")
ASSETS = ROOT / "assets"
SHOTS = ASSETS / "screenshots"
DIAGRAMS = ASSETS / "diagrams"
OUTPUT = ROOT / "output"
DIAGRAMS.mkdir(parents=True, exist_ok=True)
OUTPUT.mkdir(parents=True, exist_ok=True)

FONT_REG = r"C:\Windows\Fonts\msyh.ttc"
FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"

PURPLE = "7D2AE8"
PURPLE_DARK = "5B21B6"
PURPLE_LIGHT = "F3E8FF"
TEAL = "00A9B5"
TEAL_LIGHT = "E7FAFA"
INK = "18191F"
MUTED = "667085"
LINE = "D9DCE3"
BG = "F7F7FA"
GREEN = "167A55"
GREEN_LIGHT = "EAF7F0"
ORANGE = "D94B2B"
ORANGE_LIGHT = "FFF0EB"
GOLD = "9A6700"
GOLD_LIGHT = "FFF7D6"
WHITE = "FFFFFF"

PAGE_WIDTH_DXA = 11905  # A4
MARGIN_DXA = 912
CONTENT_DXA = 10080  # 7.0 inches, named A4 visual override


def rgb(hexstr):
    return RGBColor.from_string(hexstr)


def pil_font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def wrap_text(draw, text, font, max_width):
    lines = []
    for para in str(text).split("\n"):
        if not para:
            lines.append("")
            continue
        buf = ""
        for ch in para:
            trial = buf + ch
            if draw.textbbox((0, 0), trial, font=font)[2] <= max_width or not buf:
                buf = trial
            else:
                lines.append(buf)
                buf = ch
        if buf:
            lines.append(buf)
    return lines


def draw_centered(draw, box, text, font, fill=INK, spacing=8):
    x1, y1, x2, y2 = box
    lines = wrap_text(draw, text, font, x2 - x1 - 28)
    heights = [draw.textbbox((0, 0), line or " ", font=font)[3] for line in lines]
    total = sum(heights) + spacing * (len(lines) - 1)
    y = y1 + (y2 - y1 - total) / 2
    for line, h in zip(lines, heights):
        w = draw.textbbox((0, 0), line, font=font)[2]
        draw.text((x1 + (x2 - x1 - w) / 2, y), line, font=font, fill="#" + fill)
        y += h + spacing


def arrow(draw, p1, p2, fill=PURPLE, width=6):
    draw.line([p1, p2], fill="#" + fill, width=width)
    angle = __import__("math").atan2(p2[1] - p1[1], p2[0] - p1[0])
    head = 16
    pts = [
        p2,
        (p2[0] - head * cos(angle - pi / 6), p2[1] - head * sin(angle - pi / 6)),
        (p2[0] - head * cos(angle + pi / 6), p2[1] - head * sin(angle + pi / 6)),
    ]
    draw.polygon(pts, fill="#" + fill)


def save_value_chain():
    img = Image.new("RGB", (1800, 500), "white")
    d = ImageDraw.Draw(img)
    title = pil_font(42, True)
    d.text((55, 30), "Canva 价值链：把合规从发布门槛变成创作能力", font=title, fill="#" + INK)
    boxes = [
        ("更快发布", "创作中即时校验\n减少末端返工", TEAL_LIGHT, TEAL),
        ("行业增长", "支持高监管行业\n扩大可服务场景", PURPLE_LIGHT, PURPLE),
        ("可信 AI", "可解释、可追溯\n明确覆盖边界", GREEN_LIGHT, GREEN),
        ("知识飞轮", "争议与评测回流\n形成规则资产", GOLD_LIGHT, GOLD),
    ]
    x0, y, w, h, gap = 55, 150, 370, 260, 70
    for i, (label, body, bg, accent) in enumerate(boxes):
        x = x0 + i * (w + gap)
        d.rounded_rectangle((x, y, x + w, y + h), radius=30, fill="#" + bg, outline="#" + accent, width=4)
        d.rounded_rectangle((x + 22, y + 22, x + 92, y + 92), radius=20, fill="#" + accent)
        d.text((x + 47, y + 32), str(i + 1), font=pil_font(34, True), fill="white", anchor="ma")
        d.text((x + 115, y + 26), label, font=pil_font(32, True), fill="#" + INK)
        draw_centered(d, (x + 22, y + 100, x + w - 22, y + h - 18), body, pil_font(28), MUTED, 10)
        if i < 3:
            arrow(d, (x + w + 12, y + h // 2), (x + w + gap - 12, y + h // 2), PURPLE, 5)
    img.save(DIAGRAMS / "value_chain.png")


def save_priority_matrix():
    img = Image.new("RGB", (1500, 820), "white")
    d = ImageDraw.Draw(img)
    d.text((60, 35), "需求优先级：业务价值 × 风险/依赖成本", font=pil_font(40, True), fill="#" + INK)
    left, top, right, bottom = 160, 130, 1410, 730
    d.rectangle((left, top, right, bottom), outline="#" + LINE, width=4)
    midx, midy = (left + right) // 2, (top + bottom) // 2
    d.line((midx, top, midx, bottom), fill="#" + LINE, width=3)
    d.line((left, midy, right, midy), fill="#" + LINE, width=3)
    d.text((left, bottom + 18), "低依赖", font=pil_font(24), fill="#" + MUTED)
    d.text((right - 90, bottom + 18), "高依赖", font=pil_font(24), fill="#" + MUTED)
    d.text((35, bottom - 30), "低价值", font=pil_font(24), fill="#" + MUTED)
    d.text((35, top), "高价值", font=pil_font(24), fill="#" + MUTED)
    d.text((left + 20, top + 15), "P0：先上线", font=pil_font(27, True), fill="#" + GREEN)
    d.text((midx + 20, top + 15), "P1：验证后扩展", font=pil_font(27, True), fill="#" + PURPLE)
    d.text((left + 20, midy + 15), "控制投入", font=pil_font(27, True), fill="#" + MUTED)
    d.text((midx + 20, midy + 15), "P2：长期探索", font=pil_font(27, True), fill="#" + GOLD)
    points = [
        (390, 270, "文本规则校验", GREEN),
        (500, 360, "覆盖范围披露", GREEN),
        (690, 240, "一键修复", PURPLE),
        (980, 260, "图片/落地页", PURPLE),
        (1160, 355, "多市场包", PURPLE),
        (1040, 565, "视频/音频", GOLD),
        (650, 600, "自动法规摄取", GOLD),
    ]
    for x, y, label, color in points:
        r = 15
        d.ellipse((x-r, y-r, x+r, y+r), fill="#" + color)
        d.text((x + 22, y - 18), label, font=pil_font(24, True), fill="#" + INK)
    img.save(DIAGRAMS / "priority_matrix.png")


def save_user_flow():
    img = Image.new("RGB", (1800, 1640), "white")
    d = ImageDraw.Draw(img)
    d.text((55, 28), "Canva Grow 用户侧合规决策流程", font=pil_font(43, True), fill="#" + INK)
    def box(x, y, w, h, text, bg=BG, border=PURPLE, fs=27, bold=False):
        d.rounded_rectangle((x, y, x+w, y+h), radius=22, fill="#"+bg, outline="#"+border, width=4)
        draw_centered(d, (x, y, x+w, y+h), text, pil_font(fs, bold), INK, 7)
    def diamond(cx, cy, w, h, text):
        pts=[(cx,cy-h//2),(cx+w//2,cy),(cx,cy+h//2),(cx-w//2,cy)]
        d.polygon(pts, fill="#"+PURPLE_LIGHT, outline="#"+PURPLE)
        draw_centered(d,(cx-w//2+35,cy-h//2+20,cx+w//2-35,cy+h//2-20),text,pil_font(25,True),INK,5)
    # Main path runs vertically; exception states branch right and never imply success.
    box(210, 120, 610, 105, "用户生成/编辑营销文案", TEAL_LIGHT, TEAL, 29, True)
    box(210, 275, 610, 115, "读取活动上下文\n市场 · 行业 · 产品 · 格式", PURPLE_LIGHT, PURPLE, 27, True)
    arrow(d,(515,225),(515,275),PURPLE)
    diamond(515, 505, 520, 160, "上下文完整？")
    arrow(d,(515,390),(515,425),PURPLE)
    box(1080, 445, 610, 120, "Need your input\n补充产品分类/市场/素材类型", GOLD_LIGHT, GOLD, 25, True)
    arrow(d,(775,505),(1080,505),GOLD)
    d.text((890,465),"否",font=pil_font(24,True),fill="#"+GOLD)
    box(210, 625, 610, 120, "路由到已发布知识包\n规则版本 + 来源 + 生效期", BG, PURPLE, 26, True)
    arrow(d,(515,585),(515,625),PURPLE)
    d.text((535,592),"是",font=pil_font(24,True),fill="#"+GREEN)
    diamond(515, 855, 520, 160, "精确范围受支持？")
    arrow(d,(515,745),(515,775),PURPLE)
    box(1080, 795, 610, 120, "Outside scope\n不得输出 Ready；说明未检查项", ORANGE_LIGHT, ORANGE, 25, True)
    arrow(d,(775,855),(1080,855),ORANGE)
    d.text((890,815),"否",font=pil_font(24,True),fill="#"+ORANGE)
    box(210, 970, 610, 120, "混合决策执行\n确定性规则 + 模型分类 + 证据", TEAL_LIGHT, TEAL, 26, True)
    arrow(d,(515,935),(515,970),PURPLE)
    d.text((535,940),"是",font=pil_font(24,True),fill="#"+GREEN)
    diamond(900, 1190, 430, 150, "结果类型")
    arrow(d,(515,1090),(770,1148),PURPLE)
    box(50, 1315, 500, 120, "Ready to run\n无明确问题 + 覆盖范围披露", GREEN_LIGHT, GREEN, 24, True)
    box(650, 1315, 500, 120, "Fix before running\n定位问题 + 一键修复 + 重检", ORANGE_LIGHT, ORANGE, 24, True)
    box(1250, 1315, 500, 120, "Need your input\n证据/分类不足，禁止猜测", GOLD_LIGHT, GOLD, 24, True)
    arrow(d,(770,1250),(300,1315),GREEN)
    arrow(d,(900,1265),(900,1315),ORANGE)
    arrow(d,(1030,1250),(1500,1315),GOLD)
    box(50, 1460, 500, 75, "仅有效 Ready 允许继续发布", PURPLE_LIGHT, PURPLE, 25, True)
    arrow(d,(300,1435),(300,1460),GREEN)
    # Fix loops to editing; missing context loops to context collection.
    d.line((900,1435,900,1590,25,1590,25,170,210,170),fill="#"+ORANGE,width=5)
    arrow(d,(25,170),(210,170),ORANGE,5)
    d.text((575,1545),"修复后回到编辑并重检",font=pil_font(22,True),fill="#"+ORANGE)
    d.line((1500,1435,1760,1435,1760,330,820,330),fill="#"+GOLD,width=5)
    arrow(d,(1760,330),(820,330),GOLD,5)
    img.save(DIAGRAMS / "user_flow.png")


def save_lifecycle():
    img = Image.new("RGB", (1800, 520), "white")
    d = ImageDraw.Draw(img)
    d.text((50, 25), "合规知识生命周期：每次决策都可回流改进", font=pil_font(42, True), fill="#" + INK)
    labels = ["官方来源", "结构化规则", "双人审核", "离线评测", "版本发布", "在线决策", "争议回流", "更新迭代"]
    colors = [TEAL, PURPLE, GREEN, PURPLE, TEAL, GREEN, ORANGE, GOLD]
    x0, y, w, h, gap = 35, 155, 180, 145, 38
    for i, (label, color) in enumerate(zip(labels, colors)):
        x = x0 + i * (w + gap)
        d.rounded_rectangle((x, y, x+w, y+h), radius=24, fill="#"+BG, outline="#"+color, width=4)
        d.ellipse((x+62,y+20,x+118,y+76), fill="#"+color)
        d.text((x+90,y+27),str(i+1),font=pil_font(27,True),fill="white",anchor="ma")
        draw_centered(d,(x+10,y+78,x+w-10,y+h-8),label,pil_font(24,True),INK,4)
        if i < len(labels)-1:
            arrow(d,(x+w+5,y+h//2),(x+w+gap-5,y+h//2),PURPLE,4)
    d.rounded_rectangle((390, 365, 1410, 455), radius=24, fill="#"+PURPLE_LIGHT, outline="#"+PURPLE, width=3)
    draw_centered(d,(410,375,1390,445),"发布门禁：来源可追溯 · 审核完成 · 基准集通过 · 回滚可用",pil_font(27,True),PURPLE_DARK,6)
    img.save(DIAGRAMS / "knowledge_lifecycle.png")


def save_architecture():
    img = Image.new("RGB", (1800, 980), "white")
    d = ImageDraw.Draw(img)
    d.text((55, 30), "系统架构与数据闭环", font=pil_font(43, True), fill="#" + INK)
    def box(x,y,w,h,title,body,bg,border):
        d.rounded_rectangle((x,y,x+w,y+h),radius=24,fill="#"+bg,outline="#"+border,width=4)
        d.text((x+24,y+20),title,font=pil_font(28,True),fill="#"+INK)
        for j,line in enumerate(wrap_text(d,body,pil_font(22),w-48)[:4]):
            d.text((x+24,y+66+j*34),line,font=pil_font(22),fill="#"+MUTED)
    box(60,150,390,180,"Canva 创作面","文案、素材、活动上下文\n编辑后自动重检",TEAL_LIGHT,TEAL)
    box(550,150,420,180,"合规编排层","上下文校验 · 范围路由\n超时、降级与版本锁定",PURPLE_LIGHT,PURPLE)
    box(1070,120,660,240,"决策服务","确定性规则引擎\n模型分类/提取\n证据与解释生成",BG,PURPLE)
    arrow(d,(450,240),(550,240),PURPLE)
    arrow(d,(970,240),(1070,240),PURPLE)
    box(90,500,430,200,"知识包存储","法规来源 · 结构化规则\n市场/行业/产品/格式\n版本与生效时间",BG,TEAL)
    box(685,500,430,200,"治理控制台","覆盖矩阵 · 审核\n争议队列 · 变更记录\n角色与权限",BG,PURPLE)
    box(1280,500,430,200,"评测与观测","基准集 · 回归评测\n决策日志 · 告警\n发布门禁与回滚",BG,GREEN)
    arrow(d,(1280,600),(1115,600),GREEN)
    arrow(d,(685,600),(520,600),PURPLE)
    arrow(d,(305,500),(1270,345),TEAL)
    arrow(d,(900,500),(1390,360),PURPLE)
    arrow(d,(1495,500),(1495,360),GREEN)
    d.rounded_rectangle((300,790,1500,895),radius=28,fill="#"+GOLD_LIGHT,outline="#"+GOLD,width=4)
    draw_centered(d,(325,805,1475,880),"统一决策契约：status · issues · evidence · coverage · knowledge_version · trace_id",pil_font(26,True),INK,6)
    img.save(DIAGRAMS / "architecture.png")


def save_eval_chart():
    img = Image.new("RGB", (1500, 570), "white")
    d = ImageDraw.Draw(img)
    d.text((50, 30), "演示基准集构成（60 cases）", font=pil_font(40, True), fill="#" + INK)
    data = [("Hard negative",24,PURPLE,"不应触发修复"),("True fix",18,ORANGE,"明确问题且上下文充分"),("Needs input",18,GOLD,"缺少上下文，需追问")]
    maxv=24
    y=145
    for label,val,color,note in data:
        d.text((70,y),label,font=pil_font(27,True),fill="#"+INK)
        d.rounded_rectangle((350,y,1250,y+58),radius=22,fill="#"+BG)
        width=int(900*val/maxv)
        d.rounded_rectangle((350,y,350+width,y+58),radius=22,fill="#"+color)
        d.text((1275,y+5),str(val),font=pil_font(32,True),fill="#"+color)
        d.text((350,y+72),note,font=pil_font(22),fill="#"+MUTED)
        y+=135
    img.save(DIAGRAMS / "eval_dataset.png")


def save_rollout():
    img = Image.new("RGB", (1700, 520), "white")
    d = ImageDraw.Draw(img)
    d.text((55, 30), "分阶段上线与门禁", font=pil_font(42, True), fill="#" + INK)
    stages=[
        ("0. 影子模式","2 周","只记录不拦截\n建立基线",TEAL),
        ("1. 内部试点","2-4 周","Canva 内部/白名单\n人工复核",PURPLE),
        ("2. 受控发布","4 周","AU Beauty Text\n强制覆盖披露",GREEN),
        ("3. 扩展覆盖","按包推进","图片/平台政策/新市场\n独立评测",GOLD),
    ]
    x0,y,w,h,gap=40,150,360,250,55
    for i,(name,dur,body,color) in enumerate(stages):
        x=x0+i*(w+gap)
        d.rounded_rectangle((x,y,x+w,y+h),radius=28,fill="#"+BG,outline="#"+color,width=4)
        d.text((x+24,y+22),name,font=pil_font(27,True),fill="#"+INK)
        d.rounded_rectangle((x+24,y+70,x+150,y+112),radius=18,fill="#"+color)
        d.text((x+87,y+77),dur,font=pil_font(20,True),fill="white",anchor="ma")
        draw_centered(d,(x+24,y+128,x+w-24,y+h-20),body,pil_font(23),MUTED,7)
        if i<3:
            arrow(d,(x+w+6,y+h//2),(x+w+gap-6,y+h//2),PURPLE,4)
    img.save(DIAGRAMS / "rollout.png")


def crop_screenshots():
    for src_name, out_name in [("demo_result.png","demo_issue_crop.png"),("demo_pass.png","demo_pass_crop.png")]:
        src = Image.open(SHOTS/src_name).convert("RGB")
        w,h=src.size
        # Focus on the decision panel so the two states stay readable in a side-by-side page.
        crop=src.crop((int(w*0.70),int(h*0.11),w,int(h*0.91)))
        crop.save(SHOTS/out_name,quality=95)


def set_cell_shading(cell, fill):
    tcPr=cell._tc.get_or_add_tcPr()
    shd=tcPr.find(qn("w:shd"))
    if shd is None:
        shd=OxmlElement("w:shd")
        tcPr.append(shd)
    shd.set(qn("w:fill"),fill)


def set_cell_margins(cell, top=90, start=110, bottom=90, end=110):
    tc=cell._tc
    tcPr=tc.get_or_add_tcPr()
    tcMar=tcPr.first_child_found_in("w:tcMar")
    if tcMar is None:
        tcMar=OxmlElement("w:tcMar")
        tcPr.append(tcMar)
    for m,v in (("top",top),("start",start),("bottom",bottom),("end",end)):
        node=tcMar.find(qn("w:"+m))
        if node is None:
            node=OxmlElement("w:"+m)
            tcMar.append(node)
        node.set(qn("w:w"),str(v)); node.set(qn("w:type"),"dxa")


def set_table_geometry(table, widths, indent=110):
    assert sum(widths)==CONTENT_DXA, (widths,sum(widths))
    table.alignment=WD_TABLE_ALIGNMENT.LEFT
    table.autofit=False
    tblPr=table._tbl.tblPr
    tblW=tblPr.first_child_found_in("w:tblW")
    if tblW is None:
        tblW=OxmlElement("w:tblW"); tblPr.append(tblW)
    tblW.set(qn("w:w"),str(CONTENT_DXA)); tblW.set(qn("w:type"),"dxa")
    tblInd=tblPr.first_child_found_in("w:tblInd")
    if tblInd is None:
        tblInd=OxmlElement("w:tblInd"); tblPr.append(tblInd)
    tblInd.set(qn("w:w"),str(indent)); tblInd.set(qn("w:type"),"dxa")
    layout=tblPr.first_child_found_in("w:tblLayout")
    if layout is None:
        layout=OxmlElement("w:tblLayout"); tblPr.append(layout)
    layout.set(qn("w:type"),"fixed")
    grid=table._tbl.tblGrid
    for c in list(grid): grid.remove(c)
    for width in widths:
        gc=OxmlElement("w:gridCol"); gc.set(qn("w:w"),str(width)); grid.append(gc)
    for row in table.rows:
        for i,cell in enumerate(row.cells):
            tcPr=cell._tc.get_or_add_tcPr()
            tcW=tcPr.first_child_found_in("w:tcW")
            if tcW is None:
                tcW=OxmlElement("w:tcW"); tcPr.append(tcW)
            tcW.set(qn("w:w"),str(widths[i])); tcW.set(qn("w:type"),"dxa")
            set_cell_margins(cell)


def set_repeat_header(row):
    trPr=row._tr.get_or_add_trPr()
    elem=OxmlElement("w:tblHeader"); elem.set(qn("w:val"),"true"); trPr.append(elem)


def set_run_font(run, size=None, bold=None, color=INK, italic=False, name="Microsoft YaHei"):
    run.font.name=name
    rPr=run._element.get_or_add_rPr()
    rFonts=rPr.rFonts
    if rFonts is None:
        rFonts=OxmlElement("w:rFonts"); rPr.append(rFonts)
    for attr in ("ascii","hAnsi","eastAsia","cs"):
        rFonts.set(qn("w:"+attr),name)
    if size is not None: run.font.size=Pt(size)
    if bold is not None: run.bold=bold
    run.italic=italic
    run.font.color.rgb=rgb(color)


def format_para(p, before=0, after=4, line=1.12, keep_next=False):
    pf=p.paragraph_format
    pf.space_before=Pt(before); pf.space_after=Pt(after); pf.line_spacing=line
    pf.keep_with_next=keep_next


def add_text(doc, text, size=10, color=INK, bold=False, italic=False, after=4, before=0, align=None, style=None):
    p=doc.add_paragraph(style=style)
    if align is not None: p.alignment=align
    r=p.add_run(text); set_run_font(r,size,bold,color,italic)
    format_para(p,before,after,1.14)
    return p


def add_kicker(doc, text):
    p=doc.add_paragraph()
    r=p.add_run(text.upper()); set_run_font(r,8.2,True,PURPLE)
    format_para(p,0,3,1.0,True)
    return p


def add_heading(doc, text, level=1):
    p=doc.add_paragraph(style=f"Heading {level}")
    r=p.add_run(text)
    sizes={1:16,2:12.5,3:10.5}
    colors={1:INK,2:PURPLE_DARK,3:INK}
    set_run_font(r,sizes[level],True,colors[level])
    format_para(p,{1:6,2:5,3:3}[level],{1:6,2:4,3:3}[level],1.0,True)
    return p


def add_page_break(doc):
    doc.add_page_break()


def add_picture(doc, path, width_in, caption=None):
    p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before=Pt(2); p.paragraph_format.space_after=Pt(3)
    r=p.add_run(); shape=r.add_picture(str(path),width=Inches(width_in))
    alt = caption or Path(path).stem.replace("_", " ")
    shape._inline.docPr.set("descr", alt)
    shape._inline.docPr.set("title", alt[:120])
    if caption:
        cp=doc.add_paragraph(); cp.alignment=WD_ALIGN_PARAGRAPH.CENTER
        rr=cp.add_run(caption); set_run_font(rr,8,False,MUTED)
        format_para(cp,0,5,1.0)
    return p


def style_table(table, header=True, font_size=8.8, header_fill=PURPLE_DARK, zebra=True):
    for ri,row in enumerate(table.rows):
        if ri==0 and header: set_repeat_header(row)
        for ci,cell in enumerate(row.cells):
            cell.vertical_alignment=WD_ALIGN_VERTICAL.CENTER
            if ri==0 and header: set_cell_shading(cell,header_fill)
            elif zebra and ri%2==0: set_cell_shading(cell,BG)
            for p in cell.paragraphs:
                format_para(p,0,0,1.08)
                for run in p.runs:
                    set_run_font(run,font_size,ri==0,WHITE if ri==0 and header else INK)


def add_table(doc, headers, rows, widths, font_size=8.6, header_fill=PURPLE_DARK, zebra=True):
    table=doc.add_table(rows=1,cols=len(headers))
    table.style="Table Grid"
    for i,h in enumerate(headers): table.rows[0].cells[i].text=str(h)
    for row in rows:
        cells=table.add_row().cells
        for i,v in enumerate(row): cells[i].text=str(v)
    set_table_geometry(table,widths)
    style_table(table,True,font_size,header_fill,zebra)
    p=doc.add_paragraph(); format_para(p,0,2,1.0)
    return table


def add_callout(doc,label,text,fill=PURPLE_LIGHT,accent=PURPLE):
    p=doc.add_paragraph()
    pPr=p._p.get_or_add_pPr()
    shd=OxmlElement("w:shd"); shd.set(qn("w:fill"),fill); pPr.append(shd)
    pBdr=OxmlElement("w:pBdr")
    left=OxmlElement("w:left")
    left.set(qn("w:val"),"single"); left.set(qn("w:sz"),"18")
    left.set(qn("w:space"),"8"); left.set(qn("w:color"),accent)
    pBdr.append(left); pPr.append(pBdr)
    ind=OxmlElement("w:ind"); ind.set(qn("w:left"),"180"); ind.set(qn("w:right"),"140"); pPr.append(ind)
    r=p.add_run(label+"  "); set_run_font(r,9.5,True,accent)
    r=p.add_run(text); set_run_font(r,9.5,False,INK)
    format_para(p,4,6,1.15)
    return p


def add_metric_cards(doc,cards):
    t=doc.add_table(rows=1,cols=len(cards)); t.style="Table Grid"
    widths=[CONTENT_DXA//len(cards)]*len(cards); widths[-1]+=CONTENT_DXA-sum(widths)
    set_table_geometry(t,widths)
    set_repeat_header(t.rows[0])
    fills=[PURPLE_LIGHT,TEAL_LIGHT,GREEN_LIGHT,GOLD_LIGHT]
    accents=[PURPLE,TEAL,GREEN,GOLD]
    for i,(value,label,note) in enumerate(cards):
        c=t.cell(0,i); set_cell_shading(c,fills[i%len(fills)])
        p=c.paragraphs[0]; p.alignment=WD_ALIGN_PARAGRAPH.CENTER
        r=p.add_run(value); set_run_font(r,18,True,accents[i%len(accents)])
        p.add_run("\n")
        r=p.add_run(label); set_run_font(r,8.8,True,INK)
        p.add_run("\n")
        r=p.add_run(note); set_run_font(r,7.4,False,MUTED)
        format_para(p,0,0,1.06)
    return t


def set_cell_image(cell,path,width_in):
    p=cell.paragraphs[0]; p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    shape=p.add_run().add_picture(str(path),width=Inches(width_in))
    alt=Path(path).stem.replace("_"," ")
    shape._inline.docPr.set("descr",alt)
    shape._inline.docPr.set("title",alt[:120])
    format_para(p,0,0,1.0)


def add_page_field(paragraph):
    run=paragraph.add_run()
    fld=OxmlElement("w:fldSimple"); fld.set(qn("w:instr"),"PAGE")
    run._r.addnext(fld)


def setup_doc():
    doc=Document()
    sec=doc.sections[0]
    sec.page_width=Cm(21.0); sec.page_height=Cm(29.7)
    sec.top_margin=Inches(MARGIN_DXA/1440); sec.bottom_margin=Inches(MARGIN_DXA/1440)
    sec.left_margin=Inches(MARGIN_DXA/1440); sec.right_margin=Inches(MARGIN_DXA/1440)
    sec.header_distance=Inches(0.3); sec.footer_distance=Inches(0.3)
    sec.different_first_page_header_footer=True
    normal=doc.styles["Normal"]
    normal.font.name="Microsoft YaHei"; normal.font.size=Pt(10); normal.font.color.rgb=rgb(INK)
    normal._element.rPr.rFonts.set(qn("w:eastAsia"),"Microsoft YaHei")
    normal.paragraph_format.space_after=Pt(4); normal.paragraph_format.line_spacing=1.14
    for name,size,color,before,after in [("Heading 1",16,INK,6,6),("Heading 2",12.5,PURPLE_DARK,5,4),("Heading 3",10.5,INK,3,3)]:
        s=doc.styles[name]; s.font.name="Microsoft YaHei"; s.font.size=Pt(size); s.font.bold=True; s.font.color.rgb=rgb(color)
        s._element.rPr.rFonts.set(qn("w:eastAsia"),"Microsoft YaHei")
        s.paragraph_format.space_before=Pt(before); s.paragraph_format.space_after=Pt(after); s.paragraph_format.keep_with_next=True
    for style_name in ["List Bullet","List Number"]:
        s=doc.styles[style_name]; s.font.name="Microsoft YaHei"; s.font.size=Pt(9.5)
        s._element.rPr.rFonts.set(qn("w:eastAsia"),"Microsoft YaHei")
        s.paragraph_format.left_indent=Inches(0.34); s.paragraph_format.first_line_indent=Inches(-0.18)
        s.paragraph_format.space_after=Pt(3); s.paragraph_format.line_spacing=1.12
    header=sec.header
    hp=header.paragraphs[0]
    hp.alignment=WD_ALIGN_PARAGRAPH.LEFT
    r=hp.add_run("CANVA GROW  ·  营销内容合规层 PRD")
    set_run_font(r,8.2,True,MUTED)
    format_para(hp,0,0,1.0)
    footer=sec.footer
    fp=footer.paragraphs[0]; fp.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    r=fp.add_run("Draft v1.0  ·  2026-09-02  ·  "); set_run_font(r,8,False,MUTED)
    add_page_field(fp)
    return doc


def build_doc():
    save_value_chain(); save_priority_matrix(); save_user_flow(); save_lifecycle(); save_architecture(); save_eval_chart(); save_rollout(); crop_screenshots()
    doc=setup_doc()

    # PAGE 1 — value first
    add_kicker(doc,"Product requirements document")
    p=doc.add_paragraph(); r=p.add_run("Canva Grow\n营销内容合规层")
    set_run_font(r,27,True,INK); format_para(p,3,4,1.0)
    add_text(doc,"让品牌在 Canva 中更快生成、修复并发布可解释的合规营销内容",12.5,MUTED,False,after=10)
    add_heading(doc,"项目对 Canva 的价值",1)
    add_picture(doc,DIAGRAMS/"value_chain.png",7.0)
    add_metric_cards(doc,[
        ("↑","发布转化","减少末端返工"),
        ("↓","合规成本","把检查前移"),
        ("+","行业覆盖","从 Beauty 起步"),
        ("↻","知识复利","争议驱动迭代"),
    ])
    add_callout(doc,"核心判断","这不是一个独立法务工具，而是嵌入 Canva Grow 创作-发布链路的决策层：能检查时给出可执行结果，不能检查时明确边界并阻止错误的“可发布”暗示。",TEAL_LIGHT,TEAL)
    add_text(doc,"Owner  AI Product · Risk & Compliance     |     Status  Draft for alignment     |     Scope  AU · Beauty · Text",8.4,MUTED,False,after=0)

    # PAGE 2
    add_page_break(doc); add_kicker(doc,"01 · Context")
    add_heading(doc,"1. 文档信息与项目背景",1)
    add_table(doc,["字段","内容"],[
        ["产品名称","Canva Grow Compliance Layer（营销内容合规层）"],
        ["产品定位","创作时自动判断营销文案是否可在当前覆盖范围内继续发布，并提供修复、追问或边界披露。"],
        ["目标用户","品牌营销人员、中小企业主、代理商创作者；运营端为法规专家、内容政策与风险团队。"],
        ["本期范围","Australia · Beauty · Text；Cosmetic 与 AUST L Listed Medicine。"],
        ["非目标","不替代法律意见；不声称覆盖 Meta 平台政策、图片、落地页或未发布市场知识包。"],
    ],[1800,8280],8.8)
    add_heading(doc,"1.1 为什么现在做",2)
    add_table(doc,["用户旅程","当前断点","产品机会"],[
        ["生成文案","AI 能写，但用户不知道是否满足市场/品类义务。","生成后立即校验，问题与修复同屏。"],
        ["准备发布","合规常在末端介入，返工或等待人工。","把必要声明、禁用表达和证据要求前移。"],
        ["跨市场复用","用户易把局部规则误认为全市场覆盖。","按国家×行业×产品×格式披露精确覆盖。"],
        ["规则变化","来源、规则、模型和界面解释容易漂移。","知识包版本化，评测通过后再发布。"],
    ],[1900,3700,4480],8.5,header_fill=TEAL)
    add_heading(doc,"1.2 用户与 Jobs-to-be-done",2)
    add_table(doc,["角色","核心任务","成功体验"],[
        ["创作者","快速产出并发布广告文案","少跳转；问题清楚；可一键修复。"],
        ["品牌/法务","控制违规风险与证据链","可追溯规则版本、来源与处理记录。"],
        ["知识运营","维护多市场合规知识","覆盖矩阵清晰，变更有审核与回归评测。"],
    ],[1800,3800,4480],8.6)
    add_callout(doc,"前提假设","本 PRD 以演示站点中的 AU Beauty Text 能力为 P0 基线；所有控制台数字均为 Demo data，不代表 Canva 真实生产指标。",GOLD_LIGHT,GOLD)

    # PAGE 3
    add_page_break(doc); add_kicker(doc,"02 · Goals & scope")
    add_heading(doc,"2. 产品目标、成功指标与优先级",1)
    add_heading(doc,"2.1 北极星与护栏指标",2)
    add_table(doc,["指标","定义","试点建议目标*","用途"],[
        ["合规发布完成率","进入检查后，以有效 Ready 状态继续的会话占比","建立基线后提升","北极星"],
        ["关键遗漏召回率","必填声明/明确禁用项被识别的比例","≥95%","安全护栏"],
        ["误拦截率","真实可用文案被判 Fix 的比例","≤8%","体验护栏"],
        ["覆盖披露率","每次结果展示 checked/not checked 的比例","100%","透明度"],
        ["P95 决策耗时","从内容稳定到结果可用","≤4s","性能"],
        ["修复后完成率","点击修复后通过重检并继续的比例","≥60%","价值验证"],
    ],[2000,3300,1800,2980],8.1)
    add_text(doc,"* 为 PRD 阶段建议阈值，需由影子模式和人工复核结果校准；不得作为现状数据对外传播。",7.8,MUTED,False,after=4)
    add_heading(doc,"2.2 范围优先级",2)
    add_picture(doc,DIAGRAMS/"priority_matrix.png",6.75)
    add_table(doc,["阶段","包含","明确不包含"],[
        ["P0","文本校验、上下文补全、四态结果、修复与重检、覆盖披露、知识版本、争议/评测门禁","图片、落地页、Meta 平台政策"],
        ["P1","图片与落地页检查、平台政策包、多轮上下文、更多 AU 品类","自动扩展为所有市场"],
        ["P2","视频/音频、多市场自助接入、创作前预防式指导","无审核的自动法规发布"],
    ],[1300,4780,4000],8.4,header_fill=TEAL)

    # PAGE 4
    add_page_break(doc); add_kicker(doc,"03 · Core experience")
    add_heading(doc,"3. 核心体验：同屏检查、修复与边界说明",1)
    add_table(doc,["结果状态","触发条件","用户动作","发布权限"],[
        ["Ready to run","上下文完整、范围受支持、无明确问题","查看证据与覆盖范围后继续","允许"],
        ["Fix before running","发现必填缺失或明确风险表达","一键修复/手改后自动重检","阻止"],
        ["Need your input","产品分类、证据或上下文不足","补充信息，不做猜测","阻止"],
        ["Outside scope","市场/行业/产品/格式不在已发布范围","展示未检查项与替代路径","阻止绿色结论"],
    ],[1900,3300,3000,1880],8.3)
    add_heading(doc,"3.1 差异化结果示意",2)
    t=doc.add_table(rows=2,cols=2); t.style="Table Grid"; set_table_geometry(t,[5040,5040])
    t.cell(0,0).text="需修复：缺少强制声明"; t.cell(0,1).text="可发布：当前范围内未发现明确问题"
    for c in t.rows[0].cells: set_cell_shading(c,PURPLE_DARK)
    set_cell_image(t.cell(1,0),SHOTS/"demo_issue_crop.png",2.90)
    set_cell_image(t.cell(1,1),SHOTS/"demo_pass_crop.png",2.90)
    style_table(t,True,8.3,PURPLE_DARK,False)
    add_text(doc,"图 1  Canva Grow 演示：同一创作界面根据内容与上下文给出不同决策。",7.8,MUTED,False,after=5,align=WD_ALIGN_PARAGRAPH.CENTER)

    add_page_break(doc); add_kicker(doc,"03 · Interaction rules")
    add_heading(doc,"3.2 关键交互要求",2)
    add_table(doc,["模块","要求","验收信号"],[
        ["自动触发","内容或上下文稳定后检查；编辑即使结果过期并重跑。","旧结果不可继续使用。"],
        ["问题卡片","指出原文片段、问题类型、可能规则与下一步。","用户无需离开画布理解。"],
        ["Magic rewrite","仅改必要片段；保留品牌语气；修改后重检。","不把修复本身当作通过。"],
        ["解释与反馈","展示 checked/not checked、知识版本、trace_id；可报告结果。","支持审计与争议回流。"],
    ],[1800,5330,2950],8.2,header_fill=TEAL)
    add_heading(doc,"3.2.1 发布门禁与信息保留",2)
    add_callout(doc,"交互边界","后三个阻止状态只禁用该条 AI 结果上的下载、发布、继续等推进操作；用户仍可在对话框中继续聊天、补充信息和修改文案。",GOLD_LIGHT,GOLD)
    add_table(doc,["任何尺寸下都必须保留","产品理由"],[
        ["四个状态齐全，尤其是“需要你补充信息”和“不在覆盖范围”","避免把未知或未覆盖误呈现为绿色结论。"],
        ["每次结果都展示“已检查 / 未检查”","让用户理解结论边界，而不是误认为覆盖整个平台或整条营销链路。"],
        ["知识包版本号与 trace_id","支持复现、审计、争议定位和规则回滚。"],
        ["免责声明：本助手帮助你做出合规判断，不提供法律意见","明确产品价值与责任边界。"],
    ],[4800,5280],8.2,header_fill=PURPLE_DARK,zebra=False)

    # PAGE 6 — AI copy review trigger
    add_page_break(doc); add_kicker(doc,"03 · Trigger & entry")
    add_heading(doc,"3.3 AI 文案审核的触发方式与入口",1)
    add_callout(
        doc,
        "产品原则",
        "Automatic ≠ Everywhere。只有当营销内容已形成，并即将进入选择、编辑、使用、导出或继续发布阶段时，才自动介入完整 Compliance Check；概念探索阶段保持克制。",
        TEAL_LIGHT,
        TEAL,
    )
    add_table(doc,["触发时机","判定条件","系统动作"],[
        ["首次生成可使用文案","内容已可直接采用或继续编辑，格式在支持范围内，且没有有效检查结果。","确认必要 Context 后自动检查。"],
        ["文案发生实质性修改","用户停止编辑或确认修改后，内容哈希与上次结果不一致。","旧结果标记为 Check outdated；debounce 后重检。"],
        ["关键 Context 变化","Country、Industry、Product Type、Product Regulation、Channel 或 Content Format 变化。","重新路由知识包并重检，即使广告文本未变化。"],
        ["采用推荐改写","用户点击 Apply recommended rewrite。","更新文案后执行完整重检；改写成功不等于通过。"],
        ["准备继续使用","下载、发布、导出、Use this copy 或进入下一步时，结果不存在、失效、失败或规则版本过期。","在继续前执行 Pre-use Compliance Gate。"],
    ],[2050,3970,4060],8.0,header_fill=TEAL)
    add_page_break(doc); add_kicker(doc,"03 · In-product entry")
    add_heading(doc,"3.3.1 Canva AI 对话页入口",2)
    add_text(doc,"入口不做独立页面或右侧常驻面板。Canva AI 生成营销文案后，在该条生成结果消息下沿展示同宽的窄提示条，随对话流移动；收起态不超过 72px。",9.0,INK,False,after=5)
    add_picture(doc,SHOTS/"prd_trigger_entry_full.png",5.25,"图 2  审核入口紧贴 AI 生成结果下沿；Context 缺失时可在原对话中补齐。")
    add_table(doc,["收起态固定信息","展开后信息"],[
        ["状态徽章 + 一句话 + 一个主操作；另有“已检查 / 未检查”覆盖说明。","被标记原文、问题类型、可能适用规则、最小改写、覆盖两列、知识包版本、trace_id 与争议入口。"],
        ["四态：可以发布 / 发布前需修改 / 需要你补充信息 / 不在覆盖范围。","后三态禁用该条结果的下载、发布、继续等推进操作，但不阻断继续对话和修改。"],
    ],[5040,5040],8.2,header_fill=PURPLE_DARK,zebra=False)

    # PAGE 6 — trigger examples
    add_page_break(doc); add_kicker(doc,"03 · Trigger cases")
    add_heading(doc,"3.4 触发案例与重检闭环",1)
    t=doc.add_table(rows=2,cols=2); t.style="Table Grid"; set_table_geometry(t,[5040,5040])
    t.cell(0,0).text="案例 A · 发布前需修改"; t.cell(0,1).text="案例 B · 需要你补充信息"
    for c in t.rows[0].cells: set_cell_shading(c,PURPLE_DARK)
    set_cell_image(t.cell(1,0),SHOTS/"prd_side_fix.png",3.05)
    set_cell_image(t.cell(1,1),SHOTS/"prd_need_input.png",3.05)
    style_table(t,True,8.3,PURPLE_DARK,False)
    add_text(doc,"图 3  AUST L 文案缺少强制声明时返回 Fix；监管身份选择“不确定”且含功效声称时返回 Need your input。",7.8,MUTED,False,after=6,align=WD_ALIGN_PARAGRAPH.CENTER)
    add_table(doc,["案例","输入与上下文","结果与下一步"],[
        ["A · 强制声明缺失","Australia · Beauty · AUST L Listed Medicine · Text；文案未包含“Always read the label and follow the directions for use”。","Fix before running；定位为披露缺失，建议补充声明，应用改写后自动重检。"],
        ["B · 监管身份不确定","Product regulation = Not sure；文案含功效声称。","Need your input；询问产品是 Cosmetic 还是 AUST L，不允许模型自行猜测。"],
        ["C · 看过但不拦","文案含“我们团队最爱的一款配方”，只表达主观偏好，不构成功效或客观验证声称。","Ready to run；展开处显示“看过这句，判定无需修改”，并持续披露已检查/未检查范围。"],
    ],[950,4330,4800],8.0,header_fill=TEAL)
    add_heading(doc,"3.4.1 内容或 Context 改变后的状态",2)
    add_picture(doc,SHOTS/"prd_recheck.png",4.55,"图 4  Context 改变后旧结论立即失效，Knowledge Routing 与 Compliance Check 重新执行。")
    add_callout(doc,"失效规则","Content Hash、Context、Rule Version 三者与最近一次有效结果完全一致时复用结果；任一变化都不得沿用旧结果。检查失败或版本失效时，同样由 Pre-use Gate 阻止继续。",GOLD_LIGHT,GOLD)

    # PAGE 7
    add_page_break(doc); add_kicker(doc,"04 · End-to-end flow")
    add_heading(doc,"4. 产品整体流程",1)
    add_picture(doc,DIAGRAMS/"user_flow.png",6.9,"图 2  用户侧端到端流程；每个否定分支都有明确兜底，不以模型猜测补齐。")
    add_heading(doc,"4.1 三类必须覆盖的异常",2)
    add_table(doc,["异常","系统行为","用户文案原则"],[
        ["意图/分类不确定","进入 Need your input；给最少必要追问。","说明缺什么，不假装确定。"],
        ["范围不支持","返回 Outside scope；列出已检查与未检查项。","不使用“合规/安全”绝对措辞。"],
        ["服务/规则执行失败","结果失效并阻止继续；支持重试与人工路径。","透明说明暂时不可用。"],
    ],[2300,4200,3580],8.4)

    # PAGE 6
    add_page_break(doc); add_kicker(doc,"05 · Knowledge operations")
    add_heading(doc,"5. 合规知识控制台与治理闭环",1)
    add_picture(doc,SHOTS/"knowledge_console.png",6.95,"图 3  演示控制台总览：市场、规则、待审核与争议状态集中呈现。")
    add_picture(doc,DIAGRAMS/"knowledge_lifecycle.png",6.95,"图 4  从官方来源到在线决策，再由争议回流到更新迭代。")
    add_heading(doc,"5.1 后台能力模块",2)
    add_table(doc,["模块","核心能力","关键权限"],[
        ["知识包","市场/行业/产品/格式组合；版本与生效期","知识管理员"],
        ["来源与规则","来源快照、条款映射、结构化条件/结论","法规专家"],
        ["审核与争议","双人复核、用户反馈、判例沉淀","审核员/法务"],
        ["评测与发布","回归集、阈值、门禁、回滚","发布管理员"],
    ],[1800,4700,3580],8.4,header_fill=TEAL)

    # PAGE 7
    add_page_break(doc); add_kicker(doc,"06 · Coverage & requirements")
    add_heading(doc,"6. 覆盖矩阵与功能范围",1)
    add_picture(doc,SHOTS/"coverage_matrix.png",6.95,"图 5  覆盖必须精确到 Country × Industry × Product × Format；状态不可被用户误读为全市场。")
    add_heading(doc,"6.1 P0 功能清单",2)
    add_table(doc,["ID","功能","P0 验收标准"],[
        ["F01","上下文采集","市场、行业、产品、格式至少可追溯；缺失时追问。"],
        ["F02","知识包路由","仅命中已发布且在有效期内的版本。"],
        ["F03","文本决策","输出 Ready/Fix/Need input/Outside scope 之一。"],
        ["F04","问题定位与修复","返回问题片段、依据摘要、建议改法；修复后重检。"],
        ["F05","覆盖披露","所有结果展示 checked/not checked 与知识版本。"],
        ["F06","发布门禁","非有效 Ready 不得继续；内容变化立即使结果失效。"],
        ["F07","决策日志","记录输入哈希、上下文、结果、版本、耗时与 trace_id。"],
        ["F08","争议反馈","用户可报告结果，进入队列并关联原决策。"],
    ],[850,2100,7130],8.0)
    add_callout(doc,"边界原则","“Unsupported”不是失败，而是可信产品的必要输出。任何未覆盖组合都不得通过通用模型生成绿色结论。",ORANGE_LIGHT,ORANGE)

    # PAGE 8
    add_page_break(doc); add_kicker(doc,"07 · System & data")
    add_heading(doc,"7. 系统架构与决策契约",1)
    add_picture(doc,DIAGRAMS/"architecture.png",6.95,"图 6  规则确定性、模型理解能力与知识治理分层，避免把法规事实塞入不可审计的提示词。")
    add_heading(doc,"7.1 决策输出结构",2)
    add_table(doc,["字段","示例/规则","用途"],[
        ["status","READY / FIX / NEED_INPUT / OUTSIDE_SCOPE / ERROR","统一前端状态机"],
        ["issues[]","span、issue_type、severity、message、suggestion","定位与修复"],
        ["evidence[]","source_id、rule_id、excerpt_hash、effective_at","解释与审计"],
        ["coverage","checked、not_checked、jurisdiction、format","边界披露"],
        ["knowledge_version","AU-BEA-TEXT v1.4","重现与回滚"],
        ["trace_id / latency","唯一链路 ID / 分阶段耗时","争议定位与观测"],
    ],[2100,5050,2930],8.0,header_fill=TEAL)
    add_heading(doc,"7.2 模型使用边界",2)
    add_table(doc,["适合模型","必须由规则/知识决定"],[
        ["意图分类、实体抽取、原文片段定位、解释改写","法规是否生效、覆盖范围、强制声明、发布门禁、版本选择"],
        ["对不完整表达提出澄清问题","不得用参数记忆替代官方来源或填补未知"],
    ],[5040,5040],8.4)

    # PAGE 9
    add_page_break(doc); add_kicker(doc,"08 · Evaluation")
    add_heading(doc,"8. 评测体系与发布门禁",1)
    add_picture(doc,SHOTS/"evaluation_center.png",6.95,"图 7  演示评测中心：未运行真实基准前不展示虚构准确率，发布状态保持 Blocked。")
    add_picture(doc,DIAGRAMS/"eval_dataset.png",6.5,"图 8  演示数据集 AU-BEA-0.3 的三类样本分布。")

    add_page_break(doc); add_kicker(doc,"08 · Evaluation gate")
    add_heading(doc,"8.1 核心评测维度",2)
    add_table(doc,["维度","指标","发布门禁"],[
        ["安全性","关键遗漏召回、严重违规漏放率","严重漏放为 0；召回达到包阈值"],
        ["可用性","误拦截率、修复后通过率","不劣于当前生产版本"],
        ["边界","缺上下文/不支持组合识别率","不得输出 Ready"],
        ["可解释","证据可追溯率、错误 rule_id 率","证据覆盖 100%；无错误映射"],
        ["稳定性","P95 延迟、超时率、版本一致性","满足 SLO；可回滚"],
    ],[1700,4150,4230],8.1,header_fill=TEAL)

    # PAGE 10
    add_page_break(doc); add_kicker(doc,"09 · Rollout & risk")
    add_heading(doc,"9. 上线计划、风险与依赖",1)
    add_picture(doc,DIAGRAMS/"rollout.png",6.95,"图 9  每个知识包独立通过影子模式、人工复核和回归评测，不以一次上线覆盖所有市场。")
    add_heading(doc,"9.1 风险清单",2)
    add_table(doc,["风险","影响","控制措施","Owner"],[
        ["漏放严重违规","品牌/监管风险","强规则优先、关键召回门禁、人工复核抽样","Risk + ML"],
        ["误拦截过多","发布转化下降","Hard negative 集、分级严重度、可解释反馈","Product"],
        ["规则过期","错误结论","来源 last-checked、到期告警、紧急下线/回滚","Knowledge Ops"],
        ["覆盖误解","用户把局部当全局","所有结果固定展示 checked/not checked","Design"],
        ["生成修复引入新问题","循环返工","修复后必重检；限制修改范围","ML"],
        ["争议积压","知识无法闭环","SLA、优先级、判例复用与趋势告警","Ops"],
        ["隐私与数据滥用","客户信任受损","最小化日志、内容哈希、访问控制、保留期","Security"],
    ],[2350,2450,3730,1550],7.9)
    add_heading(doc,"9.2 关键依赖",2)
    add_table(doc,["依赖","进入 P0 前需要"],[
        ["法规与法务","确认 AU Beauty Text 的官方来源、适用范围和免责声明。"],
        ["Canva Grow","提供活动上下文、编辑事件、发布门禁与版本状态。"],
        ["数据/ML","建立经专家标注的基准集与错误分级。"],
        ["平台/安全","决策日志、访问控制、告警、回滚与数据保留策略。"],
    ],[2200,7880],8.4,header_fill=TEAL)

    # PAGE 11
    add_page_break(doc); add_kicker(doc,"10 · Acceptance")
    add_heading(doc,"10. 验收标准与待决问题",1)
    add_heading(doc,"10.1 P0 端到端验收",2)
    add_table(doc,["场景","Given / When","Then"],[
        ["缺少必填声明","AUST L 文案缺少 mandatory statement","返回 Fix；定位缺失；可一键补充；重检后才允许继续。"],
        ["产品分类未知","用户未提供 Cosmetic 或 Listed Medicine","返回 Need input；不选择默认分类。"],
        ["范围不支持","AU Fitness Text 或 Cosmetic Image","返回 Outside scope；列出未检查项；不显示 Ready。"],
        ["检查通过","AU Cosmetic Text 且无明确问题","显示 Ready、覆盖范围、规则版本与解释；内容变更后失效。"],
        ["系统失败","规则服务超时或知识包不可用","返回 Error；阻止继续；支持重试与人工路径。"],
        ["用户争议","用户报告错误结果","争议记录包含 trace_id、内容哈希、上下文和知识版本。"],
    ],[1900,4100,4080],8.2)
    add_heading(doc,"10.2 立项前必须回答",2)
    add_table(doc,["问题","建议决策"],[
        ["P0 是否硬阻断发布？","仅对高置信强制义务硬阻断；其余按风险等级与市场策略处理。"],
        ["谁拥有规则最终解释权？","法规专家负责规则，产品负责体验，发布管理员负责上线门禁。"],
        ["哪些内容可用于模型改进？","默认不使用客户原文训练；仅在明确授权和去标识后进入数据集。"],
        ["如何表述“Ready”？","固定附带“在当前已检查范围内”与 not checked 列表。"],
        ["首个真实试点群体？","建议 AU Beauty 内部/白名单品牌，先影子模式再受控发布。"],
    ],[3300,6780],8.4,header_fill=TEAL)
    add_heading(doc,"10.3 文档依据",2)
    add_text(doc,"结构与篇幅参考：《AI工具助手PRD.pdf》（11 页）。产品界面依据：Canva Grow Compliance Demo 与 Compliance Knowledge Console，访问日期 2026-08-30。控制台数字标注为演示数据。",8.5,MUTED,False,after=5)
    add_callout(doc,"最终建议","以 AU Beauty Text 为最小可信闭环：先证明“能准确识别边界、能修复、能解释、能回流”，再扩图片、平台政策和新市场。",PURPLE_LIGHT,PURPLE)

    out=OUTPUT/"Canva_Grow_营销内容合规层_PRD_飞书导入版.docx"
    doc.save(out)
    print(out)


if __name__=="__main__":
    build_doc()
