import os
import sqlite3
from database.db import DB_PATH
from dicom.reader import read_case_metadata
import re
from datetime import datetime

def scan_root(root_path):
    print(f"Scanning root folder: {root_path}")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    for case_folder in os.listdir(root_path):
        case_path = os.path.join(root_path, case_folder)
        if not os.path.isdir(case_path):
            continue

        first_dicom = None
        for root, _, files in os.walk(case_path):
            for f in files:
                if f.lower().endswith(".dcm"):
                    first_dicom = os.path.join(root, f)
                    break
            if first_dicom:
                break

        if not first_dicom:
            continue

        meta = read_case_metadata(first_dicom)
        # print(meta)
        

        def transform_name(raw_string):
            # 1. Split the string at the caret symbol '^'
            # "383331Mahmoud Salah-Eldin^El-Shimaa" -> ["383331Mahmoud Salah-Eldin", "El-Shimaa"]
            parts = raw_string.split('^')
            
            if len(parts) == 2:
                part1 = parts[0] # "383331Mahmoud Salah-Eldin"
                part2 = parts[1] # "El-Shimaa"
                
                # 2. Remove the leading numbers from the first part
                # ^\d+ matches one or more digits at the start of the string
                part1_clean = re.sub(r'^\d+', '', part1)
                
                # 3. Combine them in the desired order
                return f"{part2} {part1_clean}"
            return raw_string # Return original if format doesn't match

        
        def transform_date(date_string):
            # Example input: "20260105"
            # Desired output: "05-01-2026"

            # 1. Parse the string into a date object
            # %Y = 4-digit year, %m = 2-digit month, %d = 2-digit day
            date_obj = datetime.strptime(date_string, "%Y%m%d")

            # 2. Format it to the desired string
            # Result: "05-01-2026"
            return date_obj.strftime("%d-%m-%Y")

        name = transform_name(str(meta["name"]))
        date = transform_date(meta["date"])

        c.execute("""
        INSERT OR IGNORE INTO cases VALUES (?, ?, ?, ?, ?, ?)
        """, (
            meta["id"], name, meta["age"],
            meta["gender"], date, case_path
        ))
        
        print(meta["id"], name, meta["age"],
            meta["gender"], date, case_path)
    conn.commit()
    conn.close()
