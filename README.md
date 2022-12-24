## 3D-Model-of-NYC-Sidewalk 
### Qgis Part
1. Go to the [NYC Open Data](https://opendata.cityofnewyork.us/) website download the below datasets by shapefile format. 
   - building footprint  (download by shapefile format)
   - sidewalk            (download by shapefile format)
   - bus shelter         (download by shapefile format)
   - city bench          (download by csv format)
   - city hydrant        (download by shapefile format)
   - litter basket       (download by csv format)
   - news stand          (download by csv format)
   - parking meter       (download by shapefile format)
   - pedestrian ramp     (download by csv format)
   - tree                (download by shapefile format)
   - Road centerline     (download by csv format)
2. Create a folder to hold all the data which are the Qgis part outputs(extract the data within the interested area according to the user query address) 
3. Download the @Qgis-final-automatic.py 
4. Open the @Qgis-final-automatic.py on the Qgis
5. make sure to change each output path to the above folder path on the code and each input path to the path where you save the dataset(which you downloaded from the NYC Open data) on the code. 
    
    <img src="Qgis_Part02.gif">
    
6. run the @Qgis-final-automatic.py  code on the Qgis 
   
     <img src="Qgis_Part01.gif">
 
 7. After all the above steps, you will get all the shapefile format data which all within the interested area. 
   
     <img src="Qgis_Part03.gif">
   
 8. Then convert the shapefile format data into the CSV file on the google colab by python before feed into the unity, this is what I did before. But you can save the data into csv file format directory on the Qgis, just change the output format .shp to .csv. 
    
    <img src="Qgis_Part04.gif">

###  Unity Part
* Download the zip file from this github, unzip it. 
* Open the unzip file on the unity 
* make sure to change the file paths on all the scrips inside the script folder into the path where you save the output with CSV format from the Qgis part. (this is read all the data which got from the Qgis part into unity and generate the 3D model) 
   - Note: I only put building footprint, pedestrian ramp, tree, hydrant with different audio feedback in this 3D model, you can add as many you want with the similar code. 
  
  <img src="Qgis_Part05.gif">
