import tensorflow_parser
import image_loader
import numpy
import math

#Reading settings from file
try:
    config_file = open("config.txt","r")
    config_file_text = config_file.read()
    config_lines = config_file_text.split(";")
    set1_dir = config_lines[0].split("=")[1]
    set2_dir = config_lines[1].split("=")[1]
    tensorflow_directory = config_lines[2].split("=")[1]
    two_directory_read == False
    if set1_dir != "": two_directory_read == True
    show_failed_filenames=False
    if config_lines[3].split("=")[1] == "Y": show_failed_filenames = True
    show_failed_labels=False
    if config_lines[4].split("=")[1] == "Y": show_failed_labels = True
except:
    print "Please create or format config.txt"

#printing settings
print "starting tensorflow with the following settings:"
print "directory 1:", set1_dir
if two_directory_read == True: print "directory 2:", set2_dir
print "tensorflow directory",tensorflow_directory
print "showing failed image filenames:", show_failed_filenames
print "showing failed image labels:", show_failed_labels

filename_list = []
label_list = []

def init_tensorflow(directory):
    #Sets required variables and starts processing
    global filename_list
    global label_list
    filename_list = []
    label_list = []
    image_loader.setup_imagelist(directory)
    image_loader.reset_image_count()
    tensorflow_parser.start_tensorflow(tensorflow_directory)

def process_images():
    #returns proportion of correct labels
    num_images = image_loader.fetch_num_images()
    print 'Processing ',num_images, ' images'
    num_correct = 0
    for i in range(num_images):
        output = tensorflow_parser.full_tensorflow_cycle()
<<<<<<< HEAD
        if output[0] == True: num_correct += 1
        if show_failed_filenames == True: print output[2]
        if show_failed_labels == True: print output[1]
=======
        if output == True:
		num_correct += 1
		print("Inceptionv3 matches label, current num correct:", num_correct)
	else: print("Inceptionv3 does not match label")
>>>>>>> d5fd5b4e5b6941572e738eac25a3a5b080fb56ee
    prop_correct = float(num_correct) / float(num_images)
    return prop_correct

def run_all(directory):
    quick_setup(directory)
    proportion = process_images()
    print 'Proportion identified correctly: ',proportion,' with ',proportion*image_loader.fetch_num_images(),' of ',image_loader.fetch_num_images(),' images'


print "-----PROCESSING IMAGES FROM DIRECTORY 1-----"
run_all(set1_dir)
if two_directory_read == True:
    print "-----PROCESSING IMAGES FROM DIRECTORY 2-----"
    run_all(set2_dir)
