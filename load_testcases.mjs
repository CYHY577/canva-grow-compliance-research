import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

export async function loadTestCases(inputPath) {
  const input = await FileBlob.load(inputPath);
  const workbook = await SpreadsheetFile.importXlsx(input);
  const sheet = workbook.worksheets.getItem("测试集");
  const values = sheet.getRange("A1:R61").values;
  const headers = values[0];
  return values.slice(1).map((row, index) => {
    const record = { sheetRow: index + 2 };
    headers.forEach((header, column) => {
      record[header] = row[column] ?? null;
    });
    return record;
  });
}
