'''
PYRX DEM MODULE

This script is part of PyTrx, an object-oriented programme created for the 
purpose of calculating real-world measurements from oblique images and 
time-lapse image series.

This module, DEM, contains functionality for handling DEM data and implementing
this data into the camera environment (CamEnv) object class.

Classes
ExplicitRaster:      A class to represent a numeric Raster with explicit XY 
                     cell referencing in each grid cell.


Key functions
loadDEM:            Function for loading DEM data from different file types, 
                    which is automatically detected. Recognised file types: 
                    .mat and .tif.
DEM_FromMat:        Function for loading a DEM array from a Matlab (.mat) file 
                    containing separate X, Y, Z matrices.
DEM_FromTiff:       Function for loading a DEM array from a .tiff file 
                    containing raster-formatted data. The tiff data importing 
                    is handled by GDAL.
voxelviewshed:      Calculate a viewshed over a DEM from a given viewpoint in 
                    the DEM scene. This function is based on the viewshed 
                    function (voxelviewshed.m) available in ImGRAFT. 
      
@author: Penny How (p.how@ed.ac.uk)
         Nick Hulton 
         Lynne Buie
'''

#Import packages
import numpy as np
import scipy.io as sio
import gdal
import math
from scipy import interpolate
from gdalconst import GA_ReadOnly 
import struct
from scipy.interpolate import RectBivariateSpline

#------------------------------------------------------------------------------

class ExplicitRaster(object):   
    '''A class to represent a numeric Raster with explicit XY cell referencing
    in each grid cell.
    '''
    
    #Basic constuctor method
    def __init__(self, X, Y, Z, nodata=float('nan')): 
        #Check XYZ data is all the same size
        if not (X.shape==Y.shape and X.shape==Z.shape):
            print 'Raster data and/or co-ordinate arrays are differently sized'
            print 'X-shape',X.shape
            print 'Y-shape',Y.shape
            print 'Z-shape',Z.shape
            return
        
        #Define class atrributes
        self._data=np.array([X,Y,Z]) 
        self._nodata=nodata
        self._extents=[X[0][0]-0.5*(X[0][1]-X[0][0]),X[-1][-1]+0.5*(X[-1][-1]-
                       X[-1][-2]),Y[0][0]-0.5*(Y[1][0]-Y[0][0]),Y[-1][-1]+0.5*
                       (Y[-1][-1]-Y[-2][-1])]
    
    
    def getData(self,dim=None):
        '''Return DEM data. XYZ dimensions can be individually called with the
        dim input variable (integer: 0, 1, or 2).
        '''
        
        #Return all DEM data if no dimension is specified
        if dim==None:
            return self._data
        
        #Return specific DEM dimension 
        elif (dim==0 or dim==1 or dim==2):
            return self._data[dim]
        
        #Return None if no DEM data present 
        else:
            return None

            
    def getZ(self):
        '''Return height (Z) data of DEM.'''
        return self.getData(2)
        
     
    def getShape(self):
        '''Return the shape of the DEM data array.'''
        return self._data[0].shape

    
    def getRows(self):
        '''Return the number of rows in the DEM data array.'''
        return self._data[0].shape[0]

        
    def getCols(self):
        '''Return the number of columns in the DEM data array.'''
        return self._data[0].shape[1]

    
    def getNoData(self):
        '''Return fill value for no data in DEM array.''' 
        return self._nodata
 
       
    def getExtent(self):
        '''Return DEM extent.'''     
        return self._extents
 
       
    def subset(self,cmin,cmax,rmin,rmax):
        '''Return a specified subset of the DEM array.
        '''
        
        #Find minimum extent value
        cmin=int(max(0,cmin))
        rmin=int(max(0,rmin))
        
        #Find maximum extent value
        cmax=int(min(self._data[0].shape[1],cmax))
        rmax=int(min(self._data[0].shape[0],rmax))
        
        #Extract XYZ subset
        X=self._data[0][rmin:rmax,cmin:cmax]
        Y=self._data[1][rmin:rmax,cmin:cmax]
        Z=self._data[2][rmin:rmax,cmin:cmax]
        
        #Construct new XYZ array  
        return ExplicitRaster(X,Y,Z)
 
       
    def densify(self, densefac=2):
        '''Function to densify the DEM array by a given densification factor.
        The array is multiplied by the given densification factor and then
        subsequently values are interpolated using the SciPy function 
        RectBivariateSpline. The densification factor is set to 2 by default,
        meaning that the size of the DEM array is doubled.
        '''
        
        #Get XYZ dem data
        x=self._data[0,0,:]
        y=self._data[1,:,0]        
        z=np.transpose(self._data[2])
        
        #Multipy size of xy arrays by the densification factor
        nx=((x.size-1)*densefac)+1
        ny=((y.size-1)*densefac)+1
        
        #Define new array data spacing
        xd = np.linspace(x[0], x[-1], nx)
        yd = np.linspace(y[0], y[-1], ny)
        
        #Create mesh grid
        yv,xv = np.meshgrid(yd,xd)

        #Interpolate 
        f=RectBivariateSpline(x, y, z, bbox=[None, None, None, None], 
                              kx=1, ky=1, s=0)

        #Create empty array for Z data
        zv=np.zeros((nx,ny))
        
        #Reshape XYZ arrays
        xv=np.reshape(xv,(nx*ny))
        yv=np.reshape(yv,(nx*ny))
        zv=np.reshape(zv,(nx*ny))
             
        #Populate empty Z array
        for i in range(xv.size):
            zv[i]=f(xv[i],yv[i])

        #Transpose arrays for compatibility        
        xv=np.transpose(np.reshape(xv,(nx,ny)))
        yv=np.transpose(np.reshape(yv,(nx,ny)))
        zv=np.transpose(np.reshape(zv,(nx,ny)))

        #Construct new XYZ array        
        return ExplicitRaster(xv,yv,zv)
               
        
    def reportDEM(self):
        '''Self reporter for DEM class object. Returns the number of rows and
        columns in the array, how NaN values in the array are filled, and the
        data extent coordinates.
        '''
        
        print '\nDEM object reporting:\n'
        print 'Data has ',self.getRows(),' rows by ',self.getCols(),' columns'
        print 'No data item is: ',self.getNoData()
        print ('Data Extent Coordinates are [xmin,xmax,ymin,ymax]: ',
               self.getExtent())
    
        
