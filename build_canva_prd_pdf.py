from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(r"C:\Users\pc\Desktop\canva测试")
ASSETS = ROOT / "assets"
DIAGRAMS = ASSETS / "diagrams"
SHOTS = ASSETS / "screenshots"
OUT_DIR = ROOT / "output" / "pdf"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT = OUT_DIR / "Canva_Grow_营销内容合规层_PRD_补充版.pdf"

pdfmetrics.registerFont(TTFont("YaHei", r"C:\Windows\Fonts\msyh.ttc"))
pdfmetrics.registerFont(TTFont("YaHei-Bold", r"C:\Windows\Fonts\msyhbd.ttc"))

PURPLE = colors.HexColor("#7D2AE8")
PURPLE_DARK = colors.HexColor("#5B21B6")
PURPLE_LIGHT = colors.HexColor("#F3E8FF")
TEAL = colors.HexColor("#00A9B5")
TEAL_LIGHT = colors.HexColor("#E7FAFA")
INK = colors.HexColor("#18191F")
MUTED = colors.HexColor("#667085")
LINE = colors.HexColor("#D9DCE3")
BG = colors.HexColor("#F7F7FA")
GREEN = colors.HexColor("#167A55")
GREEN_LIGHT = colors.HexColor("#EAF7F0")
ORANGE = colors.HexColor("#D94B2B")
ORANGE_LIGHT = colors.HexColor("#FFF0EB")
GOLD = colors.HexColor("#9A6700")
GOLD_LIGHT = colors.HexColor("#FFF7D6")
WHITE = colors.white

PAGE_W, PAGE_H = A4
LEFT = RIGHT = 15 * mm
TOP = 16 * mm
BOTTOM = 14 * mm
CONTENT_W = PAGE_W - LEFT - RIGHT


styles = getSampleStyleSheet()
BODY = ParagraphStyle(
    "BodyCN", parent=styles["BodyText"], fontName="YaHei", fontSize=8.5,
    leading=12.5, textColor=INK, spaceAfter=4, wordWrap="CJK",
)
SMALL = ParagraphStyle(
    "SmallCN", parent=BODY, fontSize=7, leading=9.5, textColor=MUTED, spaceAfter=2,
)
TITLE = ParagraphStyle(
    "TitleCN", parent=BODY, fontName="YaHei-Bold", fontSize=25, leading=31,
    textColor=INK, spaceAfter=6,
)
SUBTITLE = ParagraphStyle(
    "SubtitleCN", parent=BODY, fontSize=11.5, leading=17, textColor=MUTED, spaceAfter=9,
)
H1 = ParagraphStyle(
    "H1CN", parent=BODY, fontName="YaHei-Bold", fontSize=15, leading=20,
    textColor=INK, spaceBefore=2, spaceAfter=6, keepWithNext=True,
)
H2 = ParagraphStyle(
    "H2CN", parent=BODY, fontName="YaHei-Bold", fontSize=11.2, leading=15,
    textColor=PURPLE_DARK, spaceBefore=4, spaceAfter=4, keepWithNext=True,
)
KICKER = ParagraphStyle(
    "KickerCN", parent=BODY, fontName="YaHei-Bold", fontSize=7.2, leading=9,
    textColor=PURPLE, spaceAfter=3, keepWithNext=True,
)
CAPTION = ParagraphStyle(
    "CaptionCN", parent=SMALL, alignment=TA_CENTER, spaceBefore=2, spaceAfter=4,
)
CELL = ParagraphStyle(
    "CellCN", parent=BODY, fontSize=7.4, leading=10.2, spaceAfter=0,
)
CELL_HEAD = ParagraphStyle(
    "CellHeadCN", parent=CELL, fontName="YaHei-Bold", textColor=WHITE, alignment=TA_CENTER,
)
CELL_CENTER = ParagraphStyle(
    "CellCenterCN", parent=CELL, alignment=TA_CENTER,
)
CALLOUT = ParagraphStyle(
    "CalloutCN", parent=BODY, fontSize=8.2, leading=12, leftIndent=8, rightIndent=8,
    borderColor=PURPLE, borderWidth=0.8, borderPadding=7, backColor=PURPLE_LIGHT,
    spaceBefore=4, spaceAfter=5,
)


