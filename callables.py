import asyncio
import sys

from script import meteo_data_collector
from xls_writer import write_data_to_xls


def main():
    args = sys.argv
    # args[0] = current file
    # args[1] = function name
    # args[2:] = function args : (*unpacked)
    asyncio.run(globals()[args[1]](*args[2:]))


if __name__ == "__main__":
    main()
