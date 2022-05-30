from classes.PlaceParkingHandler import PlaceParkingHandler

posSize = (333, 357)

pps = PlaceParkingHandler(posSize, "storage\\cameras\\camera2.data", 4500)
pps.runEdit("cars\\images\\test1.mp4",True)
