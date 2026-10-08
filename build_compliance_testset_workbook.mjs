import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const root = String.raw`C:\Users\pc\Desktop\canva测试`;
const outputDir = path.join(root, "outputs", "canva_poster_compliance_testset_zh");
const previewDir = path.join(outputDir, "previews");
const cases = JSON.parse(await fs.readFile(path.join(outputDir, "manifest.json"), "utf8"));
await fs.mkdir(previewDir, { recursive: true });

const wb = Workbook.create();
const guide = wb.worksheets.add("使用说明");
const tests = wb.worksheets.add("测试用例");
const results = wb.worksheets.add("评测结果");
const posters = wb.worksheets.add("海报索引");

const navy = "#0E1B3D";
const purple = "#7D2AE8";
const lightPurple = "#F3ECFF";
const blue = "#0A5ACD";
const lightBlue = "#EAF3FF";
const green = "#18864B";
const lightGreen = "#E7F6EC";
const red = "#C53A2A";
const lightRed = "#FCE9E6";
const amber = "#A66A00";
const lightAmber = "#FFF4D8";
const gray = "#5E6472";
const lightGray = "#EEF0F3";
const border = "#D8DEE9";

function titleBand(sheet, title, subtitle, lastCol) {
  sheet.mergeCells(`A1:${lastCol}1`);
  sheet.getRange("A1").values = [[title]];
  sheet.getRange(`A1:${lastCol}1`).format = {
    fill: navy,
    font: { bold: true, color: "#FFFFFF", size: 18 },
    verticalAlignment: "center",
  };
  sheet.getRange(`A1:${lastCol}1`).format.rowHeight = 34;
  sheet.mergeCells(`A2:${lastCol}2`);
  sheet.getRange("A2").values = [[subtitle]];
  sheet.getRange(`A2:${lastCol}2`).format = {
    fill: "#F7F8FB",
    font: { color: gray, size: 10 },
    verticalAlignment: "center",
  };
  sheet.getRange(`A2:${lastCol}2`).format.rowHeight = 27;
}

for (const sheet of [guide, tests, results, posters]) sheet.showGridLines = false;

