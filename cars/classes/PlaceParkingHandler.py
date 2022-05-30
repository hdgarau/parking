import logging

import cv2
import pickle
from tkinter import *
import glob

import defines
import numpy as np
import cvzone
from classes.PlaceParking import PlaceParking
import segno
import base64
from classes.Renderer import Renderer

class PlaceParkingHandler():
    places = []
    path = ''
    fileInit = []
    lastVal = '' #Ultimo nombre ingresado
    posSize = (0,0)
    master = False
    e = False
    fileStorage = ''
    dataCameras = []
    pixelsMin = 0
    hasOperator = True

    def __init__(self,posSize, fileStorage, pixelsMin = 0):
        self.posSize = posSize
        self.fileStorage = fileStorage
        self.pixelsMin = pixelsMin
        self.loadFromStorage()

    def loadFromStorage(self):
        try:
            with open(self.fileStorage, "rb") as f:
                self.places = pickle.load(f)
                f.close()
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
        for i,place in enumerate(self.places):
            if place.hasPoint(pos):
                self.remove(i)
    def setStatusByName(self, name, status):
        for i,place in enumerate(self.places):
            if place.name == name:
                place.setStatus(status)
            self.save()

    def setStorageStatusByName(self,name,status):
        for file in glob.glob(self.path + "\\*.data"):
            parkingHander = PlaceParkingHandler((0,0),file)
            parkingHander.setStatusByName(name, status)
            parkingHander.save()

    def selectByPosInStorage(self ,pos):
        for i,place in enumerate(self.places):
            if place.hasPoint(pos):
                if place.status[0] == defines.STATUS_FREE:
                    self.setStorageStatusByName(place.name,defines.STATUS_SELECTED)

    def editPlaces(self,event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.makeForm()
            if self.lastVal:
                self.add(PlaceParking(self.lastVal, (x, y), self.posSize, self.pixelsMin, self.hasOperator))
        if event == cv2.EVENT_RBUTTONDOWN:
            self.removeByPos((x,y))
        #Save changes
        self.save()

    def selectPlaces(self,event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.selectByPosInStorage((x,y))

    def save(self):
        with open(self.fileStorage, "wb") as f:
            pickle.dump(self.places, f)
            f.close()

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

    def runEdit(self, fileName,isVideo=False):
        if isVideo:
            cap = cv2.VideoCapture(fileName)
        while True:
            if isVideo:
                if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                    cap.set(cv2.CAP_PROP_POS_FRAMES,0)
                success, image = cap.read()
                image = cv2.resize(image,(1000,500))
                if not success:
                    print("NOOOOOOOOOO")
            else:
                image = cv2.imread(fileName)
            imageProccessed = self.setImageToCheck(image)
            self.loadFromStorage()
            for i, placeParking in enumerate(self.places):
                placeParking.setAndCropImageProcessed(imageProccessed)
                prevStatus = placeParking.status[0]
                placeParking.setStatus()
                if prevStatus != placeParking.status[0]:
                    self.save()
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
        self.save()
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
        self.path = path
        for file in glob.glob(path + "\\*.data"):
            with open(file, "rb") as f:
                try:
                    data= data + pickle.load(f)
                except:
                    pass
                f.close()
        self.dataCameras = data

    def getMap(self, fileName, live = False):
        while True:
            freePlace = 0
            image = cv2.imread(fileName)
            if live:
                self.setPlacesStatusByCameras("storage\\cameras")

            for i, placeParking in enumerate(self.places):
                pp = next((x for x in self.dataCameras if x.name == placeParking.name), None)
                placeParking.setStatus(pp.status[0] if pp != None else defines.STATUS_DISABLED)
                placeParking.render(image)
                if pp != None and not pp.status[0]:
                    freePlace = freePlace + 1

            Renderer().renderText(image, "Lugares libres: " + str(freePlace), (30,30), (0,0,0))
            cv2.imshow("Image", image)
            if self.hasOperator:
                cv2.setMouseCallback("Image", self.selectPlaces)
            cv2.waitKey(1)
