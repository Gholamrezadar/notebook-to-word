import json
import base64
import os
import shutil


IMAGES_PATH = 'images/'
NB_NAME = 'notebook.ipynb'
NB_NAME = 'Exercise_1.ipynb'

# If the images folder exists, recreate it
if os.path.exists(IMAGES_PATH):
    shutil.rmtree(IMAGES_PATH)
os.mkdir(IMAGES_PATH)

with open(NB_NAME, "r", encoding="utf-8") as f:
    nb = json.load(f)

    i = 0
    image_id = 0
    last_header_2 = ""
    last_header_3 = ""
    for cell in nb["cells"]:
        print("cell",i)
        # Cell is markdown
        if cell["cell_type"] == "markdown":
            if cell["source"][0][:3] == "## ":
                # reset image counter for each header
                image_id = 0
                last_header_2 = cell["source"][0][3:].strip().replace(" ", "_") + "_"
                print("\t",last_header_2)

            if cell["source"][0][:4] == "### ":
                image_id = 0
                last_header_3 = cell["source"][0][4:].strip().replace(" ", "_") + "_"
                print("\t",last_header_3)
            else:
                last_header_3 = ""

        # Cell is code
        if cell["cell_type"] == "code":
            # Cells with outputs
            if len(cell["outputs"]) > 0:
                # Loop through outputs
                for output in cell["outputs"]:
                    # If output is image
                    if "data" in output and "image/png" in output["data"]:
                        image_id+=1
                        print("\tis image")
                        image_base64 = output["data"]["image/png"]
                        image_base64 = bytes(image_base64, "utf-8")

                        # Save image
                        with open(f"{IMAGES_PATH}/{last_header_2}{last_header_3}{image_id}.png", "wb") as fh:
                            fh.write(base64.decodebytes(image_base64))
        i += 1