def P(text, style=BODY):
    return Paragraph(str(text), style)


def K(text):
    return P(text.upper(), KICKER)


def H(text, level=1):
    return P(text, H1 if level == 1 else H2)


def para(text, bold_prefix=None):
    if bold_prefix and text.startswith(bold_prefix):
        text = f"<b>{bold_prefix}</b>{text[len(bold_prefix):]}"
    return P(text)


def img(path, width=CONTENT_W, max_height=None, caption=None):
    path = Path(path)
    with PILImage.open(path) as im:
        w, h = im.size
    height = width * h / w
    if max_height and height > max_height:
        height = max_height
        width = height * w / h
    pic = Image(str(path), width=width, height=height)
    pic.hAlign = "CENTER"
    out = [pic]
    if caption:
        out.append(P(caption, CAPTION))
    return out


def cells(rows, header=True):
    out = []
    for ri, row in enumerate(rows):
        out.append([
            P(v, CELL_HEAD if header and ri == 0 else CELL)
            for v in row
        ])
    return out


def data_table(headers, rows, widths, header_color=PURPLE_DARK, font_size=None):
    data = cells([headers] + rows)
    if font_size:
        local = ParagraphStyle("LocalCell", parent=CELL, fontSize=font_size, leading=font_size + 2.5, spaceAfter=0)
        local_h = ParagraphStyle("LocalHead", parent=local, fontName="YaHei-Bold", textColor=WHITE, alignment=TA_CENTER)
        data = [[P(v, local_h if ri == 0 else local) for v in row] for ri, row in enumerate([headers] + rows)]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), header_color),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("GRID", (0, 0), (-1, -1), 0.45, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    for r in range(2, len(data), 2):
        cmds.append(("BACKGROUND", (0, r), (-1, r), BG))
    t.setStyle(TableStyle(cmds))
    return t


def callout(label, text, fill=PURPLE_LIGHT, border=PURPLE):
    s = ParagraphStyle(
        f"Callout-{label}", parent=CALLOUT, borderColor=border, backColor=fill,
    )
    return P(f"<b>{label}</b>&nbsp;&nbsp;{text}", s)


def metric_cards(cards):
    fills = [PURPLE_LIGHT, TEAL_LIGHT, GREEN_LIGHT, GOLD_LIGHT]
    accents = [PURPLE, TEAL, GREEN, GOLD]
    row = []
    for i, (value, label, note) in enumerate(cards):
        style = ParagraphStyle(
            f"Metric{i}", parent=CELL_CENTER, fontSize=7.3, leading=10, backColor=fills[i],
        )
        row.append(P(f'<font name="YaHei-Bold" size="16" color="{accents[i].hexval()}">{value}</font><br/><b>{label}</b><br/><font color="#667085">{note}</font>', style))
    t = Table([row], colWidths=[CONTENT_W / len(cards)] * len(cards))
    t.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, LINE),
        ("BACKGROUND", (0, 0), (0, 0), fills[0]),
        ("BACKGROUND", (1, 0), (1, 0), fills[1]),
        ("BACKGROUND", (2, 0), (2, 0), fills[2]),
        ("BACKGROUND", (3, 0), (3, 0), fills[3]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setTitle("Canva Grow 营销内容合规层 PRD")
    canvas.setAuthor("AI Product · Risk & Compliance")
    page = canvas.getPageNumber()
    if page > 1:
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.5)
        canvas.line(LEFT, PAGE_H - 12 * mm, PAGE_W - RIGHT, PAGE_H - 12 * mm)
        canvas.setFont("YaHei-Bold", 7)
        canvas.setFillColor(MUTED)
        canvas.drawString(LEFT, PAGE_H - 9.5 * mm, "CANVA GROW · 营销内容合规层 PRD")
        canvas.drawRightString(PAGE_W - RIGHT, PAGE_H - 9.5 * mm, "Draft v1.0")
    canvas.setFont("YaHei", 7)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(PAGE_W - RIGHT, 7 * mm, f"2026-09-02  ·  {page}")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUT), pagesize=A4, leftMargin=LEFT, rightMargin=RIGHT,
    topMargin=TOP, bottomMargin=BOTTOM, title="Canva Grow 营销内容合规层 PRD",
    author="AI Product · Risk & Compliance",
)
frame = Frame(LEFT, BOTTOM, CONTENT_W, PAGE_H - TOP - BOTTOM, id="normal")
doc.addPageTemplates(PageTemplate(id="main", frames=[frame], onPage=header_footer))

