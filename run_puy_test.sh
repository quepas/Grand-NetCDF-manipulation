#!/bin/bash
function convert_to_csv() {
  cdo -outputtab,date,lon,lat,value $1 | awk 'FNR==1{ row=$2","$3","$4","$5;print row  } FNR!=1{ row=$1","$2","$3","$4; print row}' > $2
}

python run.py /home/quepas/Research/AWACA/gitlab-projects/data-rigueur/test_data/puys_37lev_tz.nc \
                --latitude 45.0 45.9 --longitude 2.0 2.9

convert_to_csv cf_python_limited_data.nc cf_python_limited_data.csv
convert_to_csv iris_limited_data.nc iris_limited_data.csv
convert_to_csv nctoolkit_limited_data.nc nctoolkit_limited_data.csv
convert_to_csv xarray_limited_data.nc xarray_limited_data.csv
