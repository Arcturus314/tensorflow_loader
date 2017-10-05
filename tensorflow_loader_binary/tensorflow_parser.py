import os 
import image_loader
import subprocess
levels = 100
cat_present = False

def shell_source(script):
    pipe = subprocess.Popen(". %s; env" % script, stdout=subprocess.PIPE, shell=True)
    output = pipe.communicate()[0]
    env = dict((line.split("=", 1) for line in output.splitlines()))
    os.environ.update(env)

def start_tensorflow(tensorflow_directory):
    shell_source(tensorflow_directory+"/bin/activate")
    os.popen("cd " + tensorflow_directory + "/models/tutorials/image/imagenet")

def build_tensorflow_command():
    '''returns a tuple with the tensorflow commands required to process before and after images fetched from image_loader'''
    image_data = image_loader.get_next_image()
    image_filename = image_data[0]
    cat_present = image_data[1]
    image_command= "python " + tensorflow_directory + "/models/tutorials/image/imagenet/classify_image.py --image="+image_filename+" --input_width="+str(image_data[2][0])+" --input_height="+str(image_data[2][1])
    return image_command,image_filename

def run_tensorflow():
    '''Runs imagenet with command fetched from build_tensorflow_command, returns output'''
    #global output_print
    command = build_tensorflow_command()
<<<<<<< HEAD
    output = os.popen(command[0])
    output_string = output.read()
    output_string = output_string.replace('\n', ' ').replace('\r', '')
    return output_string, command[1]
=======
    output = os.popen(command)
    output_string = output.read()
    output_string = output_string.replace('\n', ' ').replace('\r', '')
    print output_string
    #output_print = output
    #for line in output_print:
    #    print(line)
    return output_string
>>>>>>> d5fd5b4e5b6941572e738eac25a3a5b080fb56ee

def parse_tensorflow_data(data):
    '''returns a boolean, describing whether "cat" is in tensorflow output and in image filename, or inverse of this'''

<<<<<<< HEAD
    if "cat," in data and cat_present == True:
=======
    if "cat" in data and cat_present == True:
>>>>>>> d5fd5b4e5b6941572e738eac25a3a5b080fb56ee
        return True
    if "cat" not in data and cat_present == False:
        return True
    #for line in output_print:
    #    print line
    return False

def full_tensorflow_cycle():
    #returns a boolean indicating whether inception provided the correct label, the inception output, and the image filename
    data = run_tensorflow()
    return parse_tensorflow_data(data[0]),data[0],data[1]
     