// 使用说明
titleBand(guide, "Canva AI 海报文字合规审核｜中文小型测评集", "12 个端到端标准答案用例：审核对象是生成或上传海报中的可见文字，不审核用户提示词。", "H");
guide.getRange("A4:H4").values = [["数据集范围", "澳大利亚", "行业", "美妆", "内容格式", "海报图片", "用例数", cases.length]];
guide.getRange("A4:H4").format = { fill: lightBlue, font: { bold: true, color: navy }, borders: { preset: "outside", style: "thin", color: border } };
guide.getRange("A6:B6").merge(); guide.getRange("C6:D6").merge(); guide.getRange("E6:F6").merge(); guide.getRange("G6:H6").merge();
guide.getRange("A6").values = [["可以发布"]];
guide.getRange("C6").values = [["发布前需修改"]];
guide.getRange("E6").values = [["需要你补充信息"]];
guide.getRange("G6").values = [["不在覆盖范围"]];
guide.getRange("A7:B8").merge(); guide.getRange("C7:D8").merge(); guide.getRange("E7:F8").merge(); guide.getRange("G7:H8").merge();
guide.getRange("A7").formulas = [["=COUNTIF('测试用例'!$N$5:$N$16,\"可以发布\")"]];
guide.getRange("C7").formulas = [["=COUNTIF('测试用例'!$N$5:$N$16,\"发布前需修改\")"]];
guide.getRange("E7").formulas = [["=COUNTIF('测试用例'!$N$5:$N$16,\"需要你补充信息\")"]];
guide.getRange("G7").formulas = [["=COUNTIF('测试用例'!$N$5:$N$16,\"不在覆盖范围\")"]];
const cards = [
  ["A6:B8", lightGreen, green], ["C6:D8", lightRed, red], ["E6:F8", lightAmber, amber], ["G6:H8", lightGray, gray]
];
for (const [range, fill, color] of cards) guide.getRange(range).format = { fill, font: { bold: true, color }, horizontalAlignment: "center", verticalAlignment: "center", borders: { preset: "outside", style: "thin", color } };
guide.getRange("A7:H8").format.font = { bold: true, size: 22 };
guide.getRange("A10:H10").merge();
guide.getRange("A10").values = [["如何使用"]];
guide.getRange("A10:H10").format = { fill: purple, font: { bold: true, color: "#FFFFFF" } };
const instructions = [
  ["1", "从 images 文件夹读取海报图片，并将同一行审核上下文一起发送给模型。"],
  ["2", "要求模型返回：提取文字、状态、问题类型、标记片段、缺失信息和下一步操作。"],
  ["3", "把模型实际输出填写到“评测结果”黄色输入列，得分列会自动比较；OCR 关键文本采用人工 0/1 评分。"],
  ["4", "内容或 Context 改变后必须重新检测；应用改写本身不等于通过。"],
  ["5", "测评集用于产品与模型验证，不替代法律意见；上线前由合规负责人复核标准答案标签。"],
];
guide.getRange("A11:H15").values = instructions.map(([n, text]) => [n, text, "", "", "", "", "", ""]);
for (let r = 11; r <= 15; r++) guide.mergeCells(`B${r}:H${r}`);
guide.getRange("A11:A15").format = { fill: lightPurple, font: { bold: true, color: purple }, horizontalAlignment: "center", verticalAlignment: "center" };
guide.getRange("B11:H15").format = { wrapText: true, verticalAlignment: "center", borders: { preset: "inside", style: "thin", color: border } };
guide.getRange("A17:H17").merge();
guide.getRange("A17").values = [["覆盖说明与依据"]];
guide.getRange("A17:H17").format = { fill: blue, font: { bold: true, color: "#FFFFFF" } };
guide.getRange("A18:H21").values = [
  ["已检查", "澳大利亚法规 · 美妆 · 产品监管身份 · 海报文字", "", "", "", "", "", ""],
  ["默认未检查", "平台政策 · 非文字视觉声称 · 落地页", "", "", "", "", "", ""],
  ["主要依据 1", "TGA：如何区分化妆品与治疗用品", "", "", "", "", "", ""],
  ["主要依据 2", "TGA：强制声明与广告一般要求", "", "", "", "", "", ""],
];
for (let r = 18; r <= 21; r++) guide.mergeCells(`B${r}:H${r}`);
guide.getRange("A18:A21").format = { font: { bold: true, color: navy }, fill: "#F7F8FB" };
guide.getRange("B18:H21").format = { wrapText: true };
guide.getRange("A1:H21").format.font.name = "Aptos";
guide.getRange("A1:H21").format.verticalAlignment = "center";
guide.getRange("A:A").format.columnWidth = 15;
guide.getRange("B:H").format.columnWidth = 17;
guide.getRange("B11:H15").format.rowHeight = 34;

