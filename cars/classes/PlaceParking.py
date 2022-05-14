import cv2
import cvzone
from datetime import datetime

class PlaceParking():
    pos = (0, 0)
    name = ''
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.5
    posText = (0, -50)
    colorText = (0, 0, 0)
    thickness = 2
    colorRectangleNotCar = (0,255,0)
    colorRectangleCar = (0,0,255)
    posSize = (0, 0)
    status = [False, '']
    pixelsMin = 250

    def __init__(self, name, pos, posSize, pixelsMin):
        self.name = name
        self.pos = pos
        self.posSize = posSize
        self.pixelsMin = pixelsMin

    def betweenX(self, pos):
        return self.pos[0] <= pos[0] and self.pos[0] + self.posSize[0] >= pos[0]
    def betweenY(self, pos):
        return self.pos[1] <= pos[1] and self.pos[1] + self.posSize[1] >= pos[1]


    def hasPoint(self, pos):
        return  self.betweenX(pos) and self.betweenY(pos)

    def render(self,image):
        cv2.rectangle(image, self.pos + self.posSize, self.colorRectangleCar if self.status[0] else self.colorRectangleNotCar, self.thickness)
        #imgok = cv2.imread("cars\\images\\bussy.jpg")
        #image[0:44,0:44,0:3] = imgok
        image = cv2.putText(image, self.name, self.pos  , self.font, self.fontScale, self.colorText, self.thickness, cv2.LINE_4)

    def getPixels(self):
        return cv2.countNonZero(self.imageProcessed)

    def setAndCropImageProcessed(self, imageProcessed):
        self.imageProcessed = imageProcessed[self.pos[1]:self.pos[1] + self.posSize[1], self.pos[0]: self.pos[0] + self.posSize[0]]

    def renderPixels(self, image):
        cvzone.putTextRect(image,str(self.getPixels()),(self.pos[0], self.pos[1] + 40),scale=0.5, thickness=1)

    def hasCar(self):
        return self.getPixels() >= self.pixelsMin

    def setStatus(self,status = None):
        self.status = [self.hasCar() if status == None else status, datetime.now()]