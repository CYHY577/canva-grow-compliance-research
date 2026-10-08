from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json

ROOT = Path(r"C:\Users\pc\Desktop\canva测试")
OUT = ROOT / "outputs" / "canva_poster_compliance_testset_zh"
IMG_DIR = OUT / "images"
IMG_DIR.mkdir(parents=True, exist_ok=True)

REG = r"C:\Windows\Fonts\msyh.ttc"
BOLD = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_H1 = ImageFont.truetype(BOLD, 62)
FONT_H2 = ImageFont.truetype(BOLD, 38)
FONT_BODY = ImageFont.truetype(REG, 31)
FONT_SMALL = ImageFont.truetype(REG, 22)
FONT_TINY = ImageFont.truetype(REG, 12)

CASES = [
    {
        "test_id": "AU-001", "title": "团队偏好表达，正常放行", "country": "Australia",
        "industry": "Beauty", "product_type": "Face moisturiser", "product_regulation": "Cosmetic",
        "channel": "Instagram", "content_format": "Poster image", "content_origin": "Canva generated",
        "text_layer_available": True, "supporting_evidence": "Not required",
        "headline": "OUR TEAM'S FAVOURITE FORMULA",
        "lines": ["With niacinamide and vitamin E", "Gentle care for everyday use"],
        "footer": "LUMEA DAILY MOISTURISER",
        "poster_visible_text_gold": "OUR TEAM'S FAVOURITE FORMULA | With niacinamide and vitamin E | Gentle care for everyday use | LUMEA DAILY MOISTURISER",
        "expected_status": "Ready to run", "expected_trigger": "Poster render completed",
        "expected_issue_type": "Checked and fine", "expected_flagged_text": "",
        "expected_missing_info": "", "expected_next_action": "Allow download, publish or continue",
        "expected_checked": "Australia law · Beauty · Cosmetic · Poster text",
        "expected_not_checked": "Platform policy · Non-text visual claims · Landing page",
        "knowledge_package": "AU-BEA-POSTER", "rule_version": "v1.0-demo",
        "gold_rationale": "Preference wording and ingredient-only wording do not state a therapeutic outcome in this test context.",
        "source_url": "https://www.tga.gov.au/resources/guidance/determining-if-your-product-cosmetic-or-therapeutic-good",
        "difficulty": "Easy", "tags": "ready,checked-and-fine,cosmetic", "palette": ["#E9F7F1", "#176B58", "#F7C9D5"]
    },
    {
        "test_id": "AU-002", "title": "AUST L 缺少强制声明", "country": "Australia",
        "industry": "Beauty", "product_type": "Beauty supplement", "product_regulation": "AUST L Listed Medicine",
        "channel": "Instagram", "content_format": "Poster image", "content_origin": "Canva generated",
        "text_layer_available": True, "supporting_evidence": "ARTG indication supplied",
        "headline": "SUPPORTS IMMUNE HEALTH",
        "lines": ["Daily wellness support", "AUST L 345678"], "footer": "VITAGLOW IMMUNE SUPPORT",
        "poster_visible_text_gold": "SUPPORTS IMMUNE HEALTH | Daily wellness support | AUST L 345678 | VITAGLOW IMMUNE SUPPORT",
        "expected_status": "Fix before running", "expected_trigger": "Poster render completed",
        "expected_issue_type": "Missing mandatory statement", "expected_flagged_text": "Advertisement lacks mandatory statement",
        "expected_missing_info": "", "expected_next_action": "Add the required label and directions statement, then re-check",
        "expected_checked": "Australia law · Beauty · AUST L · Poster text",
        "expected_not_checked": "Platform policy · Non-text visual claims · Landing page",
        "knowledge_package": "AU-BEA-POSTER", "rule_version": "v1.0-demo",
        "gold_rationale": "The listed-medicine poster omits the required short-form mandatory statement used by the demo rule package.",
        "source_url": "https://www.tga.gov.au/products/regulations-all-products/advertising/applying-advertising-code/mandatory-statements-and-other-information-required-advertising",
        "difficulty": "Medium", "tags": "fix,mandatory-disclosure,aust-l", "palette": ["#FFF4DF", "#8B4A16", "#F4A261"]
    },
    {
        "test_id": "AU-003", "title": "AUST L 强制声明齐全", "country": "Australia",
        "industry": "Beauty", "product_type": "Beauty supplement", "product_regulation": "AUST L Listed Medicine",
        "channel": "Instagram", "content_format": "Poster image", "content_origin": "Canva generated",
        "text_layer_available": True, "supporting_evidence": "ARTG indication supplied",
        "headline": "SUPPORTS IMMUNE HEALTH",
        "lines": ["Daily wellness support", "AUST L 345678"],
        "footer": "Always read the label and follow the directions for use",
        "poster_visible_text_gold": "SUPPORTS IMMUNE HEALTH | Daily wellness support | AUST L 345678 | Always read the label and follow the directions for use",
        "expected_status": "Ready to run", "expected_trigger": "Poster render completed",
        "expected_issue_type": "Checked and fine", "expected_flagged_text": "",
        "expected_missing_info": "", "expected_next_action": "Allow download, publish or continue",
        "expected_checked": "Australia law · Beauty · AUST L · Poster text",
        "expected_not_checked": "Platform policy · Non-text visual claims · Landing page",
        "knowledge_package": "AU-BEA-POSTER", "rule_version": "v1.0-demo",
        "gold_rationale": "The test claim is assumed consistent with supplied ARTG context and the mandatory statement is visible.",
        "source_url": "https://www.tga.gov.au/products/regulations-all-products/advertising/applying-advertising-code/mandatory-statements-and-other-information-required-advertising",
        "difficulty": "Medium", "tags": "ready,mandatory-disclosure,aust-l", "palette": ["#E7F2FF", "#164E8A", "#8EC5FC"]
    },
    {
        "test_id": "AU-004", "title": "监管身份不确定且含功效声称", "country": "Australia",
        "industry": "Beauty", "product_type": "Skin serum", "product_regulation": "Not sure",
        "channel": "Instagram", "content_format": "Poster image", "content_origin": "Canva generated",
        "text_layer_available": True, "supporting_evidence": "Not provided",
        "headline": "REPAIRS DAMAGED SKIN IN 7 DAYS",
        "lines": ["Clinically proven formula", "Visible renewal from within"], "footer": "DERMA RENEW SERUM",
        "poster_visible_text_gold": "REPAIRS DAMAGED SKIN IN 7 DAYS | Clinically proven formula | Visible renewal from within | DERMA RENEW SERUM",
        "expected_status": "Needs your input", "expected_trigger": "Poster render completed",
        "expected_issue_type": "Product classification required", "expected_flagged_text": "Repairs damaged skin in 7 days",
        "expected_missing_info": "Confirm Cosmetic or Therapeutic Good; provide claim evidence",
        "expected_next_action": "Ask for product regulation and supporting evidence",
        "expected_checked": "Australia law · Beauty · Poster text",
        "expected_not_checked": "Final product regulation rule set · Platform policy · Landing page",
        "knowledge_package": "AU-BEA-POSTER", "rule_version": "v1.0-demo",
        "gold_rationale": "The wording may cross the cosmetic and therapeutic boundary, so the system should ask rather than guess.",
        "source_url": "https://www.tga.gov.au/resources/guidance/determining-if-your-product-cosmetic-or-therapeutic-good",
        "difficulty": "Hard", "tags": "needs-input,classification,boundary", "palette": ["#F2EAFE", "#6331A5", "#C9A7EB"]
    },
    {
        "test_id": "AU-005", "title": "临床数据声称但未提供证据", "country": "Australia",
        "industry": "Beauty", "product_type": "Hydrating serum", "product_regulation": "Cosmetic",
        "channel": "Instagram", "content_format": "Poster image", "content_origin": "Canva generated",
        "text_layer_available": True, "supporting_evidence": "Not provided",
        "headline": "42% MORE HYDRATION",
        "lines": ["Clinically proven after one use", "Powered by hyaluronic acid"], "footer": "AQUA BOOST SERUM",
        "poster_visible_text_gold": "42% MORE HYDRATION | Clinically proven after one use | Powered by hyaluronic acid | AQUA BOOST SERUM",
        "expected_status": "Needs your input", "expected_trigger": "Poster render completed",
        "expected_issue_type": "Supporting evidence required", "expected_flagged_text": "42% more hydration; Clinically proven",
        "expected_missing_info": "Study or substantiation for the quantified clinical claim",
        "expected_next_action": "Upload or link supporting evidence, or remove the claim",
        "expected_checked": "Australia law · Beauty · Cosmetic · Poster text",
        "expected_not_checked": "Evidence validity until supplied · Platform policy · Landing page",
        "knowledge_package": "AU-BEA-POSTER", "rule_version": "v1.0-demo",
        "gold_rationale": "A quantified clinical representation cannot be verified without supporting evidence.",
        "source_url": "https://www.tga.gov.au/products/regulations-all-products/advertising/applying-advertising-code/general-requirements-advertising-therapeutic-goods-public",
        "difficulty": "Medium", "tags": "needs-input,evidence,clinical-claim", "palette": ["#E8FBFF", "#116B7B", "#69D2E7"]
    },
    {
        "test_id": "AU-006", "title": "化妆品出现治疗型声称", "country": "Australia",
        "industry": "Beauty", "product_type": "Body lotion", "product_regulation": "Cosmetic",
        "channel": "Instagram", "content_format": "Poster image", "content_origin": "Canva generated",
        "text_layer_available": True, "supporting_evidence": "Not applicable",
        "headline": "TREATS ECZEMA",
        "lines": ["Repairs damaged skin at the cellular level", "Fast relief from inflammation"], "footer": "CALM SKIN LOTION",
        "poster_visible_text_gold": "TREATS ECZEMA | Repairs damaged skin at the cellular level | Fast relief from inflammation | CALM SKIN LOTION",
        "expected_status": "Fix before running", "expected_trigger": "Poster render completed",
        "expected_issue_type": "Regulatory boundary trigger", "expected_flagged_text": "Treats eczema; Repairs damaged skin at the cellular level",
        "expected_missing_info": "", "expected_next_action": "Remove therapeutic wording or reclassify and re-check",
        "expected_checked": "Australia law · Beauty · Cosmetic · Poster text",
        "expected_not_checked": "Platform policy · Product registration validity · Landing page",
        "knowledge_package": "AU-BEA-POSTER", "rule_version": "v1.0-demo",
        "gold_rationale": "Disease treatment and cellular repair wording is inconsistent with a cosmetic-only context.",
        "source_url": "https://www.tga.gov.au/resources/guidance/determining-if-your-product-cosmetic-or-therapeutic-good",
        "difficulty": "Easy", "tags": "fix,boundary,therapeutic-claim", "palette": ["#FFF0F0", "#9C2430", "#E9858F"]
    },
    {
        "test_id": "AU-007", "title": "保证治愈与绝对功效", "country": "Australia",
        "industry": "Beauty", "product_type": "Skin treatment", "product_regulation": "AUST L Listed Medicine",
        "channel": "Instagram", "content_format": "Poster image", "content_origin": "Canva generated",
        "text_layer_available": True, "supporting_evidence": "ARTG context supplied",
        "headline": "GUARANTEED CURE",
        "lines": ["Works every time", "Zero risk. No side effects."], "footer": "AUST L 456789",
        "poster_visible_text_gold": "GUARANTEED CURE | Works every time | Zero risk. No side effects. | AUST L 456789",
        "expected_status": "Fix before running", "expected_trigger": "Poster render completed",
        "expected_issue_type": "Absolute or prohibited representation", "expected_flagged_text": "Guaranteed cure; Works every time; Zero risk; No side effects",
        "expected_missing_info": "", "expected_next_action": "Remove guarantee and safety absolutes, then re-check",
        "expected_checked": "Australia law · Beauty · AUST L · Poster text",
        "expected_not_checked": "Platform policy · Non-text visual claims · Landing page",
        "knowledge_package": "AU-BEA-POSTER", "rule_version": "v1.0-demo",
        "gold_rationale": "The poster represents the product as guaranteed, universally effective and without risk.",
        "source_url": "https://www.tga.gov.au/products/regulations-all-products/advertising/applying-advertising-code/general-requirements-advertising-therapeutic-goods-public",
        "difficulty": "Easy", "tags": "fix,guarantee,safety-absolute", "palette": ["#251D3A", "#FFFFFF", "#FF6B6B"]
    },
    {
        "test_id": "AU-008", "title": "成分与质地描述，正常放行", "country": "Australia",
        "industry": "Beauty", "product_type": "Face moisturiser", "product_regulation": "Cosmetic",
        "channel": "Instagram", "content_format": "Poster image", "content_origin": "Canva generated",
        "text_layer_available": True, "supporting_evidence": "Not required",
        "headline": "LIGHTWEIGHT EVERYDAY MOISTURISER",
        "lines": ["With niacinamide and vitamin E", "Silky texture. Fresh finish."], "footer": "NOVA SKIN",
        "poster_visible_text_gold": "LIGHTWEIGHT EVERYDAY MOISTURISER | With niacinamide and vitamin E | Silky texture. Fresh finish. | NOVA SKIN",
        "expected_status": "Ready to run", "expected_trigger": "Poster render completed",
        "expected_issue_type": "Checked and fine", "expected_flagged_text": "",
        "expected_missing_info": "", "expected_next_action": "Allow download, publish or continue",
        "expected_checked": "Australia law · Beauty · Cosmetic · Poster text",
        "expected_not_checked": "Platform policy · Non-text visual claims · Landing page",
        "knowledge_package": "AU-BEA-POSTER", "rule_version": "v1.0-demo",
        "gold_rationale": "The poster describes ingredients and sensory attributes without a therapeutic outcome claim.",
        "source_url": "https://www.tga.gov.au/resources/guidance/determining-if-your-product-cosmetic-or-therapeutic-good",
        "difficulty": "Easy", "tags": "ready,ingredient-claim,cosmetic", "palette": ["#F8F5EE", "#4F5B45", "#BEC9A9"]
    },
    {
        "test_id": "AU-009", "title": "国家不在当前知识包覆盖范围", "country": "New Zealand",
        "industry": "Beauty", "product_type": "Face cream", "product_regulation": "Cosmetic",
        "channel": "Instagram", "content_format": "Poster image", "content_origin": "Canva generated",
        "text_layer_available": True, "supporting_evidence": "Not provided",
        "headline": "SMOOTHER LOOKING SKIN",
        "lines": ["A daily botanical face cream", "Made for every morning"], "footer": "KIWI BLOOM",
        "poster_visible_text_gold": "SMOOTHER LOOKING SKIN | A daily botanical face cream | Made for every morning | KIWI BLOOM",
        "expected_status": "Outside scope", "expected_trigger": "Poster render completed",
        "expected_issue_type": "Coverage unavailable", "expected_flagged_text": "",
        "expected_missing_info": "Supported New Zealand knowledge package",
        "expected_next_action": "Show coverage limits; do not return a green conclusion",
        "expected_checked": "Poster text extracted",
        "expected_not_checked": "New Zealand law · Platform policy · Landing page",
        "knowledge_package": "None", "rule_version": "None",
        "gold_rationale": "The MVP knowledge package is Australia-only, so the system must not invent New Zealand rules.",
        "source_url": "", "difficulty": "Easy", "tags": "outside-scope,country,coverage", "palette": ["#ECEFF3", "#3F4B59", "#B8C2CC"]
    },
    {
        "test_id": "AU-010", "title": "缺少国家 Context", "country": "",
        "industry": "Beauty", "product_type": "Eye serum", "product_regulation": "Cosmetic",
        "channel": "Instagram", "content_format": "Poster image", "content_origin": "Canva generated",
        "text_layer_available": True, "supporting_evidence": "Not provided",
        "headline": "VISIBLE RESULTS IN 3 DAYS",
        "lines": ["A brighter look around the eyes", "Dermatologist tested"], "footer": "LUMINA EYE SERUM",
        "poster_visible_text_gold": "VISIBLE RESULTS IN 3 DAYS | A brighter look around the eyes | Dermatologist tested | LUMINA EYE SERUM",
        "expected_status": "Needs your input", "expected_trigger": "Poster render completed",
        "expected_issue_type": "Context missing", "expected_flagged_text": "Visible results in 3 days",
        "expected_missing_info": "Country",
        "expected_next_action": "Ask user to confirm country before applying rules",
        "expected_checked": "Poster text extracted · Beauty · Cosmetic",
        "expected_not_checked": "Country-specific law · Platform policy · Landing page",
        "knowledge_package": "Pending routing", "rule_version": "None",
        "gold_rationale": "Country is required for rule routing; the system should ask rather than infer Australia.",
        "source_url": "", "difficulty": "Medium", "tags": "needs-input,missing-context,country", "palette": ["#FFF8E8", "#6E5422", "#F4CD72"]
    },
    {
        "test_id": "AU-011", "title": "上传图片且 OCR 低置信", "country": "Australia",
        "industry": "Beauty", "product_type": "Anti-ageing cream", "product_regulation": "Cosmetic",
        "channel": "Instagram", "content_format": "Poster image", "content_origin": "Uploaded raster",
        "text_layer_available": False, "supporting_evidence": "Not provided",
        "headline": "NEW FORMULA",
        "lines": ["daily face cream"], "footer": "Visibly reduces wrinkles by 80% in 3 days",
        "poster_visible_text_gold": "NEW FORMULA | daily face cream | Visibly reduces wrinkles by 80% in 3 days",
        "expected_status": "Needs your input", "expected_trigger": "Image upload completed",
        "expected_issue_type": "OCR confidence too low", "expected_flagged_text": "Possible claim in low-contrast footer",
        "expected_missing_info": "Confirm or edit extracted poster text",
        "expected_next_action": "Show OCR uncertainty and request text confirmation",
        "expected_checked": "High-confidence poster text only",
        "expected_not_checked": "Low-confidence footer · Platform policy · Landing page",
        "knowledge_package": "AU-BEA-POSTER", "rule_version": "v1.0-demo",
        "gold_rationale": "The raster has no text layer and the claim is intentionally low contrast; the system must not silently ignore it.",
        "source_url": "", "difficulty": "Hard", "tags": "needs-input,ocr,low-confidence", "palette": ["#DDE1DF", "#60706A", "#CED3D0"], "low_contrast": True
    },
    {
        "test_id": "AU-012", "title": "强制声明存在但不可读", "country": "Australia",
        "industry": "Beauty", "product_type": "Beauty supplement", "product_regulation": "AUST L Listed Medicine",
        "channel": "Instagram", "content_format": "Poster image", "content_origin": "Canva generated",
        "text_layer_available": True, "supporting_evidence": "ARTG indication supplied",
        "headline": "SUPPORTS HEALTHY SKIN",
        "lines": ["Daily beauty support", "AUST L 567890"],
        "footer": "Always read the label and follow the directions for use",
        "poster_visible_text_gold": "SUPPORTS HEALTHY SKIN | Daily beauty support | AUST L 567890 | Always read the label and follow the directions for use",
        "expected_status": "Fix before running", "expected_trigger": "Poster render completed",
        "expected_issue_type": "Mandatory statement not prominent", "expected_flagged_text": "Always read the label and follow the directions for use",
        "expected_missing_info": "", "expected_next_action": "Increase disclosure size and contrast, then re-check",
        "expected_checked": "Australia law · Beauty · AUST L · Poster text",
        "expected_not_checked": "Platform policy · Non-text visual claims · Landing page",
        "knowledge_package": "AU-BEA-POSTER", "rule_version": "v1.0-demo",
        "gold_rationale": "The mandatory statement is technically present but intentionally too small and faint to be prominent.",
        "source_url": "https://www.tga.gov.au/products/regulations-all-products/advertising/applying-advertising-code/mandatory-statements-and-other-information-required-advertising",
        "difficulty": "Hard", "tags": "fix,legibility,mandatory-disclosure", "palette": ["#FFF2EA", "#7A3B2E", "#E6A88D"], "tiny_footer": True
    }
]

