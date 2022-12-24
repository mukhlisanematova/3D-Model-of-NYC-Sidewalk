
# 8.5 mins

from qgis.utils import iface

# 1. add the OSM as basemap
tms = 'type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png&zmax=19&zmin=0'
tms_layer = iface.addRasterLayer(tms, "OSM", "wms")

# 2. Add RoadCenter Line CSV file
uri = "file:///C:/Users/Yinzi/Downloads/VRModelDataset/RoadCenterline.csv?delimiter={}&crs=epsg:4326&wktField={}".format(",", "the_geom")
layer_csv = QgsVectorLayer(uri, 'RoadCenterLine', 'delimitedtext')
layer_csv.isValid()
QgsProject.instance().addMapLayer(layer_csv)

# 3. Add shortest path between location A and location B
import processing
shortestpath_input = 'delimitedtext://file:///C:/Users/Yinzi/Downloads/VRModelDataset/RoadCenterline.csv?delimiter=,&crs=epsg:4326&wktField=the_geom'
shortestpath_output = 'C:/Users/Yinzi/Downloads/VR model/Output/ShortestPath/shortest_path.shp'
# location A
enter_A = QInputDialog().getText(None, "Input", "Please enter your start location:")
# import geopy
from geopy.geocoders import Nominatim
locator = Nominatim(user_agent="OSM")
locationA = locator.geocode(enter_A[0])
location_A = str(locationA.longitude) + ","+ str(locationA.latitude) + " [EPSG:4326]"
# print("Start: "+ location_A)
# location B
enter_B = QInputDialog().getText(None, "Input", "Please enter your destination:")
locator = Nominatim(user_agent="OSM")
locationB = locator.geocode(enter_B[0])
location_B = str(locationB.longitude) + ","+ str(locationB.latitude) + " [EPSG:4326]"
# print("End: " + location_B)

# location_A =  73.977674,40.761653 [EPSG:4326]'
# loation_B = '-73.983059,40.759019 [EPSG:4326]'
processing.run("native:shortestpathpointtopoint", \
{'INPUT':shortestpath_input,\
'STRATEGY':0,\
'DIRECTION_FIELD':'',\
'VALUE_FORWARD':'',\
'VALUE_BACKWARD':'',\
'VALUE_BOTH':'',\
'DEFAULT_DIRECTION':2,\
'SPEED_FIELD':'',\
'DEFAULT_SPEED':50,\
'TOLERANCE':0,\
'START_POINT':location_A,\
'END_POINT':location_B,\
'OUTPUT':shortestpath_output})
# show the shortest path in QGIS interface (you can cancel it later when you don't need it)
shortestPathLayer = iface.addVectorLayer(shortestpath_output, '', 'ogr') 

# 4. get the bounding box / study area according to the shortest part
boundingbox_input = shortestpath_output
boundingbox_output = 'C:/Users/Yinzi/Downloads/VR model/Output/BoundingBox/bounding_box.shp'
processing.run("native:boundingboxes", \
{'INPUT':boundingbox_input,
'OUTPUT':boundingbox_output})
# show the boudingbox polygon in the QGIS interface,(you can cancel it later if you don't need it')
boudingboxLayer = iface.addVectorLayer(boundingbox_output, '', 'ogr')

# 5.1 extract sidewalk inside the bounding box
sidewalk_input = '/vsizip/C:/Users/Yinzi/Downloads/VR model/VR_dataset/Sidewalk.zip/geo_export_c0f8cd1c-ffcd-42ce-a41c-ac7b61a87b1b.shp|layername=geo_export_c0f8cd1c-ffcd-42ce-a41c-ac7b61a87b1b'
clippath = 'C:/Users/Yinzi/Downloads/VR model/Output/BoundingBox/bounding_box.shp'
SelectedSideWalk_output = 'C:/Users/Yinzi/Downloads/VR model/Output/selected_sidewalk/selected_sidewalk.shp'
sidewalk_layer = iface.addVectorLayer(sidewalk_input, '', 'ogr')
processing.run("native:clip", {'INPUT':sidewalk_input,\
'OVERLAY':clippath,'OUTPUT':SelectedSideWalk_output})
# Add selected sidewalk output to the qgis interface
iface.addVectorLayer(SelectedSideWalk_output, '', 'ogr')

