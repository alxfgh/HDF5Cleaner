# Convert tiff to h5, replacing the dataset in the h5 file if it exists
# Usage: tifftoh5.py
import h5py
import numpy as np
import tifffile
import shutil
from tkinter import filedialog

# Get the input file name
tiff_file = filedialog.askopenfilename(title='Select TIFF file', filetypes=(('TIFF file', '*.tif'),))
original_h5_file = filedialog.askopenfilename(title='Select original H5 file', filetypes=(('H5 file', '*.h5'),))
new_h5_file = filedialog.asksaveasfilename(title='Save as', filetypes=(('H5 file', '*.h5'),), defaultextension='.h5')

#Close application if no file selected
if not tiff_file or not original_h5_file or not new_h5_file:
    print('No file selected')
    exit()

#Copy properties from original h5 file to new h5 file
shutil.copyfile(original_h5_file, new_h5_file)

# Open the input file in read mode
with h5py.File(new_h5_file, 'r+') as f:
    #Get the images from the tiff file
    tiff_images = tifffile.imread(tiff_file)
    #Load the images dataset
    images = f['Cube']['Images']
    #Overwrite the images dataset in the h5 file with numpy array
    images[...] = np.array(tiff_images)