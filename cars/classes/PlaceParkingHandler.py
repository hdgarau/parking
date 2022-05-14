import logging

import cv2
import pickle
from tkinter import *
import glob
import numpy as np
import cvzone
from classes.PlaceParking import PlaceParking
import segno
import base64
import qrcode
from PIL import Image
from pyzbar import pyzbar

class PlaceParkingHandler():
    places = []
    fileInit = []
    lastVal = '' #Ultimo nombre ingresado
    posSize = (0,0)
    master = False
    e = False
    fileStorage = ''
    dataCameras = []
    pixelsMin = 0

    def __init__(self,posSize, fileStorage, pixelsMin = 0):
        self.posSize = posSize
        self.fileStorage = fileStorage
        self.pixelsMin = pixelsMin
        try:
            with open(self.fileStorage, "rb") as f:
                self.places = pickle.load(f)
        except:
            pass

    def render(self):
        for place in self.places:
            place.render()

    def add(self, Place):
        self.places.append(Place)

    def remove(self, i):
        return self.places.pop(i)

    def removeByPos(self, pos):
        for i,posPlace in enumerate(self.places):
            if posPlace.hasPoint(pos):
                self.remove(i)

    def editPlaces(self,event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.makeForm()
            if self.lastVal:
                self.add(PlaceParking(self.lastVal, (x, y), self.posSize, self.pixelsMin))
        if event == cv2.EVENT_RBUTTONDOWN:
            self.removeByPos((x,y))
        #Save changes
        self.save()

    def save(self):
        with open(self.fileStorage, "wb") as f:
            pickle.dump(self.places, f)

    def callbackOk(self,event=None):
        self.lastVal = self.e.get()
        self.master.destroy()

    def callbackCancel(self):
        lastVal = ''
        master.destroy()

    def makeForm(self):
        self.master = Tk()
        self.e = Entry(self.master)
        self.e.pack()
        b1 = Button(self.master, text="OK", width=10, command=self.callbackOk)
        self.e.bind("<Return>", self.callbackOk)
        b2 = Button(self.master, text="Cancel", width=10, command=self.callbackCancel)
        b1.pack()
        b2.pack()
        self.master.focus_set()
        self.e.focus_set()
        mainloop()

    def runEdit(self, fileName):
        while True:
            image = cv2.imread(fileName)
            imageProccessed = self.setImageToCheck(image)

            for i, placeParking in enumerate(self.places):
                placeParking.setAndCropImageProcessed(imageProccessed)
                placeParking.setStatus()
                placeParking.render(image)
                placeParking.renderPixels(image)
            cv2.imshow("Image", image)
            cv2.setMouseCallback("Image", self.editPlaces)
            cv2.waitKey(1)

    def run(self,fileName):
        image = cv2.imread(fileName)
        imageProccessed = self.setImageToCheck(image)
        for i, placeParking in enumerate(self.places):
            placeParking.setAndCropImageProcessed(imageProccessed)
            placeParking.setStatus()
        #cv2.imshow("test",image)

    def setImageToCheck(self,image):
        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        img = cv2.GaussianBlur(img, (3,3), 1)
        img = cv2.adaptiveThreshold( img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
        img = cv2.medianBlur(img, 5)
        kernel = np.ones((3, 3), np.int8)
        img = cv2.dilate(img, kernel, iterations=1)
        return img

    def setPlacesStatusByCameras(self, path):
        data = []
        for file in glob.glob(path + "\\*.data"):
            with open(file, "rb") as f:
                data= data + pickle.load(f)
        self.dataCameras = data

    def getMap(self, fileName):
        while True:
            image = cv2.imread(fileName)

            for i, placeParking in enumerate(self.places):
                pp = next((x for x in self.dataCameras if x.name == placeParking.name), None)
                #print(pp.name + ' ' + str(pp.status))
                placeParking.setStatus(pp.status[0] if pp != None else False)
                placeParking.render(image)
                #placeParking.renderPixels(image)
            cv2.imshow("Image", image)
            #cv2.imshow("QRImage", imageQR)
            #cv2.setMouseCallback("Image", self.editPlaces)
            cv2.waitKey(1)
