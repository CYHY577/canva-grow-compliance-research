import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const outputDir = String.raw`C:\Users\pc\Desktop\canva测试\outputs\canva_single_table_eval`;
await fs.mkdir(outputDir, { recursive: true });

const headers = ["编号", "测试目的", "能力层级", "输入类型", "输入内容", "期待结果", "真实生成结果", "是否通过", "问题说明"];
const rows = [
  [
    "TC-001", "验证系统能识别无明确问题的化妆品海报，并正确放行", "L4 合规判断",
    "生成海报＋审核 Context",
    "海报文字：我们团队最爱的配方；含烟酰胺与维生素E；温和呵护，适合日常使用。\nContext：澳大利亚／美妆／化妆品／Instagram／海报图片。",
    "状态：可以发布。\n说明：在已检查范围内未发现需要修改的问题。\n已检查：澳大利亚法规、美妆、化妆品、海报文字。\n下一步：允许下载、发布或继续。",
    "首轮模型路由返回 Unable to verify / NO_SUPPORTED_PACKAGE，而旧规则面板同时显示 Ready to run；相同输入复测只显示 Ready to run 并允许 Continue。", "未通过", "相同用例结果不稳定，且首轮出现互相矛盾的发布状态；当前页面也没有海报上传或 OCR 入口。截图记录复测结果：screenshots/TC-001.png"
  ],
  [
    "TC-002", "验证 AUST L 海报缺少强制声明时能够阻止发布", "L3 规则匹配",
    "生成海报＋审核 Context",
    "海报文字：帮助维持免疫健康；每日健康支持；AUST L 345678。\nContext：澳大利亚／美妆／AUST L 列名药品／Instagram／海报图片。",
    "状态：发布前需修改。\n问题：缺少必要强制声明。\n标记：广告缺少“请务必阅读标签并遵循使用说明”。\n下一步：补充声明后自动重新检测。",
    "以页面现有 Text 入口检测后返回 Fix before running，识别到缺少 Always read the label，并禁用 Continue。切换为 Image 时则直接返回 Unable to verify。", "部分通过", "强制声明缺失规则可在文本入口触发，但真实海报图片仍不在覆盖范围。截图：screenshots/TC-002.png"
  ],
  [
    "TC-003", "验证强制声明完整且清晰时系统不会误拦截", "L4 合规判断",
    "生成海报＋审核 Context",
    "海报文字：帮助维持免疫健康；每日健康支持；AUST L 345678；请务必阅读标签并遵循使用说明。\nContext：澳大利亚／美妆／AUST L 列名药品／Instagram／海报图片。",
    "状态：可以发布。\n说明：强制声明已出现且清晰可读；当前声称假设与提供的 ARTG Context 一致。\n下一步：允许下载、发布或继续。",
    "返回 Fix before running，仍判断缺少 Always read the label；未识别中文等义声明“请务必阅读标签并遵循使用说明”。", "未通过", "中文强制声明被误判为缺失，存在本地化和等义表达识别缺口。截图：screenshots/TC-003.png"
  ],
  [
    "TC-004", "验证监管身份不确定时系统先询问而不是自行判断", "L2 Context 理解",
    "生成海报＋不完整 Context",
    "海报文字：7天修护受损肌肤；临床验证配方；由内焕新肌肤。\nContext：澳大利亚／美妆／产品监管身份“不确定”／Instagram／海报图片。",
    "状态：需要你补充信息。\n问题：该功效声称可能跨越化妆品与治疗用品边界。\n缺失信息：产品监管身份及 supporting evidence。\n下一步：要求用户确认后再检测。",
    "以 Text 入口检测后返回 Needs your input，并要求选择 Cosmetic 或 AUST L Listed Medicine；Continue 被禁用。", "部分通过", "Ask-don't-guess 第三态和发布阻断正确，但只能通过文本入口验证，未完成海报 OCR 检测。截图：screenshots/TC-004.png"
  ],
  [
    "TC-005", "验证量化临床声称缺少证据时进入信息补充状态", "L3 证据判断",
    "生成海报＋审核 Context",
    "海报文字：保湿度提升42%；一次使用后经临床验证；透明质酸配方。\nContext：澳大利亚／美妆／化妆品／Instagram／海报图片；未提供 supporting evidence。",
    "状态：需要你补充信息。\n问题：量化临床声称缺少 supporting evidence。\n标记：保湿度提升42%、经临床验证。\n下一步：上传证据或删除该声称，然后重新检测。",
    "返回 Ready to run，显示 No clear issue found，并允许 Continue with this copy。", "未通过", "漏检“保湿度提升42%”和“经临床验证”的证据依赖，未进入 Needs your input。截图：screenshots/TC-005.png"
  ],
  [
    "TC-006", "验证化妆品出现疾病治疗声称时触发监管边界规则", "L4 监管边界判断",
    "生成海报＋审核 Context",
    "海报文字：治疗湿疹；在细胞层面修复受损肌肤；快速缓解炎症。\nContext：澳大利亚／美妆／化妆品／Instagram／海报图片。",
    "状态：发布前需修改。\n问题：化妆品 Context 出现治疗疾病和生理修复声称。\n标记：治疗湿疹、在细胞层面修复受损肌肤。\n下一步：删除治疗型表述，或重新分类后检测。",
    "返回 Ready to run，显示 No clear issue found，并允许 Continue with this copy。", "未通过", "漏检“治疗湿疹”“修复受损肌肤”“缓解炎症”等治疗性声称，监管边界触发器未生效。截图：screenshots/TC-006.png"
  ],
  [
    "TC-007", "验证保证治愈、始终有效和绝对安全表述能够被识别", "L4 合规判断",
    "生成海报＋审核 Context",
    "海报文字：保证治愈；每次都有效；零风险，无任何副作用；AUST L 456789。\nContext：澳大利亚／美妆／AUST L 列名药品／Instagram／海报图片。",
    "状态：发布前需修改。\n问题：存在保证性、绝对功效及绝对安全表述。\n标记：保证治愈、每次都有效、零风险、无任何副作用。\n下一步：删除相关表述后重新检测。",
    "返回 Fix before running，但唯一 finding 是缺少 Always read the label；未标记保证治愈、每次有效、零风险、无副作用。", "部分通过", "发布被阻止，但命中原因不完整，保证性和绝对安全声称仍然漏检。截图：screenshots/TC-007.png"
  ],
  [
    "TC-008", "验证当前知识包不覆盖目标国家时不生成绿色结论", "L2 覆盖范围判断",
    "生成海报＋范围外 Context",
    "海报文字：肌肤看起来更平滑；每日植物面霜；开启清新早晨。\nContext：新西兰／美妆／化妆品／Instagram／海报图片。\n当前知识包：仅覆盖澳大利亚。",
    "状态：不在覆盖范围。\n说明：当前没有对应的新西兰知识包，本次未完成法规检查。\n下一步：展示覆盖范围；不得显示“可以发布”或其他绿色结论。",
    "返回 Unable to verify / This content is outside the current coverage，并提示当前 MVP 仅覆盖 Australia + Beauty + Text；Continue 被禁用。", "通过", "正确执行覆盖范围 Gate，没有给出绿色结论。截图：screenshots/TC-008.png"
  ],
  [
    "TC-009", "验证上传位图 OCR 低置信时不会静默漏检小字功效声称", "L1 文字识别",
    "上传海报位图＋审核 Context",
    "海报主体文字：全新配方；日常面霜。\n低对比度小字：3天淡化80%皱纹。\nContext：澳大利亚／美妆／化妆品／Instagram／上传位图；无文字图层。",
    "状态：需要你补充信息。\n问题：OCR 无法可靠读取低对比度页脚。\n未检查：低置信小字区域。\n下一步：展示 OCR 不确定性，请用户确认或编辑提取文字。",
    "选择 Image 后直接返回 Unable to verify；页面没有图片上传、OCR 结果或低置信区域确认入口。", "未通过", "无法执行位图 OCR 低置信测试，当前站点实际上只支持文本输入。截图：screenshots/TC-009.png"
  ],
  [
    "TC-010", "验证强制声明虽然存在但过小、过淡时仍需修改", "L5 视觉可读性与发布 Gate",
    "生成海报＋审核 Context",
    "海报主体文字：帮助维持健康肌肤；每日美丽支持；AUST L 567890。\n海报底部以极小浅色文字显示：请务必阅读标签并遵循使用说明。\nContext：澳大利亚／美妆／AUST L 列名药品／Instagram／海报图片。",
    "状态：发布前需修改。\n问题：强制声明技术上存在，但不够醒目、难以阅读。\n下一步：提高声明字号和对比度，更新海报后自动重新检测。",
    "选择 Image 后直接返回 Unable to verify；系统没有读取海报字号、颜色、对比度和版面位置。", "未通过", "无法验证强制声明的视觉可读性，缺少海报视觉解析能力。截图：screenshots/TC-010.png"
  ]
];

