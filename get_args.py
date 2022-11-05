import argparse


# get arguments from command line
# 1. required: original tar file path
# 2. required: version text
# 3. optional: output tar file path, default to today's date + version text under 'output' folder
# 4. optional: wheather to upload to box, default to false

def get_args():
    parser = argparse.ArgumentParser(description="Remap AP Image")
    parser.add_argument("-i", "--input", dest="path", help="Path to tar file")
    parser.add_argument("-t", "--text", help="Version text to be updated for info and info.ver", required=True)
    parser.add_argument("-o", "--output", help="Path to output tar file", required=False)
    parser.add_argument("-u", "--upload", help="Upload to box", required=False)
    args = parser.parse_args()
    return args