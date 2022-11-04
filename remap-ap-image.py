# a script to untar .tar file and find the info.ver file, edit it with additional text: hello world, and then tar it back up
from datetime import date
import os
import sys
import tarfile
import shutil


def version_template(version_text):
    return f"""image_family: ap1g6a
ws_management_version: {version_text}
ap_version: {version_text}
info_end:
altboot_fallback: 1
"""

def main():

    file_path = sys.argv[1]
    version_text = sys.argv[2]
    # quit if no file path or version text given
    if not file_path or not version_text:
        print("No file path or version text given")
        return
    # open tar file
    tar = tarfile.open(file_path)
    # if file is not a tar file or is empty, quit
    if not tar or tar.members == []:
        print("No tar file found")
        return
    # extract all files and create a temp folder
    tar.extractall(path="temp")
    # open info.ver file
    info_ver_path = os.path.join("temp", "info.ver")
    with open(info_ver_path, 'a') as f:
        # make this file empty
        f.truncate(0)
        # write the version template to the file
        f.write(version_template(version_text))
    # open info file
    ver_path = os.path.join("temp", "ver")
    with open(ver_path, 'a') as f:
        f.truncate(0)
        f.write(version_template(version_text))
    # open tar file and create a new tar file named with today's date + version text
    date_string = date.today().strftime("%b-%d-%Y")
    tar = tarfile.open(f"{date_string}-{version_text}.tar", "w")
    # for each file in the temp folder, add it to the new tar file
    for file in os.listdir('temp'):
        file_path = os.path.join("temp", file)
        tar.add(file_path, arcname=file)
    # close tar file
    tar.close()
    # remove temp folder
    shutil.rmtree('temp')

# run main function
if __name__ == '__main__':
    main()