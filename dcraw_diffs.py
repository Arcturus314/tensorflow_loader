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
    comp_output = ""
    shell_source(directory)
    comp_output = os.popen(dcraw_comp[0] + dcraw_execs[i] + dcraw_comp[1] + dcraw_dp[i] + " " + dcraw_v[i] + dcraw_comp[2])
    print("GCC Compilation Output for " + dcraw_dp[i] + " and " + dcraw_v[i] + "\n" + comp_output)

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
        #image renaming
        os.popen("mv " + image[0:-3]+".ppm " + output_filename)
        os.popen("rm " + image[0:-3]+".ppm")

#comparing images between DCraw versions
