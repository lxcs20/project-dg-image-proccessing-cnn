import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Create the main window
window = tk.Tk()
window.title("Image Input")

# Create a function that will be called when the user clicks the "Browse" button
def browse_button():
    # Open a file browser dialog and get the selected file's path
    file_path = filedialog.askopenfilename()
    # Update the label with the file's path
    label.config(text=file_path)
    # Open the image file and display it in the canvas
    image = Image.open(file_path)
    image = image.resize((300, 300), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, image=image, anchor=tk.NW)
    canvas.image = image

# Create a "Browse" button that will call the browse_button function when clicked
browse_button = tk.Button(text="Browse", command=browse_button)
browse_button.pack()

# Create a label to display the selected file's path
label = tk.Label(text="No file selected")
label.pack()

# Create a canvas to display the image
canvas = tk.Canvas(width=300, height=300)
canvas.pack()

# Run the main loop
window.mainloop()
