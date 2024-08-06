# **rename_jpgs**

## **Overview:**

There are 2 values that the script is extracting and using for renaming files:

- **Order number** in the format: **`00012345`**
- **Order name** in the format: **`412ABCDEF`**
  
Both of these values can be found (in ideal scenario) twice in the image. They are then concatenated and scanned file is renamed in this case to: **'12345_412ABCDEF.jpg'**

Script only runs in terminal and looks like this:

![Screenshot 2024-08-06 084339](https://github.com/user-attachments/assets/a6870873-fa13-49bc-ad17-0d08d4e517ab)


## **Installation:**

To use this script, you need to have Python installed along with EasyOCR. You can find it here: https://pypi.org/project/easyocr/

## **Usage:**

Place the script in the directory containing your .jpg files and run it. The script will then process all .jpg files in the directory and rename them based on the extracted text

## **Observations and bugs:**

I used this script at work extensively. With most recent update there is only about 1% of incompletely renamed files.

Bugs that I've noticed:

1. ~~Most common bug was that the ocr failed to recognise either order number, or order name, or both. This lead to results like: '12345.jpg', '_412ABCDEF.jpg', '.jpg'~~
   ~~This is in some cases due to physical damage of the documents itself (this is production environment - there can be stains and various damage occuring...).
   I am sure there is some optimisation that can be done to improve the success rate here, but for now this bug is the least concerning one.~~

   - Fixed. (Removed min_size parameter.)

3. ~~Some files were renamed to '12345_403RB.jpg'.
   The '403RB' part here is a concern because it's wrong. This is some unrelated internal code that is not the order name.
   This bug is caused by not specific enough regex implemented in the code and needs to be fixed.~~
   
   - Fixed. (Updated regex.)

5. Traceback error.
   This occured only 3-5 times in over 2500 files but it is concerning because it stops program from running.
   I can't really recreate it, therefore I don't really know what is causing it but I think it has something to do with file names before renaming.
   I observed this issue only when renaming large amounts of files with multiple instances of the script running. In day to day use the issue does not occur.