story = []


def add(*items):
    for item in items:
        if isinstance(item, (list, tuple)):
            story.extend(item)
        else:
            story.append(item)


def new_page():
    story.append(PageBreak())


# PAGE 1
add(K("Product requirements document"), P("Canva Grow<br/>营销内容合规层", TITLE))
add(P("让品牌在 Canva 中更快生成、修复并发布可解释的合规营销内容", SUBTITLE))
add(H("项目对 Canva 的价值"))
add(img(DIAGRAMS / "value_chain.png", CONTENT_W))
add(Spacer(1, 4), metric_cards([
    ("↑", "发布转化", "减少末端返工"),
    ("↓", "合规成本", "把检查前移"),
    ("+", "行业覆盖", "从 Beauty 起步"),
    ("KB", "知识复利", "争议驱动迭代"),
]), Spacer(1, 8))
add(callout("核心判断", "这不是一个独立法务工具，而是嵌入 Canva Grow 创作-发布链路的决策层：能检查时给出可执行结果，不能检查时明确边界并阻止错误的“可发布”暗示。", TEAL_LIGHT, TEAL))
add(Spacer(1, 7), P("Owner&nbsp;&nbsp;AI Product · Risk & Compliance&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;Status&nbsp;&nbsp;Draft for alignment&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;Scope&nbsp;&nbsp;AU · Beauty · Text", SMALL))

# PAGE 2
new_page(); add(K("01 · Context"), H("1. 文档信息与项目背景"))
add(data_table(["字段", "内容"], [
    ["产品名称", "Canva Grow Compliance Layer（营销内容合规层）"],
    ["产品定位", "创作时自动判断营销文案是否可在当前覆盖范围内继续发布，并提供修复、追问或边界披露。"],
    ["目标用户", "品牌营销人员、中小企业主、代理商创作者；运营端为法规专家、内容政策与风险团队。"],
    ["本期范围", "Australia · Beauty · Text；Cosmetic 与 AUST L Listed Medicine。"],
    ["非目标", "不替代法律意见；不声称覆盖 Meta 平台政策、图片、落地页或未发布市场知识包。"],
], [31*mm, CONTENT_W-31*mm]))
add(H("1.1 为什么现在做", 2))
add(data_table(["用户旅程", "当前断点", "产品机会"], [
    ["生成文案", "AI 能写，但用户不知道是否满足市场或品类义务。", "生成后立即校验，问题与修复同屏。"],
    ["准备发布", "合规常在末端介入，造成返工或等待。", "把必要声明、禁用表达和证据要求前移。"],
    ["跨市场复用", "用户容易把局部规则误认为全市场覆盖。", "按国家×行业×产品×格式披露精确覆盖。"],
    ["规则变化", "来源、规则、模型和界面解释容易漂移。", "知识包版本化，评测通过后再发布。"],
], [29*mm, 57*mm, CONTENT_W-86*mm], TEAL))
add(H("1.2 用户与 Jobs-to-be-done", 2))
add(data_table(["角色", "核心任务", "成功体验"], [
    ["创作者", "快速产出并发布广告文案", "少跳转；问题清楚；可一键修复。"],
    ["品牌/法务", "控制违规风险与证据链", "可追溯规则版本、来源与处理记录。"],
    ["知识运营", "维护多市场合规知识", "覆盖矩阵清晰，变更有审核与回归评测。"],
], [28*mm, 59*mm, CONTENT_W-87*mm]))
add(callout("前提假设", "本 PRD 以演示站点中的 AU Beauty Text 能力为 P0 基线；所有控制台数字均为 Demo data，不代表 Canva 真实生产指标。", GOLD_LIGHT, GOLD))

