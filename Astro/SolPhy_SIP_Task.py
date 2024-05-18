import astropy.io.fits as fits
import cv2
import numpy as np
import matplotlib.pyplot as plt


filename = input("Please enter the file name(with .fits extension): " )
with fits.open(filename) as hdul:
    image_data = hdul[0].data
    

normalized_image = ((image_data - image_data.min()) / (image_data.max() - image_data.min()) * 255)
jpeg_path = 'source_image.jpg' 
cv2.imwrite(jpeg_path, normalized_image)


sun = cv2.imread('source_image.jpg')
helios = cv2.imread('source_image.jpg')
gray_img = cv2.cvtColor(sun, cv2.COLOR_BGR2GRAY)
img = cv2.medianBlur(gray_img, 5)
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)


circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,120,param1=100,param2=30,minRadius=700,maxRadius=1250)
circles = np.uint16(np.around(circles))


for i in circles[0,:]:
   # draw the outer circle
   cv2.circle(sun,(i[0],i[1]),i[2],(0,255,0),5)
   # draw the center of the circle
   cv2.circle(sun,(i[0],i[1]),5,(255,0,0),5)
   print("\n\n\n\nRadius of the sun:",i[2])
   print("Coordinates of the center:({},{})  (In pixel-coordinates)\n\n\n\n".format(i[0],i[1]))

ret, bw_img = cv2.threshold(helios, 100, 255, cv2.THRESH_BINARY)     

cv2.imwrite("Limb_detected_sun.jpg", sun)
cv2.imwrite("Binary_sun.jpg", bw_img)

fig, axs = plt.subplots(1,2, figsize=(10,5))
axs[0].imshow(sun)
axs[0].set_title("Limb detected sun")
axs[1].imshow(bw_img)
axs[1].set_title("Binary image")

plt.tight_layout()
plt.show()
