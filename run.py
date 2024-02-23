from argparse import ArgumentParser
from pathlib import Path
from time import perf_counter

parser = ArgumentParser()
parser.add_argument("input", type=Path)
parser.add_argument("--output-postfix", type=str, default="limited_data.nc")
parser.add_argument("--field-name", type=str, default="air_temperature")
parser.add_argument("--latitude", type=float, nargs=2, default=[90, -90])
parser.add_argument("--longitude", type=float, nargs=2, default=[-180, 180])
args = parser.parse_args()

print(args)


def limit_with_netcdf4(input_file: str, output_file: str, field_name: str,
                       longitude_range: list[float, float], latitude_range: list[float, float]) -> None:
    from netCDF4 import Dataset

    Dataset(input_file, "r")


def limit_with_iris(input_file: str, output_file: str, field_name: str,
                    longitude_range: list[float, float], latitude_range: list[float, float]) -> None:
    """
    With iris, we load with a constraint limiting the field and region
    """
    from iris import load, Constraint, save

    constraint = Constraint(
        name=field_name,
        coord_values={
            'longitude': lambda cell: longitude_range[0] < cell < longitude_range[1],
            'latitude': lambda cell: latitude_range[0] < cell < latitude_range[1]
        })
    cubes = load(input_file, constraint)
    save(cubes, output_file)


def limit_with_cf_python(input_file: str, output_file: str, field_name: str,
                         longitude_range: list[float, float], latitude_range: list[float, float]):
    """
    With cf-python, we load the file and then create a limited subset (although lazy with dask!)
    """
    from cf import read, wi, write

    # read() always returns a list of available fields, so it is a bit easier if we select only one field !
    field_list = read(input_file, select=field_name)
    field = field_list[0]
    # Don't know why, but we cannot specify latitude/longitude instead of X/Y
    # It seems, that for some files, cf-python is not able to correctly decode all axes/dimensions.
    # Also: subspace() creates a new field !
    temp = field.subspace(X=wi(*longitude_range), Y=wi(*latitude_range))
    write(temp, output_file)


to_check = {
    "iris": lambda: limit_with_iris(args.input, f"iris_{args.output_postfix}", args.field_name,
                                    args.longitude, args.latitude),
    "cf-python": lambda: limit_with_cf_python(args.input, f"cf_python_{args.output_postfix}", args.field_name,
                                              args.longitude, args.latitude)
}

for library, test_fun in to_check.items():
    t0 = perf_counter()
    test_fun()
    t1 = perf_counter()
    print(f"{library} took: {t1 - t0:.2f}s")