# PAGE 3
new_page(); add(K("02 · Goals & scope"), H("2. 产品目标、成功指标与优先级"), H("2.1 北极星与护栏指标", 2))
add(data_table(["指标", "定义", "试点建议目标*", "用途"], [
    ["合规发布完成率", "进入检查后，以有效 Ready 状态继续的会话占比", "建立基线后提升", "北极星"],
    ["关键遗漏召回率", "必填声明或明确禁用项被识别的比例", "≥95%", "安全护栏"],
    ["误拦截率", "真实可用文案被判 Fix 的比例", "≤8%", "体验护栏"],
    ["覆盖披露率", "每次结果展示 checked/not checked 的比例", "100%", "透明度"],
    ["P95 决策耗时", "从内容稳定到结果可用", "≤4 秒", "性能"],
    ["修复后完成率", "点击修复后通过重检并继续的比例", "≥60%", "价值验证"],
], [32*mm, 63*mm, 32*mm, CONTENT_W-127*mm], font_size=6.8))
add(P("* PRD 阶段建议阈值，需由影子模式和人工复核结果校准，不得作为现状数据对外传播。", SMALL))
add(H("2.2 范围优先级", 2), img(DIAGRAMS / "priority_matrix.png", 475, max_height=245))
add(data_table(["阶段", "包含", "明确不包含"], [
    ["P0", "文本校验、上下文补全、四态结果、修复与重检、覆盖披露、知识版本、争议/评测门禁", "图片、落地页、Meta 平台政策"],
    ["P1", "图片与落地页检查、平台政策包、多轮上下文、更多 AU 品类", "自动扩展为所有市场"],
    ["P2", "视频/音频、多市场自助接入、创作前预防式指导", "无审核的自动法规发布"],
], [22*mm, 83*mm, CONTENT_W-105*mm], TEAL, font_size=6.9))

# PAGE 4
new_page(); add(K("03 · Core experience"), H("3. 核心体验：同屏检查、修复与边界说明"))
add(data_table(["结果状态", "触发条件", "用户动作", "发布权限"], [
    ["Ready to run", "上下文完整、范围受支持、无明确问题", "查看证据与覆盖范围后继续", "允许"],
    ["Fix before running", "发现必填缺失或明确风险表达", "一键修复/手改后自动重检", "阻止"],
    ["Need your input", "产品分类、证据或上下文不足", "补充信息，不做猜测", "阻止"],
    ["Outside scope", "市场/行业/产品/格式不在已发布范围", "展示未检查项与替代路径", "不得输出绿色结论"],
], [32*mm, 59*mm, 54*mm, CONTENT_W-145*mm], font_size=6.8))
add(H("3.1 差异化结果示意", 2))
issue = img(SHOTS / "demo_issue_crop.png", 68*mm, max_height=92*mm)[0]
passed = img(SHOTS / "demo_pass_crop.png", 68*mm, max_height=92*mm)[0]
shot_table = Table([
    [P("需修复：缺少强制声明", CELL_HEAD), P("可发布：当前范围未发现明确问题", CELL_HEAD)],
    [issue, passed],
], colWidths=[CONTENT_W/2, CONTENT_W/2])
shot_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), PURPLE_DARK),
    ("GRID", (0,0), (-1,-1), 0.45, LINE),
    ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING", (0,1), (-1,1), 5), ("BOTTOMPADDING", (0,1), (-1,1), 5),
]))
add(shot_table, P("图 1  Canva Grow 演示：同一创作界面根据内容与上下文给出不同决策。", CAPTION))
add(H("3.2 关键交互要求", 2))
add(data_table(["模块", "要求", "验收信号"], [
    ["自动触发", "内容或上下文稳定后检查；编辑后使旧结果过期并重跑。", "旧结果不可继续使用。"],
    ["问题卡片", "指出原文片段、问题类型、可能规则与下一步。", "用户无需离开画布理解。"],
    ["Magic rewrite", "仅改必要片段；保留品牌语气；修改后重检。", "不把修复本身当作通过。"],
    ["解释与反馈", "展示 checked/not checked、知识版本、trace_id；可报告结果。", "支持审计与争议回流。"],
], [27*mm, 84*mm, CONTENT_W-111*mm], TEAL, font_size=6.7))

