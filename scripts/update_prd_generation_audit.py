from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Inches


ROOT = Path(r"C:\Users\pc\Desktop\canva测试")
SOURCE = ROOT / "output" / "Canva_Grow_营销内容合规层_PRD_AI工具助手结构版.docx"
OUTPUT = ROOT / "output" / "Canva_Grow_营销内容合规层_PRD_V2.1_生成即检查版.docx"
ASSETS = ROOT / "prd-assets"


def set_paragraph_text(paragraph, text, bold=False, color=None):
    for run in list(paragraph.runs):
        paragraph._element.remove(run._element)
    run = paragraph.add_run(text)
    run.bold = bold
    run.font.name = "Microsoft YaHei"
    run._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")
    if color:
        run.font.color.rgb = color
    return run


def replace_picture(paragraph, image_path, width_inches):
    for run in list(paragraph.runs):
        paragraph._element.remove(run._element)
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.add_run().add_picture(str(image_path), width=Inches(width_inches))


def set_cell(table, row, col, text):
    cell = table.cell(row, col)
    cell.text = text
    for paragraph in cell.paragraphs:
        for run in paragraph.runs:
            run.font.name = "Microsoft YaHei"
            run._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")


doc = Document(SOURCE)

# Cover and product principle
set_paragraph_text(doc.paragraphs[2], "V2.1 · 生成阶段规则约束 + 最终海报独立审核 · 对齐最新 Demo")
set_paragraph_text(doc.paragraphs[6], "生成阶段默认介入，最终仍以成品海报为审核对象")
set_paragraph_text(
    doc.paragraphs[7],
    "Compliance Layer 在用户点击“生成”后自动连续执行两层保障：先根据用户意图、产品 Context 与适用知识包约束内容生成，尽量直接产出当前检查范围内可用的营销版本；海报渲染后，再对最终画面执行独立审核。Prompt 用于理解意图和受控生成，但最终判断必须以海报中的实际可见内容为准。",
)

# Background, opportunity, goals
set_paragraph_text(
    doc.paragraphs[16],
    "Canva AI 已能帮助用户快速生成广告图片和海报，但生成模型可能遗漏强制声明、改写文字，或在图片中产生额外文本。仅在生成后提示风险会让用户先看到不可用内容；仅依赖生成约束又无法证明最终海报与规则一致。因此，产品需要把生成约束与最终海报审核组成一条连续自动链路。",
)
set_paragraph_text(doc.paragraphs[19], "合规检查若与生成割裂，会造成“先产出问题内容、再提示修复”的体验矛盾。")
set_paragraph_text(doc.paragraphs[20], "因此，Compliance Layer 默认在生成阶段介入，并在最终海报展示前完成独立审核。")
set_paragraph_text(
    doc.paragraphs[26],
    "Canva 拥有用户意图、产品 Context、生成过程、文字图层、最终像素画面、编辑与导出状态，可以将规则前置为生成约束，并在展示前复核最终产物。用户无需手动发起检查，也不会先看到未经审核的候选海报。",
)
set_paragraph_text(
    doc.paragraphs[38],
    "帮助用户在不离开 Canva AI 创作链路的情况下，直接获得在当前检查范围内可用的营销海报；当系统不能安全自动处理时，再给出补充信息或发布前修改的明确下一步。",
)
set_paragraph_text(doc.paragraphs[39], "用户点击生成后，内容生成与风险检查自动连续执行，无需手动触发。")
set_paragraph_text(doc.paragraphs[40], "生成时应用用户意图、产品 Context 和版本化知识包约束，降低问题内容进入最终海报的概率。")
set_paragraph_text(doc.paragraphs[41], "渲染后独立读取文字图层与 OCR 结果，并检查强制声明完整性、规则语义和视觉可读性。")
set_paragraph_text(doc.paragraphs[42], "能保持核心营销意图时默认自动优化；依赖缺失信息时提示补充；仍有明确问题时才进入发布前需修改。")
set_paragraph_text(doc.paragraphs[43], "未经最终审核的候选海报不展示，下载、发布和继续操作保持禁用。")
set_paragraph_text(doc.paragraphs[44], "最终结果持续披露已检查/未检查范围、知识包版本和 trace_id。")

