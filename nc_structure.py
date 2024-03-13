from pathlib import Path

from netCDF4 import Dataset
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("path", type=Path)
args = parser.parse_args()

dataset = Dataset(args.path)
print(f"----- File: {args.path} -----")
print(f"Dimensions: {list(dataset.dimensions.keys())}")
print(f"Variables : {list(dataset.variables.keys())}")

