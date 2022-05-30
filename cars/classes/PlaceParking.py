import cv2
import cvzone
from datetime import datetime
from datetime import timedelta

import defines
from cars.classes.Renderer import Renderer

class PlaceParking():
    keepStatusOnFree = [defines.STATUS_SELECTED]
    pos = (0, 0)
    name = ''
    status = [None, None]
    pixelsMin = 250
    status_setted = None
    has_operator = False

    def __init__(self, name, pos, posSize, pixelsMin, hasOperator):
        self.name = name
        self.pos = pos
        self.posSize = posSize
        self.pixelsMin = pixelsMin
        self.has_operator = hasOperator

    def betweenX(self, pos):
        return self.pos[0] <= pos[0] and self.pos[0] + self.posSize[0] >= pos[0]
    def betweenY(self, pos):
        return self.pos[1] <= pos[1] and self.pos[1] + self.posSize[1] >= pos[1]


    def hasPoint(self, pos):
        return  self.betweenX(pos) and self.betweenY(pos)

    def render(self,image):
        image = Renderer().render(image,self.status,self.name,self.pos, self.posSize)

    def getPixels(self):
        return cv2.countNonZero(self.imageProcessed)

    def setAndCropImageProcessed(self, imageProcessed):
        self.imageProcessed = imageProcessed[self.pos[1]:self.pos[1] + self.posSize[1], self.pos[0]: self.pos[0] + self.posSize[0]]

    def renderPixels(self, image):
        cvzone.putTextRect(image,str(self.getPixels()),(self.pos[0], self.pos[1] + 40),scale=0.5, thickness=1)

    def hasCar(self):
        return self.getPixels() >= self.pixelsMin

    def setStatus(self,status = None):
        if status == None:
            if self.status[1] != None and self.status[1] + timedelta(seconds=3)  > datetime.now() or self.status == defines.STATUS_SELECTED:
                return
            if self.status_setted:
                status = self.status_setted
            else:
                if self.hasCar():
                    if self.status[0] == defines.STATUS_BUSSY:
                        return
                    if not self.has_operator or self.status[0] == defines.STATUS_SELECTED:
                        status = defines.STATUS_BUSSY
                    else:
                        status = defines.STATUS_BUSSY if not self.has_operator else defines.STATUS_BAD_PARKING
                else:
                    status = defines.STATUS_FREE if self.status[0] not in self.keepStatusOnFree else self.status[0]
        self.status = [status, datetime.now()]
