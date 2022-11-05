# a script to untar .tar file and find the info.ver file, edit it with additional text: hello world, and then tar it back up
from datetime import date
from upload_file import upload_file_to_box
from yaspin import yaspin
from get_args import get_args
from boxsdk import Client, CCGAuth

import os
import sys
import tarfile
import shutil

import time


auth = CCGAuth(
  client_id="egkrr2d915ry6y70i83vjopp0j310dr4",
  client_secret="rPViiMNUOZERGzm2Te4lancNcpWFMl4m",
  enterprise_id="956673804"
)

client = Client(auth)

me = client.user().get()


def version_template(version_text):
    return f"""image_family: ap1g6a
ws_management_version: {version_text}
ap_version: {version_text}
info_end:
altboot_fallback: 1
"""


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

    with yaspin(text="Checking files exists", color="yellow") as spinner:
        # open tar file
        tar = tarfile.open(file_path)
        # if file is not a tar file or is empty, quit
        if not tar or tar.members == []:
            print("No tar file found")
            return
        # extract all files and create a temp folder
        spinner.text = "Extracting files"
        tar.extractall(path="temp")
        # open info.ver file
        info_ver_path = os.path.join("temp", "info.ver")
        spinner.text = "Modifying info.ver and info"
        with open(info_ver_path, 'a') as f:
            # make this file empty
            f.truncate(0)
            # write the version template to the file
            f.write(version_template(version_text))
        # open info file
        ver_path = os.path.join("temp", "info")
        with open(ver_path, 'a') as f:
            f.truncate(0)
            f.write(version_template(version_text))
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
            file_id=upload_file_to_box(client, '180673298837', output_path)
            with yaspin(text="Creating sharing link", color="yellow") as spinner:
                url = client.file(file_id).get_shared_link(access='open', allow_download=True, allow_edit=True)
                spinner.text = ""
                spinner.color = "green"
                spinner.ok(f"You can view the file via: {url}")
        else:
            spinner.text = ""
            spinner.color = "green"
            spinner.ok(
                f"✅ New tar file created: {date_string}-{version_text}.tar")


# run main function
if __name__ == '__main__':
    main()
