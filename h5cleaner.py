import h5py
import numpy as np
import tifffile
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import sys, os
def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Create a Tkinter root window
root = tk.Tk()

# Set the title of the window
root.title('H5 Cleaner')

# Set the icon of the window
root.iconbitmap(resource_path('icon.ico'))

# Center the window on the screen
root.withdraw()
root.update_idletasks()

#Set the size of the window and center it on the screen
root.geometry("300x200")
x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
root.geometry("+%d+%d" % (x, y))




# Define a function to handle file conversion to 16 bit TIFF
def convert_file_16bit():
    # Open a file dialog box to allow the user to select the input file
    input_file_path = filedialog.askopenfilename()

    # Open the input file in read mode
    with h5py.File(input_file_path, 'r') as f:

        # Get the 'Images' dataset from the root group
        #images = f['Images']

        if 'Images' in f:
            # Get the 'Images' dataset from the root group
            images = f['Images']
        else:
            # Get the 'Images' dataset from the '/Cube/Images' subgroup
            images = f['/Cube/Images']

        # Convert the dataset to a numpy array
        data = np.array(images).astype(np.uint16)

        # Open a file dialog box to allow the user to select the output folder and file name
        output_file_path = filedialog.asksaveasfilename(title='Save as', filetypes=(('TIFF file', '*.tif'),))

        # Add the .tif extension to the file name if not present
        if not output_file_path.endswith('.tif'):
            output_file_path += '.tif'

        # Convert and save the numpy array as a 16-bit TIFF file
        tifffile.imwrite(output_file_path, data, imagej=True)

        # Show success message
        messagebox.showinfo("Success", "File conversion to 16-bit TIFF was successful.")

# Define a function to handle file conversion to 32 bit TIFF
def convert_file_32bit():
    # Open a file dialog box to allow the user to select the input file
    input_file_path = filedialog.askopenfilename()

    # Open the input file in read mode
    with h5py.File(input_file_path, 'r') as f:

        # Get the 'Images' dataset from the root group
        #images = f['Images']

        if 'Images' in f:
            # Get the 'Images' dataset from the root group
            images = f['Images']
        else:
            # Get the 'Images' dataset from the '/Cube/Images' subgroup
            images = f['/Cube/Images']

        # Convert the dataset to a numpy array
        data = np.array(images)

        # Open a file dialog box to allow the user to select the output folder and file name
        output_file_path = filedialog.asksaveasfilename(title='Save as', filetypes=(('TIFF file', '*.tif'),))

        # Add the .tif extension to the file name if not present
        if not output_file_path.endswith('.tif'):
            output_file_path += '.tif'

        # Convert and save the numpy array as a 16-bit TIFF file
        tifffile.imwrite(output_file_path, data, imagej=True)

        # Show success message
        messagebox.showinfo("Success", "File conversion to 32-bit TIFF was successful.")

# Define a function to handle moving data around
def move_data():
    # Open a file dialog box to allow the user to select the input file
    input_file_path = filedialog.askopenfilename()

    # Open the input file in read mode
    with h5py.File(input_file_path, 'r') as f:

        # Create a new output file using a file dialog box in write mode
        output_file_path = filedialog.asksaveasfilename(title='Save as', filetypes=(('HDF5 file', '*.h5'),) , defaultextension='.h5')

        # Add the .tif extension to the file name if not present
        if not output_file_path.endswith('.h5'):
            output_file_path += '.h5'

        # Create a new output file in write mode
        with h5py.File(output_file_path, 'w') as f_out:

            # Copy the 'Images' subgroup from the 'Cube' group in f to the 'Data' group in f_out
            f.copy('/Cube/Images', dest=f_out)

        # Show success message
        messagebox.showinfo("Success", "Dataset was moved to root folder succesfully.")

# Create a button to select a file and convert it
convert_button = tk.Button(text="Convert to 16-bit TIFF", command=convert_file_16bit, height=2, width=20)

# Pack the button into the root window
convert_button.pack(pady=10)

# Create a button to select a file and convert it
convert_button = tk.Button(text="Convert to 32-bit TIFF", command=convert_file_32bit, height=2, width=20)

# Pack the button into the root window
convert_button.pack(pady=10)

# Create a button to move data around
move_data_button = tk.Button(text="Move dataset for ImageJ", command=move_data, height=2, width=20)

# Pack the button into the root window
move_data_button.pack(pady=10)

# Create a Label widget and place it in the bottom left corner of the window
copyright_label = tk.Label(root, text="v1.0 / Alexander Al-Feghali", font=("Arial", 8))
copyright_label.pack(side="right", anchor="sw")

# Start the Tkinter main loop
root.deiconify()
root.mainloop()