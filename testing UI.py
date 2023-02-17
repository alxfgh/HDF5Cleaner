import h5py
import numpy as np
import tifffile
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Progressbar

# Create a Tkinter root window
root = tk.Tk()

# Center the window on the screen
root.withdraw()
root.update_idletasks()
x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
root.geometry("+%d+%d" % (x, y))

# Define a function to handle file conversion
def convert_file():
    # Open a file dialog box to allow the user to select the input file
    input_file_path = filedialog.askopenfilename()

    # Open the input file in read mode
    with h5py.File(input_file_path, 'r') as f:

        # Get the 'Images' dataset from the root group
        images = f['Images']

        # Convert the dataset to a numpy array
        data = np.array(images)

        # Open a file dialog box to allow the user to select the output folder and file name
        output_file_path = filedialog.asksaveasfilename(initialdir='/', title='Save as', filetypes=(('TIFF files', '*.tif'),))

        # Add the .tif extension to the file name if not present
        if not output_file_path.endswith('.tif'):
            output_file_path += '.tif'

        # Initialize progress bar
        progress = Progressbar(root, orient="horizontal", length=200, mode="determinate")
        progress.pack(pady=10)

        # Convert and save the numpy array as a 16-bit TIFF file
        tifffile.imwrite(output_file_path, data, imagej=True, plugin='tifffile')
        progress['value'] = 100

        # Show success message
        messagebox.showinfo("Success", "File conversion successful.")

# Define a function to handle moving data around
def move_data():
    # Open a file dialog box to allow the user to select the input file
    input_file_path = filedialog.askopenfilename()

    # Open the input file in read mode
    with h5py.File(input_file_path, 'r') as f:

        # Create a new output file in write mode
        with h5py.File('outputconversion3.h5', 'w') as f_out:

            # Copy the 'Images' subgroup from the 'Cube' group in f to the 'Data' group in f_out
            f.copy('/Cube/Images', dest=f_out)

        # Show success message
        messagebox.showinfo("Success", "Data move successful.")

# Create a button to move data around
move_data_button = tk.Button(text="Move Data", command=move_data, height=2, width=20)

# Pack the button into the root window
move_data_button.pack(pady=10)

# Create a button to select a file and convert it
convert_button = tk.Button(text="Convert", command=convert_file, height=2, width=20)

# Pack the button into the root window
convert_button.pack(pady=10)



# Start the Tkinter main loop
root.deiconify()
root.mainloop()
