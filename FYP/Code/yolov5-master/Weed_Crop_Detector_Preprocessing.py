from cv2 import cv2
import numpy as np
import Augmentor
import os


# Base Input Image:
#####################################
# Channel 0 = Red (R)               #
# Channel 1 = Near-Infrared (NIR)   #
# Channel 2 = Red                   #
#####################################

def main():
    file_index = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20",
                 "21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40",
                 "41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59","60"]
    
    # Mask plants from soil
    mask_image(file_index)

    # Augmentation (60->140)
    aug_image(file_index)

    # Rename Augmented Pictures
    rename_images("D://OneDrive - Asia Pacific University//UC3F2007CS//S2//FYP//Code//Carrot_Dataset//Base_Masked_Images//output//")

# Output Masked Images
def mask_image(file_index):
    for item in file_index:
        file_num = file_index[int(item)-1]
        file_name = "%s_mask" % (int(item))
        path = "D:\\OneDrive - Asia Pacific University\\UC3F2007CS\\S2\\FYP\\Code\\Carrot_Dataset\\Images\\0%s_image.png" % (file_num)
        mask_write_path = "D:\\OneDrive - Asia Pacific University\\UC3F2007CS\\S2\\FYP\\Code\\Carrot_Dataset\\Base_Masked_Images\\"+file_name+".png" 
        image = cv2.imread(path)
        #cv2.imshow("Input Image",input_image)
        if image is None: 
            print ("Masking: Could not open image.")
            return -1
        else:

            # Median blur - Remove salt-and-pepper noise
            input_image = cv2.medianBlur(image,7)

            # Extract RED and NIR channels
            Red_Image = input_image[:,:,0]
            NIR_Image = input_image[:,:,1]   
            
            # Obtain NDVI Mask (Normalized Difference Vegetation Index) and OTSU binarization
            NDVI_Mask = ndvi_otsu_thresh(Red_Image, NIR_Image)

            # Apply Mask (Remove Soil for training)
            Masked_Image = input_image.copy()
            Masked_Image = cv2.bitwise_and(image,image,mask = NDVI_Mask)
            cv2.imwrite(mask_write_path, Masked_Image) 

            # Resize image (For display only)
            # input_image= resize_image(Masked_Image, 100)
            # cv2.waitKey(0)  # Wait for any keystroke in the window
            
# Output Masked Images
def mask_image_basic(path):
    image = cv2.imread(path)
    if image is None: 
        print ("Masking: Could not open image.")
        return -1
    else:
        # Median blur - Remove salt-and-pepper noise
        input_image = cv2.medianBlur(image,7)

        # Extract RED and NIR channels
        Red_Image = input_image[:,:,0]
        NIR_Image = input_image[:,:,1]   
        
        # Obtain NDVI Mask (Normalized Difference Vegetation Index) and OTSU binarization
        NDVI_Mask = ndvi_otsu_thresh(Red_Image, NIR_Image)

        # Apply Mask (Remove Soil for training)
        Masked_Image = input_image.copy()
        Masked_Image = cv2.bitwise_and(image,image,mask = NDVI_Mask)
        temp_folder = "D://OneDrive - Asia Pacific University//UC3F2007CS//S2//FYP//Code//Carrot_Dataset//Preprocess_Temp//Processed_Temp.png"
        cv2.imwrite(temp_folder, Masked_Image) 
        
# Output Augmented Masked Images
def aug_image(file_index):
    p = Augmentor.Pipeline("D://OneDrive - Asia Pacific University//UC3F2007CS//S2//FYP//Code//Carrot_Dataset//Base_Masked_Images")
    p.rotate(probability=0.8, max_left_rotation=10, max_right_rotation=10)
    p.zoom(probability=0.5, min_factor=1.1, max_factor=1.6)
    
    # Produce 140 augmentedimages
    p.sample(140)           

# NDVI masking + OTSU thresholding
def ndvi_otsu_thresh(Red_Image, NIR_Image):
    #print(np.iinfo(Red_Image.dtype)) #Return min-max pixel value
    # Normalize to float ( 0-1 ) for calculations
    Red_Image = cv2.normalize(Red_Image, None, 0, 1, cv2.NORM_MINMAX, cv2.CV_32FC1)
    NIR_Image = cv2.normalize(NIR_Image, None, 0, 1, cv2.NORM_MINMAX, cv2.CV_32FC1)
    
    # Obtain NDVI 
    NDVI_Mask = (NIR_Image - Red_Image) / (NIR_Image + Red_Image)

    # Normalize back to 8-bit ( 0-255 )
    NDVI_Mask = cv2.normalize(NDVI_Mask, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
    
    # Masking with OTSU (+tuning) Thresholding
    th, _ = cv2.threshold(NDVI_Mask, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    _, NDVI_Mask = cv2.threshold(NDVI_Mask, th+10,  255, cv2.THRESH_BINARY)
    
    # Morphological Transformations - Remove salt-and-pepper noise
    kernal = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))

    # Opening
    NDVI_Mask = cv2.morphologyEx(NDVI_Mask, cv2.MORPH_OPEN, kernal, iterations = 1)

    # Dilation
    NDVI_Mask = cv2.dilate(NDVI_Mask, kernal, iterations = 1)

    # Region filling
    floodfill = NDVI_Mask.copy()
    h, w = NDVI_Mask.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8) # Mask: +2 pixels larger than img
    cv2.floodFill(floodfill, mask, (0,0), 255) # Floodfill background - white
    floodfill_inv = cv2.bitwise_not(floodfill) # Invert
    NDVI_Mask = NDVI_Mask | floodfill_inv # bitwise OR 

    return NDVI_Mask

# Rename all augmented images
def rename_images (path):
    os.getcwd()
    for i, filename in enumerate(os.listdir(path)):
        os.rename(path + filename, path + str(i+1) + "_aug.png")

# Resize Image for Output 
def resize_image (input_image, scale_percent):
    width = int(input_image.shape[1] * scale_percent / 100)
    height = int(input_image.shape[0] * scale_percent / 100)
    dimension = (width, height)
    output_image = cv2.resize(input_image, dimension, interpolation = cv2.INTER_AREA)  
    return output_image

if __name__ == "__main__":
    main()