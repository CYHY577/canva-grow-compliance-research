import fs from "node:fs/promises";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const inputPath = process.argv[2];
if (!inputPath) throw new Error("Usage: node inspect_testset.mjs <xlsx-path>");

const input = await FileBlob.load(inputPath);
const workbook = await SpreadsheetFile.importXlsx(input);

if (process.argv.includes("--write-cases")) {
  const sheet = workbook.worksheets.getItem("测试集");
  const values = sheet.getRange("A1:R61").values;
  const headers = values[0];
  const cases = values.slice(1).map((row, index) => {
    const record = { sheetRow: index + 2 };
    headers.forEach((header, column) => {
      record[header] = row[column] ?? null;
    });
    return record;
  });
  const outputPath = process.argv[process.argv.indexOf("--write-cases") + 1];
  if (!outputPath) throw new Error("--write-cases requires an output path");
  await fs.writeFile(outputPath, `export default ${JSON.stringify(cases)};\n`, "utf8");
  console.log(outputPath);
  process.exit(0);
}

if (process.argv.includes("--formulas")) {
  const testSheet = workbook.worksheets.getItem("测试集");
  const summarySheet = workbook.worksheets.getItem("结果汇总");
  console.log("TEST_INPUT_FORMULAS");
  console.log(JSON.stringify(testSheet.getRange("O1:R61").formulas));
  console.log("SUMMARY_FORMULAS");
  console.log(JSON.stringify(summarySheet.getRange("A1:E21").formulas));
  process.exit(0);
}

if (process.argv.includes("--verify-results")) {
  const testSheet = workbook.worksheets.getItem("测试集");
  const summarySheet = workbook.worksheets.getItem("结果汇总");
  console.log("RESULTS");
  console.log(JSON.stringify(testSheet.getRange("A1:A61").values.map((row, i) => [row[0], ...(testSheet.getRange(`O${i + 1}:R${i + 1}`).values[0] ?? [])])));
  console.log("SUMMARY_VALUES");
  console.log(JSON.stringify(summarySheet.getRange("A5:E18").values));
  console.log("SUMMARY_FORMULAS");
  console.log(JSON.stringify(summarySheet.getRange("A5:E18").formulas));
  process.exit(0);
}

if (process.argv.includes("--render-summary")) {
  const outputPath = process.argv[process.argv.indexOf("--render-summary") + 1];
  if (!outputPath) throw new Error("--render-summary requires an output path");
  const preview = await workbook.render({
    sheetName: "结果汇总",
    range: "A1:E21",
    scale: 1.5,
    format: "png",
  });
  await fs.writeFile(outputPath, new Uint8Array(await preview.arrayBuffer()));
  console.log(outputPath);
  process.exit(0);
}

const overview = await workbook.inspect({
  kind: "workbook,sheet,table",
  maxChars: 12000,
  tableMaxRows: 12,
  tableMaxCols: 20,
  tableMaxCellChars: 300,
});
console.log("OVERVIEW");
console.log(overview.ndjson);

for (const sheet of workbook.worksheets.items) {
  const used = sheet.getUsedRange(true);
  console.log(`SHEET ${sheet.name}`);
  console.log(`USED ${used?.address ?? "none"}`);
  if (!used) continue;
  const rows = used.values ?? [];
  for (let i = 0; i < rows.length; i += 1) {
    console.log(JSON.stringify({ row: i + 1, values: rows[i] }));
  }
}