// 测试用例
titleBand(tests, "标准答案测试用例", "一行一个中文海报案例；预期字段用于模型判定对照，来源链接用于规则复核。", "AA");
const headers = ["test_id","title","image_file","country","industry","product_type","product_regulation","channel","content_format","content_origin","text_layer_available","supporting_evidence","poster_visible_text_gold","expected_status","expected_trigger","expected_issue_type","expected_flagged_text","expected_missing_info","expected_next_action","expected_checked","expected_not_checked","knowledge_package","rule_version","gold_rationale","source_url","difficulty","tags"];
const headerLabels = ["用例编号","用例名称","图片文件","国家/地区","行业","产品类型","产品监管身份","渠道","内容格式","内容来源","是否有文字图层","证明材料","海报可见文字标准答案","预期状态","预期触发方式","预期问题类型","预期标记片段","预期缺失信息","预期下一步操作","已检查范围","未检查范围","知识包","规则版本","标准答案理由","规则来源链接","难度","标签"];
tests.getRange("A4:AA4").values = [headerLabels];
const rows = cases.map(c => headers.map(h => c[h] ?? ""));
tests.getRange(`A5:AA${4 + rows.length}`).values = rows;
tests.getRange("A4:AA4").format = { fill: blue, font: { bold: true, color: "#FFFFFF" }, wrapText: true, verticalAlignment: "center" };
tests.getRange(`A5:AA${4 + rows.length}`).format = { font: { size: 9 }, verticalAlignment: "top", wrapText: true };
tests.getRange(`A4:AA${4 + rows.length}`).format.borders = { insideHorizontal: { style: "thin", color: "#E4E8EF" }, bottom: { style: "thin", color: border } };
tests.getRange("A:A").format.columnWidth = 11;
tests.getRange("B:B").format.columnWidth = 24;
tests.getRange("C:C").format.columnWidth = 24;
tests.getRange("D:L").format.columnWidth = 18;
tests.getRange("M:M").format.columnWidth = 42;
tests.getRange("N:N").format.columnWidth = 20;
tests.getRange("O:W").format.columnWidth = 28;
tests.getRange("X:X").format.columnWidth = 48;
tests.getRange("Y:Y").format.columnWidth = 46;
tests.getRange("Z:AA").format.columnWidth = 16;
tests.getRange(`A5:AA${4 + rows.length}`).format.rowHeight = 72;
tests.freezePanes.freezeRows(4);
tests.freezePanes.freezeColumns(3);
tests.tables.add(`A4:AA${4 + rows.length}`, true, "ComplianceTestCases");
tests.getRange(`N5:N${4 + rows.length}`).conditionalFormats.add("containsText", { text: "可以发布", format: { fill: lightGreen, font: { color: green, bold: true } } });
tests.getRange(`N5:N${4 + rows.length}`).conditionalFormats.add("containsText", { text: "发布前需修改", format: { fill: lightRed, font: { color: red, bold: true } } });
tests.getRange(`N5:N${4 + rows.length}`).conditionalFormats.add("containsText", { text: "需要你补充信息", format: { fill: lightAmber, font: { color: amber, bold: true } } });
tests.getRange(`N5:N${4 + rows.length}`).conditionalFormats.add("containsText", { text: "不在覆盖范围", format: { fill: lightGray, font: { color: gray, bold: true } } });

// 评测结果
titleBand(results, "模型评测结果", "黄色列填写模型实际输出；状态、问题类型、下一步操作与 OCR 关键文本各占 25%。", "O");
results.getRange("A4:O4").values = [["用例编号","预期状态","实际状态","状态得分","预期问题类型","实际问题类型","问题得分","预期下一步操作","实际下一步操作","操作得分","实际提取文字","OCR关键文本得分","耗时（毫秒）","错误备注","整体通过"]];
for (let i = 0; i < cases.length; i++) {
  const row = 5 + i;
  results.getRange(`A${row}`).values = [[cases[i].test_id]];
  results.getRange(`B${row}`).formulas = [[`='测试用例'!N${row}`]];
  results.getRange(`D${row}`).formulas = [[`=IF(C${row}=\"\",\"\",--(C${row}=B${row}))`]];
  results.getRange(`E${row}`).formulas = [[`='测试用例'!P${row}`]];
  results.getRange(`G${row}`).formulas = [[`=IF(F${row}=\"\",\"\",--(F${row}=E${row}))`]];
  results.getRange(`H${row}`).formulas = [[`='测试用例'!S${row}`]];
  results.getRange(`J${row}`).formulas = [[`=IF(I${row}=\"\",\"\",--(I${row}=H${row}))`]];
  results.getRange(`O${row}`).formulas = [[`=IF(COUNT(D${row},G${row},J${row},L${row})<4,\"\",--(SUM(D${row},G${row},J${row},L${row})=4))`]];
}
results.getRange("A4:O4").format = { fill: purple, font: { bold: true, color: "#FFFFFF" }, wrapText: true, verticalAlignment: "center" };
results.getRange(`A5:O${4 + cases.length}`).format = { font: { size: 9 }, verticalAlignment: "top", wrapText: true };
results.getRange(`C5:C${4 + cases.length}`).format.fill = lightAmber;
results.getRange(`F5:F${4 + cases.length}`).format.fill = lightAmber;
results.getRange(`I5:I${4 + cases.length}`).format.fill = lightAmber;
results.getRange(`K5:N${4 + cases.length}`).format.fill = lightAmber;
results.getRange(`C5:C${4 + cases.length}`).dataValidation = { rule: { type: "list", values: ["可以发布", "发布前需修改", "需要你补充信息", "不在覆盖范围"] } };
results.getRange(`L5:L${4 + cases.length}`).dataValidation = { rule: { type: "list", values: [0, 1] } };
results.getRange(`D5:D${4 + cases.length}`).format.numberFormat = "0";
results.getRange(`G5:G${4 + cases.length}`).format.numberFormat = "0";
results.getRange(`J5:J${4 + cases.length}`).format.numberFormat = "0";
results.getRange(`L5:L${4 + cases.length}`).format.numberFormat = "0";
results.getRange(`O5:O${4 + cases.length}`).format.numberFormat = "0";
results.getRange("A:A").format.columnWidth = 11;
results.getRange("B:C").format.columnWidth = 21;
results.getRange("D:D").format.columnWidth = 12;
results.getRange("E:F").format.columnWidth = 28;
results.getRange("G:G").format.columnWidth = 12;
results.getRange("H:I").format.columnWidth = 42;
results.getRange("J:J").format.columnWidth = 12;
results.getRange("K:K").format.columnWidth = 50;
results.getRange("L:M").format.columnWidth = 14;
results.getRange("N:N").format.columnWidth = 30;
results.getRange("O:O").format.columnWidth = 14;
results.getRange(`A5:O${4 + cases.length}`).format.rowHeight = 58;
results.freezePanes.freezeRows(4);
results.freezePanes.freezeColumns(2);
results.tables.add(`A4:O${4 + cases.length}`, true, "EvaluationResults");
results.getRange(`O5:O${4 + cases.length}`).conditionalFormats.add("cellIs", { operator: "equal", formula: 1, format: { fill: lightGreen, font: { color: green, bold: true } } });
results.getRange(`O5:O${4 + cases.length}`).conditionalFormats.add("cellIs", { operator: "equal", formula: 0, format: { fill: lightRed, font: { color: red, bold: true } } });

