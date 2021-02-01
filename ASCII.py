#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu Sep  3 18:34:58 2020
@author: aaronwright
Purpose: Recreate contours of images by pring characters to terminal
"""

# Import required libraries.
from PIL import Image
import sys

# Save all ASCII characters to string
ascii_char = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

# Types of brightness
AVERAGE = 1
LIGHTNESS = 2
LUMINOSITY = 3

# Colours
BLUE = '\033[94m'
GREEN = '\033[92m'
DEFAULT = ""
END = '\033[0m'


# For each row in pixels_matrix, create new row, and add the averaged RGB values.
# Append each row to the RGB matrix.
def rgb_conversion(matrix, brightness):
    rgb_matrix = []
    for row in matrix:
        rgb_row = []
        for values in row:
            # Determine brightness type.
            if brightness == AVERAGE:
                rgb_row.append(round(sum(values) / len(values)))
            elif brightness == LIGHTNESS:
                rgb_row.append((max(values) + min(values)) / 2)
            elif brightness == LUMINOSITY:
                rgb_row.append(.21*values[0] + .72*values[1] + .07*values[2])
        rgb_matrix.append(rgb_row)
        
    return rgb_matrix

# For each row in the pixel array, create new row and add the associated
# ascii character. Append each row the ascii character matrix.
def ascii_conversion(matrix, char):
    ascii_matrix = []
    for row in matrix:
            ascii_row = []
            for value in row:
                ascii_row.append(char[int(value / 255 * len(char))])
            ascii_matrix.append(ascii_row)     
            
    return ascii_matrix

# Import image and convert to RGB.
def import_image(path):
    # Import image and covert to RGB mode.
    try:
        img = Image.open(path).convert("RGB")    
        print("Image imported successfully!\nImage dimensions: "
          "{} x {}.".format(img.width, img.height))
    except:
        print("Image import unsuccessfull.")   
        
    return img

# Check if user wants to invert image
def ascii_inversion(ascii_char):
    # Request input
    while True:
        reverse = input("Invert? \nY (yes) : N (no) : E (exit): ")
        if reverse.lower() == "y" or reverse.lower() == "n":
            break
        elif reverse.lower() == "e":
            sys.exit()  
    # If user responds yes to inversion, reverse ascii character string.
    if reverse.lower() == "y":
        ascii_char = ascii_char[::-1]
        
    return ascii_char

# Check the brightnesss type
def brightness_check():
    brightness = 0
    while brightness not in range(1, 4):
        try:
            brightness = int(input("Brightness Type? \n1 (average) : 2 "
                               "(Lightness) : 3 (Luminosity): "))  
        except ValueError:
            print("\nPlease input an integer. Try again!")    
            
    return brightness

# Check the filter to be used
def select_filter(): 
    # Map colours
    colours = {1 : DEFAULT, 2 : BLUE, 3 : GREEN}  

    ascii_filter = 0
    while ascii_filter not in range(1, len(colours)+1):
        try:
            ascii_filter = int(input("Filter Type? \n1 (default) : 2 "
                               "(Blue) : 3 (Green): "))
        except ValueError:
            print("\nPlease input an integer. Try again!")
            
    colour = colours[ascii_filter]    
    
    return ascii_filter, colour
    
    
############### Start of Script ################

# Import image and covert to RGB mode.
path = "/Users/aaronwright/Documents/Programming/Python/Personal/ASCII/mum.jpg"
img = import_image(path)

# Check if image should be inverted.
ascii_char = ascii_inversion(ascii_char)

# Extract pixel RGB data to list & convert pixels list to array
pixels = list(img.getdata())
pixels_matrix = [pixels[i:i+img.width] for i in range(0, len(pixels), img.width)]

# Check brightness type
brightness = brightness_check()

# Check filter type
ascii_filter, colour = select_filter()

# Convert pixel data to RGB values before mapping to ascii_characters
rgb_matrix = rgb_conversion(pixels_matrix, brightness)
ascii_matrix = ascii_conversion(rgb_matrix, ascii_char)

# For each row in the ascii matrix, increase the character count and print without
# commas etc.
for row in ascii_matrix:
    line = [x for x in row]
    line = "".join(line)
    print("{}{}{}".format(colour, line, END))

print("\nPlease zoom out as far as you can and enjoy")

