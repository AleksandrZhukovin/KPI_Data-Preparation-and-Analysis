cd /d satellite_data\R10
gdal_merge.py -separate -o con10.tif T36UUB_20190821T085601_B02_10m.jp2 T36UUB_20190821T085601_B03_10m.jp2 T36UUB_20190821T085601_B04_10m.jp2 T36UUB_20190821T085601_B08_10m.jp2
gdalwarp -t_srs EPSG:4326 con10.tif pr10.tif
cd ..
cd R20
gdal_merge.py -separate -o con20.tif T36UUB_20190821T085601_B02_20m.jp2 T36UUB_20190821T085601_B03_20m.jp2 T36UUB_20190821T085601_B04_20m.jp2 T36UUB_20190821T085601_B8A_20m.jp2
gdalwarp -t_srs EPSG:4326 con20.tif pr20.tif
cd ..
cd R60
gdal_merge.py -separate -o con60.tif T36UUB_20190821T085601_B02_60m.jp2 T36UUB_20190821T085601_B03_60m.jp2 T36UUB_20190821T085601_B04_60m.jp2 T36UUB_20190821T085601_B8A_60m.jp2
gdalwarp -t_srs EPSG:4326 con60.tif pr60.tif
move "D:\Універ\Спец. прог\лаба 7\satellite_data\R10\pr10.tif" "D:\Універ\Спец. прог\лаба 7\satellite_data\res\pr10.tif"
move "D:\Універ\Спец. прог\лаба 7\satellite_data\R20\pr20.tif" "D:\Універ\Спец. прог\лаба 7\satellite_data\res\pr20.tif"
move "D:\Універ\Спец. прог\лаба 7\satellite_data\R60\pr60.tif" "D:\Універ\Спец. прог\лаба 7\satellite_data\res\pr60.tif"
cd "D:\Універ\Спец. прог\лаба 7\satellite_data\res\"
gdal_merge.py -separate -o com.tif pr60.tif pr20.tif pr10.tif 
gdalwarp -q -cutline Kyiv_regions.shp -crop_to_cutline com.tif out.tif

gdalwarp -tr 30 30 pan.tif pan30.tif
gdalwarp -tr 60 60 out.tif out60.tif

gdal_pansharpen pan.tif pr60.tif pan_60.tif -r square