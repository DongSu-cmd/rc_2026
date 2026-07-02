import numpy as np 
 
arr = np.zeros((2,5))  
print(arr) 
arr = np.zeros((2,2,2))  
print(arr) 

img = cv2.imread("test.jpg")
img2 = np.zeros((100, 200))
img3 = np.zeros_like(img)
img4 = np.shape(img)
 
arr = np.ones(5)  
print(arr) 
arr = np.ones((2,2))  
print(arr)



print(type(img))
cv2.imshow("img", img)
cv2.imshow("img2", img2)
cv2.imshow("img3", img3)
cv2.waitKey(0)