import os 
import image_loader

def start_tensorflow():
    os.popen("source ~/tensorflow/bin/activate\ncd ~/models/tutorials/image/imagenet")

def build_tensorflow_commands():
    '''returns a tuple with the tensorflow commands required to process before and after images fetched from image_loader'''
    image_data = image_loader.get_next_images()
    image_before_command = "python classify_image.py --image="+image_data[0][0]+" input_width="+image_data[1][0][0]+" input_height="+image_data[1][0][1]
    image_after_command = "python classify_image.py --image="+image_data[0][1]+" input_width="+image_data[1][1][0]+" input_height="+image_data[1][0][1]
    return image_before_command, image_after_command

def run_tensorflow():
    commands = build_tensorflow_commands()
    output_before = os.popen(commands[0])
    output_after = os.popen(commands[1])
    print("before\n"+output_before)
    print("after\n"+output_after)
    return output_before, output_after

def parse_tensorflow_data(data):
    before_confidence = float(tensorflow_data[0].split("= ")[1].split(")")[0])
    after_confidence = float(tensorflow_data[1].split("= ")[1].split(")")[0])
    return before_confidence, after_confidence

def full_tensorflow_cycle():
    build_tensorflow_commands()
    data = run_tensorflow()
    return parse_tensorflow_data(data)
     
