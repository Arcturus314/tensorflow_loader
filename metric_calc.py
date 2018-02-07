import tensorflow_parser
import image_loader
#import numpy
import math

#Reading settings from file
try:
    config_file = open("config.txt","r")
    config_file_text = config_file.read()
    config_lines = config_file_text.split(";")

    #mapping directories
    i = 0
    directories = [] #stores directory paths
    while "IMAGE_DIRECTORY" in config_lines[i]:
        directories.append(config_lines[i].split("=")[1])
        i += 1
    tensorflow_directory = config_lines[i].split("=")[1]
    output_filename = config_lines[i+1].split("=")[1]
    show_failed_filenames=False
    if config_lines[i+2].split("=")[1] == "Y": show_failed_filenames = True
    show_failed_labels=False
    if config_lines[i+3].split("=")[1] == "Y": show_failed_labels = True
except:
    print "Please create or format config.txt"
    quit()

#printing settings
print "starting tensorflow with the following settings:"
for i in range(len(directories)):
    print "directory",i,":",directories[i]
print "output filename :",output_filename
print "tensorflow directory :",tensorflow_directory
print "showing failed image filenames :", show_failed_filenames
print "showing failed image labels :", show_failed_labels

filename_list = []
label_list = []

#opening file
output_file = open(output_filename, "w")

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
    #returns proportion of correct labels, and adds failed image filenames and labels (contigent on setting) to list
    info_list = []
    num_images = image_loader.fetch_num_images()
    print 'Processing ',num_images, ' images'
    num_correct = 0
    for i in range(num_images):
        output = tensorflow_parser.full_tensorflow_cycle()
        if output[0] == True: num_correct += 1
	else:
            if show_failed_filenames == True: info_list.append(output[2])
            if show_failed_labels == True: info_list.append(output[1])
    prop_correct = float(num_correct) / float(num_images)
    return prop_correct, info_list

def run_all(directory):
    init_tensorflow(directory)
    output_list = process_images()
    proportion = output_list[0]
    proportion_print = 'Proportion identified correctly: '+str(proportion)+' with '+str(proportion*image_loader.fetch_num_images())+' of '+str(image_loader.fetch_num_images())+' images'
    print proportion_print
    output_file.write("------"+proportion_print)
    if (show_failed_filenames or show_failed_labels):
        print "Failed Images, Directory:", directory
        output_file.write("Failed Images, Directory:"+directory+"\n")
    for element in output_list[1]:
        print element
        output_file.write(element)
        output_file.write("\n")


for i in range(len(directories)):
    print "----- PROCESSING IMAGES FROM DIRECTORY",i,"-----"
    run_all(directories[i])
