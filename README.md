# PyTrx
PyTrx (short for 'Python Tracking') is a Python object-oriented toolbox created for the purpose of calculating real-world measurements from oblique images and time-lapse image series. Its primary purpose is to obtain velocities, surface areas, and distances from imagery of glacial environments.<br>

Authors: Penelope How (p.how@ed.ac.uk), Nick Hulton, and Lynne Buie (née Addison)<br>

<hr>

<h3>PyTrx citations</h3>

We are happy for others to use and adapt PyTrx for their own processing needs. Please refer to the following key publication and Digital Object Identifier (DOI) where possible:<br>

<h3>How et al. (2018) PyTrx: A Python toolbox for deriving velocities, surface areas and line measurements from oblique imagery in glacial environments. Geoscientific Instrumentation, Methods and Data Systems Discussion, <a href="https://doi.org/10.5194/gi-2018-28">doi:10.5194/gi-2018-28</a>, In Review.</h3> <br>

If you use PyTrx for scientific papers, please also cite some of our previous work which is listed below: <br>

<b>*PyTrx used for detection of supraglacial lakes and meltwater plumes*</b><br>
How et al. (2017) Rapidly changing subglacial hydrological pathways at a tidewater glacier revealed through simultaneous observations of water pressure, supraglacial lakes, meltwater plumes and surface velocities. <i>The Cryosphere</i> 11, 2691-2710, <a href="https://doi.org/10.5194/tc-11-2691-2017">doi:10.5194/tc-11-2691-2017</a><br>

<b>*PyTrx used for georectification of glacier calving event locations*</b><br>
How et al. (In Review) Calving controlled by melt-undercutting: detailed mechanisms revealed through time-lapse observations. <i>Annals of Glaciology</i><br>

<b>*PhD thesis by Penelope How, for which PyTrx was developed primarily*</b><br>
How (2018) Dynamical change at tidewater glaciers examined using time-lapse photogrammetry. PhD thesis, University of Edinburgh, UK, <a href="https://hdl.handle.net/1842/31103">https://hdl.handle.net/1842/31103</a><br>

<b>*MSc thesis by Lynne Buie, where PyTrx was created in its earliest form*</b><br>
Addison (2015) PyTrx: feature tracking software for automated production of glacier velocity. MSc thesis, University of Edinburgh, UK, <a href="https://hdl.handle.net/1842/11794">https://hdl.handle.net/1842/11794</a><br>

<hr>

<h3>Permissions and acknowledgements</h3>
<b>Example image sets</b> distributed with PyTrx were collected as part of <a href="https://www.researchinsvalbard.no/project/7037">CRIOS</a> (Calving Rates and Impact On Sea level), and are used here with permission. <br><br> 
<b>The DEM of the Kongsfjorden area</b> provided as an example dataset for PyTrx originates from the freely available DEM dataset provided by the <a href="https://geodata.npolar.no/">Norwegian Polar Institute</a>, data product 'S0 Terrengmodell - Delmodell_5m_2009_13822_33 (GeoTIFF)'  <a href="https://doi.org/10.21334/npolar.2014.dce53a47">doi:10.21334/npolar.2014.dce53a47</a>. This data is licensed under the <a href="https://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International (CC BY 4.0) license</a>.<br><br>
<b>The DEM of the Tempelfjorden area</b> provided as an example dataset for PyTrx originates from <a href="https://www.pgc.umn.edu/data/arcticdem/">ArcticDEM</a>, Scene ID WV01_20130714_1020010 (July 14, 2013). <a href="https://www.pgc.umn.edu/guides/arcticdem/additional-information/">There is no license for the ArcticDEM data and it can be used and distributed freely</a>. The DEM was created from DigitalGlobe, Inc., imagery and funded under National Science Foundation awards 1043681, 1559691, and 1542736. <br><br>
Refer to the readme document in the Examples folder of this repository for more information on the DEMs provided and distributed with PyTrx.<br><br>
Parts of the <b>georectification functions</b> in the PyTrx toolbox were inspired and translated from <a href="http://imgraft.glaciology.net/">ImGRAFT</a>, a photogrammetry toolbox for Matlab (<a href="https://www.geosci-instrum-method-data-syst.net/4/23/2015/gi-4-23-2015.pdf">Messerli and Grinsted, 2015</a>). Where possible, ImGRAFT has been credited for in the corresponding PyTrx scripts (primarily some passages in the CamEnv.py script) and cited in relevant PyTrx publications. 

<hr>
<h3>PyTrx scripts</h3>