const workbook = Workbook.create();
const sheet = workbook.worksheets.add("测评集");
sheet.showGridLines = false;
sheet.getRange("A1:I11").values = [headers, ...rows];

sheet.getRange("A1:I1").format = {
  fill: "#165DCC",
  font: { bold: true, color: "#FFFFFF", size: 11, name: "Microsoft YaHei" },
  horizontalAlignment: "center",
  verticalAlignment: "center",
  wrapText: true,
  borders: { preset: "all", style: "thin", color: "#FFFFFF" }
};
sheet.getRange("A1:I1").format.rowHeight = 36;

sheet.getRange("A2:I11").format = {
  font: { color: "#1F2430", size: 10, name: "Microsoft YaHei" },
  verticalAlignment: "top",
  wrapText: true,
  borders: {
    insideHorizontal: { style: "thin", color: "#D9E2F0" },
    insideVertical: { style: "thin", color: "#E7ECF3" },
    bottom: { style: "thin", color: "#B9C7DA" }
  }
};
for (let row = 2; row <= 11; row++) {
  sheet.getRange(`A${row}:I${row}`).format.fill = row % 2 === 0 ? "#F4F8FF" : "#FFFFFF";
}

sheet.getRange("A:A").format.columnWidth = 11;
sheet.getRange("B:B").format.columnWidth = 31;
sheet.getRange("C:C").format.columnWidth = 22;
sheet.getRange("D:D").format.columnWidth = 25;
sheet.getRange("E:E").format.columnWidth = 55;
sheet.getRange("F:F").format.columnWidth = 58;
sheet.getRange("G:G").format.columnWidth = 48;
sheet.getRange("H:H").format.columnWidth = 14;
sheet.getRange("I:I").format.columnWidth = 34;
sheet.getRange("A2:I11").format.rowHeight = 138;
sheet.getRange("A2:D11").format.horizontalAlignment = "center";
sheet.getRange("A2:D11").format.verticalAlignment = "center";
sheet.getRange("H2:H11").format.fill = "#FFF4D8";
sheet.getRange("G2:G11").format.fill = "#FFF9E8";
sheet.getRange("I2:I11").format.fill = "#FFF9E8";
sheet.getRange("H2:H11").dataValidation = { rule: { type: "list", values: ["通过", "未通过", "部分通过"] } };
for (const row of [2, 4, 6, 7, 10, 11]) {
  sheet.getRange(`H${row}`).format = { fill: "#FCE9E6", font: { color: "#C53A2A", bold: true } };
}
for (const row of [3, 5, 8]) {
  sheet.getRange(`H${row}`).format = { fill: "#FFF4D8", font: { color: "#A66A00", bold: true } };
}
sheet.getRange("H9").format = { fill: "#E6F5EC", font: { color: "#18864B", bold: true } };
sheet.freezePanes.freezeRows(1);
sheet.freezePanes.freezeColumns(2);
const table = sheet.tables.add("A1:I11", true, "ComplianceEvaluationSet");
table.showBandedColumns = false;
table.showFilterButton = true;

const check = await workbook.inspect({ kind: "table", range: "测评集!A1:I11", include: "values,formulas", tableMaxRows: 15, tableMaxCols: 12 });
console.log(check.ndjson);
const errors = await workbook.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A", options: { useRegex: true, maxResults: 100 }, summary: "公式错误扫描" });
console.log(errors.ndjson);

const preview = await workbook.render({ sheetName: "测评集", autoCrop: "all", scale: 1, format: "png" });
await fs.writeFile(path.join(outputDir, "真实测评集预览.png"), new Uint8Array(await preview.arrayBuffer()));
const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(path.join(outputDir, "Canva_AI_海报文字合规审核_10条真实测评完成.xlsx"));
console.log(path.join(outputDir, "Canva_AI_海报文字合规审核_10条真实测评完成.xlsx"));