# Core feature design
set_paragraph_text(doc.paragraphs[51], "4.1 生成阶段默认介入与最终海报独立审核")
set_paragraph_text(
    doc.paragraphs[52],
    "用户输入广告需求并点击生成后，系统先校验 Context、路由适用知识包，将监管边界、强制声明、证据依赖和表达限制转为生成约束。Canva AI 由此生成背景图和可编辑文字层。海报完成渲染后，Compliance Layer 必须再次独立审核最终产物：读取原生文字图层，对扁平化或模型生成在图中的文字执行 OCR，检查强制声明是否完整，并校验字号、对比度、遮挡与裁切等可读性。生成阶段的规则约束不能替代最终审核。",
)
replace_picture(doc.paragraphs[54], ASSETS / "07-generation-audit-sync.png", 6.45)
set_paragraph_text(doc.paragraphs[55], "图 1  最新网页：生成、规则约束与最终海报文字审核同步自动执行，用户只看到复检后的版本。")

set_paragraph_text(
    doc.paragraphs[57],
    "审核从用户点击“生成”开始，与内容生成自动连续执行，不再设置单独的“开始检查”按钮。处理中只展示统一进度状态；最终海报通过独立审核或完成保守处理后，才进入结果卡片与侧边提示。",
)
set_paragraph_text(doc.paragraphs[59], "首次生成：先路由知识包并约束生成，渲染后立即执行最终海报独立审核。")
set_paragraph_text(doc.paragraphs[60], "处理期间：不展示候选海报，下载、发布和继续操作保持禁用。")
set_paragraph_text(doc.paragraphs[61], "文字、Context 或知识包版本变化时，旧结果立即失效并自动重跑；完全一致时才复用有效结果。")
replace_picture(doc.paragraphs[62], ASSETS / "08-conservative-need-input.png", 6.45)
set_paragraph_text(doc.paragraphs[63], "图 2  Context 不完整：系统仍生成经最终审核的保守版本，并提示用户补充产品信息。")

set_paragraph_text(doc.paragraphs[67], "4.4 自动处理优先级与结果详情")
set_paragraph_text(doc.paragraphs[68], "默认自动优化：在不改变核心营销意图时，删除或改写问题表达、补齐可自动确定的声明，并重新渲染。")
set_paragraph_text(doc.paragraphs[69], "需要补充信息：判断依赖产品监管身份、证据或其他缺失信息时，生成保守版本并提示最少必要信息。")
set_paragraph_text(doc.paragraphs[70], "发布前需修改：只有自动优化并完整重检后仍存在明确问题，才进入该状态并阻止下载或发布。")
set_paragraph_text(doc.paragraphs[71], "自动优化后必须再次执行文字提取、强制声明、规则语义和视觉可读性检查；修复动作本身不算通过。")
set_paragraph_text(doc.paragraphs[72], "结果详情展示原文区域、自动处理记录、可能适用规则、已检查/未检查范围、知识包版本与 trace_id。")
set_paragraph_text(doc.paragraphs[73], "用户修改海报或 Context 后立即使旧结果失效；重新生成与最终审核完成前不得沿用旧结果推进。")

# Product flow and cases
set_paragraph_text(
    doc.paragraphs[81],
    "以下流程描述产品上线后的真实用户路径。核心是“双阶段保障”：生成前/生成中应用规则约束，渲染后对最终海报独立审核。四条泳道分别是用户、Canva AI、Compliance Layer 和知识与规则服务。",
)
replace_picture(doc.paragraphs[82], ASSETS / "product_flow_generation_audit_sync.png", 6.55)
set_paragraph_text(doc.paragraphs[83], "图 3  产品上线后泳道流程：用户一次点击，生成约束、海报渲染、最终审核和必要的自动优化连续完成。")
set_paragraph_text(doc.paragraphs[85], "用户输入营销意图，确认或选择产品 Context，并点击生成。")
set_paragraph_text(doc.paragraphs[86], "系统校验 Context、路由已发布知识包，将规则转为生成约束；缺失信息时采用保守生成策略。")
set_paragraph_text(doc.paragraphs[87], "Canva AI 在约束下生成背景图与可编辑文字层，形成仅在后台存在的候选海报。")
set_paragraph_text(doc.paragraphs[88], "渲染完成后，Compliance Layer 自动读取文字图层并以 OCR 识别扁平化或图片内额外文字。")
set_paragraph_text(doc.paragraphs[89], "最终审核检查强制声明完整性、规则语义、证据依赖以及文字的视觉可读性。")
set_paragraph_text(doc.paragraphs[90], "可安全处理的问题默认自动优化并重渲染、重审；缺信息则返回保守版本与补充提示；仍有明确问题才返回发布前需修改。")
set_paragraph_text(doc.paragraphs[91], "只有完成最终审核的海报才展示；文字、Context 或知识包版本变化后，旧结果失效并自动重跑。")

