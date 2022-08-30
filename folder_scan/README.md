# Folder scan
In case you have a camera we do not have a direct support for and scanning the images from a folder is a viable option, here's one way of doing it.

1. Make sure you are sending an image to a running PEKAT VISION by setting the correct file extensions.
2. Rewrite the path to the folder where the scanning will be done.

The script connects to an already running instance of PEKAT VISION on the local machine on port 8000.

Everytime a new picture arrives in the folder, the script will send it to the PEKAT VISION and log the result.