def load_DEM(demfile):
    '''Function for loading DEM data from different file types, which is 
    automatically detected. Recognised file types: .mat and .tif.
    '''
    
    #Determine file type based on filename suffix
    suffix=demfile.split('.')[-1].upper()
    
    #MAT file import if detected
    if suffix==("MAT"):
        return DEM_FromMat(demfile)
        
    #TIF file import if detected
    elif suffix==("TIF") or suffix==("TIFF"):
        return DEM_FromTiff(demfile)
    
    #No DEM data passed if file type is not recognised
    else:
        print 'DEM format (suffix) not supported'
        print 'DEM file: ',demfile,' not read'
        return None

    
def DEM_FromMat(matfile):
    '''Function for loading a DEM array from a Matlab (.mat) file containing
    separate X, Y, Z matrices.
    '''
    
    #Load Matlab file and XYZ matrices as arrays
    mat = sio.loadmat(matfile)
    X=np.ascontiguousarray(mat['X'])
    Y=np.ascontiguousarray(mat['Y'])
    Z=np.ascontiguousarray(mat['Z'])

    #Flip array if not compatible
    if Y[0][0]>Y[-1][0]:
        print '\nFlipping input DEM'
        X = np.flipud(X)
        Y = np.flipud(Y)
        Z = np.flipud(Z)
    
    #Construct DEM array
    dem=ExplicitRaster(X,Y,Z)
    return dem 


def DEM_FromTiff(tiffFile):
    '''Function for loading a DEM array from a .tiff file containing
    raster-formatted data. The tiff data importing is handled by GDAL.
    '''
    
    #Open tiff file with GDAL
    dataset = gdal.Open(tiffFile, GA_ReadOnly)
    
    #Define columns and rows in raster
    cols = dataset.RasterXSize
    rows = dataset.RasterYSize
    
    #Transform raster and define origins for populating
    geotransform = dataset.GetGeoTransform() 
    originX = geotransform[0]
    originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeight = geotransform[5]
    
    #Get Z data from raster
    band = dataset.GetRasterBand(1)
    scanline = band.ReadRaster( 0, 0, band.XSize, band.YSize,band.XSize, 
                               band.YSize, band.DataType)
    value = struct.unpack('f' * band.XSize *band.YSize, scanline)
    Z=np.array(value).reshape(rows,cols)

    #Create empty arrays for XY data    
    X=np.zeros((rows,cols))
    Y=np.zeros((rows,cols))
    
    #Populate empty arrays from origins
    originX=originX+(pixelWidth*0.5)
    originY=originY+(pixelWidth*0.5)
    for i in range(rows):
        for j in range(cols):
            X[i,j]=(j*pixelWidth)+originX
            Y[i,j]=(i*pixelHeight)+originY
    
    #Flip array if not compatible
    if Y[0,0]>Y[-1,0]:   
        X=np.flipud(X) 
        Y=np.flipud(Y)
        Z=np.flipud(Z)
     
    #Construct DEM array
    dem=ExplicitRaster(X,Y,Z)    
    return dem

    
