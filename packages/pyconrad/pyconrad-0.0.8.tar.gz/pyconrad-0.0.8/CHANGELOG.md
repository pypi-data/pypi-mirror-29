## 0.0.9 (unreleased)
* [ ]  Fix memory leak issue/PyGrid
* [ ]  Print automatically citations of used classes (feature for CONRAD?)
* [ ]  Fork JPype to allow unified memory for numpy/Java?
* [ ]  OpenCL support:
	* [ ]  Efficient OpenCLMemory/create OpenCLGrid from pyopencl.array.Array
	* [ ]  Add more examples: 
		e.g. use following projects gpyfft,gputools,DeepCL 
## 0.0.8
* [x]  OpenCL support:
	* [x]  Get CONRAD's OpenCL device, command queue, context
	* [x]  Create OpenCLGrids from Numpy
 	* [x]  Upload/Download numpy
	* [x]  Efficient OpenCLMemory/create OpenCLGrid from pyopencl.array.Array
	* [x]  Add example 
* [x]  More convenience functions in pyopencl.config
* [x]  Better desktop integration for conrad_imagej:
	* [x]  Add .desktop files
	* [x]  Support for .vtk, .np and  .npz support
