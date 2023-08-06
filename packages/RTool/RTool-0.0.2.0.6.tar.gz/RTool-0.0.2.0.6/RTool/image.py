'''RTool/image.py

This module is a combination of various image manipulation tools. To be
used in combination with RTool.video.

'''

def pixelateImage(imagePath, savePath=rootPath, bitSize=32):
    '''Pixelate an image to a specified bit size.

    This method currently only uses the median method of compression.

    Args:
        imagePath (str): The path to an image file
        savePath (str): The path in which to save the output.
            Defaults to the script's rootPath.
        bitSize (int): The verticle resolution of the output image.
            Defaults to 32.
    Todo:
        * Add more compression methods
        * Fix horizontal bitScale and portrait style images
    
    '''
    imgNameWithExtension = basename(imagePath)
    imgName = imgNameWithExtension[:imgNameWithExtension.find('.')]
    img = Image.open(imagePath)
    pixels = img.load()

    width, height = img.size

    scaleRatio = height/width
    bitSizeY = int(round(bitSize*scaleRatio))
    widthBitRatio  = int(round(width/bitSize))
    heightBitRatio = int(round(height/bitSizeY))

    bitImgs = [[0] * (bitSizeY)] * (bitSize)

    print("pixelImage: %s | (%d,%d)->(%d,%d) || %s"
          %(imgName,width,height,bitSize,bitSizeY,stopwatch.current()))

    #outputImg = Image.new('RGB', (width,height), (0,0,0)) # used to maintain resolution
    bitOutputImg = Image.new('RGB', (bitSize, bitSizeY), (0,0,0))
    bitPixels = bitOutputImg.load()
    
    for x in range(bitSize):
        for y in range(bitSizeY):
            '''
            print(x,y,"test[x][y]="+str(bitImgs[x][y]))
            print(( x*widthBitRatio,
                  y*heightBitRatio,
                 (x+1)*widthBitRatio,
                 (y+1)*heightBitRatio))
            '''
            xPrime = (x+1)*widthBitRatio
            if xPrime > width:
                xPrime = width
            yPrime = (y+1)*heightBitRatio
            if yPrime > height:
                yPrime = height
            bitImgs[x][y] = img.crop(
                ( x*widthBitRatio,
                  y*heightBitRatio,
                 (x+1)*widthBitRatio,
                 (y+1)*heightBitRatio))
            medianColor = ImageStat.Stat(bitImgs[x][y]).median
            roundedMedianColor = [int(color) for color in medianColor]
            #print(roundedMeanColor)
            bit = Image.new(
                'RGB',
                (widthBitRatio,heightBitRatio),
                tuple(roundedMedianColor))
            #outputImg.paste(bit, (x*widthBitRatio,y*heightBitRatio))
            bitPixels[x,y] = tuple(roundedMedianColor)


    bitOutputImg.format = "PNG"
    outputName = 'out_%s_%sbit.png'%(imgName, str(bitSize))
    bitOutputImg.save(os.path.join(savePath, outputName))
    #displayImg.show()
    #outputImg.save('out_%s_%s.png'%(imgName,str(bitSize)))

    #run_command("echo %PATH%")
    #run_command("start %s"%(os.path.join(rootPath,outputName)))
