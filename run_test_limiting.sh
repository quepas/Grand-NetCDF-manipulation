#!/bin/bash
function convert_to_csv() {
  # The output CSV has the following fields: date, level, longitude, latitude, variable, value
  cdo -outputtab,date,lev,lon,lat,name,value $1 | awk 'FNR==1{ row=$2","$3","$4","$5","$6","$7;print row  } FNR!=1{ row=$1","$2","$3","$4","$5","$6; print row}' > $2
}

python run.py /home/quepas/Research/AWACA/gitlab-projects/data-rigueur/test_data/puys_37lev_tz.nc \
                --latitude 0.0 90.0 --longitude 0.0 180.0
#                --latitude 45.0 46.0 --longitude 2.0 3.0

convert_to_csv cf_python_limited_data.nc cf_python_limited_data.csv
convert_to_csv iris_limited_data.nc iris_limited_data.csv
convert_to_csv nctoolkit_limited_data.nc nctoolkit_limited_data.csv
convert_to_csv xarray_limited_data.nc xarray_limited_data.csv

python3 nc_structure.py /home/quepas/Research/AWACA/gitlab-projects/data-rigueur/test_data/puys_37lev_tz.nc
python3 nc_structure.py cf_python_limited_data.nc
python3 nc_structure.py iris_limited_data.nc
python3 nc_structure.py nctoolkit_limited_data.nc
python3 nc_structure.py xarray_limited_data.nc
