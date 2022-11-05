# a script to untar .tar file and find the info.ver file, edit it with additional text: hello world, and then tar it back up
from datetime import date
from lib.auth import auth
from lib.create_share_link import create_share_link
from lib.upload_file import upload_file_to_box
from lib.get_args import get_args
from yaspin import yaspin

import os
import tarfile
import shutil

import time


def version_template(version_text):
    return f"""image_family: ap1g6a
ws_management_version: {version_text}
ap_version: {version_text}
info_end:
altboot_fallback: 1
"""


def swap_version_text(file_name, version_text):
    file_path = os.path.join("temp", file_name)
    with open(file_path, 'a') as f:
        f.truncate(0)  # remove all text
        f.write(version_template(version_text))


def main():
    args = get_args()
    file_path = args.path
    version_text = args.text
    # quit if no file path or version text given
    if not file_path or not version_text:
        print("No file path or version text given")
        return

    date_string = date.today().strftime("%b-%d-%Y")
    output_path = args.output if args.output else os.path.join(
        "output", f"{date_string}-{version_text}.tar")
    box_upload = args.upload
    
    # delete temp folder if exists
    if os.path.exists("temp"):
        shutil.rmtree("temp")

    with yaspin(text="Checking files exists", color="yellow") as spinner:
        # Authenication
        client = auth()
        spinner.text = f"Authenticated as {client.user().get()['name']}"
        time.sleep(0.8)
        # open tar file
        tar = tarfile.open(file_path)
        # if file is not a tar file or is empty, quit
        if not tar or tar.members == []:
            print("No tar file found")
            return
        # extract all files and create a temp folder
        spinner.text = "Extracting files"
        tar.extractall(path="temp")
        # swap info.ver and info file
        swap_version_text("info.ver", version_text)
        swap_version_text("info", version_text)
        # open tar file and create a new tar file named with today's date + version text
        spinner.text = "Creating new tar file"
        # check if 'output' folder exists, if not, create it
        if not os.path.exists("output"):
            os.mkdir("output")
        tar = tarfile.open(output_path, "w")
        # for each file in the temp folder, add it to the new tar file
        spinner.text = "Adding files to new tar file"
        for file in os.listdir('temp'):
            file_path = os.path.join("temp", file)
            tar.add(file_path, arcname=file)
        # close tar file
        tar.close()
        # remove temp folder
        shutil.rmtree('temp')

        if (box_upload):
            spinner.text = "Uploading to box"
            try:
                file_id = upload_file_to_box(
                    client, '180673298837', "test.txt", spinner)
                create_share_link(client, file_id, spinner)
            except Exception as e:
                spinner.text = ""
                spinner.color = "red"
                spinner.fail(f"Upload failed: {e}")
                return
        else:
            spinner.text = ""
            spinner.color = "green"
            spinner.ok(
                f"✅ New tar file created: {date_string}-{version_text}.tar")


# run main function
if __name__ == '__main__':
    main()