set_paragraph_text(doc.paragraphs[95], "场景：用户要求 AUST L 产品突出功效，但候选海报遗漏 “ALWAYS READ THE LABEL AND FOLLOW THE DIRECTIONS FOR USE”。")
set_paragraph_text(doc.paragraphs[96], "结果：最终审核识别声明缺失，系统在不改变核心营销意图的情况下自动补齐、重新渲染并完整复核。用户只看到复核后的海报；若声明仍缺失或不可读，才进入“发布前需修改”。")
replace_picture(doc.paragraphs[97], ASSETS / "07-generation-audit-sync.png", 6.45)
set_paragraph_text(doc.paragraphs[98], "图 4  自动优化后生成：问题候选版本不展示，侧边记录自动处理内容与最终审核范围。")

set_paragraph_text(doc.paragraphs[100], "场景：用户希望使用“临床验证，14 天紧致 30%”，但 Product Regulation 为 Not sure，且未提供匹配证据。")
set_paragraph_text(doc.paragraphs[101], "结果：系统不复现临床与量化声称，先生成经最终审核的非量化保守版本，并进入“需要补充信息”。用户仍可查看和编辑保守版本；若希望恢复量化声称，需补充监管身份和 supporting evidence。")
replace_picture(doc.paragraphs[102], ASSETS / "08-conservative-need-input.png", 6.45)
set_paragraph_text(doc.paragraphs[103], "图 5  需要补充信息：不猜测分类，也不阻断保守生成；提示用于提高后续表达准确性。")

set_paragraph_text(doc.paragraphs[105], "场景：用户要求生成日常保湿海报，最终文字包含“我们团队最爱的一款配方”、成分事实和非量化肤感描述。")
set_paragraph_text(doc.paragraphs[106], "结果：生成时未做不必要改写；最终审核完成后返回“可以发布”，详情展示 Checked and fine，证明系统既能发现问题，也能避免误拦截。")
replace_picture(doc.paragraphs[107], ASSETS / "09-synced-ready.png", 6.45)
set_paragraph_text(doc.paragraphs[108], "图 6  同步检查后生成：最终海报在已识别并检查的文字范围内无需修改。")

# Scope, evaluation, system and acceptance prose
set_paragraph_text(doc.paragraphs[112], "Canva AI 广告图片/海报生成；基于用户意图、产品 Context 和知识包的生成约束。")
set_paragraph_text(doc.paragraphs[113], "用户点击生成后自动连续执行生成、渲染、文字提取、最终审核与必要的自动优化。")
set_paragraph_text(doc.paragraphs[114], "原生文字图层读取、OCR 兜底、强制声明完整性和文字视觉可读性检查。")
set_paragraph_text(doc.paragraphs[117], "四态结果、自动处理记录、问题区域、覆盖披露、知识包版本与 trace_id。")
set_paragraph_text(doc.paragraphs[118], "未经审核候选不展示；生成/审核中禁用下载与发布；内容、Context 或版本变化后自动失效并重跑。")
set_paragraph_text(
    doc.paragraphs[131],
    "评测需要覆盖两条链路：一是生成约束能否避免问题内容进入最终版本，二是最终海报审核能否识别模型遗漏、文字变化、图片内额外文本、声明不完整和可读性问题。核心目标不是模型泛泛谈法规，而是做到候选不外露、处理可追溯、结果可复现。",
)
set_paragraph_text(doc.paragraphs[135], "文字图层与 OCR 的字符准确率、区域召回率和图片内额外文字检出率。")
set_paragraph_text(doc.paragraphs[136], "知识包路由准确率、生成约束命中率与规则 ID 正确率。")
set_paragraph_text(doc.paragraphs[137], "强制声明遗漏召回率、视觉可读性问题召回率与严重漏放率。")
set_paragraph_text(doc.paragraphs[138], "自动优化成功率、保守生成准确率、误拦截率和用户理解度。")
set_paragraph_text(doc.paragraphs[139], "未经审核候选曝光率、P95 全链路耗时、超时率、版本一致性与可回滚性。")

