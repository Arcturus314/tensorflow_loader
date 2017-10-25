import os
import shutil
from PIL import Image

local_directory = "/"
supported_image_formats = [".png", ".jpeg",".jpg"]
imagelist = []
image_count = 0

def reset_image_count():
    '''resets the image_count variable to 0'''
    global image_count
    image_count = 0

def fetch_num_images():
    return len(imagelist)

def set_directory(directory):
    '''sets the image directory to 'directory' '''
    global local_directory
    local_directory = directory

def scan_image_filenames():
    global imagelist
    '''scans local_directory for images, returns a sorted list of image filenames'''
    filelist = next(os.walk(local_directory))[2]
    imagelist = []
    for element in filelist:
        for postfix in supported_image_formats:
            if postfix in element: imagelist.append(element)
    return imagelist

def setup_imagelist(directory):
    '''downloads an image set from a specific url to a specific variable, and sets up internal variables for image processing'''
    global imagelist
    set_directory(directory)
    reset_image_count()
    imagelist = scan_image_filenames()

def get_next_image():
    '''returns filename, has_cat, (width, height)'''
    global image_count
    image_filename = imagelist[image_count]
    im = Image.open(local_directory+"/"+image_filename)
    print 'Processing image number: ',image_count,' filename: ',image_filename
    image_size = im.size
    image_count += 1
    return local_directory+"/"+image_filename, "cat" in image_filename, image_size
