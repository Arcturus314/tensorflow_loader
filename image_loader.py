import os
from git import Repo
from PIL import Image

#IMAGES MUST BE IN '.png' FORMAT
local_directory = "/home/kaveh/tensorflow_loader/images"
supported_image_formats = [".png",".jpg",".jpeg"]
image_count = 0
imagelist = ""

def set_directory(directory):
    '''sets the image directory to 'directory' '''
    global local_directory
    local_directory = directory

def reset_image_count():
    '''resets the current image count (as pairs) to 0'''
    global image_count
    image_count = 0

def fetch_images_github(url):
    '''downloads an image dataset from a GitHub repository to local_directory'''
    Repo.clone_from(url, local_directory) 

def scan_image_filenames():
    '''scans local_directory for images, returns a sorted list of image filenames'''
    filelist = next(os.walk(local_directory))[2]
    imagelist = []
    for element in filelist:
        for postfix in supported_image_formats:
            if postfix in element: imagelist.append(element)
    return imagelist_sort(imagelist)

def imagelist_sort(imagelist):
    '''sorts a list of image names for before and after as well as number, from smallest to largest'''
    for index in range(1,len(imagelist)):
        current_val = get_image_number(imagelist, index)
        position = index
        while position>0 and get_image_number(imagelist, position-1)>current_val:
            imagelist[position]=imagelist[position-1]
            position = position-1
        imagelist[position] = current_val
    for pair in range(len(imagelist)/2):
        if "after" in imagelist[pair*2]:
            imagelist_temp = imagelist
            imagelist[pair*2+1] = imagelist_temp[pair*2]
            imagelist[pair*2]   = imagelist_temp[pair*2+1] 
    return imagelist

def get_image_number(imagelist, index):
    '''returns the image pair number of a specific image index from imagelist'''
    return int(imagelist[index].split("_")[0])

def fetch_max_id():
    '''returns the maximum image pair id in imagelist'''
    max_id = -1
    imagelist = scan_image_filenames(local_directory)
    for image in imagelist:
        number = int(image.split("_")[0])
        if number > max_id: max_id = number
    return max_id

def setup_imagelist(directory, url):
    '''downloads an image set from a specific url to a specific variable, and sets up internal variables for image processing'''
    global imagelist
    set_directory(directory)
    fetch_images_github(url)
    reset_image_count()
    imagelist = scan_image_filenames()

def get_next_images():
    '''returns [[filename_before, filename_after], [(before_width,before_height),(after_width,after_height)]'''
    global image_count
    image_filenames = [imagelist[image_count], imagelist[image_count+1]]
    image_sizes = []
    for image in image_filenames:
        im = Image.open(local_directory+"/"+image)
        image_sizes.append(im.size)
    return image_filename, image_sizes 
