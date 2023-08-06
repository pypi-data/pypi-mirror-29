# fs-sparse: a wrapper to check sparse file


## Generate test files

Using scripts provided in `test/create_test_file.sh`, it will generate two
files:

* `normal.dat` with no holes;
* `sparse.dat` with holes.


## Usage

The interface exposes three functions, see example below. Note that if a file
has no holes, the # of extents (or tuple) will be 1.

    In [1]: import sparse

    In [2]: sparse.get_extents("test/sparse.dat")
    Out[2]: [(0, 8192), (28672, 36864), (40960, 45056)]

    In [3]: sparse.get_extents("test/normal.dat")
    Out[3]: [(0, 8192)]

    In [4]: sparse.is_sparse("test/normal.dat")
    Out[4]: False


Please open issues for bug fix or feature requests.


