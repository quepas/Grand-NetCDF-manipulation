"""
Open one NetCDF file and write it back using various libraries and tools.

The idea is to check what are the default and basic assumption of these tools that will transform (and how!) our NetCDF
files. For example, some tools will reorder dimension variable which might (will be?) affect the memory layout
in the file.
"""

from argparse import ArgumentParser
from functools import partial
from time import perf_counter

parser = ArgumentParser()
parser.add_argument("input_file", type=str)
# parser.add_argument("output_file", type=str)
args = parser.parse_args()


def rewrite_with_xarray(input_file: str, output_file: str) -> None:
    from xarray import open_dataset

    dataset = open_dataset(input_file)
    dataset.to_netcdf(output_file)


def rewrite_with_nctoolkit(input_file: str, output_file: str) -> None:
    from nctoolkit import open_data

    dataset = open_data(input_file, checks=True)
    dataset.to_nc(output_file)


def rewrite_with_iris(input_file: str, output_file: str) -> None:
    from iris import load, save

    cubes = load(input_file)
    save(cubes, output_file)


def rewrite_with_cf(input_file: str, output_file: str) -> None:
    from cf import read, write

    fields = read(input_file)
    write(fields, output_file)


to_check = {
    "xarray": partial(rewrite_with_xarray, input_file=args.input_file),
    "nctoolkit": partial(rewrite_with_nctoolkit, input_file=args.input_file),
    "iris": partial(rewrite_with_iris, input_file=args.input_file),
    "cf-python": partial(rewrite_with_cf, input_file=args.input_file)
}

for library, test_fun in to_check.items():
    t0 = perf_counter()
    test_fun(output_file=f"results/rewrite/{library}.nc")
    t1 = perf_counter()
    print(f"Rewrite! {library} took: {t1 - t0:.2f}s")
