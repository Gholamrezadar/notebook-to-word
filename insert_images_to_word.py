from docx import Document
from docx.shared import Inches
import glob
import os

TEMPLATE_PATH = 'a.docx'
NOTEBOOK_NAME = "Exercise_1"
IMAGES_PATH = f'{NOTEBOOK_NAME}\\images'
OUTPUT_PATH = f'{NOTEBOOK_NAME}.docx'

MAX_IMAGE_WIDTH = 6  # inches

document = Document('a.docx')

last_part = ""
last_secc = ""
image_id_non_reset = 0
for f in glob.glob(f'{IMAGES_PATH}\\**\\*.png', recursive=True):
    image_id_non_reset +=1
    print(
        f"> {image_id_non_reset} - Loaded {f}")
    path = f.split('\\')
    part = ""
    secc = ""

    if len(path) == 3:
        file_name = path[-1]
    if len(path) == 4:
        part = path[2].replace("_", " ")
        file_name = path[-1]
    if len(path) == 5:
        part = path[2].replace("_", " ")
        secc = path[3].replace("_", " ")
        file_name = path[-1]

    # print(part, secc, file_name)
    # part is not empty and secc is empty
    if part == "" and secc == "":
        paragraph = document.add_paragraph("")
        paragraph.alignment = 1
        r = paragraph.add_run()
        pic = r.add_picture(f, width=Inches(MAX_IMAGE_WIDTH))
        # document.add_paragraph(file_name[:-4])

    # part is not empty and secc is not empty
    if part != "" and secc != "":
        if last_part != part:
            last_part = part
            last_secc = ""
            document.add_page_break()
            document.add_heading(part, 1)

        if last_secc != secc:
            last_secc = secc
            document.add_heading(secc, 2)

        paragraph = document.add_paragraph("")
        paragraph.alignment = 1
        r = paragraph.add_run()
        pic = r.add_picture(f, width=Inches(MAX_IMAGE_WIDTH))
        # document.add_paragraph(file_name[:-4])

    # part is empty and secc is not empty
    if part != "" and secc == "":
        if last_part != part:
            last_part = part
            document.add_heading(part, 1)

        paragraph = document.add_paragraph("")
        paragraph.alignment = 1
        r = paragraph.add_run()
        pic = r.add_picture(f, width=Inches(MAX_IMAGE_WIDTH))
        # document.add_paragraph(file_name[:-4])


document.save(OUTPUT_PATH)
print("Wrote to", OUTPUT_PATH)