# Tables
set_cell(doc.tables[0], 0, 0, "一句话定位  用户点击生成后，系统先用产品 Context 与知识包约束内容生成，再独立审核最终海报；只向用户展示经审核的版本，并在必要时自动优化或提示补充信息。")
set_cell(doc.tables[1], 4, 1, "V2.1 · 2026-09-07")
set_cell(doc.tables[1], 5, 1, "Canva AI · Australia Compliance Layer · release 009")

set_cell(doc.tables[3], 1, 1, "嵌入 Canva AI 海报生成链路的双阶段营销内容合规决策层。")
set_cell(doc.tables[3], 2, 1, "在用户点击生成后，以意图、Context 与知识包约束内容生成；渲染后独立审核最终海报并返回可执行结果。")
set_cell(doc.tables[3], 3, 1, "受控生成、文字图层读取、OCR、强制声明完整性、视觉可读性、自动优化、四态结果、自动重检与发布 Gate。")
set_cell(doc.tables[3], 4, 1, "把 Prompt 当作最终合规审核对象、替用户作法律裁决、平台政策、商标、人物形象、落地页、视频和音频。")

set_cell(doc.tables[4], 1, 2, "缺失信息时采用保守生成，并进入“需要补充信息”；不猜测产品分类或证据。")
set_cell(doc.tables[4], 3, 1, "如果先生成问题内容再提示，用户会经历不必要返工。")
set_cell(doc.tables[4], 3, 2, "能保持核心意图时默认自动优化，只有重检后仍有明确问题才进入 Fix。")
set_cell(doc.tables[4], 4, 1, "生成约束或最终审核都可能过度改写主观表达。")
set_cell(doc.tables[4], 4, 2, "提供 Checked and fine 与自动处理记录，既证明看过，也证明没有过度干预。")

set_cell(doc.tables[5], 0, 0, "核心链路  输入意图与 Context → 路由知识包 → 约束生成 → 后台候选海报 → 最终文字/OCR 审核 → 自动优化并重审（如需）→ 展示经审核版本 → 编辑/下载/发布。")

set_cell(doc.tables[7], 1, 0, "经审核版本完成率")
set_cell(doc.tables[7], 1, 1, "点击生成后，成功获得最终审核版本的会话占比")
set_cell(doc.tables[7], 2, 0, "关键遗漏召回率")
set_cell(doc.tables[7], 2, 1, "强制声明、明确禁止项或图片内额外文本被最终审核识别的比例")
set_cell(doc.tables[7], 3, 0, "自动优化成功率")
set_cell(doc.tables[7], 3, 1, "不改变核心营销意图且完整重检后可展示的自动处理占比")
set_cell(doc.tables[7], 3, 2, "建立基线后提升")
set_cell(doc.tables[7], 5, 0, "未经审核候选曝光率")
set_cell(doc.tables[7], 5, 1, "候选海报在最终审核完成前被用户看到的比例")
set_cell(doc.tables[7], 5, 2, "0%")
set_cell(doc.tables[7], 6, 1, "用户点击生成到经审核结果可用的全链路耗时")

set_cell(doc.tables[8], 1, 1, "理解营销意图并驱动受控生成")
set_cell(doc.tables[8], 1, 2, "参与生成约束；不作为最终审核对象")
set_cell(doc.tables[8], 2, 1, "海报视觉主体与承载文字的像素画面")
set_cell(doc.tables[8], 2, 2, "P0 不判断主体合规，但检查文字可读性")
set_cell(doc.tables[8], 3, 2, "是，最终审核优先读取")
set_cell(doc.tables[8], 4, 2, "是，OCR 识别模型生成或烘焙文字")
set_cell(doc.tables[8], 5, 1, "国家、行业、产品、监管身份、渠道、格式与证据状态")

