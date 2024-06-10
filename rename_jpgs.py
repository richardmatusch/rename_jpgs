import os
import re
import easyocr

# with integrated graphics running this script returns a warning that it is defaulting to cpu processing, which is slower, but for my use case still usable... 
reader = easyocr.Reader(['en'])

# getting all .jpg files in the current directory
files = [f for f in os.listdir('.') if f.lower().endswith('.jpg')]
no_of_files = len(files)

# variables for handling duplicates and keeping track of correctly renamed files
names = {}
correctly_renamed = 0
not_correctly_renamed = []

def extract_order_number(string, matched_order_number):
    """searching for the order number in a format '000XXXXX' and returning only last 5 digits"""
    match = re.search(r'0{3}([1-9]\d{4})', string)
    if match and matched_order_number == "":
        matched_order_number = match.group(1)
    return matched_order_number
    
def extract_order_name(string, matched_order_name):
    """searching for the order name and returning it"""
    match = re.search(r'20[01]DB|[2348][0-9O]{2}[CPTD][A-Z]{5,10}', string)
    if match and matched_order_name == "":
        matched_order_name = "_" + match.group(0)[0:3].replace('O', '0') + match.group(0)[3:]
    return matched_order_name # OCR sometimes mistakes 0 for O...

def rename_files():
    """looping through the current dictionary, using ocr on .jpg files and using previous two functions to search for relevant data for file renaming"""
    global correctly_renamed

    for file in files:
        strings = reader.readtext(file, detail=0, min_size=100)

        matched_order_number = ""
        matched_order_name = ""

        for string in strings:
            matched_order_number = extract_order_number(string, matched_order_number)
            matched_order_name = extract_order_name(string, matched_order_name)

        new_name = matched_order_number + matched_order_name + ".jpg"

        # handling duplicates
        if new_name in names:
            names[new_name] += 1
            new_name = f"{matched_order_number}{matched_order_name} ({names[new_name]}).jpg"
        else:
            names[new_name] = 1

        # renaming files
        os.rename(file, new_name)
        # handling correctly and incorrectly renamed files for report at the end
        if len(new_name) >= 15 and "_" in new_name: 
            correctly_renamed += 1
        else:
            not_correctly_renamed.append(new_name)
        print(f"renamed '{file}' to '{new_name}'")

rename_files()

print(f"\ntotal jpg's in the directory: {no_of_files}\ncorrectly renamed: {correctly_renamed}\nnot renamed correctly: {no_of_files - correctly_renamed}, {not_correctly_renamed}\nsuccess rate: {round((correctly_renamed/no_of_files)*100, 2)}%")
# prompt to keep the script running till user exits
input("\npress enter to exit...")