// 海报索引
titleBand(posters, "中文测试海报索引", "原图位于 images/AU-ZH-xxx.png；poster_contact_sheet.png 提供 12 张海报总览。", "F");
posters.getRange("A4:F4").values = [["用例编号", "用例名称", "预期状态", "图片文件", "海报可见文字标准答案", "难度"]];
posters.getRange(`A5:F${4 + cases.length}`).values = cases.map(c => [c.test_id, c.title, c.expected_status, c.image_file, c.poster_visible_text_gold, c.difficulty]);
posters.getRange("A4:F4").format = { fill: purple, font: { bold: true, color: "#FFFFFF" }, wrapText: true };
posters.getRange(`A5:F${4 + cases.length}`).format = { wrapText: true, verticalAlignment: "top", font: { size: 10 } };
posters.getRange("A:A").format.columnWidth = 11;
posters.getRange("B:B").format.columnWidth = 28;
posters.getRange("C:C").format.columnWidth = 22;
posters.getRange("D:D").format.columnWidth = 24;
posters.getRange("E:E").format.columnWidth = 60;
posters.getRange("F:F").format.columnWidth = 12;
posters.getRange(`A5:F${4 + cases.length}`).format.rowHeight = 52;
posters.freezePanes.freezeRows(4);
posters.tables.add(`A4:F${4 + cases.length}`, true, "PosterIndex");

for (const sheet of [tests, results, posters]) sheet.getUsedRange().format.font.name = "Aptos";

const inspect = await wb.inspect({ kind: "table", range: "使用说明!A1:H21", include: "values,formulas", tableMaxRows: 25, tableMaxCols: 10 });
console.log(inspect.ndjson);
const errors = await wb.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A", options: { useRegex: true, maxResults: 100 }, summary: "final formula error scan" });
console.log(errors.ndjson);

for (const sheetName of ["使用说明", "测试用例", "评测结果", "海报索引"]) {
  const preview = await wb.render({ sheetName, autoCrop: "all", scale: 1, format: "png" });
  await fs.writeFile(path.join(previewDir, `${sheetName}.png`), new Uint8Array(await preview.arrayBuffer()));
}

const output = await SpreadsheetFile.exportXlsx(wb);
await output.save(path.join(outputDir, "Canva_AI_海报文字合规审核_中文小型测评集.xlsx"));
console.log(path.join(outputDir, "Canva_AI_海报文字合规审核_中文小型测评集.xlsx"));