ZH_OVERRIDES = [
    {
        "test_id": "AU-ZH-001", "country": "澳大利亚", "industry": "美妆", "product_type": "面部保湿霜",
        "product_regulation": "化妆品", "channel": "Instagram", "content_format": "海报图片", "content_origin": "Canva 生成",
        "supporting_evidence": "无需提供", "headline": "我们团队最爱的配方",
        "lines": ["含烟酰胺与维生素 E", "温和呵护，适合日常使用"], "footer": "LUMEA 日常保湿霜",
        "expected_status": "可以发布", "expected_trigger": "海报渲染完成",
        "expected_issue_type": "已检查，无需修改", "expected_flagged_text": "", "expected_missing_info": "",
        "expected_next_action": "允许下载、发布或继续", "expected_checked": "澳大利亚法规 · 美妆 · 化妆品 · 海报文字",
        "expected_not_checked": "平台政策 · 非文字视觉声称 · 落地页",
        "gold_rationale": "在本测试 Context 下，团队偏好和成分描述没有表达治疗效果。",
        "difficulty": "简单", "tags": "可以发布,已检查无需修改,化妆品"
    },
    {
        "test_id": "AU-ZH-002", "country": "澳大利亚", "industry": "美妆", "product_type": "美容营养补充剂",
        "product_regulation": "AUST L 列名药品", "channel": "Instagram", "content_format": "海报图片", "content_origin": "Canva 生成",
        "supporting_evidence": "已提供 ARTG 适应症", "headline": "帮助维持免疫健康",
        "lines": ["每日健康支持", "AUST L 345678"], "footer": "VITAGLOW 免疫支持",
        "expected_status": "发布前需修改", "expected_trigger": "海报渲染完成",
        "expected_issue_type": "缺少强制声明", "expected_flagged_text": "广告缺少必要强制声明", "expected_missing_info": "",
        "expected_next_action": "补充阅读标签和遵循使用说明的声明，然后重新检测",
        "expected_checked": "澳大利亚法规 · 美妆 · AUST L · 海报文字", "expected_not_checked": "平台政策 · 非文字视觉声称 · 落地页",
        "gold_rationale": "列名药品海报缺少本 Demo 知识包要求的简短强制声明。",
        "difficulty": "中等", "tags": "发布前需修改,强制声明,AUST L"
    },
    {
        "test_id": "AU-ZH-003", "country": "澳大利亚", "industry": "美妆", "product_type": "美容营养补充剂",
        "product_regulation": "AUST L 列名药品", "channel": "Instagram", "content_format": "海报图片", "content_origin": "Canva 生成",
        "supporting_evidence": "已提供 ARTG 适应症", "headline": "帮助维持免疫健康",
        "lines": ["每日健康支持", "AUST L 345678"], "footer": "请务必阅读标签并遵循使用说明",
        "expected_status": "可以发布", "expected_trigger": "海报渲染完成",
        "expected_issue_type": "已检查，无需修改", "expected_flagged_text": "", "expected_missing_info": "",
        "expected_next_action": "允许下载、发布或继续", "expected_checked": "澳大利亚法规 · 美妆 · AUST L · 海报文字",
        "expected_not_checked": "平台政策 · 非文字视觉声称 · 落地页",
        "gold_rationale": "假设健康声称与提供的 ARTG Context 一致，且强制声明清晰可见。",
        "difficulty": "中等", "tags": "可以发布,强制声明,AUST L"
    },
    {
        "test_id": "AU-ZH-004", "country": "澳大利亚", "industry": "美妆", "product_type": "护肤精华",
        "product_regulation": "不确定", "channel": "Instagram", "content_format": "海报图片", "content_origin": "Canva 生成",
        "supporting_evidence": "未提供", "headline": "7天修护受损肌肤",
        "lines": ["临床验证配方", "由内焕新肌肤"], "footer": "DERMA 焕新精华",
        "expected_status": "需要你补充信息", "expected_trigger": "海报渲染完成",
        "expected_issue_type": "需要确认产品监管身份", "expected_flagged_text": "7天修护受损肌肤",
        "expected_missing_info": "确认属于化妆品还是治疗用品，并提供声称证据",
        "expected_next_action": "询问产品监管身份和 supporting evidence",
        "expected_checked": "澳大利亚法规 · 美妆 · 海报文字", "expected_not_checked": "最终产品监管规则集 · 平台政策 · 落地页",
        "gold_rationale": "该表述可能跨越化妆品与治疗用品边界，系统应先询问而不是猜测。",
        "difficulty": "困难", "tags": "需要补充信息,产品分类,监管边界"
    },
    {
        "test_id": "AU-ZH-005", "country": "澳大利亚", "industry": "美妆", "product_type": "保湿精华",
        "product_regulation": "化妆品", "channel": "Instagram", "content_format": "海报图片", "content_origin": "Canva 生成",
        "supporting_evidence": "未提供", "headline": "保湿度提升42%",
        "lines": ["一次使用后经临床验证", "透明质酸配方"], "footer": "AQUA BOOST 保湿精华",
        "expected_status": "需要你补充信息", "expected_trigger": "海报渲染完成",
        "expected_issue_type": "需要 supporting evidence", "expected_flagged_text": "保湿度提升42%；经临床验证",
        "expected_missing_info": "量化临床声称对应的研究或证明材料",
        "expected_next_action": "上传 supporting evidence，或删除该声称",
        "expected_checked": "澳大利亚法规 · 美妆 · 化妆品 · 海报文字", "expected_not_checked": "证据有效性 · 平台政策 · 落地页",
        "gold_rationale": "缺少 supporting evidence 时无法验证量化临床声称。",
        "difficulty": "中等", "tags": "需要补充信息,证据,临床声称"
    },
    {
        "test_id": "AU-ZH-006", "country": "澳大利亚", "industry": "美妆", "product_type": "身体乳",
        "product_regulation": "化妆品", "channel": "Instagram", "content_format": "海报图片", "content_origin": "Canva 生成",
        "supporting_evidence": "不适用", "headline": "治疗湿疹",
        "lines": ["在细胞层面修复受损肌肤", "快速缓解炎症"], "footer": "CALM SKIN 身体乳",
        "expected_status": "发布前需修改", "expected_trigger": "海报渲染完成",
        "expected_issue_type": "监管边界触发", "expected_flagged_text": "治疗湿疹；在细胞层面修复受损肌肤",
        "expected_missing_info": "", "expected_next_action": "删除治疗型表述，或重新分类后检测",
        "expected_checked": "澳大利亚法规 · 美妆 · 化妆品 · 海报文字", "expected_not_checked": "平台政策 · 产品注册有效性 · 落地页",
        "gold_rationale": "疾病治疗和细胞修复表述与化妆品 Context 不一致。",
        "difficulty": "简单", "tags": "发布前需修改,监管边界,治疗型声称"
    },
    {
        "test_id": "AU-ZH-007", "country": "澳大利亚", "industry": "美妆", "product_type": "皮肤治疗产品",
        "product_regulation": "AUST L 列名药品", "channel": "Instagram", "content_format": "海报图片", "content_origin": "Canva 生成",
        "supporting_evidence": "已提供 ARTG Context", "headline": "保证治愈",
        "lines": ["每次都有效", "零风险，无任何副作用"], "footer": "AUST L 456789",
        "expected_status": "发布前需修改", "expected_trigger": "海报渲染完成",
        "expected_issue_type": "绝对化或禁止性表述", "expected_flagged_text": "保证治愈；每次都有效；零风险；无任何副作用",
        "expected_missing_info": "", "expected_next_action": "删除保证性和绝对安全表述，然后重新检测",
        "expected_checked": "澳大利亚法规 · 美妆 · AUST L · 海报文字", "expected_not_checked": "平台政策 · 非文字视觉声称 · 落地页",
        "gold_rationale": "海报将产品表述为保证治愈、始终有效且没有风险。",
        "difficulty": "简单", "tags": "发布前需修改,保证性声称,绝对安全"
    },
    {
        "test_id": "AU-ZH-008", "country": "澳大利亚", "industry": "美妆", "product_type": "面部保湿霜",
        "product_regulation": "化妆品", "channel": "Instagram", "content_format": "海报图片", "content_origin": "Canva 生成",
        "supporting_evidence": "无需提供", "headline": "轻盈日常保湿霜",
        "lines": ["含烟酰胺与维生素 E", "丝滑质地，清爽肤感"], "footer": "NOVA SKIN",
        "expected_status": "可以发布", "expected_trigger": "海报渲染完成",
        "expected_issue_type": "已检查，无需修改", "expected_flagged_text": "", "expected_missing_info": "",
        "expected_next_action": "允许下载、发布或继续", "expected_checked": "澳大利亚法规 · 美妆 · 化妆品 · 海报文字",
        "expected_not_checked": "平台政策 · 非文字视觉声称 · 落地页",
        "gold_rationale": "海报仅描述成分、质地和肤感，没有表达治疗效果。",
        "difficulty": "简单", "tags": "可以发布,成分描述,化妆品"
    },
    {
        "test_id": "AU-ZH-009", "country": "新西兰", "industry": "美妆", "product_type": "面霜",
        "product_regulation": "化妆品", "channel": "Instagram", "content_format": "海报图片", "content_origin": "Canva 生成",
        "supporting_evidence": "未提供", "headline": "肌肤看起来更平滑",
        "lines": ["每日植物面霜", "开启清新早晨"], "footer": "KIWI BLOOM",
        "expected_status": "不在覆盖范围", "expected_trigger": "海报渲染完成",
        "expected_issue_type": "缺少对应知识覆盖", "expected_flagged_text": "", "expected_missing_info": "新西兰知识包",
        "expected_next_action": "展示覆盖限制，不得返回绿色结论",
        "expected_checked": "已提取海报文字", "expected_not_checked": "新西兰法规 · 平台政策 · 落地页",
        "knowledge_package": "无", "rule_version": "无",
        "gold_rationale": "当前 MVP 知识包仅覆盖澳大利亚，系统不得自行生成新西兰规则。",
        "difficulty": "简单", "tags": "不在覆盖范围,国家,知识覆盖"
    },
    {
        "test_id": "AU-ZH-010", "country": "", "industry": "美妆", "product_type": "眼部精华",
        "product_regulation": "化妆品", "channel": "Instagram", "content_format": "海报图片", "content_origin": "Canva 生成",
        "supporting_evidence": "未提供", "headline": "3天可见效果",
        "lines": ["眼周看起来更加明亮", "经皮肤科测试"], "footer": "LUMINA 眼部精华",
        "expected_status": "需要你补充信息", "expected_trigger": "海报渲染完成",
        "expected_issue_type": "Context 缺失", "expected_flagged_text": "3天可见效果", "expected_missing_info": "国家",
        "expected_next_action": "应用规则前询问用户确认国家",
        "expected_checked": "已提取海报文字 · 美妆 · 化妆品", "expected_not_checked": "国家法规 · 平台政策 · 落地页",
        "knowledge_package": "等待路由", "rule_version": "无",
        "gold_rationale": "国家是知识路由的必要字段，系统不应默认推断为澳大利亚。",
        "difficulty": "中等", "tags": "需要补充信息,Context缺失,国家"
    },
    {
        "test_id": "AU-ZH-011", "country": "澳大利亚", "industry": "美妆", "product_type": "抗老面霜",
        "product_regulation": "化妆品", "channel": "Instagram", "content_format": "海报图片", "content_origin": "上传位图",
        "supporting_evidence": "未提供", "headline": "全新配方", "lines": ["日常面霜"], "footer": "3天淡化80%皱纹",
        "expected_status": "需要你补充信息", "expected_trigger": "图片上传完成",
        "expected_issue_type": "OCR 置信度过低", "expected_flagged_text": "低对比度页脚中可能存在功效声称",
        "expected_missing_info": "确认或编辑系统提取出的海报文字", "expected_next_action": "展示 OCR 不确定性并请求确认文字",
        "expected_checked": "仅检查高置信海报文字", "expected_not_checked": "低置信页脚 · 平台政策 · 落地页",
        "gold_rationale": "上传位图没有文字图层，功效声称被设计为低对比度，系统不得静默忽略。",
        "difficulty": "困难", "tags": "需要补充信息,OCR,低置信"
    },
    {
        "test_id": "AU-ZH-012", "country": "澳大利亚", "industry": "美妆", "product_type": "美容营养补充剂",
        "product_regulation": "AUST L 列名药品", "channel": "Instagram", "content_format": "海报图片", "content_origin": "Canva 生成",
        "supporting_evidence": "已提供 ARTG 适应症", "headline": "帮助维持健康肌肤",
        "lines": ["每日美丽支持", "AUST L 567890"], "footer": "请务必阅读标签并遵循使用说明",
        "expected_status": "发布前需修改", "expected_trigger": "海报渲染完成",
        "expected_issue_type": "强制声明不够醒目", "expected_flagged_text": "请务必阅读标签并遵循使用说明",
        "expected_missing_info": "", "expected_next_action": "提高声明字号和对比度，然后重新检测",
        "expected_checked": "澳大利亚法规 · 美妆 · AUST L · 海报文字", "expected_not_checked": "平台政策 · 非文字视觉声称 · 落地页",
        "gold_rationale": "强制声明虽然存在，但被刻意设置得过小、过淡，不够醒目。",
        "difficulty": "困难", "tags": "发布前需修改,可读性,强制声明"
    }
]

