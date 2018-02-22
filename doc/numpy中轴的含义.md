By definition, the axis number of the dimension is the index of that dimension within the array's shape. It is also the position used to access that dimension during indexing.

For example, if a 2D array a has shape (5,6), then you can access a[0,0] up to a[4,5]. Axis 0 is thus the first dimension (the "rows"), and axis 1 is the second dimension (the "columns"). In higher dimensions, where "row" and "column" stop really making sense, try to think of the axes in terms of the shapes and indices involved.

If you do .sum(axis=n), for example, then dimension n is collapsed and deleted, with all values in the new matrix equal to the sum of the corresponding collapsed values. For example, if b has shape (5,6,7,8), and you do c = b.sum(axis=2), then axis 2 (dimension with size 7) is collapsed, and the result has shape (5,6,8). Furthermore, c[x,y,z] is equal to the sum of all elements c[x,y,:,z].

参考资料

[how is axis indexed in numpy's array?
](https://stackoverflow.com/questions/17079279/how-is-axis-indexed-in-numpys-array/17079437#17079437)
[comment]: <tags> (numpy, axis)
[comment]: <description> (From Numpy's tutorial, axis can be indexed with integers, like 0 is for column, 1 is for row, but I don't grasp why they are indexed this way? And How do I figure out each axis' index when coping with multidimensional array?)
[comment]: <title> (numpy中轴的含义)
[comment]: <author> (夏洛之枫)