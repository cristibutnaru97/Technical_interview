import sys
import unittest
import os
from datetime import datetime
from openpyxl import Workbook
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def export_to_excel(data, filename):
    wb = Workbook()
    ws = wb.active

    # Header
    headers = list(data[0].keys())
    ws.append(headers)

    # Data rows
    for row in data:
        ws.append([row[h] for h in headers])

    # Footer: timestamp
    ws.append([])
    ws.append([f"Generated: {datetime.now()}"])

    wb.save(filename)
    print(f"Excel file saved as {filename}")

def export_to_pdf(data, filename):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    y = height - 50

    headers = list(data[0].keys())
    c.drawString(50, y, " | ".join(headers))
    y -= 20

    for row in data:
        c.drawString(50, y, " | ".join(str(row[h]) for h in headers))
        y -= 20

    # Footer
    c.drawString(50, 30, f"Generated: {datetime.now()}")

    c.save()
    print(f"PDF file saved as {filename}")


class TestExportFiles(unittest.TestCase):

    def setUp(self):
        self.data = [
            {"company": "ACME SRL", "revenue": 100000, "profit": 12000},
            {"company": "BETA SRL", "revenue": 200000, "profit": 50000}
        ]
        self.folder = "."  # folder curent
        today = datetime.now().strftime("%Y-%m-%d")
        self.xlsx_file = os.path.join(self.folder, f"report_testing_{today}.xlsx")
        self.pdf_file = os.path.join(self.folder, f"report_testing_{today}.pdf")

    def test_excel_file_created_and_not_empty(self):
        export_to_excel(self.data, self.xlsx_file)
        self.assertTrue(os.path.exists(self.xlsx_file), "Excel file was not created")
        self.assertGreater(os.path.getsize(self.xlsx_file), 0, "Excel file is empty")
        os.remove(self.xlsx_file)

    def test_pdf_file_created_and_not_empty(self):
        export_to_pdf(self.data, self.pdf_file)
        self.assertTrue(os.path.exists(self.pdf_file), "PDF file was not created")
        self.assertGreater(os.path.getsize(self.pdf_file), 0, "PDF file is empty")
        os.remove(self.pdf_file)
        print(1)

if __name__ == "__main__":
    data = [
        {"company": "ACME SRL", "revenue": 100000, "profit": 12000},
        {"company": "BETA SRL", "revenue": 200000, "profit": 50000}
    ]

    format_ = sys.argv[1].lower() if len(sys.argv) > 1 else "xlsx"
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"report_{today}.{format_}"

    if format_ == "xlsx":
        export_to_excel(data, filename)
    elif format_ == "pdf":
        export_to_pdf(data, filename)
    else:
        print("Unsupported format. Use 'pdf' or 'xlsx'.")
    #unittest.main()
