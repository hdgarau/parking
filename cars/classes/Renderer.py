import defines
import cv2
from classes.tools.Switch import Switch

class Renderer:
    textFont = cv2.FONT_HERSHEY_SIMPLEX
    textFontScale = 0.5
    posText = (0, -50)
    textThickness = 2
    posSize = (0, 0)

    def render(self, image ,status, name, pos, posSize):
        color = None
        image_status = None
        text_color = None
        if status[0] == defines.STATUS_FREE:
            image_status = cv2.imread("cars\\images\\free.jpg")
            color = defines.STATUS_COLOR_FREE
            text_color = defines.STATUS_COLOR_TEXT_FREE
        elif status[0] == defines.STATUS_BUSSY:
            image_status = cv2.imread("cars\\images\\bussy.jpg")
            color = defines.STATUS_COLOR_BUSSY
            text_color = defines.STATUS_COLOR_TEXT_BUSSY
        elif status[0] ==defines.STATUS_SELECTED:
            image_status = None
            color = defines.STATUS_COLOR_SELECTED
            text_color = defines.STATUS_COLOR_TEXT_SELECTED
        elif status[0] ==defines.STATUS_BAD_PARKING:
            image_status = None
            color = defines.STATUS_COLOR_BAD_PARKING
            text_color = defines.STATUS_COLOR_TEXT_BAD_PARKING
        else:
            image_status = None
            color = defines.STATUS_COLOR_DISABLED
            text_color = defines.STATUS_COLOR_TEXT_DISABLED
        cv2.rectangle(image, pos + posSize, color, self.textThickness)
        #if image_status.any() != None:
        #    image[pos[0]:pos[0]+44,pos[1]:pos[1]+44,0:3] = image_status
        self.renderText(image, name, pos, text_color)
        return image

    def renderText(self,image, text ,pos,color):
        cv2.putText(image, text, pos , self.textFont, self.textFontScale, color, self.textThickness,
                        cv2.LINE_4)