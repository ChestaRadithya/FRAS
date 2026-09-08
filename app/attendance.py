import openpyxl
from datetime import datetime
import os

def mark_attendance(student_name):
    now = datetime.now()
    file_path = f"data/attendance/attendance_{now.strftime('%Y_%m')}.xlsx"
    today_str = now.strftime('%Y-%m-%d')
    
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    if not os.path.exists(file_path):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Attendance Log"
        ws.cell(row=1, column=1, value="Student Name")
    else:
        wb = openpyxl.load_workbook(file_path)
        ws = wb.active

    date_col = None
    for col in range(2, ws.max_column + 2):
        if ws.cell(row=1, column=col).value == today_str:
            date_col = col
            break
        elif ws.cell(row=1, column=col).value is None:
            date_col = col
            ws.cell(row=1, column=col, value=today_str)
            break

    student_row = None
    for row in range(2, ws.max_row + 2):
        if ws.cell(row=row, column=1).value == student_name:
            student_row = row
            break
        elif ws.cell(row=row, column=1).value is None:
            student_row = row
            ws.cell(row=row, column=1, value=student_name)
            break

    ws.cell(row=student_row, column=date_col, value=".")
    wb.save(file_path)
    print(f"[{now.strftime('%H:%M:%S')}] Marked '.' for {student_name}")