def voxelviewshed(dem,viewpoint):
    '''Calculate a viewshed over a DEM from a given viewpoint in the DEM scene.
    This function is based on the viewshed function (voxelviewshed.m) available 
    in ImGRAFT.
    
    The ImGRAFT voxelviewshed.m script is available at:
    http://github.com/grinsted/ImGRAFT/blob/master/voxelviewshed.m
    
    Inputs
    X,Y,Z:                      Input DEM (regular grid).
    viewpoint:                  3-element vector specifying the viewpoint.
    
    Output
    vis:                        Boolean visibility matrix (which is the same 
                                size as dem)
    '''
    #Get XYZ arrays    
    X=dem.getData(0)
    Y=dem.getData(1)
    Z=dem.getData(2)

    #Get array shape
    sz=Z.shape    

    #Get grid spacing
    dx=abs(X[1,1]-X[0,0])
    dy=abs(Y[1,1]-Y[0,0])

    #Linearise the grid
    X=np.reshape(X,X.shape[0]*X.shape[1],order='F')
    Y=np.reshape(Y,Y.shape[0]*Y.shape[1],order='F')
    Z=np.reshape(Z,Z.shape[0]*Z.shape[1],order='F')
    
    #Define viewpoint in DEM grid space      
    X=(X-viewpoint[0])/dx
    Y=(Y-viewpoint[1])/dy        
    Z=Z-viewpoint[2]

    #Create empty array
    d=np.zeros(len(X))

    #Populate array    
    for i in range(len(X)):
        if (np.isnan(X[i]) or np.isnan(Y[i]) or np.isnan(Z[i])):
            d[i]=float('NaN')
        else:
            d[i]=np.sqrt(X[i]*X[i]+Y[i]*Y[i]+Z[i]*Z[i])
            
    #Pythagoras' theorem
    #ImGRAFT/Matlab equiv: x=atan2(Y,X)+math.pi)/(math.pi*2);             (MAT)
    dint=np.round(np.sqrt(X*X+Y*Y))
    
    #Create empty array 
    x=np.empty(X.shape[0])

    #Populate array
    for i in xrange(X.shape[0]):
        x[i]=(math.atan2(Y[i],X[i])+math.pi)/(math.pi*2)
    y=Z/d
    
    #Round values and sort array
    #ImGRAFT/Matlab equiv: [~,ix]=sortrows([round(sqrt(X.^2+Y.^2)) x]);   (MAT) 
    ix=np.lexsort((x,dint)).tolist()

    #Return a boolean of all array values that are not zero       
    #ImGRAFT/Matlab equiv: loopix=find(diff(x(ix))<0);                    (MAT)
    loopix=np.nonzero(np.diff(x[ix])<0)[0]

    #Create boolean array of 1's
    #ImGRAFT/Matlab equiv: vis=true(size(X,1),1);                         (MAT)
    vis=np.ones(x.shape, dtype=bool)        

    #Return maximum value (ignoring nans)
    maxd=np.nanmax(d) 

    #Number of points in voxel horizon    
    N=np.ceil(2.*math.pi/(dx/maxd))

    #Populate viewshed x array
    #ImGRAFT/Matlab equiv: voxx=(0:N)'/N;                                 (MAT)
    voxx=np.zeros(int(N)+1)
    n=voxx.shape[0]
    for i in range(n):
        voxx[i]=i*1./(n-1)
    
    #Define viewshed y array
    #ImGRAFT/Matlab equiv: voxy=zeros(size(voxx))-inf;                    (MAT)
    voxy=np.zeros(n)-1.e+308

    #Define visibility of each point in the array
    for k in range(loopix.size-1):            
        lp=ix[loopix[k]+1:loopix[k+1]+1]
        lp=lp[-1:]+lp[:]+lp[:1]
        yy=y[lp]
        xx=x[lp]     
        xx[0]=xx[0]-1
        xx[-1]=xx[-1]+1       
        f = interpolate.interp1d(voxx,voxy)
        vis[lp[1:-1]]=f(xx[1:-1])<yy[1:-1]        
        f=interpolate.interp1d(xx,yy)
        voxy=np.maximum(voxy,f(voxx))

    #Re-format voolean array
    vis=np.reshape(vis,sz,order='F')
    vis.shape=sz

    #Return boolean array
    return vis


#------------------------------------------------------------------------------

#if __name__ == "__main__":   
#    print '\nProgram finished'

#------------------------------------------------------------------------------   