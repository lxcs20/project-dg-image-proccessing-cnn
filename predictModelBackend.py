

from keras.models import load_model
from skimage.transform import resize
import numpy as np
import cv2

class PredictDigit:

    #fill rectangle 
    def fillRect(self, img):
        #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(img, 20,255)
        conts, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        img2 = img.copy()
        for cont in conts:
            x,y,w,h = cv2.boundingRect(cont)
            cv2.rectangle(img2,(x,y),(x+w,y+h),(0,255,0),-1)
        return img2
    
    def cropImage(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img2 = self.fillRect(img)
        can = cv2.Canny(img2, 20, 200)
        contours, _hierarchy = cv2.findContours(can, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        crop_image = []
        for cnt in contours:
            x,y,w,h = cv2.boundingRect(cnt)
            pic = np.asarray(list(gray[y:y+h,x:x+w]))
            # Resize the image array
            new = resize(pic, (28, 28))
            crop_image.append(list(new))
        return crop_image
    
    def preDigit(self, crop_image, modelPath):
        model = load_model(modelPath)
        image_array = np.asarray(crop_image)
        result = np.argmax(model.predict(image_array))
        print(result)
        if result <= 11:
            la = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
            print(la[result])
        else:
            print("0")
    
    def Predict(self ,img, modelPath):
        self.preDigit(self.cropImage(img), modelPath)
        

myPredict = PredictDigit()

img = cv2.imread("digit8.png")
myPredict.Predict(img, "model/digit1")
