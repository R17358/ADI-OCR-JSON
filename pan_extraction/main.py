import os
import json
import re

folder_path = r"pan_extraction/results"


for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # print(f"✅ Extracted from {filename}:")
            # print(data["analyzeResult"]["content"])
            
        text = data["analyzeResult"]["content"]

        
        dob_pattern = r"\b\d{2}/\d{2}/\d{4}\b"
        pan_pattern = r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"
        name_pattern = r'\b(?:[A-Za-z]{2,}(?:\s+[A-Za-z]{2,}){0,3})\b'

        
        dob_match = re.search(dob_pattern, text)
        pan_match = re.search(pan_pattern, text)
        name_match = re.search(name_pattern, text)
        

        dob = dob_match.group() if dob_match else None
        pan = pan_match.group() if pan_match else None
        name = name_match.group() if name_match else None

       
        print("Extracted Details:")
        print("Name:", name)
        print("DOB:", dob)
        print("PAN:", pan)
        
        print("*"*10)
        print("\n"*4)