# 5.2 extract building footprint within the bounding box
building_footprint_input = '/vsizip/C:/Users/Yinzi/Downloads/VR model/VR_dataset/Building Footprints.zip/geo_export_732f1519-b12f-42a6-aef3-14326affa8cc.shp|layername=geo_export_732f1519-b12f-42a6-aef3-14326affa8cc'
clippath = 'C:/Users/Yinzi/Downloads/VR model/Output/BoundingBox/bounding_box.shp'
selected_building_footprint_output = 'C:/Users/Yinzi/Downloads/VR model/Output/selected_building_footprint/selected_building_footprint.shp'
building_footprint_layer = iface.addVectorLayer(building_footprint_input, '', 'ogr')
processing.run("native:clip", {'INPUT':building_footprint_input,\
'OVERLAY':clippath,'OUTPUT':selected_building_footprint_output})
# Add selected building footprint output to the qgis interface
iface.addVectorLayer(selected_building_footprint_output, '', 'ogr')

# 5.3 extract bus shelters within the bounding box
bus_stop_input = '/vsizip/C:/Users/Yinzi/Downloads/VR model/VR_dataset/Bus Stop Shelters.zip/geo_export_012c7e63-1405-44be-ace1-f02cfbe992e5.shp|layername=geo_export_012c7e63-1405-44be-ace1-f02cfbe992e5'
overlay_layer = 'C:/Users/Yinzi/Downloads/VR model/Output/BoundingBox/bounding_box.shp'
selected_bus_stop_output = 'C:/Users/Yinzi/Downloads/VR model/Output/selected_infrastructure/selected_bus_shelters.shp'
trees_layer = iface.addVectorLayer(bus_stop_input, '', 'ogr')
processing.run("native:intersection", \
{'INPUT':bus_stop_input,\
'OVERLAY':overlay_layer,\
'INPUT_FIELDS':[],\
'OVERLAY_FIELDS':[],\
'OVERLAY_FIELDS_PREFIX':'',\
'OUTPUT':selected_bus_stop_output})
iface.addVectorLayer(selected_bus_stop_output, '', 'ogr')

# 5.4 extract street trees within the bounding box
trees_input = '/vsizip/C:/Users/Yinzi/Downloads/VR model/VR_dataset/2015 Street Tree Census - Tree Data.zip/geo_export_b17e9c4b-ba62-4937-a5c4-768cfc97caf0.shp|layername=geo_export_b17e9c4b-ba62-4937-a5c4-768cfc97caf0'
overlay_layer = 'C:/Users/Yinzi/Downloads/VR model/Output/BoundingBox/bounding_box.shp'
selected_trees_output = 'C:/Users/Yinzi/Downloads/VR model/Output/selected_infrastructure/selected_trees.shp'
trees_layer = iface.addVectorLayer(trees_input, '', 'ogr')
processing.run("native:intersection", \
{'INPUT':trees_input,\
'OVERLAY':overlay_layer,\
'INPUT_FIELDS':[],\
'OVERLAY_FIELDS':[],\
'OVERLAY_FIELDS_PREFIX':'',\
'OUTPUT':selected_trees_output})
iface.addVectorLayer(selected_trees_output, '', 'ogr')

# 5.5 extract citywide hydrants within the bounding box
hydrants_input = '/vsizip/C:/Users/Yinzi/Downloads/VR model/VR_dataset/NYCDEP Citywide Hydrants.zip/geo_export_112a1204-439c-46bb-944d-8e417c55732d.shp|layername=geo_export_112a1204-439c-46bb-944d-8e417c55732d'
overlay_layer = 'C:/Users/Yinzi/Downloads/VR model/Output/BoundingBox/bounding_box.shp'
selected_hydrants_output = 'C:/Users/Yinzi/Downloads/VR model/Output/selected_infrastructure/selected_city_hydrants.shp'
hydrants_layer = iface.addVectorLayer(hydrants_input, '', 'ogr')
processing.run("native:intersection", \
{'INPUT':hydrants_input,\
'OVERLAY':overlay_layer,\
'INPUT_FIELDS':[],\
'OVERLAY_FIELDS':[],\
'OVERLAY_FIELDS_PREFIX':'',\
'OUTPUT':selected_hydrants_output})
iface.addVectorLayer(selected_hydrants_output, '', 'ogr')

# 5.6 extract Parking Meters within the bounding box
parking_meters_input = '/vsizip/C:/Users/Yinzi/Downloads/VR model/VR_dataset/Parking Meters GPS Coordinates and Status.zip/geo_export_0b3d18b0-13af-4fc5-8611-1110af6a867f.shp|layername=geo_export_0b3d18b0-13af-4fc5-8611-1110af6a867f'
overlay_layer = 'C:/Users/Yinzi/Downloads/VR model/Output/BoundingBox/bounding_box.shp'
selected_parking_meters_output = 'C:/Users/Yinzi/Downloads/VR model/Output/selected_infrastructure/selected_parking_meters.shp'
parking_meters_layer = iface.addVectorLayer(parking_meters_input, '', 'ogr')
processing.run("native:intersection", \
{'INPUT':parking_meters_input,\
'OVERLAY':overlay_layer,\
'INPUT_FIELDS':[],\
'OVERLAY_FIELDS':[],\
'OVERLAY_FIELDS_PREFIX':'',\
'OUTPUT':selected_parking_meters_output})
iface.addVectorLayer(selected_parking_meters_output, '', 'ogr')

