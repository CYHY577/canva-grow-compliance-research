from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"C:\Users\pc\Desktop\canva测试")
OUT = ROOT / "output" / "Canva_AI_海报文字合规审核_产品流程图.png"
OUT.parent.mkdir(parents=True, exist_ok=True)

W, H = 2000, 2200
im = Image.new("RGB", (W, H), "#FFFFFF")
d = ImageDraw.Draw(im)
regular = r"C:\Windows\Fonts\msyh.ttc"
bold = r"C:\Windows\Fonts\msyhbd.ttc"
F_TITLE = ImageFont.truetype(bold, 54)
F_SUB = ImageFont.truetype(regular, 25)
F_NODE = ImageFont.truetype(bold, 28)
F_BODY = ImageFont.truetype(regular, 24)
F_SMALL = ImageFont.truetype(regular, 21)
F_LABEL = ImageFont.truetype(bold, 22)

INK = "#25212B"
MUTED = "#706A76"
PURPLE = "#7D2AE8"
PURPLE_BG = "#F5EEFF"
BLUE = "#2B6DE5"
BLUE_BG = "#EDF4FF"
GREEN = "#17865A"
GREEN_BG = "#EAF8F2"
AMBER = "#A56D00"
AMBER_BG = "#FFF4D6"
RED = "#BF3F30"
RED_BG = "#FFF0ED"
GRAY = "#68636D"
GRAY_BG = "#F0EFF2"
BORDER = "#DCD6E2"


def centered_text(rect, lines, font=F_NODE, color=INK, gap=8):
    if isinstance(lines, str):
        lines = lines.split("\n")
    heights = [d.textbbox((0, 0), t, font=font)[3] for t in lines]
    total = sum(heights) + gap * (len(lines) - 1)
    y = rect[1] + (rect[3] - rect[1] - total) / 2
    for t, hh in zip(lines, heights):
        bb = d.textbbox((0, 0), t, font=font)
        x = rect[0] + (rect[2] - rect[0] - (bb[2] - bb[0])) / 2
        d.text((x, y), t, font=font, fill=color)
        y += hh + gap


def rounded(x, y, w, h, text, fill="#FFFFFF", stroke=PURPLE, font=F_NODE, radius=22):
    rect = (x, y, x + w, y + h)
    d.rounded_rectangle(rect, radius=radius, fill=fill, outline=stroke, width=4)
    centered_text(rect, text, font=font)
    return rect