trigger_rows = [
    ("首次生成", "用户点击生成", "校验 Context、路由知识包、约束生成；渲染后立即最终审核", "避免先展示问题海报再提示"),
    ("文字实质修改", "用户停止编辑或确认编辑", "旧结果失效，debounce 后重新渲染并最终审核", "避免沿用旧海报结论"),
    ("Context 变化", "国家、行业、产品、监管身份、渠道或格式变化", "重新路由知识包、重新生成约束并复核最终海报", "避免沿用旧规则"),
    ("自动优化", "最终审核发现可安全处理的问题", "修改文字层、重新渲染并执行完整最终审核", "避免把修复动作当作通过"),
    ("准备继续使用", "下载/发布时结果不存在、过期或失败", "执行 Pre-use Gate；检查完成前保持禁用", "避免异常路径绕过"),
]
for row_index, values in enumerate(trigger_rows, start=1):
    for col_index, value in enumerate(values):
        set_cell(doc.tables[9], row_index, col_index, value)

state_rows = [
    ("可以发布", "最终海报已完成独立审核；无明确问题，或自动优化后重检通过", "查看处理记录、编辑或继续", "允许"),
    ("发布前需修改", "自动优化并重检后仍存在明确问题", "按定位修改后自动重检", "阻止"),
    ("需要补充信息", "判断依赖监管身份、证据或其他缺失信息；当前已生成保守版本", "可查看/编辑保守版本；补充信息可恢复更具体表达", "保守版本经最终审核后允许；原声称不可恢复"),
    ("不在覆盖范围", "当前国家/行业/产品/格式没有已发布知识包", "查看覆盖范围或转人工", "阻止"),
    ("暂时无法检查", "OCR、规则或模型服务失败", "重试或转人工", "阻止"),
]
for row_index, values in enumerate(state_rows, start=1):
    for col_index, value in enumerate(values):
        set_cell(doc.tables[10], row_index, col_index, value)

set_cell(doc.tables[11], 0, 0, "处理顺序  可保持核心营销意图 → 默认自动优化并重检；判断依赖缺失信息 → 需要补充信息并生成保守版本；自动优化后仍有明确问题 → 发布前需修改。未经最终审核的候选海报不得展示、下载或发布。")

set_cell(doc.tables[12], 4, 2, "Not sure 时采用保守生成并提示补充；不复现依赖分类或证据的具体声称")

set_cell(doc.tables[13], 1, 0, "OCR 低置信或文字不可读")
set_cell(doc.tables[13], 1, 1, "不把不确定文字当作完整输入；尝试重新渲染或提高可读性")
set_cell(doc.tables[13], 1, 2, "检查中不展示；仍失败则暂时无法检查")
set_cell(doc.tables[13], 2, 1, "禁止模型自行生成规则或绿色结论")
set_cell(doc.tables[13], 3, 1, "候选内容保持内部状态，旧结果立即失效")
set_cell(doc.tables[13], 4, 1, "不得保留示例图，也不得展示未审候选")
set_cell(doc.tables[13], 4, 2, "明确生成失败，可重新生成")

set_cell(doc.tables[15], 1, 2, "生成时尽量补齐；最终审核再次检查，缺失则自动优化，仍失败才 Fix")
set_cell(doc.tables[15], 2, 2, "生成约束避免治疗型表达；最终审核识别潜在边界")
set_cell(doc.tables[15], 3, 2, "缺少证据时生成非量化保守版本并 Need input")
set_cell(doc.tables[15], 5, 2, "最终审核不得漏检；低置信不得假装完整")

set_cell(doc.tables[16], 0, 0, "发布门禁  未经最终审核候选曝光率必须为 0；严重漏放必须为 0；自动优化必须完整重检；证据与规则映射需 100% 可追溯。")

component_rows = [
    ("生成编排层", "根据用户意图、Context 与知识包组织文案/图像生成", "不得绕过知识包或直接展示候选"),
    ("GLM 文案与图像生成", "在受控约束下生成背景图、品牌名、标题与文字层", "不输出最终合规结论"),
    ("最终文字提取层", "读取 Canva 文字图层，OCR 识别图片内额外文字", "低置信文字不得当作确定输入"),
    ("知识路由/规则层", "同时提供生成约束、强制义务、覆盖与 Gate", "知识包缺失时不得让模型补规则"),
    ("最终海报审核层", "检查声明完整性、语义、证据依赖和文字可读性，决定处理路径", "不得把生成约束或自动修复当作最终通过"),
]
for row_index, values in enumerate(component_rows, start=1):
    for col_index, value in enumerate(values):
        set_cell(doc.tables[17], row_index, col_index, value)

