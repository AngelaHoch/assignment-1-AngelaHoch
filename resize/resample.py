import numpy
import math
from .interpolation import bilinear_interpolation as inter

class resample:

    def resize(self, image, fx = None, fy = None, interpolation = None):
        """calls the appropriate funciton to resample an image based on the interpolation method
        image: the image to be resampled
        fx: scale along x direction (eg. 0.5, 1.5, 2.5)
        fx: scale along y direction (eg. 0.5, 1.5, 2.5)
        interpolation: method used for interpolation ('either bilinear or nearest_neighbor)
        returns a resized image based on the interpolation method
        """

        if interpolation == 'bilinear':
            return self.bilinear_interpolation(image, fx, fy)

        elif interpolation == 'nearest_neighbor':
            return self.nearest_neighbor(image, fx, fy)

    def nearest_neighbor(self, image, fx, fy):
        """resizes an image using bilinear interpolation approximation for resampling
        image: the image to be resampled
        fx: scale along x direction (eg. 0.5, 1.5, 2.5)
        fx: scale along y direction (eg. 0.5, 1.5, 2.5)
        returns a resized image based on the nearest neighbor interpolation method
        """

        #print(image.shape)
        #print("y, x")
        
        sizex = int(image.shape[1] * float(fx))
        sizey = int(image.shape[0] * float(fy))
        
        newImage = numpy.zeros((sizey, sizex))

        #print(newImage.shape)
        
        for j in range(sizey):
            y = int(j / ((sizey) / (image.shape[0])))
            for i in range(sizex):
                x = int(i / ((sizex) / (image.shape[1])))
                newImage[j][i] = image[y][x]
                
        image = newImage
        
        return image

    def bilinear_interpolation(self, image, fx, fy):
        """resizes an image using bilinear interpolation approximation for resampling
        image: the image to be resampled
        fx: scale along x direction (eg. 0.5, 1.5, 2.5)
        fx: scale along y direction (eg. 0.5, 1.5, 2.5)
        returns a resized image based on the bilinear interpolation method
        """
        #inter_obj = inter.interpolation()
        
        sizex = int(image.shape[1] * float(fx))
        sizey = int(image.shape[0] * float(fy))

        newImage = numpy.zeros((sizey, sizex))

        for j in range(sizey):
            y = (j / ((sizey) / (image.shape[0])))
            ytest = int(y)
            for i in range(sizex):
                x = (i / ((sizex) / (image.shape[1])))
                xtest = int(x)                
                if (y != ytest or x != xtest):
                    x1 = int(math.floor(x))
                    x2 = int(math.ceil(x))
                    if x2 >= image.shape[1]:
                        x2 = x1
                    y1 = int(math.floor(y))
                    y2 = int(math.ceil(y))
                    if y2 >= image.shape[0]:                       
                        y2 = y1
                    pt1 = (y1,x1);
                    pt2 = (y1,x2);
                    pt3 = (y2,x1);
                    pt4 = (y2,x2);
                    unknown = (y,x);
                    #intensity = inter_obj.bilinear_interpolation(image, pt1, pt2, pt3, pt4, unknown)
                    intensity = inter(image, pt1, pt2, pt3, pt4, unknown)
                    newImage[j][i] = intensity
                else:
                    newImage[j][i] = image[int(y)][int(x)]
                
        image = newImage

        return image