# SUPPLEMENT PAGE A
new_page(); add(K("03 · Core experience"), H("3.3 AI 文案审核的触发方式与入口"))
add(callout("产品原则", "Automatic 不等于 Everywhere。系统只在营销内容已经形成、即将被选择、编辑、下载、发布或继续使用时介入；概念探索阶段保持克制。", TEAL_LIGHT, TEAL))
add(data_table(["触发方式", "系统判断", "用户入口 / 系统动作"], [
    ["首次生成可使用文案", "内容已形成，且 Country × Industry × Product × Format 有已发布知识包。", "AI 回复下沿自动出现审核条；无需用户主动发起。"],
    ["文案发生实质修改", "内容哈希变化后，旧结果立即标记失效；停止编辑或确认后防抖重检。", "保持对话可编辑，但禁用下载、发布与继续。"],
    ["关键 Context 变化", "Country、Industry、Product Type、Product Regulation、Channel 或 Format 任一变化。", "重新路由知识包并完整重检。"],
    ["应用建议改写", "改写只代表内容已更新，不代表问题已经解决。", "应用后自动完整重检；新结果决定是否放行。"],
    ["准备继续使用", "当前无结果、结果过期、检查失败或 Rule Version 失效。", "下载 / 发布 / 继续之前执行 Pre-use Compliance Gate。"],
], [33*mm, 82*mm, CONTENT_W-115*mm], TEAL, font_size=6.15))
add(H("3.3.1 主入口：跟随 AI 生成结果", 2))
add(img(SHOTS / "prd_trigger_entry_full.png", 360, max_height=300, caption="图 1A  可使用文案生成后，审核条紧贴 AI 回复下沿自动出现；发布动作在有效 Ready 前保持禁用。"))
add(data_table(["入口", "呈现与权限规则"], [
    ["AI 回复下沿", "收起态只展示状态、短说明、主操作及 checked/not checked；展开后显示原文、可能规则、最小改写、版本与 trace_id。"],
    ["发布前门禁", "页面没有固定发布按钮时，对该条结果的下载、发布、继续等推进操作实施门禁，但不阻断用户继续对话和修改。"],
], [35*mm, CONTENT_W-35*mm], font_size=6.7))

