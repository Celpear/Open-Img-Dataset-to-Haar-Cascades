import os
import shutil
import argparse
import utils.progressBar as progressBar
import utils.scaler as scaler


# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='python3 convertProject2OpenCVHaar.py --output_dir haar-folder')

# Add arguments (e.g., input_folder and output_folder)
parser.add_argument('--data_dir', help='Path to the dataset folder', required=True)
parser.add_argument('--output_dir', help='Path to the output folder', required=True)

# Parse the command line arguments
args = parser.parse_args()

# Input
dataPath = args.data_dir
dataOutPath = args.output_dir
if dataPath.endswith("/"): dataPath = dataPath[:-1]
if dataOutPath.endswith("/"): dataOutPath = dataOutPath[:-1]

# Use the listdir method of os to get a list of all files in the directory
images = os.listdir(dataPath+"/")
# Use the listdir method of os to get a list of all files in the directory
labels = os.listdir(dataPath+"/Label/")

# Reset Files
if not os.path.exists(dataOutPath+"/"):
    # If not, create the folder
    os.makedirs(dataOutPath+"/")
    print(f"The folder {dataOutPath}/ was created.")
else:
    print(f"The folder {dataOutPath}/ already exists.")

# Check if the folder exists
if os.path.exists(dataOutPath):
    # Delete the contents of the folder
    shutil.rmtree(dataOutPath)
    print(f"The contents of the folder {dataOutPath} were deleted.")
else:
    print(f"The folder {dataOutPath} does not exist.")
if not os.path.exists(dataOutPath+"/img_p/"):
    # If not, create the folder
    os.makedirs(dataOutPath+"/img_p/")
    print(f"The folder {dataOutPath}img_p/ was created.")
else:
    print(f"The folder {dataOutPath}img_p/ already exists.")

cc_id = 0
cc_max = 0
for label in labels:
    # Open the file in read mode ('r')
    with open(dataPath+"/Label/"+label, 'r') as file:
        # Iterate through each line in the file
        for line in file:
            cc_max += 1

# Discover Labels
for label in labels:
    # Open the file in read mode ('r')
    with open(dataPath+"/Label/"+label, 'r') as file:
        # Iterate through each line in the file
        for line in file:
            # Process each line as needed
            # name_of_the_class    left    top     right     bottom
            data = line.strip().split()
            filename = label.replace(".txt","")
            # copy image to output
            # shutil.copy(datasetPath+"/"+imgSelect+"/"+filename+".jpg", outPath+"/img_p/"+str(cc_id)+".jpg")
            resize_box_pos = scaler.translateBoxes(line.strip(), dataPath+"/"+filename+".jpg", (2000, 2000),False)
            scaler.padAndSaveImage(dataPath+"/"+filename+".jpg", dataOutPath+"/img_p/"+str(cc_id)+".jpg",(2000, 2000))
            classe = resize_box_pos[0]
            left = float(resize_box_pos[1])
            top = float(resize_box_pos[2])
            right = float(resize_box_pos[3])
            bottom = float(resize_box_pos[4])
            # create pos.txt
            pos_file_path = dataOutPath+"/"+"pos.txt"
            with open(pos_file_path, 'a') as file:
                # Write the new line to the file
                file.write(f'{dataOutPath+"/img_p/"+str(cc_id)+".jpg"} {left} {top} {right} {bottom}' + '\n')
            progressBar.clear_screen()
            progressBar.progress_bar(cc_id, cc_max, prefix='Convert Progress:', suffix='', length=40)
            cc_id += 1
progressBar.clear_screen()
print("Convert Done!")
