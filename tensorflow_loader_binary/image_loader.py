import os
import shutil
from git import Repo
from PIL import Image

#IMAGES MUST BE IN '.png' FORMAT
local_directory = "/home/kaveh/tensorflow_loader/images"
supported_image_formats = [".png", ".jpeg"]
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

def fetch_images_github(url):
    '''downloads an image dataset from a GitHub repository to local_directory, deleting the contents of the local directory if not already empty'''
    shutil.rmtree(local_directory)
    Repo.clone_from(url, local_directory) 

def scan_image_filenames():
    global imagelist
    '''scans local_directory for images, returns a sorted list of image filenames'''
    filelist = next(os.walk(local_directory))[2]
    imagelist = []
    for element in filelist:
        for postfix in supported_image_formats:
            if postfix in element: imagelist.append(element)
    #return imagelist_sort(imagelist)
    return imagelist

def setup_imagelist(directory, url):
    '''downloads an image set from a specific url to a specific variable, and sets up internal variables for image processing'''
    global imagelist
    set_directory(directory)
    fetch_images_github(url)
    reset_image_count()
    imagelist = scan_image_filenames()

def get_next_image():
    '''returns filename, has_cat, (width, height)'''
    global image_count
    image_filename = imagelist[image_count]
    im = Image.open(local_directory+"/"+image_filename)
    print 'Processing image number: ',image_count,' filename ',image_filename
    image_size = im.size
    image_count += 1
    return local_directory+"/"+image_filename, "cat" in image_filename, image_size