def stadium(x, y, w, h, text, fill=PURPLE_BG, stroke=PURPLE):
    return rounded(x, y, w, h, text, fill, stroke, radius=h // 2)


def diamond(cx, cy, w, h, text, fill="#FFFFFF", stroke=BLUE):
    pts = [(cx, cy - h // 2), (cx + w // 2, cy), (cx, cy + h // 2), (cx - w // 2, cy)]
    d.polygon(pts, fill=fill)
    d.line(pts + [pts[0]], fill=stroke, width=5, joint="curve")
    centered_text((cx - w // 2 + 35, cy - h // 2 + 18, cx + w // 2 - 35, cy + h // 2 - 18), text, font=F_NODE)
    return (cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2)


def arrow(points, color=PURPLE, label=None, label_pos=None, dashed=False):
    if dashed:
        for i in range(len(points) - 1):
            a, b = points[i], points[i + 1]
            dist = max(abs(b[0] - a[0]), abs(b[1] - a[1]))
            n = max(1, int(dist / 18))
            for s in range(0, n, 2):
                t1 = s / n
                t2 = min((s + 1) / n, 1)
                d.line((a[0] + (b[0]-a[0])*t1, a[1] + (b[1]-a[1])*t1,
                        a[0] + (b[0]-a[0])*t2, a[1] + (b[1]-a[1])*t2), fill=color, width=5)
    else:
        d.line(points, fill=color, width=6, joint="curve")
    a, b = points[-2], points[-1]
    if abs(b[0]-a[0]) >= abs(b[1]-a[1]):
        if b[0] > a[0]: tri=[(b[0],b[1]),(b[0]-18,b[1]-11),(b[0]-18,b[1]+11)]
        else: tri=[(b[0],b[1]),(b[0]+18,b[1]-11),(b[0]+18,b[1]+11)]
    else:
        if b[1] > a[1]: tri=[(b[0],b[1]),(b[0]-11,b[1]-18),(b[0]+11,b[1]-18)]
        else: tri=[(b[0],b[1]),(b[0]-11,b[1]+18),(b[0]+11,b[1]+18)]
    d.polygon(tri, fill=color)
    if label and label_pos:
        d.rounded_rectangle((label_pos[0]-9,label_pos[1]-5,label_pos[0]+d.textbbox((0,0),label,font=F_LABEL)[2]+9,label_pos[1]+31),radius=8,fill="#FFFFFF")
        d.text(label_pos, label, font=F_LABEL, fill=color)


def note(x, y, w, title, text, fill, stroke):
    h=132
    d.rounded_rectangle((x,y,x+w,y+h),radius=20,fill=fill,outline=stroke,width=4)
    d.text((x+24,y+18),title,font=F_NODE,fill=stroke)
    d.text((x+24,y+64),text,font=F_SMALL,fill=INK)
    return (x,y,x+w,y+h)


# Header
d.text((90, 55), "Canva AI 海报文字合规审核产品流程图", font=F_TITLE, fill=INK)
d.text((92, 127), "从海报生成完成开始检查最终可见文字；用户 Prompt 仅用于生成，不进入合规判断。", font=F_SUB, fill=MUTED)
d.rounded_rectangle((88, 180, 1912, 2080), radius=28, fill="#FBFAFC", outline=BORDER, width=3)

cx = 760
start = stadium(cx-170, 225, 340, 86, "开始", fill=PURPLE_BG)
input_node = rounded(cx-220, 355, 440, 112, "输入海报生成需求", fill="#FFFFFF")
generate = rounded(cx-230, 515, 460, 126, "生成背景图与文字图层\n组合为可用营销海报", fill=PURPLE_BG)
trigger = rounded(cx-220, 695, 440, 112, "海报渲染完成\n自动触发审核", fill=BLUE_BG, stroke=BLUE)
extract = rounded(cx-220, 855, 440, 112, "读取文字图层\n扁平图片使用 OCR", fill=BLUE_BG, stroke=BLUE)
context = diamond(cx, 1075, 430, 170, "必要 Context\n是否完整？", fill="#FFFFFF", stroke=BLUE)
scope = diamond(cx, 1325, 430, 170, "当前组合\n是否在覆盖范围？", fill="#FFFFFF", stroke=BLUE)
route = rounded(cx-220, 1465, 440, 112, "路由已发布知识包", fill=GREEN_BG, stroke=GREEN)
decision = diamond(cx, 1730, 460, 180, "是否发现\n明确问题？", fill="#FFFFFF", stroke=BLUE)
ready = note(cx-220, 1880, 440, "可以发布", "在已检查范围内继续使用", GREEN_BG, GREEN)
finish = stadium(cx-130, 2040, 260, 70, "结束", fill=GREEN_BG, stroke=GREEN)

# Right-side outcomes
need = note(1325, 1010, 480, "需要补充信息", "补充产品监管身份或证据", AMBER_BG, AMBER)
need_action = rounded(1375, 1180, 380, 96, "补充 Context", fill="#FFFFFF", stroke=AMBER, font=F_BODY)
outside = note(1325, 1300, 480, "不在覆盖范围", "说明覆盖边界，不给绿色结论", GRAY_BG, GRAY)
outside_finish = stadium(1435, 1475, 260, 70, "结束", fill=GRAY_BG, stroke=GRAY)
fix = note(1325, 1660, 480, "发布前需修改", "定位文字并提供最小改写", RED_BG, RED)
fix_action = rounded(1375, 1835, 380, 96, "编辑或应用建议", fill="#FFFFFF", stroke=RED, font=F_BODY)

# Main spine
for a,b in [(start,input_node),(input_node,generate),(generate,trigger),(trigger,extract)]:
    arrow([((a[0]+a[2])//2,a[3]),((b[0]+b[2])//2,b[1])])
arrow([(cx,extract[3]),(cx,context[1])])
arrow([(cx,context[3]),(cx,scope[1])],label="是",label_pos=(780,1195))
arrow([(cx,scope[3]),(cx,route[1])],label="是",label_pos=(780,1412))
arrow([(cx,route[3]),(cx,decision[1])])
arrow([(cx,decision[3]),(cx,ready[1])],label="否",label_pos=(780,1828))
arrow([(cx,ready[3]),(cx,finish[1])])

# Branches
arrow([(context[2],1075),(need[0],1075)],color=AMBER,label="否",label_pos=(1115,1034))
arrow([((need[0]+need[2])//2,need[3]),((need_action[0]+need_action[2])//2,need_action[1])],color=AMBER)
arrow([(need_action[2],1228),(1870,1228),(1870,930),(cx+250,930),(cx+250,context[1]+28)],color=AMBER,dashed=True,label="补充后重检",label_pos=(1580,890))

arrow([(scope[2],1325),(outside[0],1325)],color=GRAY,label="否",label_pos=(1115,1284))
arrow([((outside[0]+outside[2])//2,outside[3]),((outside_finish[0]+outside_finish[2])//2,outside_finish[1])],color=GRAY)

arrow([(decision[2],1730),(fix[0],1730)],color=RED,label="是",label_pos=(1120,1688))
arrow([((fix[0]+fix[2])//2,fix[3]),((fix_action[0]+fix_action[2])//2,fix_action[1])],color=RED)
arrow([(fix_action[2],1883),(1890,1883),(1890,790),(trigger[2]+60,790),(trigger[2]+60,751),(trigger[2],751)],color=RED,dashed=True,label="修改后重检",label_pos=(1580,760))

# Bottom rule note
d.rounded_rectangle((140, 2130, 1860, 2178), radius=16, fill="#F5EEFF")
d.text((170, 2141), "结果失效规则：海报文字、Context 或规则版本任一变化 → 旧结果失效 → 自动重新检查。", font=F_LABEL, fill=PURPLE)

im.save(OUT, quality=95)
print(OUT)
