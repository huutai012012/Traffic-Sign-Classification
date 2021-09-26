''' 
									Đề Tài Nhận Diện Biển Báo Giao Thông 
										Tác giả:
											Đoàn Hữu Tài
											Nguyễn Hoàng Dương
											Đặng Thế Duy
											Kiều Văn Tấn
											Ngô Tín Khoa

'''


from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
from time import sleep
from threading import Thread
from function import *

#Biến tạm của Gui


#biến báo trại thái hiển thị
# 0 là ảnh màu
# 1 là ảnh xám
# 2 là ảnh nhịn phân
State = 150;
global PridictVal
PridictVal = np.array([100, 100, 100, 100, 100])

video = cv2.VideoCapture(1,cv2.CAP_DSHOW)



# Tạo cửa sổ GUI
window =Tk()
window.title('Đề Tài Nhận Diện Biển Báo Giao Thông')
window.geometry("1200x600")



# Load model
model = load_model('TSR.h5')




# Tạo canvas show video 

canvas_w = 800
canvas_h = 550
canvas = Canvas(window,width = canvas_w ,height = canvas_h, bg ='red')
canvas.pack()
canvas.grid(column = 0 ,row = 0)

# Tạo tiêu đề 
tieuDe = tk.Label(window,text = "Đề Tài Nhận Diện Biển Báo Giao Thông",fg="blue",font=("Arial",15))
tieuDe.place(relx = 1, x =-30, y = 10, anchor = NE)




# Tạo chữ tên biển báo
bienBao = tk.Label(window,text = "Tên biển báo :",fg="blue",font=("Arial",15))
bienBao.place(relx = 1, x =-205, y = 230, anchor = NE)




# Tạo txt in tên biển báo
tenBienBao = tk.Label(window,text = " ",fg="blue",font=("Arial",15))
tenBienBao.place(relx = 1, x =-100, y = 300, anchor = NE)





#tạo chữ Ngưỡng
nguong = tk.Label(window,text = "Chọn Ngưỡng : ",fg="blue",font=("Arial",15))
nguong.place(relx = 1,x =-190, y =170, anchor = NE)




# tạo danh sách chọn
DanhSach  = Combobox(window,font="Helvetica 10 bold")
DanhSach['value'] = (100,110,120,130,140,150,160,170,180)
DanhSach.current(5)  # set giá trị có trong combobox khi vừa mở lên ứng với index 0 trong list
DanhSach.place(relx = 1, x = -90,y=170,anchor = NE,height=30, width=60)




#  Tạo nút nhấn Set chế độ hiển thị
def handleButton():
	global State 
	State = DanhSach.get()
	return

hienThi = tk.Button(window,text = 'Hiển thị' , font="Helvetica 16 bold",height=2, width=10,bg ='sky blue', command = handleButton)
hienThi.place(relx = 1, x =-110, y = 70, anchor = NE)



#tạo nút thoát
def closeWindow():
	window.destroy()

close = tk.Button(window,text = 'Thoát',font="Helvetica 16 bold",height=2, width=10,bg ='sky blue',command=closeWindow)
close.place(relx = 1, x =-110, y = 500, anchor = NE)



def update_frame():
	global canvas, photo ,PridictVal
	ret,frame = video.read()  # lấy ảnh từ cap
	frame = cv2.resize(frame, dsize = None, fx= 1.3, fy=1.2)
	'''
	đoạn này để tập làm gui thôi à 
	if State == 'Ảnh màu':
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # chuyển hệ màu từ BGR sang RGB vì opencv dùng hệ màu BGR
	elif State == 'Ảnh xám':
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	else:
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		ret2,frame = cv2.threshold(frame,127,255,cv2.THRESH_BINARY_INV)
	'''


	contours,hierarchy = getContour(frame,int(State))
	if len(contours)>0:
		count = 0
		for i in range(0,len(contours)):
			area = cv2.contourArea(contours[i])
			if area>areaMin:				
				# điều kiện để tìm contour lớn hơn ereaMin pixel 
				#cv2.drawContours(img, contours, i, (0,255,0), 3)
				#khi tìm đc contour thứ i đủ điều kiện thì xét xem phải contour kín hay k rồi vẽ rectange vào
				peri = cv2.arcLength(contours[i], True)
				approx = cv2.approxPolyDP(contours[i], 0.02 * peri, True)
				# x y là tọa độ điểm đầu, w h là rộng và cao
				x , y , w, h = cv2.boundingRect(approx)
				if (x>fix)&((640-x)>fix)&(y>fix)&((480-y)>y):
					img_crop = frame[(y-fix):(y + h+ fix),(x-fix):(x + w + fix)]
					cv2.rectangle(frame, (x , y ), (x + w , y + h ), (0, 255, 0), 5)
					

				else: 
					img_crop = frame[(y):(y + h),(x):(x + w)]
					cv2.rectangle(frame, (x , y ), (x + w , y + h ), (0, 255, 0), 5)
				Y = model.predict_classes(preprocessing(img_crop))
				s = [str(i) for i in Y] 
				PridictVal[count] = int("".join(s))
				count = count + 1
				if count > 5:
					break







	# in kết quả và đặt lại giá trị PridicttVal
	strForShow = ""

	for i in range(0,4):
		if PridictVal[i]==100:
			continue
		print(classes[PridictVal[i]+1],end="			")
		strForShow = "".join([strForShow,(classes[PridictVal[i]+1]),"\n"])
	print("")
	tenBienBao.configure(text = strForShow )
	PridictVal = np.array([100, 100, 100, 100, 100])
	strForShow = ""



	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))  #chuyển ảnh từ numpy array (cv2) sang format của PIL
	canvas.create_image(0,0, image = photo , anchor=tk.NW ) # chuyển ảnh PIL sang canvas để hiện lên gui, anchor là điểm neo NW trên trái
	window.after(15,update_frame) # cứ sau 15ms sẽ chạy hàm update frame



update_frame()


window.mainloop() # hiển thị 