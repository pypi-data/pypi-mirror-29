cdef extern from "../src/iters/filemap.hpp" namespace "ss::iter":
    cdef cppclass ScalarType:
        ScalarType()
        ScalarType(ScalarType)

cdef extern from "../src/iters/filemap.hpp" namespace "ss::iter::ScalarType":
    cdef ScalarType Null
    cdef ScalarType Int64
    cdef ScalarType Float
    cdef ScalarType Bool
    cdef ScalarType ByteSlice
    cdef ScalarType Utf8
    cdef ScalarType Object
    cdef ScalarType JsonUtf8