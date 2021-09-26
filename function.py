'''
						Functions file chứa các hàm cần dùng 
'''
from keras.models import load_model
from tkinter import*
from tkinter import filedialog
from PIL import ImageTk, Image
import numpy as np
import cv2
areaMin = 6000
fix = 20
classes = { 1:'Speed limit (20km/h)',
            2:'Speed limit (30km/h)',      
            3:'Speed limit (50km/h)',       
            4:'Speed limit (60km/h)',      
            5:'Speed limit (70km/h)',    
            6:'Turn right ahead',  #Speed limit (80km/h)    
            7:'End of speed limit (80km/h)',     
            8:'Speed limit (100km/h)',    
            9:'Speed limit (120km/h)',     
           10:'No passing',   
           11:'No passing veh over 3.5 tons',     
           12:'Right-of-way at intersection',     
           13:'Priority road',    
           14:'Yield',     
           15:'Stop',       
           16:'No vehicles',       
           17:'Veh > 3.5 tons prohibited',       
           18:'No entry',       
           19:'General caution',     
           20:'Dangerous curve left',      
           21:'Dangerous curve right',   
           22:'Double curve',      
           23:'Bumpy road',     
           24:'Slippery road',       
           25:'Road narrows on the right',  
           26:'Road work',    
           27:'',      
           28:'Pedestrians',     
           29:'Children crossing',     
           30:'Bicycles crossing',       
           31:'Beware of ice/snow',
           32:'Wild animals crossing',      
           33:'End speed + passing limits',      
           34:'Turn right ahead',     
           35:'Turn left ahead',       
           36:'Ahead only',      
           37:'Go straight or right',      
           38:'Go straight or left',      
           39:'Keep right',     
           40:'Keep left',      
           41:'Roundabout mandatory',     
           42:'End of no passing',      
           43:'Turn right ahead' }#End no passing veh > 3.5 tons

'''
Ảnh đưa vào phải trong không gian màu hsv
Hàm trả về ảnh của các đối tượng màu đỏ
img là ảnh gốc đọc từ cam, imgHSV là ảnh chuyển sang không gian màu HSV
Tương tự cho các màu khác
'''
def detectRed(img):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0,50,100])
    upper_red = np.array([10,255,255])
    red_mask = cv2.inRange(imgHSV, lower_red, upper_red)
    red = cv2.bitwise_and(img, img, mask=red_mask)
    return red
def detectBlue(img):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    low_blue = np.array([94, 50, 2])
    high_blue = np.array([126, 255, 255])
    blue_mask = cv2.inRange(imgHSV, low_blue, high_blue)
    blue = cv2.bitwise_and(img, img, mask=blue_mask)
    return blue
def detect(img):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    low = np.array([0, 42, 0])
    high = np.array([179, 255, 255])
    mask = cv2.inRange(imgHSV, low, high)
    result = cv2.bitwise_and(img, img, mask=mask)
    return result
'''
Hàm tìm biên dạng của ảnh, img là ảnh đầu vào:
Làm mờ ảnh => chuyển ảnh xám => lọc canny để tách biên => tìm contour và thứ tự contour(hierarchy)

trong hàm Canny 25 25 là các threshold: có thể thay đổi để tìm biên tốt hơn
'''
def getContour(img,thresholdVal):
    imgBlur = cv2.GaussianBlur(img,(7,7),0)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    ret,imgBin = cv2.threshold(imgGray,thresholdVal,255,cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(imgBin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return contours, hierarchy

# hàm dự đoán: input là im
def test_on_img(img):
    data=[]
    image = Image.open(img)
    image = image.resize((30,30))
    data.append(np.array(image))
    X_test=np.array(data)
    Y_pred = model.predict_classes(X_test)
    return image,Y_pred


# Hàm dự đoán
def preprocessing(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(img)
    data=[]   
    image = im_pil.resize((30,30))
    data.append(np.array(image))
    X_test=np.array(data)
    return X_test

    