for case, override in zip(CASES, ZH_OVERRIDES):
    case.update(override)
    case["poster_visible_text_gold"] = " | ".join([case["headline"], *case["lines"], case["footer"]])

def fit_center(draw, text, font, y, fill, max_width=900):
    current = font
    while draw.textbbox((0, 0), text, font=current)[2] > max_width and current.size > 24:
        current = ImageFont.truetype(BOLD if font == FONT_H1 else REG, current.size - 2)
    box = draw.textbbox((0, 0), text, font=current)
    draw.text(((1080 - (box[2] - box[0])) / 2, y), text, font=current, fill=fill)

def draw_poster(case):
    bg, ink, accent = case["palette"]
    image = Image.new("RGB", (1080, 1350), bg)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((70, 70, 1010, 1280), radius=44, outline=accent, width=4)
    draw.ellipse((690, 115, 1040, 465), fill=accent)
    draw.ellipse((755, 170, 975, 390), fill=bg)
    draw.rounded_rectangle((150, 650, 430, 1115), radius=55, fill=accent)
    draw.rounded_rectangle((190, 575, 390, 730), radius=35, fill=ink)
    draw.rectangle((230, 540, 350, 605), fill=ink)
    draw.ellipse((520, 810, 925, 1215), outline=accent, width=12)
    draw.ellipse((610, 900, 835, 1125), fill=accent)
    fit_center(draw, case["headline"], FONT_H1, 150, ink)
    y = 300
    for line in case["lines"]:
        fit_center(draw, line, FONT_BODY, y, ink)
        y += 55
    draw.text((100, 90), case["test_id"], font=FONT_SMALL, fill=ink)
    if case.get("low_contrast"):
        draw.text((700, 1250), case["footer"], font=FONT_TINY, fill="#D2D6D3")
    elif case.get("tiny_footer"):
        font = ImageFont.truetype(REG, 11)
        box = draw.textbbox((0, 0), case["footer"], font=font)
        draw.text(((1080 - (box[2] - box[0])) / 2, 1242), case["footer"], font=font, fill="#E2CFC7")
    else:
        fit_center(draw, case["footer"], FONT_SMALL, 1230, ink, 880)
    image.save(IMG_DIR / f'{case["test_id"]}.png', optimize=True)

