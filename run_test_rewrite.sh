#!/bin/bash
function convert_to_csv() {
  # The output CSV has the following fields: date, level, longitude, latitude, variable, value
  cdo -outputtab,date,lev,lon,lat,name,value $1 | awk 'FNR==1{ row=$2","$3","$4","$5","$6","$7;print row  } FNR!=1{ row=$1","$2","$3","$4","$5","$6; print row}' > $2
}

INPUT_FILE=/home/quepas/Research/AWACA/gitlab-projects/data-rigueur/test_data/puys_37lev_tz.nc

python test_rewrite.py $INPUT_FILE

convert_to_csv $INPUT_FILE results/rewrite/base.csv
convert_to_csv results/rewrite/xarray.nc results/rewrite/xarray.csv
convert_to_csv results/rewrite/iris.nc results/rewrite/iris.csv
convert_to_csv results/rewrite/nctoolkit.nc results/rewrite/nctoolkit.csv
convert_to_csv results/rewrite/cf-python.nc results/rewrite/cf-python.csv

python3 nc_structure.py /home/quepas/Research/AWACA/gitlab-projects/data-rigueur/test_data/puys_37lev_tz.nc
python3 nc_structure.py results/rewrite/xarray.nc
python3 nc_structure.py results/rewrite/iris.nc
python3 nc_structure.py results/rewrite/nctoolkit.nc
python3 nc_structure.py results/rewrite/cf-python.nc