set_cell(doc.tables[18], 1, 1, "READY / FIX / NEED_INPUT / OUTSIDE_SCOPE / ERROR；处理中为 GENERATING / CHECKING")
set_cell(doc.tables[18], 2, 1, "source、regions、confidence、text_hash、render_hash")
set_cell(doc.tables[18], 3, 1, "region_id、span、issue_type、reason、auto_action、suggestion")
set_cell(doc.tables[18], 4, 1, "checked、not_checked、jurisdiction、format、readability_scope")
set_cell(doc.tables[18], 5, 0, "generation_guardrails / knowledge_version")
set_cell(doc.tables[18], 5, 1, "应用的生成约束、强制义务与知识包版本，如 AU-BEA-POSTER-TEXT v1.4")
set_cell(doc.tables[18], 6, 0, "final_audit / models")
set_cell(doc.tables[18], 6, 1, "文字层/OCR、强制声明、语义、可读性结果及使用的 copy/image/decision model")
set_cell(doc.tables[18], 7, 0, "trace_id / latency")
set_cell(doc.tables[18], 7, 1, "全链路唯一 ID；生成、渲染、提取、审核与自动优化分阶段耗时")

acceptance_rows = [
    ("首次生成", "用户输入新海报需求并点击生成", "生成约束与最终审核自动连续执行；检查完成前不展示候选，不开放下载/发布"),
    ("缺强制声明", "AUST L 候选海报缺 mandatory statement", "默认补齐、重渲染并完整重检；仍缺失或不可读时才返回 Fix"),
    ("监管身份未知", "Not sure 且用户请求临床或量化功效", "不复现该声称，生成保守版本并返回 Need input；不得根据 Prompt 猜分类"),
    ("检查无问题", "AU Cosmetic 最终海报文字无明确问题", "返回 Ready，展示 Checked and fine、覆盖、版本与最终审核记录"),
    ("文字修改", "用户停止编辑海报文字", "旧结果立即失效；重新渲染和最终审核完成前推进操作不可用"),
    ("自动优化", "系统可在不改变核心意图时处理问题", "写回文字层、重渲染并完整重检；修复动作本身不算通过"),
    ("范围不支持", "非 AU Beauty Poster 组合", "返回 Outside scope，不生成规则、不显示绿色结论"),
    ("服务异常", "OCR、模型或知识包不可用", "不展示未审候选；返回 Error 并提供重试"),
]
for row_index, values in enumerate(acceptance_rows, start=1):
    for col_index, value in enumerate(values):
        set_cell(doc.tables[19], row_index, col_index, value)

feature_rows = {
    1: ("F01", "受控海报生成", "基于意图、Context 与知识包生成新背景图和文字层"),
    2: ("F02", "自动连续触发", "点击生成后自动执行约束生成、渲染和最终审核"),
    3: ("F03", "最终文字提取", "文字图层优先，OCR 识别图片内额外文字并返回区域/置信度"),
    4: ("F04", "Context", "六字段可追溯；缺失时采用保守生成并提示"),
    6: ("F06", "处理与四态", "先自动优化，再 Need input，仍有明确问题才 Fix；范围外为 Outside scope"),
    8: ("F08", "自动优化与重检", "不改变核心意图时写回、重渲染并完整最终审核"),
    10: ("F10", "展示与发布 Gate", "未经审核候选不展示；生成/检查中及无有效结果时阻止推进"),
    11: ("F11", "缓存失效", "文字、Context 或知识包版本任一变化即失效并重跑"),
}
for row_index, values in feature_rows.items():
    for col_index, value in enumerate(values):
        set_cell(doc.tables[21], row_index, col_index, value)

doc.core_properties.title = "Canva Grow 营销内容合规层 PRD V2.1"
doc.core_properties.subject = "生成阶段规则约束与最终海报独立审核"
doc.core_properties.comments = "生成即检查版"
doc.save(OUTPUT)
print(OUTPUT)
