import tensorflow_parser
import image_loader
import numpy
import math
from scipy.stats import norm

def init_tensorflow(directory, url):
    image_loader.setup_imagelist(directory,url)
    tensorflow_parser.start_tensorflow()

def process_images(): #returns mean and standard deviation of confidence for both sets
    pair_number = image_loader.fetch_max_id()
    before_confidences = []
    after_confidences = []
    for i in xrange(pair_number):
        pair_data = full_tensorflow_cycle()
        before_confidences.append(pair_data[0])
        after_confidences.append(pair_data[1])
    return numpy.mean(before_confidences),numpy.std(before_confidences,1),numpy.mean(after_confidences),numpy.std(after_confidences,1)

def two_sample_z(mean_a, mean_b, stddev_a, stddev_b, conf_level):
    normalized_parameter = (mean_a-mean_b)/(math.sqrt(stddev_a^2+stddev_b^2))
    if normalized_parameter>0:
        if 1-norm.cdf(normalized_parameter) < conf_level/2: print("Mean of population a > mean of population b to within given confidence level")
        print("No conclusion can be found")
    if normalized_parameter<0:
        if norm.cdf(normalized_parameter) < conf_level/2: print("Mean of population b > mean of population a to within given confidence level")
        print("No conclusion can be found")

def run_all(conf_level):
    image_stats = process_images()
    print("sample a is before processing\nsample b is after processing")
    two_sample_z(image_stats[0],image_stats[1],image_stats[2],image_stats[3],conf_level)
