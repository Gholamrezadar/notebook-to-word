import json
import base64
import os
import shutil

NB_NAME = 'notebook.ipynb'
NB_NAME = 'Exercise_1.ipynb'
IMAGES_PATH = os.path.join(NB_NAME[:-6],'images')

# If the images folder exists, recreate it
if os.path.exists(IMAGES_PATH):
    shutil.rmtree(IMAGES_PATH)
os.makedirs(IMAGES_PATH)

with open(NB_NAME, "r", encoding="utf-8") as f:
    nb = json.load(f)

    i = 0  # cell id
    image_id = 0  # image id; restarts when reaches a new h2 or h3
    image_id_non_reset = 0  # image id; doesnt restart when reaches a new h2 or h3
    last_header_2 = ""  # double hashtag headers (##)
    last_header_3 = ""  # triple hashtag headers (###)

    for cell in nb["cells"]:
        # print("cell",i)
        # Cell is markdown
        if cell["cell_type"] == "markdown":
            if cell["source"][0][:3] == "## ":
                # reset image counter for each header
                image_id = 0
                last_header_2 = cell["source"][0][3:].strip().replace(" ", "_")
                # print("\t",last_header_2)

            if cell["source"][0][:4] == "### ":
                image_id = 0
                last_header_3 = cell["source"][0][4:].strip().replace(" ", "_")
                # print("\t",last_header_3)
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
                        image_id += 1
                        image_id_non_reset += 1
                        # Convert image from base64 to bytes
                        image_base64 = output["data"]["image/png"]
                        image_base64 = bytes(image_base64, "utf-8")

                        # Set the image file name
                        image_file_name = ""

                        # Case 1: Image in H2 and H3
                        if last_header_3 != "" and last_header_2 != "":
                            folder_path = os.path.join(
                                IMAGES_PATH, last_header_2, last_header_3)
                            if not os.path.exists(folder_path):
                                os.makedirs(folder_path)
                            image_file_name = os.path.join(
                                folder_path, f"{image_id:0>2}.png")

                        # Case 2: Image out of H2 and H3
                        if last_header_3 == "" and last_header_2 == "":
                            image_file_name = os.path.join(
                                IMAGES_PATH, f"{image_id:0>2}.png")

                        # Case 3: Image in H2 and not H3
                        if last_header_3 != "" and last_header_2 == "":
                            image_file_name = os.path.join(
                                IMAGES_PATH, f"{image_id:0>2}.png")

                        # Case 4: Image in H3 and not H2
                        if last_header_3 == "" and last_header_2 != "":
                            folder_path = os.path.join(
                                IMAGES_PATH, last_header_2)
                            if not os.path.exists(folder_path):
                                os.makedirs(folder_path)
                            image_file_name = os.path.join(
                                folder_path, f"{image_id:0>2}.png")

                        # Save image
                        print(
                            f"> {image_id_non_reset} - Saved {image_file_name}")
                        with open(image_file_name, "wb") as fh:
                            fh.write(base64.decodebytes(image_base64))
        i += 1
