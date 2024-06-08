import os
import re
import easyocr

# with integrated graphics this returns a warning that it is defaulting to cpu processing, which is slower, but for my use case still usable... 
reader = easyocr.Reader(['en'])
# getting all .jpg files in the current directory
files = [f for f in os.listdir('.') if f.lower().endswith('.jpg')]
no_of_files = len(files)
# dictionary for handling duplicates while renaming
names = {}
# variables to keep track of success rate
correctly_renamed = 0
not_correctly_renamed = []

def extract_order_number(string, matched_order_number):
    """extracting the order number from the string in a format '000XXXXX' and adding it to matched_order_number variable.
    this assumes that the order number has a length of five digits (up to 99999) with three zeros at the beginning.
    currently, we are around no. 30000... this is since 2015 so it should work a while..."""
    match = re.search(r'0{3}([1-9]\d{4})', string)
    if match and matched_order_number == "":
        matched_order_number = match.group(1)
    return matched_order_number
    
def extract_order_name(string, matched_order_name):
    """extracting the name of the ordered product and adding it into extracted_data dictionary. in our case, this is a chemical mixture..."""
    match = re.search(r'([2348][0-9O]{2}[CPTD][A-Z]{1,10})', string)
    if match and matched_order_name == "":
        # replacing potential 'O's with '0's in the second and third char. of the match... OCR sometimes mistakes 0 for O...
        matched_order_name = "_" + match.group(1)[0:3].replace('O', '0') + match.group(1)[3:]
    return matched_order_name

def rename_files():
    global correctly_renamed
    for file in files:
        strings = reader.readtext(file, detail=0, min_size=160)

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

print(f"\ntotal jpg's in the directory: {no_of_files}\ncorrectly renamed: {correctly_renamed}\nnot renamed correctly: {no_of_files - correctly_renamed} ({not_correctly_renamed})\nsuccess rate: {(correctly_renamed/no_of_files)*100}%")
# wait for user input before exiting
input("\npress enter to exit...")