# SUPPLEMENT PAGE B
new_page(); add(K("03 · Core experience"), H("3.4 触发案例与重检闭环"))
fix_shot = img(SHOTS / "prd_side_fix.png", 76*mm, max_height=91*mm)[0]
input_shot = img(SHOTS / "prd_need_input.png", 76*mm, max_height=91*mm)[0]
trigger_shots = Table([
    [P("案例 A · 明确问题", CELL_HEAD), P("案例 B · 缺少信息", CELL_HEAD)],
    [fix_shot, input_shot],
], colWidths=[CONTENT_W/2, CONTENT_W/2])
trigger_shots.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), PURPLE_DARK),
    ("GRID", (0,0), (-1,-1), 0.45, LINE),
    ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING", (0,1), (-1,1), 5), ("BOTTOMPADDING", (0,1), (-1,1), 5),
]))
add(trigger_shots, P("图 1B  同一入口承载 Fix before running 与 Need your input；状态不同，但 checked/not checked、知识版本与下一步始终可见。", CAPTION))
add(data_table(["案例", "触发链路", "预期结果"], [
    ["AUST L 文案缺强制声明", "首次生成可使用文案 → 自动检查", "Fix before running；应用声明后必须重检。"],
    ["监管身份为 Not sure 且含功效声称", "首次生成 / Context 不完整 → 自动追问", "Need your input；系统不猜测产品分类。"],
    ["用户修改文案或 Context", "旧结果失效 → Knowledge Routing → 完整重检", "重检期间所有推进动作禁用，聊天与编辑保持可用。"],
], [47*mm, 72*mm, CONTENT_W-119*mm], TEAL, font_size=6.45))
add(H("3.4.1 结果失效与自动重检", 2))
recheck_pic = img(SHOTS / "prd_recheck.png", 66*mm, max_height=76*mm)[0]
recheck_notes = data_table(["事件", "系统行为"], [
    ["内容 / Context 改变", "立即使旧结果失效，显示 Checking；旧结果不得用于继续。"],
    ["检查完成", "用新 status、coverage、knowledge version 与 trace_id 原位替换。"],
    ["签名未变化", "Content Hash + Context + Rule Version 完全一致时复用最近有效结果。"],
], [28*mm, 62*mm], PURPLE_DARK, font_size=6.25)
recheck_table = Table([[recheck_pic, recheck_notes]], colWidths=[72*mm, CONTENT_W-72*mm])
recheck_table.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 3), ("RIGHTPADDING", (0,0), (-1,-1), 3)]))
add(recheck_table, P("图 1C  Context 改变后，原结果即时失效并在同一位置重新检查。", CAPTION))

# PAGE 7
new_page(); add(K("04 · End-to-end flow"), H("4. 产品整体流程"))
add(img(DIAGRAMS / "user_flow.png", 445, max_height=450, caption="图 2  用户侧端到端流程；否定分支都有明确兜底，不以模型猜测补齐。"))
add(H("4.1 三类必须覆盖的异常", 2))
add(data_table(["异常", "系统行为", "用户文案原则"], [
    ["意图/分类不确定", "进入 Need your input；给最少必要追问。", "说明缺什么，不假装确定。"],
    ["范围不支持", "返回 Outside scope；列出已检查与未检查项。", "不使用“合规/安全”绝对措辞。"],
    ["服务/规则执行失败", "结果失效并阻止继续；支持重试与人工路径。", "透明说明暂时不可用。"],
], [36*mm, 75*mm, CONTENT_W-111*mm], font_size=7.0))

# PAGE 6
new_page(); add(K("05 · Knowledge operations"), H("5. 合规知识控制台与治理闭环"))
add(img(SHOTS / "knowledge_console.png", 470, max_height=285, caption="图 3  演示控制台总览：市场、规则、待审核与争议状态集中呈现。"))
add(img(DIAGRAMS / "knowledge_lifecycle.png", 495, max_height=145, caption="图 4  从官方来源到在线决策，再由争议回流到更新迭代。"))
add(H("5.1 后台能力模块", 2))
add(data_table(["模块", "核心能力", "关键权限"], [
    ["知识包", "市场/行业/产品/格式组合；版本与生效期", "知识管理员"],
    ["来源与规则", "来源快照、条款映射、结构化条件/结论", "法规专家"],
    ["审核与争议", "双人复核、用户反馈、判例沉淀", "审核员/法务"],
    ["评测与发布", "回归集、阈值、门禁、回滚", "发布管理员"],
], [29*mm, 84*mm, CONTENT_W-113*mm], TEAL, font_size=7.0))

