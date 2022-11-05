# AP version patcher

Simple script to patch ap image to match WLC version + box file upload with shared link.

| Argument | Description | Required | Default |
| --- | --- | --- | --- |
| -i, --input | Path to tar file | Yes | |
| -t, --text | Version text to be updated for info and info.ver | Yes | |
| -o, --output | Path to output tar file | No | {`date`}-{`text`}.tar |
| -u, --upload | Upload to box | No | `False` |