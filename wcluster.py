# coding: utf-8

"""Python bindings for wcluster

C++ code from: https://github.com/percyliang/brown-cluster

Help taken from:
- https://realpython.com/python-bindings-overview/#how-its-installed
- https://intermediate-and-advanced-software-carpentry.readthedocs.io/en/latest/c++-wrapping.html

"""

import ctypes
import pathlib

libname = pathlib.Path().absolute() / "wcluster.so"
c_lib = ctypes.CDLL(libname)



def parse_args(filename, n_clusters):
    argv = f"wcluster --text {filename} --c {n_clusters}".split()
    argc = len(argv)

    # Source: https://stackoverflow.com/a/16700231
    string_buffers = [ctypes.create_string_buffer(8) for i in range(argc)]
    string_addresses = list(map(ctypes.addressof, string_buffers))
    c_argv = (ctypes.c_char_p*argc)(*string_addresses)
    # Source: https://stackoverflow.com/a/3494857
    c_argv[:] = [bytes(s, "utf-8") for s in argv]
    return argc, argv, c_argv

def generate_clusters(filename, n_clusters):
    argc, argv, c_argv = parse_args(filename, n_clusters)
    c_lib.main(argc, c_argv)


def get_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", default="./README", type=str, help="Text file path")
    parser.add_argument("-c", "--n_clusters", default=5, type=int, help="Number of clusters")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = get_args()
    generate_clusters(args.filename, args.n_clusters)
