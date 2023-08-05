
MRCZ is a highly optimized compressed version of the popular electron microscopy 
MRC image format.  It uses the Blosc meta-compressor library as a backend.  It 
can use a number of high-performance loseless compression codecs such as 'lz4' 
and 'zstd', it can apply bit-shuffling filters, and operates compression in a 
blocked and multi-threaded way to take advantage of modern multi-core CPUs.