# 5.7 extract pedestrian ramp within the bounding box
pedestrian_ramp_input = 'delimitedtext://file:///C:/Users/Yinzi/Downloads/VR%20model/VR_dataset/Pedestrian_Ramp_Locations.csv?type=csv&maxFields=10000&detectTypes=yes&wktField=the_geom&geomType=Point&crs=EPSG:4326&spatialIndex=no&subsetIndex=no&watchFile=no'
overlay_layer = 'C:/Users/Yinzi/Downloads/VR model/Output/BoundingBox/bounding_box.shp'
selected_pedestrian_ramp_output = 'C:/Users/Yinzi/Downloads/VR model/Output/selected_infrastructure/selected_pedestrian_ramp.shp'
processing.run("native:intersection", \
{'INPUT':pedestrian_ramp_input,\
'OVERLAY':overlay_layer,\
'INPUT_FIELDS':[],\
'OVERLAY_FIELDS':[],\
'OVERLAY_FIELDS_PREFIX':'',\
'OUTPUT':selected_pedestrian_ramp_output})
iface.addVectorLayer(selected_pedestrian_ramp_output, '', 'ogr')

# 5.8 extract litter basket within the bounding box
litter_baskets_input = 'delimitedtext://file:///C:/Users/Yinzi/Downloads/VR%20model/VR_dataset/DSNY_Litter_Basket_Inventory.csv?type=csv&maxFields=10000&detectTypes=yes&wktField=point&geomType=Point&crs=EPSG:4326&spatialIndex=no&subsetIndex=no&watchFile=no&field=DIRECTION:integer'
overlay_layer = 'C:/Users/Yinzi/Downloads/VR model/Output/BoundingBox/bounding_box.shp'
selected_litter_baskets_output = 'C:/Users/Yinzi/Downloads/VR model/Output/selected_infrastructure/selected_litter_baskets.shp'
processing.run("native:intersection", \
{'INPUT':litter_baskets_input,\
'OVERLAY':overlay_layer,\
'INPUT_FIELDS':[],\
'OVERLAY_FIELDS':[],\
'OVERLAY_FIELDS_PREFIX':'',\
'OUTPUT':selected_litter_baskets_output})
iface.addVectorLayer(selected_litter_baskets_output, '', 'ogr')

# 5.9 extract city benches within the bounding box
city_benches_input = 'delimitedtext://file:///C:/Users/Yinzi/Downloads/VR%20model/VR_dataset/City_Bench_Locations.csv?type=csv&maxFields=10000&detectTypes=yes&wktField=the_geom&geomType=Point&crs=EPSG:4326&spatialIndex=no&subsetIndex=no&watchFile=no'
overlay_layer = 'C:/Users/Yinzi/Downloads/VR model/Output/BoundingBox/bounding_box.shp'
selected_city_benches_output = 'C:/Users/Yinzi/Downloads/VR model/Output/selected_infrastructure/selected_city_benches.shp'
processing.run("native:intersection", \
{'INPUT':city_benches_input,\
'OVERLAY':overlay_layer,\
'INPUT_FIELDS':[],\
'OVERLAY_FIELDS':[],\
'OVERLAY_FIELDS_PREFIX':'',\
'OUTPUT':selected_city_benches_output})
iface.addVectorLayer(selected_city_benches_output, '', 'ogr')

# 5.10 extract news stands within the bounding box
news_stands_input = 'delimitedtext://file:///C:/Users/Yinzi/Downloads/VR%20model/VR_dataset/NewsStands.csv?type=csv&maxFields=10000&detectTypes=yes&wktField=the_geom&geomType=Point&crs=EPSG:4326&spatialIndex=no&subsetIndex=no&watchFile=no'
overlay_layer = 'C:/Users/Yinzi/Downloads/VR model/Output/BoundingBox/bounding_box.shp'
selected_news_stands_output = 'C:/Users/Yinzi/Downloads/VR model/Output/selected_infrastructure/selected_news_stands.shp'
processing.run("native:intersection", \
{'INPUT':news_stands_input,\
'OVERLAY':overlay_layer,\
'INPUT_FIELDS':[],\
'OVERLAY_FIELDS':[],\
'OVERLAY_FIELDS_PREFIX':'',\
'OUTPUT':selected_news_stands_output})
iface.addVectorLayer(selected_news_stands_output, '', 'ogr')
