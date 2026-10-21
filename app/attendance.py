import openpyxl
from datetime import datetime
import os

def get_indo_month_year(date_obj):
    indo_months = {
        1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April',
        5: 'Mei', 6: 'Juni', 7: 'Juli', 8: 'Agustus',
        9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'
    }
    return f"{indo_months[date_obj.month]} {date_obj.year}"

def mark_attendance(student_name):
    file_path = ".\data\Salinan dari Absensi X RPL 2 - Semester Ganjil TA 2025-2026 (2).xlsx"
    
    if not os.path.exists(file_path):
        print(f"Error: Database file '{file_path}' not found in the root directory.")
        return

    now = datetime.now()
    target_sheet_name = get_indo_month_year(now)
    today_day = now.day 
    
    try:
        wb = openpyxl.load_workbook(file_path)
        
        if target_sheet_name not in wb.sheetnames:
            print(f"Error: Sheet '{target_sheet_name}' not found in the workbook.")
            return
            
        ws = wb[target_sheet_name]
        
        # 1. Scan the first 10 rows to find the header row containing today's date (1-31)
        date_col = None
        header_row = None
        for row in range(1, 11):
            for col in range(1, ws.max_column + 1):
                cell_val = ws.cell(row=row, column=col).value
                if cell_val == today_day or str(cell_val) == str(today_day):
                    date_col = col
                    header_row = row
                    break
            if date_col:
                break
                
        if not date_col:
            print(f"Could not find a column for day '{today_day}' in sheet '{target_sheet_name}'.")
            return

        # 2. Scan the first 5 columns to find the student's name
        student_row = None
        start_search_row = header_row + 1 if header_row else 1
        for row in range(start_search_row, ws.max_row + 1):
            for col in range(1, 6): 
                cell_val = ws.cell(row=row, column=col).value
                if cell_val and str(cell_val).strip().lower() == student_name.strip().lower():
                    student_row = row
                    break
            if student_row:
                break
                
        if not student_row:
            print(f"Could not find student '{student_name}' in the spreadsheet.")
            return

        # 3. Mark attendance (using 'H' for Hadir)
        ws.cell(row=student_row, column=date_col, value="H") 
        wb.save(file_path)
        print(f"[{now.strftime('%H:%M:%S')}] Marked 'H' for {student_name} on {target_sheet_name} {today_day}")
        
    except Exception as e:
        print(f"Error updating Excel file: {e}")