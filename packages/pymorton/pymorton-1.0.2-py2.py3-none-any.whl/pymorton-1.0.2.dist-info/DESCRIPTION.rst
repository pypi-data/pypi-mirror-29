A lightweight Python library that enables ordinal hashing of multidimensonal data via Morton coding / Z-ordering, along with support for geospatial indexing.

In mathematical analysis and computer science, `Z-order`, `Morton-order`, or a `Morton-code` is a function which maps multidimensional data to one dimension while preserving locality of the data points. It was introduced in 1966 by IBM researcher, G. M. Morton. The z-value of a point in multidimensions is calculated by interleaving the binary representations of its coordinate values. Once the data are sorted into this ordering, any one-dimensional data structure can be used, such as binary search trees, B-trees, skip lists, or hash tables. The resulting ordering can equivalently be described as the order one would achieve from a depth-first traversal of a quadtree,
where `{x, y, ..., K}` are combined into a single ordinal value that is easily compared, searched, and indexed against other Morton numbers.


