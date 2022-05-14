from classes.PlaceParkingHandler import PlaceParkingHandler

posSize = (50, 100)

pps = PlaceParkingHandler(posSize, "storage\\map.data")
#pps.runEdit("cars\\images\\mapa.jpg")
pps.setPlacesStatusByCameras("storage\\cameras")
pps.getMap("cars\\images\\mapa-min.jpg")
