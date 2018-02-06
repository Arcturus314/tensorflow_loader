#Kaveh Pezeshki
#Feb 5 2018
#Clay-Wolkin Research


#This script will compile two different versions of DCraw with separated _dp and _v files. It will then execute DCraw with a given set of options on 5 input Canon .CR2 images, and examine any differences in the binary files.

#imports necessary for command-line interaction
import os
import subprocess
from sys import exit


#-------------------USER SETTINGS----------------------

#file directory
directory = "/home/kaveh/tensorflow_loader"

#command line arguments for dcraw: ./<dcraw compiled name> <command line args> <image filename>
dcraw_args = " -r 1 1 1 1 -q 0 -H 0 "

#command line arguments for compiling dcraw
dcraw_comp = ["gcc -o "," -O4 ","-lm -DNODEPS"]

#image files to test on
image_filenames = ["IMG1.CR2", "IMG2.CR2", "IMG3.CR2", "IMG4.CR2", "IMG5.CR2"]

#input dcraw files to compile
#stored in two lists, where indices correspond to each of the two files to compile
dcraw_dp = ["dcraw1_dp.c", "dcrwa2_dp.c"]
dcraw_v  = ["dcraw1_v.c" , "dcraw1_v.c" ]

#names of output dcraw executables
dcraw_execs = ["dcraw1", "dcraw2", "dcraw3", "dcraw4", "dcraw5"]

#-----------END OF USER SETTINGS----------------------
output_image_filenames = []
comparisons = [] #list of lists of lists, with row and col headings being processing methods for each image, and there being a list of this comparison table for each image

def shell_source(script):
    pipe = subprocess.Popen(". %s; env" % script, stdout=subprocess.PIPE, shell=True)
    output = pipe.communicate()[0]
    env = dict((line.split("=", 1) for line in output.splitlines()))

#compiling DCraw versions
if len(dcraw_dp) != len(dcraw_v.c) or len(dcraw_dp) != len(dcraw_execs):
    sys.exit("cdraw dp and v file mismatch. Please check configuration")

for i in range(len(dcraw_dp)):
    #compiling
    comp_output = ""
    shell_source(directory)
    comp_output = os.popen(dcraw_comp[0] + dcraw_execs[i] + dcraw_comp[1] + dcraw_dp[i] + " " + dcraw_v[i] + dcraw_comp[2])
    print("GCC Compilation Output for " + dcraw_dp[i] + " and " + dcraw_v[i] + "\n" + comp_output)
    #testing compilation
    if dcraw_execs[i] not in os.listdir(directory):
        print("----COMPILATION FAILED: EXEC DOES NOT EXIST----")
        dcraw_execs.remove(dcraw_execs[i])
    else:
        print("----COMPILATION SUCCESSFUL----")

#testing DCraw versions on provided image sets
for exec_ver in dcraw_execs:
    for image in image_filenames:
        #image conversion
        print("Testing image " + image + " with DCraw version " + exec_ver)
        output_filename = image + "_" + exec_ver
        output_image_filenames += output_filename
        print("Output image filename: " + output_filename)
        output = os.popen("./"+exec_ver+dcraw_args+" "+image)
        print(output)
        #testing conversion
        if image[0:-3]+".ppm" not in os.listdir(directory):
            print("----IMAGE CONVERSION FAILED: .PPM NOT IN DIRECTORY----")
            output_image_filenames.remove(output_filename)
        else:
            print("----IMAGE CONVERSION SUCCESSFUL----")
            #image renaming
            os.popen("mv " + image[0:-3]+".ppm " + output_filename)
            os.popen("rm " + image[0:-3]+".ppm")

#comparing images between DCraw versions

for i in range(len(image_filenames)):
    #stores the filenames of the images that will be compared
    image_comp_names = []
    #stores the image comparison matrix
    image_comp_diffs = []

    #fetching image filenames
    for j in range(len(dcraw_execs)):
        image_comp.append(output_image_filenames[i+j*4])
    #the first row of the matrix is a header with filenames
    image_comp_diffs += image_comp_names

    #testing differences between files
    for img1 in image_comp:
        #differences for one row of the matrix: ex image 0 vs image 0, image 1, image 2, ...
        img1_diffs = []
        #cycling through images again
        for img2 in image_comp:
            #we don't need to run a test of an image against itself
            if img1 == img2:
                img1_diffs += "X" #we use an 'X' when a test is not necessary
            else:
                diff = os.popen("diff "+img1+" "+img2) #testing differences
                if "differ" in diff:
                    img1_diffs += "F"  #we use 'F' if the images differ
                else:
                    img1_diffs += "T"  #we use 'T' if the image are the same

        image_comp_diffs += img1_diffs #once all the comparisons for a specific image version are complete we append the results array to the comparison matrix

    comparisons += image_comp_diffs #once all the comparisons for a specific image are complete we append the comparison matrix the the complete comparison 3D matrix

#printing images

for image in comparisons:
    print("Results for image: " + image_filenames[comparisons.index(image)])
    for row in image:
        print(row)
