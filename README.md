# **rename_jpgs**

## **Overview:**

There are 2 values that the script is extracting and using for renaming files:

- **Order number** in the format: **`00034822`**
- **Order name** in the format: **`812CMBLSZ`**
  
Both of these values can be found (in ideal scenario) twice in the image. They are then concatenated and scanned file is renamed in this case to: **'34822_812CMBLSZ.jpg'**


## **Installation:**

To use this script, you need to have Python installed along with the following dependencies:
- `os`
- `re`
- `easyocr`

## **Usage:**

- place the script in the directory containing your .jpg files
- run the script using Python
- the script will process all .jpg files in the directory and rename them based on the extracted text

## **Observations and bugs after first testing:**

I used this script at work over the course of 2 days and renamed over 2500 files. Most of the files (my subjective estimate more than 90%) were renamed correctly.

Bugs that I've noticed:

1. Most common bug was that the ocr failed to recognise either order number, or order name, or both. This lead to results like:
   - '34822.jpg'
   - '_812CMBLSZ.jpg'
   - '.jpg'
     
   This is in most cases due to physical damage of the documents itself (this is production environment - there can be stains and various damage occuring...).
   I am sure there is some optimisation that can be done to improve the success rate here, but for now this bug is the least concerning one.

~~2. Some files were renamed to '12345_403RB.jpg'.
   The '403RB' part here is a concern because it's wrong. This is some unrelated internal code that is not the order name.
   This bug is caused by not specific enough regex implemented in the code and needs to be fixed.~~ This should be fixed now.

3. Traceback error.
   This occured only 3-5 times in over 2500 files but it is most concerning because it stops program from running.
   I cannot really recreate it (for now) therefore I do not really know what is causing it.
   I will try to implement some sort of try/except code to circumvent this error.




