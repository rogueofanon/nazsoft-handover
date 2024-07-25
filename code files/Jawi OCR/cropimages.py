import cv2
import os
from PIL import Image
import numpy as np
import argparse

def crop_white_space(image_path, output_path, padding=10):
    """
    Helper function to crop the white space out of an image.
    """
    #Read the image
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    #Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #Create a binary mask where white is 255, and black is 0
    _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

    #Invert the binary amsk
    binary = cv2.bitwise_not(binary)

    #Sum the columns to find where text starts
    column_sum = np.sum(binary, axis=0)

    # Find the first column where the sum is greater than zero
    for i, sum_value in enumerate(column_sum):
        if sum_value > 0:
            break

    #Add padding
    crop_start = max(i - padding, 0)

    #Crop the image from this column to the end
    cropped_image = image[:, crop_start:]

    #Save the cropped image
    cv2.imwrite(output_path, cropped_image)

def process_folder(input_folder, output_folder):
    """
    Helper function to crop through all images in the input folder to the output folder.
    """
    #Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    #Process each image in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            crop_white_space(input_path, output_path)
            print(f"Cropped and saved: {filename}")

def main():
    parser = argparse.ArgumentParser(description="Crop whitespace out of images in a folder.")
    parser.add_argument("input_folder", type=str, help="The folder containing the input images.")
    parser.add_argument("output_folder", type=str, help="The output folder.")
    parser.add_argument("--padding", type=int, default=10, help="Amount of padding on the side.")
    args = parser.parse_args()

    process_folder(args.input_folder, args.output_folder)

if __name__ == "__main__":
    main()