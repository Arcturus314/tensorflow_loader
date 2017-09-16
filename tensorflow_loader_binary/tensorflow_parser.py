import os 
import image_loader
levels = 100
cat_present = False

def start_tensorflow():
    os.popen("source ~/tensorflow/bin/activate\ncd ~/models/tutorials/image/imagenet")

def build_tensorflow_command():
    '''returns a tuple with the tensorflow commands required to process before and after images fetched from image_loader'''
    image_data = image_loader.get_next_image()
    cat_present = image_data[2]
    image_command= "python classify_image.py --image="+image_data[0]+" input_width="+image_data[2][0]+" input_height="+image_data[2][1]
    return image_command

def run_tensorflow():
    '''Runs imagenet with command fetched from build_tensorflow_command, returns output'''
    command = build_tensorflow_command()
    output = os.popen(command)
    print("output\n"+output)
    return output

def parse_tensorflow_data(data):
    '''returns a boolean, describing whether "cat" is in tensorflow output and in image filename, or inverse of this'''
    output = run_tensorflow()

#    output_lines = output.split("\n")
#    valid_output_lines = []
#    for line in output_lines:
#        if "=" in line:
#            valid_output_lines.append(line)

    if "cat," in output and cat_present == True:
        return True
    if "cat" not in output and cat_present == False:
        return True
    return False

def full_tensorflow_cycle():
    build_tensorflow_commands()
    data = run_tensorflow()
    return parse_tensorflow_data(data)
     