Detailed documentation is included in the scripts that make up PyTrx. Each script contains classes and functions for handling each aspect needed for photogrammetric processing:<br><br>

<b>*CamEnv.py*</b><br>
Handles the associated data with the camera environment.<br>
The <b>GCPs</b> class handles the Ground Control Points (GCPs) and their correspondence to the associated DEM and CamImage object.<br>
The <b>CamCalib</b> class handles information concerning the camera calibration, i.e. the intrinsic camera matrix and lens distortion coefficients. This class contains functionality for reading in calibration files from .txt and .mat formats.<br>
The <b>CamEnv</b> compiles all the information about the camera environment from the GCPs and CamCalib classes, and also contains information about the camera object (pose and location). This is also where georectification functionality is held, with functions for projection and inverse projection. The class is initialised using a .txt file containing file path directories to all the associated data files.<br>

<b>*DEM.py*</b><br>
Handles the DEM data. This currently supports .mat and .tif file types.<br>
The <b>ExplicitRaster</b> class represents a DEM as a numeric raster with explicit XY cell referencing in each grid cell. The class includes functions for densification, calculating viewsheds, and incorporates unbound functions that import a DEM file from .mat and .tif formats.<br>

<b>*FileHandler.py*</b><br>
This module contains a set of functions for reading in data from files (such as image data and calibration information) and writing out data.<br>

<b>*Images.py*</b><br>
Handles the image data, and the image sequence.<br> 
The <b>CamImage</b> class holds information about a singular image and contains functionality for importing image data from file and passing specific image bands forward for subsequent processing.<br>
The <b>ImageSequence</b> class holds information about an image sequence, i.e. a collection of CamImage objects, from which specific images and image pairs can be called.<br>

<b>*Measure.py*</b><br>
Contains classes for calculating homography and velocities, and measuring surface areas and distances from oblique imagery.<br>
The <b>Velocity</b> class enables processing with an ImageSequence object. Camera homography and velocities are derived and held within this class.<br>
The <b>Area</b> class performs automated and manual detection of surface areas from imagery and georectifies polygons to real-world coordinates.<br>
The <b>Line</b> class performs manual detection of lines from imagery (e.g. glacier terminus position) and georectifies lines to real-world coordinates. <br>

<b>*Utilities.py*</b><br>
This module contains a set of functions for plotting and interpolating data.<br><br>

<b>For beginners in programming, it is advised to look at the example applications provided and adapt them accordingly for your own use. For experienced programmers... get stuck in. Feel free to contact us if you run into major problems or have constructive comments that will help us further PyTrx and its capabilities. We will not respond to minor troubleshooting or unconstructive comments.</b><br>

<hr>

<h3>PyTrx set-up and requirements</h3>

PyTrx requires the following key Python packages in order to run: <br><br>

<b>OpenCV (v3.1.0):</b> <a href="https://opencv.org/releases.html">opencv.org</a><br>
<b>GDAL (v1.1.4):</b> <a href="http://www.gisinternals.com/archive.php">gisinternals.com</a><br>
<b>Pillow (PIL) (v1.1.7):</b> <a href="http://www.pythonware.com/products/pil/">pythonware.com</a><br>
<b>OsGeo (v1.1.4):</b> Often comes with distributions of GDAL<br><br>

These packages may not necessarily be installed with distributions of Python (e.g. PythonXY, Anaconda), so you may have to download them from the given links. It is important to download the package versions specified as we cannot guarantee that all others are compatible with PyTrx. <br>

PyTrx also needs other packages, which are commonly included with distributions of Python. Compatibility with all versions of these packages are highly likely: <b>datetime</b>, <b>glob</b>, <b>imghdr</b>, <b>math</b>, <b>Matplotlib</b>, <b>NumPy</b>, <b>operator</b>, <b>os</b>, <b>PyLab</b>, <b>SciPy</b>, <b>struct</b>, and <b>sys</b> <br>

<hr>

<h3>Links</h3>

There are other useful software available for terrestrial photogrammetry in glaciology: <br>

<a href="http://www.lancaster.ac.uk/staff/jamesm/software/pointcatcher.htm">Pointcatcher</a> - Matlab-based GUI toolbox for feature-tracking and georectification <br>
<a href="http://imgraft.glaciology.net/">ImGRAFT</a> - Matlab toolbox for feature-tracking and georectification <br>
<a href="http://www.mn.uio.no/geo/english/research/projects/icemass/cias/">CIAS</a> - IDL gui for feature-tracking <br>
<a href="https://www.geosci-model-dev.net/9/307/2016/">PRACTISE</a> - Matlab toolbox for georectification
