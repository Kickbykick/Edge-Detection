###To run the code, use the commandline and provide one of the pgm files.

'python cannyEdgeDetectionAlgo.py lena.pgm'

###How to convert PPM to PGM

    pgmVersion = filename.replace('.ppm', '.pgm')
    newPgmArray = []
    
    for i in  range(0, len(npArray)):
	    if ( (i+1) % 3 == 0 ):
		    greyscaleCalc = (0.1140*npArray[i]) + (0.5870*npArray[i-1]) + (0.29890*npArray[i-2])
			value = int(greyscaleCalc)
		    newPgmArray.append(int(value))
		    
    fileArray = np.array(newPgmArray)
    ppf.createFile(pgmVersion, "P2\n", stringRC, stringMax, fileArray)
