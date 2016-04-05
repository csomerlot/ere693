import time, numpy

def flowAccumulate(flowdirData, bmppointData=None):
    '''process (loop through) datasets'''
    
    #Make output array
    height = len(flowdirData)
    width = len(flowdirData[0])
    outputData = numpy.empty([height, width], dtype=float)
    
    start = time.time()
    print "Starting at %s" % (time.asctime())
    count = 0
    for R in range(1, height-1):
        if count in [1, 2, 5, 10, 15, 25, 50, 100, 200, 500, 1000, 1500, 2000]:
            print "Processing %i rows took %i seconds" % (count, (time.time()-start))
        count += 1
        
        for C in range(1, width-1):
            c = C
            r = R
            passedVal = 1
            while 0 < r < height and 0 < c < width:
                if bmppointData:
                    bmpval = bmppointData[r][c]
                    if bmpval > 0: 
                        passedVal = 1 - bmpval
                outputData[r][c] += passedVal
                flowdirval = flowdirData[r][c]
                if flowdirval == 1:
                    c += 1
                    r += 0
                if flowdirval == 2:
                    c += 1
                    r += 1
                if flowdirval == 4:
                    c += 0
                    r += 1
                if flowdirval == 8:
                    c += -1
                    r += 1
                if flowdirval == 16:
                    c += -1
                    r += 0
                if flowdirval == 32:
                    c += -1
                    r += -1
                if flowdirval == 64:
                    c += 0
                    r += -1
                if flowdirval == 128:
                    c += 1
                    r += -1
                    
    return outputData
    