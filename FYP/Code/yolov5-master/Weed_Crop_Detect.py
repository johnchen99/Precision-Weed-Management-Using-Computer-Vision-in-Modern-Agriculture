import argparse
import time
from pathlib import Path
import detect
import Weed_Crop_Detector_Preprocessing
import cv2
import os
import sys
import shutil
import torch
import torchvision
import torch.backends.cudnn as cudnn
import numpy as np
from numpy import random
from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
     scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path
from utils.plots import plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized


def main(path):

    image_name = str(path)
    path = "D://OneDrive - Asia Pacific University//UC3F2007CS//S2//FYP//Code//yolov5-master//frontend//src//assets//Images//%s" % (
        image_name)

    # Preprocess
    Weed_Crop_Detector_Preprocessing.mask_image_basic(path)

    # Detect photo, Bound >= 55% Confidence
    detect.main(["--weights", "D://OneDrive - Asia Pacific University//UC3F2007CS//S2//FYP//Code//yolov5-master//weights//best.pt",
                 "--source", "D://OneDrive - Asia Pacific University//UC3F2007CS//S2//FYP//Code//Carrot_Dataset//Preprocess_Temp",
                 "--conf-thres", "0.55", "--img-size", "966", "--save-txt", "--exist-ok",
                 "--project", "D://OneDrive - Asia Pacific University//UC3F2007CS//S2//FYP//Code//yolov5-master//frontend//src//assets"])

    # Read output, calculate and return midpoints
    coordinate = "D://OneDrive - Asia Pacific University//UC3F2007CS//S2//FYP//Code//yolov5-master//frontend//src//assets//exp//labels//Processed_Temp.txt"

    midpoint_array = []
    with open(coordinate, 'r+') as data:
        for line in data:
            lines = line.split()
            x = float(lines[1])
            y = float(lines[2])
            width = float(lines[3])
            height = float(lines[4])
            midpoint_x = (x + width)/2
            midpoint_y = (y + height)/2
            midpoint = str(round(midpoint_x, 5)) + ", " + \
                       str(round(midpoint_y, 5))
            midpoint_array.append(str(midpoint))

        # Remove original coordinates in txt
        data.truncate(0)
    return midpoint_array
# if __name__ == "__main__":
#     main()
