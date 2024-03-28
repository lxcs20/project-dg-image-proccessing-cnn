import tkinter as tk
from tkinter import filedialog, LabelFrame
from PIL import Image, ImageTk

from keras.models import load_model
from skimage.transform import resize
import numpy as np
import cv2

window = tk.Tk()
window.title("Recognition Lao Alpabet form image")
window.geometry("550x350+400+200")

#load model
model = load_model("model/ac9896")


def predict(path):
    img  = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
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
    if result < 30:
        la = ["ກ", "ຂ", "ຄ", "ງ", "ຈ", "ສ", "ຊ", "ຍ", "ດ", "ຕ", "ຖ", "ທ", "ນ", "ບ", "ປ", "ຜ", 
        "ຝ", "ພ", "ຟ", "ມ","ຢ", "ຣ", "ລ", "ວ", "ຫ", "ອ", "ຮ", "ໜ", "ໝ", "ຫຼ"]
        #set text in label
        label.config(text="ຜົນການຈື່ຈຳຕົວອັກສອນ: " + str(la[result]))
    else:
        label.config(text = "ຂໍອາໄພສາມາດທຳນາຍໄດ້ພຽງເທື່ອລະຕົວອັກສອນ", width=35, font=10)
    

def openImage():   
    #open and load imamge
    path = filedialog.askopenfilename()
    image = Image.open(path)
    image = image.resize((200, 200), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, image=image, anchor=tk.NW)
    canvas.image = image
    canvas.pack()
    label.pack()
    predict(path)
    
group2 = LabelFrame(window, text="Predict", bg="#FFF8EA", padx= 10, pady=10)
group2.place(x = 0, y = 0)

group1 = LabelFrame(window, text="Predict", bg="#FFF8EA", padx= 10, pady=10)
group1.pack(fill="both", expand="yes")

button = tk.Button(group1, text = "ເປີດຮູບພາບ", width=15, fg = "#6C00FF", bg = "#F7F5EB", command = openImage)
button.pack()

group2 = LabelFrame(group1, bg="white")
group2.pack(pady=10)

canvas = tk.Canvas(group2, width = 200, height = 200)

label = tk.Label(group1,text = "", font=15, width=35, bg="#FFF8EA")

window.mainloop()