# PAGE 7
new_page(); add(K("06 · Coverage & requirements"), H("6. 覆盖矩阵与功能范围"))
add(img(SHOTS / "coverage_matrix.png", 480, max_height=330, caption="图 5  覆盖必须精确到 Country × Industry × Product × Format；状态不可被误读为全市场。"))
add(H("6.1 P0 功能清单", 2))
add(data_table(["ID", "功能", "P0 验收标准"], [
    ["F01", "上下文采集", "市场、行业、产品、格式至少可追溯；缺失时追问。"],
    ["F02", "知识包路由", "仅命中已发布且在有效期内的版本。"],
    ["F03", "文本决策", "输出 Ready/Fix/Need input/Outside scope 之一。"],
    ["F04", "问题定位与修复", "返回问题片段、依据摘要、建议改法；修复后重检。"],
    ["F05", "覆盖披露", "所有结果展示 checked/not checked 与知识版本。"],
    ["F06", "发布门禁", "非有效 Ready 不得继续；内容变化立即使结果失效。"],
    ["F07", "决策日志", "记录输入哈希、上下文、结果、版本、耗时与 trace_id。"],
    ["F08", "争议反馈", "用户可报告结果，进入队列并关联原决策。"],
], [13*mm, 37*mm, CONTENT_W-50*mm], font_size=6.5))
add(callout("边界原则", "Unsupported 不是失败，而是可信产品的必要输出。任何未覆盖组合都不得通过通用模型生成绿色结论。", ORANGE_LIGHT, ORANGE))

# PAGE 8
new_page(); add(K("07 · System & data"), H("7. 系统架构与决策契约"))
add(img(DIAGRAMS / "architecture.png", 475, max_height=290, caption="图 6  规则确定性、模型理解能力与知识治理分层，避免把法规事实塞入不可审计的提示词。"))
add(H("7.1 决策输出结构", 2))
add(data_table(["字段", "示例/规则", "用途"], [
    ["status", "READY / FIX / NEED_INPUT / OUTSIDE_SCOPE / ERROR", "统一前端状态机"],
    ["issues[]", "span、issue_type、severity、message、suggestion", "定位与修复"],
    ["evidence[]", "source_id、rule_id、excerpt_hash、effective_at", "解释与审计"],
    ["coverage", "checked、not_checked、jurisdiction、format", "边界披露"],
    ["knowledge_version", "AU-BEA-TEXT v1.4", "重现与回滚"],
    ["trace_id / latency", "唯一链路 ID / 分阶段耗时", "争议定位与观测"],
], [36*mm, 92*mm, CONTENT_W-128*mm], TEAL, font_size=6.6))
add(H("7.2 模型使用边界", 2))
add(data_table(["适合模型", "必须由规则/知识决定"], [
    ["意图分类、实体抽取、原文片段定位、解释改写", "法规是否生效、覆盖范围、强制声明、发布门禁、版本选择"],
    ["对不完整表达提出澄清问题", "不得用参数记忆替代官方来源或填补未知"],
], [CONTENT_W/2, CONTENT_W/2], font_size=7.0))

# PAGE 9
new_page(); add(K("08 · Evaluation"), H("8. 评测体系与发布门禁"))
add(img(SHOTS / "evaluation_center.png", 450, max_height=300, caption="图 7  演示评测中心：未运行真实基准前不展示虚构准确率，发布状态保持 Blocked。"))
add(img(DIAGRAMS / "eval_dataset.png", 465, max_height=165, caption="图 8  演示数据集 AU-BEA-0.3 的三类样本分布。"))
add(H("8.1 核心评测维度", 2))
add(data_table(["维度", "指标", "发布门禁"], [
    ["安全性", "关键遗漏召回、严重违规漏放率", "严重漏放为 0；召回达到包阈值"],
    ["可用性", "误拦截率、修复后通过率", "不劣于当前生产版本"],
    ["边界", "缺上下文/不支持组合识别率", "不得输出 Ready"],
    ["可解释", "证据可追溯率、错误 rule_id 率", "证据覆盖 100%；无错误映射"],
    ["稳定性", "P95 延迟、超时率、版本一致性", "满足 SLO；可回滚"],
], [27*mm, 73*mm, CONTENT_W-100*mm], TEAL, font_size=6.8))

