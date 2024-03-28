#library GUI
import tkinter as tk
from tkinter import filedialog, LabelFrame
from PIL import Image, ImageTk
#model and image
from skimage.transform import resize
from keras.models import load_model
import numpy as np
import cv2

#defind tkinter gui
window = tk.Tk()
window.title("Recognition Lao Alpabet")
window.geometry("550x350+400+200")
window.config(bg = "#856ff8")

#load model
model = load_model("model/ac9618")

#predict function
def openImage():
    #open and load imamge
    path = filedialog.askopenfilename()
    image = Image.open(path)
    image = image.resize((150, 150), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, image=image, anchor=tk.NW)
    canvas.image = image
    canvas.pack()

    img  = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #
    canny = cv2.Canny(img, 20,255)
    conts, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    img2 = img.copy()
    for cont in conts:
        x,y,w,h = cv2.boundingRect(cont)
        cv2.rectangle(img2,(x,y),(x+w,y+h),(0,255,0),-1)

    can = cv2.Canny(img2, 20, 200)
    contours, _hierarchy = cv2.findContours(can, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    crop_image = []
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        pic = np.asarray(list(gray[y:y+h,x:x+w]))
        # Resize the image array
        new = resize(pic, (32, 32))
        crop_image.append(list(new))
        
    #predict and diplay result
    image_array = np.asarray(crop_image)
    result = np.argmax(model.predict(image_array))
    print(result)
    la = ["ກ", "ຂ", "ຄ", "ງ", "ຈ", "ສ", "ຊ", "ຍ", "ດ", "ຕ", "ຖ", "ທ", "ນ", "ບ", "ປ", "ຜ", 
    "ຝ", "ພ", "ຟ", "ມ","ຢ", "ຣ", "ລ", "ວ", "ຫ", "ອ", "ຮ", "ໜ", "ໝ", "ຫຼ"]
    #set text in label
    label.config(text=str(la[result]))
    label.pack()

group1 = LabelFrame(window, text="Predict", bg="#FFF8EA", padx= 10, pady=10)
group1.pack(fill="both", expand="yes")

#button input image
button = tk.Button(group1, text = "Open Image", fg = "#6C00FF", bg = "#F7F5EB", command = openImage)
button.pack()

group2 = LabelFrame(group1, bg="white")
group2.pack()

#canvas image
canvas = tk.Canvas(group2, width = 150, height = 150)

#label result
label = tk.Label(group1,text = "", font=15, width=5, bg="#FFF8EA")

#runwindow tkinter
window.mainloop()