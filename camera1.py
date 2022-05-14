from classes.PlaceParkingHandler import PlaceParkingHandler

posSize = (33, 57)

pps = PlaceParkingHandler(posSize, "storage\\cameras\\camera1.data", 250)
pps.runEdit("cars\\images\\download.jpg")