# PAGE 10
new_page(); add(K("09 · Rollout & risk"), H("9. 上线计划、风险与依赖"))
add(img(DIAGRAMS / "rollout.png", 490, max_height=150, caption="图 9  每个知识包独立通过影子模式、人工复核和回归评测，不以一次上线覆盖所有市场。"))
add(H("9.1 风险清单", 2))
add(data_table(["风险", "影响", "控制措施", "Owner"], [
    ["漏放严重违规", "品牌/监管风险", "强规则优先、关键召回门禁、人工复核抽样", "Risk + ML"],
    ["误拦截过多", "发布转化下降", "Hard negative 集、分级严重度、可解释反馈", "Product"],
    ["规则过期", "错误结论", "来源 last-checked、到期告警、紧急下线/回滚", "Knowledge Ops"],
    ["覆盖误解", "用户把局部当全局", "所有结果固定展示 checked/not checked", "Design"],
    ["生成修复引入新问题", "循环返工", "修复后必重检；限制修改范围", "ML"],
    ["争议积压", "知识无法闭环", "SLA、优先级、判例复用与趋势告警", "Ops"],
    ["隐私与数据滥用", "客户信任受损", "最小化日志、内容哈希、访问控制、保留期", "Security"],
], [39*mm, 39*mm, 72*mm, CONTENT_W-150*mm], font_size=6.4))
add(H("9.2 关键依赖", 2))
add(data_table(["依赖", "进入 P0 前需要"], [
    ["法规与法务", "确认 AU Beauty Text 的官方来源、适用范围和免责声明。"],
    ["Canva Grow", "提供活动上下文、编辑事件、发布门禁与版本状态。"],
    ["数据/ML", "建立经专家标注的基准集与错误分级。"],
    ["平台/安全", "决策日志、访问控制、告警、回滚与数据保留策略。"],
], [38*mm, CONTENT_W-38*mm], TEAL, font_size=7.0))

# PAGE 11
new_page(); add(K("10 · Acceptance"), H("10. 验收标准与待决问题"), H("10.1 P0 端到端验收", 2))
add(data_table(["场景", "Given / When", "Then"], [
    ["缺少必填声明", "AUST L 文案缺少 mandatory statement", "返回 Fix；定位缺失；可一键补充；重检后才允许继续。"],
    ["产品分类未知", "用户未提供 Cosmetic 或 Listed Medicine", "返回 Need input；不选择默认分类。"],
    ["范围不支持", "AU Fitness Text 或 Cosmetic Image", "返回 Outside scope；列出未检查项；不显示 Ready。"],
    ["检查通过", "AU Cosmetic Text 且无明确问题", "显示 Ready、覆盖范围、规则版本与解释；内容变更后失效。"],
    ["系统失败", "规则服务超时或知识包不可用", "返回 Error；阻止继续；支持重试与人工路径。"],
    ["用户争议", "用户报告错误结果", "争议记录包含 trace_id、内容哈希、上下文和知识版本。"],
], [31*mm, 65*mm, CONTENT_W-96*mm], font_size=6.8))
add(H("10.2 立项前必须回答", 2))
add(data_table(["问题", "建议决策"], [
    ["P0 是否硬阻断发布？", "仅对高置信强制义务硬阻断；其余按风险等级与市场策略处理。"],
    ["谁拥有规则最终解释权？", "法规专家负责规则，产品负责体验，发布管理员负责上线门禁。"],
    ["哪些内容可用于模型改进？", "默认不使用客户原文训练；仅在明确授权和去标识后进入数据集。"],
    ["如何表述 Ready？", "固定附带“在当前已检查范围内”与 not checked 列表。"],
    ["首个真实试点群体？", "建议 AU Beauty 内部/白名单品牌，先影子模式再受控发布。"],
], [58*mm, CONTENT_W-58*mm], TEAL, font_size=7.0))
add(H("10.3 文档依据", 2))
add(P("结构与篇幅参考：《AI工具助手PRD.pdf》（11 页）。产品界面依据：Canva Grow Compliance Demo 与 Compliance Knowledge Console，访问日期 2026-08-30。控制台数字标注为演示数据。", SMALL))
add(callout("最终建议", "以 AU Beauty Text 为最小可信闭环：先证明“能准确识别边界、能修复、能解释、能回流”，再扩图片、平台政策和新市场。"))

doc.build(story)
print(OUT)
