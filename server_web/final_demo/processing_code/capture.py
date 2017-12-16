import cv2

name="front"
vidcap = cv2.VideoCapture('./'+name+'.mp4')

count = 0

while(vidcap.isOpened()):

    ret, image = vidcap.read()
    if(int(vidcap.get(1)) % 3 == 0):
        cv2.imwrite("./"+name+"/%d.jpg" % count, image)
        print('Saved frame%d.jpg' % count)
        count += 1

vidcap.release()
