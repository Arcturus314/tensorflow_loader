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

def start_tensorflow():
    shell_source("/home/kaveh/tensorflow/bin/activate")
    os.popen("cd /home/kaveh/tensorflow/models/tutorials/image/imagenet")
def build_tensorflow_command():
    '''returns a tuple with the tensorflow commands required to process before and after images fetched from image_loader'''
    image_data = image_loader.get_next_image()
    cat_present = image_data[2]
    image_command= "python /home/kaveh/tensorflow/models/tutorials/image/imagenet/classify_image.py --image="+image_data[0]+" --input_width="+str(image_data[2][0])+" --input_height="+str(image_data[2][1])
    return image_command

def run_tensorflow():
    '''Runs imagenet with command fetched from build_tensorflow_command, returns output'''
    command = build_tensorflow_command()
    output = os.popen(command)
#    output_file = open(output, "r")
    print("Output follows:")
    for line in output:
        print(line)
    return output

def parse_tensorflow_data(data):
    '''returns a boolean, describing whether "cat" is in tensorflow output and in image filename, or inverse of this'''
    output = run_tensorflow()
#    output_file = open(output, "r")
#    output_lines = output.split("\n")
#    valid_output_lines = []
#    for line in output_lines:
#        if "=" in line:
#            valid_output_lines.append(line)

    if "cat," in output.read() and cat_present == True:
        return True
    if "cat" not in output.read() and cat_present == False:
        return True
    return False

def full_tensorflow_cycle():
    build_tensorflow_command()
    data = run_tensorflow()
    return parse_tensorflow_data(data)
     