for case in CASES:
    draw_poster(case)
    case["image_file"] = f'images/{case["test_id"]}.png'

# Quick visual QA/contact sheet for reviewers.
thumb_w, thumb_h = 270, 338
contact = Image.new("RGB", (thumb_w * 4, (thumb_h + 58) * 3), "#FFFFFF")
contact_draw = ImageDraw.Draw(contact)
label_font = ImageFont.truetype(BOLD, 18)
for idx, case in enumerate(CASES):
    x = (idx % 4) * thumb_w
    y = (idx // 4) * (thumb_h + 58)
    poster = Image.open(IMG_DIR / f'{case["test_id"]}.png').resize((thumb_w, thumb_h))
    contact.paste(poster, (x, y))
    contact_draw.rectangle((x, y + thumb_h, x + thumb_w, y + thumb_h + 58), fill="#F4F0FF")
    label = f'{case["test_id"]}  {case["expected_status"]}'
    contact_draw.text((x + 10, y + thumb_h + 17), label, font=label_font, fill="#5B23B8")
contact.save(OUT / "poster_contact_sheet.png", optimize=True)

with (OUT / "manifest.json").open("w", encoding="utf-8") as f:
    json.dump(CASES, f, ensure_ascii=False, indent=2)

print(f"Created {len(CASES)} posters in {IMG_DIR}")
