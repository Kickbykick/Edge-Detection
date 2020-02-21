import numpy as np
import PgmPpmFormatter as ppf
import math
import sys

ImageName = ""

def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        print("Please provide the name of a file in the form image.pgm.")
        return

    data = ppf.readImageFile(filename)
    ImageName = filename
    theImage = data[0]
    imageWidth, imageHeight = data[1]
    maxpixel = data[2]

    #Smooth array and use the Canny Edge Detection Algorithm on it
    smooth_array2d = ppf.convolve2D(theImage, ppf.gaussian2dKernel(5, 1.4))
    ppf.writeimage(ImageName.strip(".pgm") + "GuassianBlur.pgm", 'P2', maxpixel, smooth_array2d)
    cannyEdge(smooth_array2d, imageWidth, imageHeight, maxpixel, ImageName)   

def cannyEdge(theArray, imageWidth, imageHeight, maxpixel, filename):
    gradientVector = np.zeros_like(theArray)
    thetaVector = np.zeros_like(theArray)
    cannyVector = np.zeros_like(theArray)

    highThreshold = 0.19* maxpixel
    lowThreshold = 0.05 * highThreshold
    firstSide = 0
    scndSide = 0
    
    #Central Difference Variables
    ctDiffX = 0
    ctDiffY = 0
    for y in range(1, theArray.shape[1]-1): 
        for x in range(1, theArray.shape[0]-1):
            ctDiffX = ( theArray[x-1, y] - theArray[x+1, y] ) / 2
    
            ctDiffY = ( theArray[x, y-1] - theArray[x, y+1] ) / 2

            # Calculate Gradient
            calcGrad = np.hypot( ctDiffX, ctDiffY ) 
            theTheta = math.atan2( abs(ctDiffY), abs(ctDiffX) )

            gradientVector[x, y] = calcGrad
            thetaVector[x, y] = theTheta
    
    for y in range(1, thetaVector.shape[1]-1): 
        for x in range(1, thetaVector.shape[0]-1):
            firstSide = maxpixel
            scndSide = maxpixel
                
            if (0 <= thetaVector[x, y] < 22.5) or (157.5 <= thetaVector[x, y] <= 180):
                firstSide = gradientVector[x, y+1]
                scndSide = gradientVector[x, y-1]
            #angle 45
            elif (22.5 <= thetaVector[x, y] < 67.5):
                firstSide = gradientVector[x+1, y-1]
                scndSide = gradientVector[x-1, y+1]
            #angle 90
            elif (67.5 <= thetaVector[x, y] < 112.5):
                firstSide = gradientVector[x+1, y]
                scndSide = gradientVector[x-1, y]
            #angle 135
            elif (112.5 <= thetaVector[x, y] < 157.5):
                firstSide = gradientVector[x-1, y-1]
                scndSide = gradientVector[x+1, y+1]

            # Thining Algorithm
            if ( (gradientVector[x,y] >= firstSide) and (gradientVector[x,y] >= scndSide) ):
                cannyVector[x,y] = gradientVector[x, y]
            # else:
            #     cannyVector[x,y] = 0
            
            if( cannyVector[x, y] < lowThreshold ):
                cannyVector[x,y] = 0
            elif( lowThreshold <= cannyVector[x, y] and cannyVector[x, y] < highThreshold ):
                if( (gradientVector[x+1, y]>=highThreshold)or(gradientVector[x+1, y-1]>=highThreshold)or(gradientVector[x+1, y+1]>=highThreshold)
                    or(gradientVector[x-1, y]>=highThreshold)or(gradientVector[x-1, y-1]>=highThreshold)or(gradientVector[x-1, y+1]>=highThreshold)
                    or(gradientVector[x, y+1]>=highThreshold)or(gradientVector[x, y-1]>=highThreshold) ):
                    cannyVector[x, y] = 0
                else:
                    cannyVector[x, y] = maxpixel

    ppf.writeimage(filename.strip(".pgm") + "GradientCalculation.pgm", 'P2', maxpixel, gradientVector)
    print "Making Edge Detected Image ........"
    ppf.writeimage(filename.strip(".pgm") + "CannyEdgeDetectionOutput.pgm", 'P2', maxpixel, cannyVector)


if __name__== "__main__":
    main()