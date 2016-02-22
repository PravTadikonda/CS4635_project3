# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
#from PIL import Image
from PIL import Image, ImageFilter
class Agent:
    COLOR_CUTOFF = 255;
    NUM_OF_3x3_ANS = 8;
    NUM_OF_2x2_ANS = 6;
    SIMILAR = 0.028
    SIMILAR_NO_CHANGE = 0.029
    SIMILAR_HALF = 0.001
    SIMILAR_UNION = 0.025
    MIN_EDGE = 52 
    MAX_EDGE = 131

    logger_enabled = False

    Hash = {}
    allDirections =  [[-1,-1],[0,-1],[1,-1],[-1,0],[1,0],[-1,1],[0,1],[1,1]]
    TotalBlack = 0
    BubleBack = 0  
    figCount = 0
    maxSmallFig =  800
    errorSmallFig = 40

    # subtractValue = False
    # SIMILAR_ADD = 0.028
    # SIMILAR_XOR = 0.021
    # SIMILAR = 0.14

    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an integer representing its
    # answer to the question: "1", "2", "3", "4", "5", or "6". These integers
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName() (as Strings).
    #
    # In addition to returning your answer at the end of the method, your Agent
    # may also call problem.checkAnswer(int givenAnswer). The parameter
    # passed to checkAnswer should be your Agent's current guess for the
    # problem; checkAnswer will return the correct answer to the problem. This
    # allows your Agent to check its answer. Note, however, that after your
    # agent has called checkAnswer, it will *not* be able to change its answer.
    # checkAnswer is used to allow your Agent to learn from its incorrect
    # answers; however, your Agent cannot change the answer to a question it
    # has already answered.
    #
    # If your Agent calls checkAnswer during execution of Solve, the answer it
    # returns will be ignored; otherwise, the answer returned at the end of
    # Solve will be taken as your Agent's answer to this problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self,problem):
        # if (problem.name != 'Basic Problem E-12'): # and (problem.name != 'Basic Problem D-02') and (problem.name != 'Basic Problem D-03') and (problem.name != 'Basic Problem D-11') and (problem.name != 'Basic Problem E-01') and (problem.name != 'Basic Problem E-02') and (problem.name != 'Basic Problem E-03') and (problem.name != 'Basic Problem E-05') and (problem.name != 'Basic Problem E-06') and(problem.name != 'Basic Problem E-07') and(problem.name != 'Basic Problem E-08')and (problem.name != 'Basic Problem E-10') and (problem.name != 'Basic Problem E-11'):
        #      return -1
        print problem.name, '-', problem.checkAnswer(6)
        answer = -1;

        figureA = problem.figures['A'];
        figureB = problem.figures['B'];
        figureC = problem.figures['C'];   
        figureD = problem.figures['D'];
        figureE = problem.figures['E'];
        figureF = problem.figures['F'];
        figureG = problem.figures['G'];
        figureH = problem.figures['H'];

        transformations = {}

        if (problem.problemType == '3x3'):
            if not (problem.hasVerbal):
            # if (problem.hasVisual):
                figureAImage = Image.open(figureA.visualFilename)
                figureBImage = Image.open(figureB.visualFilename)
                figureCImage = Image.open(figureC.visualFilename)
                figureDImage = Image.open(figureD.visualFilename)
                figureEImage = Image.open(figureE.visualFilename)
                figureFImage = Image.open(figureF.visualFilename)
                figureGImage = Image.open(figureG.visualFilename)
                figureHImage = Image.open(figureH.visualFilename)
                

                answer = self.diagonalFigures(figureAImage, figureEImage, problem)
                

                                # print 'ACROSS:', acrossTransformation
                                # print 'DOWN:', downwardTransformation
                if (answer == -1):
                    filler = ''
                    transformations['A-B-C'] = self.findTransformation(figureAImage, figureBImage, figureCImage);
                    transformations['D-E-F'] = self.findTransformation(figureDImage, figureEImage, figureFImage);
                    transformations['A-D-G'] = self.findTransformation(figureAImage, figureDImage, figureGImage);
                    transformations['B-E-H'] = self.findTransformation(figureBImage, figureEImage, figureHImage);

                    answerTransformation = {}
                    for ans in range(1, self.NUM_OF_3x3_ANS + 1):
                        # print ans
                        # print '----------------------------------------'
                        answerComparisons = {}
                        figureImage = Image.open(problem.figures[str(ans)].visualFilename);
                        #across
                        acrossTransformation = self.findTransformation(figureGImage, figureHImage, figureImage);
                        answerComparisons['Row1'] = self.compareTransformations(transformations['A-B-C'], acrossTransformation);
                        answerComparisons['Row2'] = self.compareTransformations(transformations['D-E-F'], acrossTransformation);
                        #downward
                        downwardTransformation = self.findTransformation(figureCImage, figureFImage, figureImage);
                        answerComparisons['Col1'] = self.compareTransformations(transformations['A-D-G'], downwardTransformation);
                        answerComparisons['Col2'] = self.compareTransformations(transformations['B-E-H'], downwardTransformation);

                        answerTransformation[str(ans)] = answerComparisons;
                        # print 'ACROSS:', acrossTransformation
                        # print 'DOWN:', downwardTransformation

                    answer = self.chooseAnswer(answerTransformation);
                    # print answerTransformation
                if (answer == -1):
                    smallFigDic = {}
                
                    smallFigDic['a'] = self.parseImage(figureAImage)
                    if(smallFigDic.has_key("a")):
                        smallFigDic['b'] = self.parseImage(figureBImage)
                    if(smallFigDic.has_key("b")):
                        smallFigDic['c'] = self.parseImage(figureCImage)
                    if(smallFigDic.has_key("c")):
                        smallFigDic['d'] = self.parseImage(figureDImage)
                    if(smallFigDic.has_key("d")):
                        smallFigDic['e'] = self.parseImage(figureEImage)
                    if(smallFigDic.has_key("e")):
                        smallFigDic['f'] = self.parseImage(figureFImage)
                    if(smallFigDic.has_key("f")):
                        smallFigDic['g'] = self.parseImage(figureGImage)
                    if(smallFigDic.has_key("g")):
                        smallFigDic['h'] = self.parseImage(figureHImage)

                    # print smallFigDic
                    if(smallFigDic.has_key("h") and smallFigDic["h"]):
                        answer = self.smallFigDiagonal(smallFigDic, problem)
                if (answer == -1):
                    shapesAndDirections = self.findShapesAndDirections(figureAImage, figureBImage, figureCImage, figureDImage, figureEImage, figureFImage, figureGImage, figureHImage)
                    if (shapesAndDirections != None):
                        answerTransformation = {}
                        for ans in range(1, self.NUM_OF_3x3_ANS + 1):
                            # print ans
                            # print '----------------------------------------'
                            answerComparisons = {}
                            figureImage = Image.open(problem.figures[str(ans)].visualFilename);
                            currImageData = self.findImageData(figureImage)
                            #across
                            if (currImageData != None):
                                acrossTransformation = self.checkEquation(shapesAndDirections['G'], shapesAndDirections['H'], currImageData)
                                downwardTransformation = self.checkEquation(shapesAndDirections['C'], shapesAndDirections['F'], currImageData)

                                if (not acrossTransformation and not downwardTransformation):
                                    answer = ans
                if (answer == -1):
                    answer = self.specialDiagonalFigures(figureAImage, figureEImage, problem)
                
                if (answer == -1):
                    listOfImages = self.seperateImages(figureAImage, figureBImage, figureCImage, figureDImage, figureEImage, figureFImage, figureGImage, figureHImage)
                    transformations['A-B-C'] = self.findInsideOutsideSimilarities(listOfImages[0][0], listOfImages[1][0], listOfImages[2][0], listOfImages[0][1], listOfImages[1][1], listOfImages[2][1])
                    transformations['D-E-F'] = self.findInsideOutsideSimilarities(listOfImages[3][0], listOfImages[4][0], listOfImages[5][0], listOfImages[3][1], listOfImages[4][1], listOfImages[5][1])
                    transformations['A-D-G'] = self.findInsideOutsideSimilarities(listOfImages[0][0], listOfImages[3][0], listOfImages[6][0], listOfImages[0][1], listOfImages[3][1], listOfImages[6][1])
                    transformations['B-E-H'] = self.findInsideOutsideSimilarities(listOfImages[1][0], listOfImages[4][0], listOfImages[7][0], listOfImages[1][1], listOfImages[4][1], listOfImages[7][1])
                    

                    answerTransformation = {}
                    for ans in range(1, self.NUM_OF_3x3_ANS + 1):
                        self.logger( ans)
                        self.logger( '----------------------------------------')
                        answerComparisons = {}

                        figureImage = Image.open(problem.figures[str(ans)].visualFilename);
                        (currInside, currOutside) = self.seperateImage(figureImage)
                        #across
                        acrossTransformation = self.findInsideOutsideSimilarities(listOfImages[6][0], listOfImages[7][0], currInside, listOfImages[6][1], listOfImages[7][1], currOutside)
                        answerComparisons['Row1'] = self.compareTransformations(transformations['A-B-C'], acrossTransformation);
                        answerComparisons['Row2'] = self.compareTransformations(transformations['D-E-F'], acrossTransformation);
                        #downward
                        downwardTransformation = self.findInsideOutsideSimilarities(listOfImages[2][0], listOfImages[5][0], currInside, listOfImages[2][1], listOfImages[5][1], currOutside)
                        answerComparisons['Col1'] = self.compareTransformations(transformations['A-D-G'], downwardTransformation);
                        answerComparisons['Col2'] = self.compareTransformations(transformations['B-E-H'], downwardTransformation);

                        answerTransformation[str(ans)] = answerComparisons;
                        self.logger( ('ACROSS:', acrossTransformation))
                        self.logger( ('DOWN:', downwardTransformation)) 

                    answer = self.chooseAnswer(answerTransformation);
                    self.logger( ('ANSWERS', answerTransformation))
                if (answer == -1):
                    row1 = self.subProblem(figureAImage,figureBImage,figureCImage)
                    row2 = self.subProblem(figureDImage,figureEImage,figureFImage)

                    if(row1[0] and row2[0]):
                        minNum = 1
                        tempAns = -1

                        for ans in range(1, self.NUM_OF_3x3_ANS + 1):
                            figureImage = Image.open(problem.figures[str(ans)].visualFilename);
                            row3 = self.subProblem(figureGImage,figureHImage,figureImage)
                            
                            if(row3[0] and row3[1] < minNum):
                                minNum = row3[1]
                                tempAns = ans

                        if tempAns != -1:
                            answer = tempAns
            else:
                #for homework 2
                filler = ''
        else:
            #for homework 1
            filler = ''

        # print transformations
        print answer
        return answer

    def findShapesAndDirections(self, figure1, figure2, figure3, figure4, figure5, figure6, figure7, figure8):
        shapesAndDirections = {}

        shapesAndDirections['A'] = self.findImageData(figure1)
        shapesAndDirections['B'] = self.findImageData(figure2)
        shapesAndDirections['C'] = self.findImageData(figure3)
        shapesAndDirections['D'] = self.findImageData(figure4)
        shapesAndDirections['E'] = self.findImageData(figure5)
        shapesAndDirections['F'] = self.findImageData(figure6)
        shapesAndDirections['G'] = self.findImageData(figure7)
        shapesAndDirections['H'] = self.findImageData(figure8)
        # print shapesAndDirections

        if (None in shapesAndDirections.values()):
            return None

        if (self.checkEquation(shapesAndDirections['A'], shapesAndDirections['B'], shapesAndDirections['C'])):
            return None
        if (self.checkEquation(shapesAndDirections['D'], shapesAndDirections['E'], shapesAndDirections['F'])):
            return None
        if (self.checkEquation(shapesAndDirections['A'], shapesAndDirections['D'], shapesAndDirections['G'])):
            return None
        if (self.checkEquation(shapesAndDirections['B'], shapesAndDirections['E'], shapesAndDirections['H'])):
            return None
        return shapesAndDirections

    def checkEquation(self, tup1, tup2, tup3):
        (tup11, tup12) = tup1
        (tup21, tup22) = tup2
        (tup31, tup32) = tup3
        # print tup1, tup2, tup3
        return (tup11 + tup21 - tup12 - tup22 != tup31 - tup32)
    def findImageData(self, figure):
        figureData = {}

        width = figure.size[0]
        height = figure.size[1]
        numOfPix = width*height

        prevColor = 255;
        blackPixCount = 0
        numOfObjects = 0
        downWards = 0
        upWards = 0

        checkPrevColor = 255
        checkBlackPix = 0
        checkNumObjs = 0
        checkDown = 0
        checkUp = 0


        for x in range(0, width):
            for y in range(0, height):
                RGB = figure.getpixel((x,y))

                if(y == (height/2 - 20)):
                    if (RGB[0] < self.COLOR_CUTOFF):
                        if (prevColor == self.COLOR_CUTOFF):
                            blackPixCount = 0
                            numOfObjects = numOfObjects + 1

                        blackPixCount = blackPixCount + 1
                        prevColor = 0
                    else:
                        if (prevColor < self.COLOR_CUTOFF):
                            # print blackPixCount
                            if(numOfObjects > 0):
                                if (blackPixCount < 10 and blackPixCount > 6):
                                    upWards = upWards + 1
                                elif (blackPixCount > 44 and blackPixCount < 48):
                                    downWards = downWards + 1
                        prevColor = 255
                
                elif(y == (height/2 + 20)):
                    if (RGB[0] < self.COLOR_CUTOFF):
                        if (checkPrevColor == self.COLOR_CUTOFF):
                            checkBlackPix = 0
                            checkNumObjs = checkNumObjs + 1

                        checkBlackPix = checkBlackPix + 1
                        checkPrevColor = 0
                    else:
                        if (checkPrevColor < self.COLOR_CUTOFF):
                            if(checkNumObjs > 0):
                                # print checkBlackPix
                                if (checkBlackPix < 8 and checkBlackPix > 4):
                                    checkDown = checkDown + 1
                                elif (checkBlackPix > 44 and checkBlackPix < 49):
                                    checkUp = checkUp + 1
                        checkPrevColor = 255
        # print checkUp, '=', upWards
        # print checkDown, '=', downWards
        # print '----'
        if (checkUp == upWards) and (checkDown == downWards):
            # figureData[letter] = (upWards, downWards)
            # return figureData
            return (upWards, downWards)

        # print 'NUMBER OF OBJECTS', numOfObjects
        return None

    #TODO: return a list [1st quad, 2nd quad, 3rd quad, 4th quad, total]
    def numOfBlackPix(self, figure):
        figure.convert('RGB');
        blackPix = 0;
        actualPix = 0;
        width = figure.size[0]
        height = figure.size[1]
        for x in range(0, width):
            for y in range(0, height):
                actualPix = actualPix + 1;
                (R, G, B, T) = figure.getpixel((x, y))
                if R < self.COLOR_CUTOFF:
                    blackPix = blackPix + 1;
        return blackPix;

    def diagonalFigures(self, figure1, figure2, problem):
        if (self.noChangeFigures(figure1, figure2)[0]):
            answerTransformation = {}
            for ans in range(1, self.NUM_OF_3x3_ANS + 1):
                figureImage = Image.open(problem.figures[str(ans)].visualFilename);
                #diagonal
                (diagTrue, percent) = self.noChangeFigures(figure2, figureImage);
                if(diagTrue):
                    answerTransformation[str(ans)] = (diagTrue, percent)
            self.logger( answerTransformation)
            
            if(len(answerTransformation) == 1):
                return answerTransformation.keys()[0]
            elif (len(answerTransformation) > 1):
                minPercent = 1.0
                answer = -1
                for d in answerTransformation:
                    (true, prcnt) = answerTransformation[d];
                    if prcnt < minPercent:
                        minPercent = prcnt
                        answer = d
                return answer
        return -1

    #TODO: make add have two levels (what is being added)
    def findTransformation(self, figure1, figure2, figure3):
        transitions = {}

        firstTwo = self.noChangeFigures(figure1, figure2)
        secondTwo = self.noChangeFigures(figure2, figure3)
        if (firstTwo[0] and secondTwo[0]):
            transitions['NO_CHANGE'] = secondTwo;
            return transitions

        splitAns = self.splitHalfFigures(figure1, figure2, figure3)
        if (splitAns[0]):
            transitions['SPLIT_SIMILARITY'] = splitAns[1]
            return transitions

        addAns = self.addFigures(figure1, figure2, figure3)
        if (addAns[0]):
            transitions['ADD'] = addAns[1]
        if(self.xorFigures(figure1, figure2, figure3)):
            transitions['XOR'] = True
            return transitions
        if (not addAns[0]) and (self.unionFigures(figure1, figure2, figure3)):
            transitions['UNION'] = True
            return transitions
        return transitions

    def noChangeFigures(self, figure1, figure2):
        noChangeBool = False
        figure1BlackPixCount = 0;
        figure2BlackPixCount = 0;
        figure1.convert('RGB')
        figure2.convert('RGB')

        width = figure1.size[0]
        height = figure1.size[1]
        differences = 0;
        numOfPix = width*height;
        newImg = Image.new('RGB', (width, height), 'white')
        newPix = newImg.load()
        
        for x in range(0, width):
            for y in range(0, height):
                RGB1 = figure1.getpixel((x, y))
                RGB2 = figure2.getpixel((x, y))
                newPix[x,y] = (RGB2[0], RGB2[1], RGB2[2])

                if RGB1[0] < self.COLOR_CUTOFF:
                    figure1BlackPixCount = figure1BlackPixCount + 1;
                if RGB2[0] < self.COLOR_CUTOFF:
                    figure2BlackPixCount = figure2BlackPixCount + 1;

                if (RGB1[0] < self.COLOR_CUTOFF) ^ (RGB2[0] < self.COLOR_CUTOFF):
                    differences = differences + 1;
                    newPix[x, y] = (255,0,100)

        if (float(differences)/numOfPix < self.SIMILAR_NO_CHANGE):
            noChangeBool = True;
        # self.logger( ('DIFFERENCE',float(differences)/numOfPix))
        # newImg.show()  
        return (noChangeBool, float(differences)/numOfPix)

    def addFigures(self, figure1, figure2, figure3):
        addBool = False
        figure1.convert('RGB')
        figure2.convert('RGB')
        figure3.convert('RGB')

        width = figure1.size[0]
        height = figure1.size[1]
        differences = 0;
        numOfPix = width*height;
        
        #check if this revision of addition (black Pix Exist) is necessary
        for x in range(0, width):
            for y in range(0, height):
                (R1, G1, B1, T1) = figure1.getpixel((x, y))
                (R2, G2, B2, T2) = figure2.getpixel((x, y))
                (R3, G3, B3, T3) = figure3.getpixel((x, y))

                blackPixExist = False
                if R1 < self.COLOR_CUTOFF:
                    blackPixExist = True
                if R2 < self.COLOR_CUTOFF:
                    blackPixExist = True
                
                if (blackPixExist) ^ (R3 < self.COLOR_CUTOFF):
                    differences = differences + 1;

        if (float(differences)/numOfPix < self.SIMILAR):
            addBool = True;

        if not addBool:
            differences = 0;
            for x in range(0, width):
                for y in range(0, height):
                    (R1, G1, B1, T1) = figure1.getpixel((x, y))
                    (R2, G2, B2, T2) = figure2.getpixel((x, y))
                    (R3, G3, B3, T3) = figure3.getpixel((x, y))
                    
                    blackPixExist = False
                    if R1 < self.COLOR_CUTOFF:
                        blackPixExist = True
                    if R3 < self.COLOR_CUTOFF:
                        blackPixExist = True
                    
                    if (blackPixExist) ^ (R2 < self.COLOR_CUTOFF):
                        differences = differences + 1;
            if (float(differences)/numOfPix < self.SIMILAR):
                addBool = True;
        self.logger( ('ADD',float(differences)/numOfPix))
        return (addBool, float(differences)/numOfPix)

    def subtractFigures(self, figure1, figure2, figure3):
        figure1BlackPixCount = self.numOfBlackPix(figure1);
        figure2BlackPixCount = self.numOfBlackPix(figure2);
        figure3BlackPixCount = self.numOfBlackPix(figure3);

        if (figure1BlackPixCount - figure2BlackPixCount == figure3BlackPixCount):
            return True
        return False
        
    def xorFigures(self, figure1, figure2, figure3):
        xorBool = False
        figure1.convert('RGB')
        figure2.convert('RGB')
        figure3.convert('RGB')

        width = figure1.size[0]
        height = figure1.size[1]
        differences = 0;
        numOfPix = width*height;
        # newImg = Image.new('RGB', (width, height), 'white')
        # newPix = newImg.load()
        
        for x in range(0, width):
            for y in range(0, height):
                (R1, G1, B1, T1) = figure1.getpixel((x, y))
                (R2, G2, B2, T2) = figure2.getpixel((x, y))
                (R3, G3, B3, T3) = figure3.getpixel((x, y))
                # newPix[x, y] = (R3,G3,B3)

                blackPixExist1 = False
                blackPixExist2 = False
                if R1 < self.COLOR_CUTOFF:
                    blackPixExist1 = True
                if R2 < self.COLOR_CUTOFF:
                    blackPixExist2 = True
                
                if (blackPixExist1 ^ blackPixExist2) ^ (R3 < self.COLOR_CUTOFF):
                    differences = differences + 1;
                    # newPix[x, y] = (255,0,100)

        if (float(differences)/numOfPix < self.SIMILAR):
            xorBool = True;
        # self.logger( ('XOR PERCENTAGE:',(float(differences)/numOfPix < self.SIMILAR), float(differences)/numOfPix))
        # newImg.show()
        # return (xorBool, float(differences)/numOfPix)
        return xorBool
    
    def unionFigures(self, figure1, figure2, figure3):
        unionBool = False
        figure1.convert('RGB')
        figure2.convert('RGB')
        figure3.convert('RGB')

        width = figure1.size[0]
        height = figure1.size[1]
        differences = 0;
        numOfPix = width*height;
        
        for x in range(0, width):
            for y in range(0, height):
                (R1, G1, B1, T1) = figure1.getpixel((x, y))
                (R2, G2, B2, T2) = figure2.getpixel((x, y))
                (R3, G3, B3, T3) = figure3.getpixel((x, y))

                blackPixExist1 = False
                blackPixExist2 = False
                if R1 < self.COLOR_CUTOFF:
                    blackPixExist1 = True
                if R2 < self.COLOR_CUTOFF:
                    blackPixExist2 = True
                
                if (blackPixExist1 and blackPixExist2) ^ (R3 < self.COLOR_CUTOFF):
                    differences = differences + 1;

        if (float(differences)/numOfPix < self.SIMILAR_UNION):
            unionBool = True;
        
        self.logger( ('UNION:', float(differences)/numOfPix))
        
        return unionBool

    def splitHalfFigures(self, figure1, figure2, figure3):
        transitions = {}
        splitBool = False
        figure1.convert('RGB')
        figure2.convert('RGB')
        figure3.convert('RGB')
        width = figure1.size[0]
        height = figure1.size[1]
        numOfPix = width*height/2

        R12differenceTop = 0.0
        R13differenceTop = 0.0
        R23differenceTop = 0.0
        
        R12differenceBottom = 0.0
        R13differenceBottom = 0.0
        R23differenceBottom = 0.0
        
        for x in range(0, width):
            for y in range(0, height):
                (R1, G1, B1, T1) = figure1.getpixel((x,y))
                (R2, G2, B2, T2) = figure2.getpixel((x,y))
                (R3, G3, B3, T3) = figure3.getpixel((x,y))
                if(y < height/2):
                    if (R1 < self.COLOR_CUTOFF) ^ (R2 < self.COLOR_CUTOFF):
                        R12differenceTop = R12differenceTop + 1.0
                    if (R1 < self.COLOR_CUTOFF) ^ (R3 < self.COLOR_CUTOFF):
                        R13differenceTop = R13differenceTop + 1.0
                    if (R2 < self.COLOR_CUTOFF) ^ (R3 < self.COLOR_CUTOFF):
                        R23differenceTop = R23differenceTop + 1.0
                else:
                    if (R1 < self.COLOR_CUTOFF) ^ (R2 < self.COLOR_CUTOFF):
                        R12differenceBottom = R12differenceBottom + 1.0
                    if (R1 < self.COLOR_CUTOFF) ^ (R3 < self.COLOR_CUTOFF):
                        R13differenceBottom = R13differenceBottom + 1.0
                    if (R2 < self.COLOR_CUTOFF) ^ (R3 < self.COLOR_CUTOFF):
                        R23differenceBottom = R23differenceBottom + 1.0

        topSimilarity = None
        bottomSimilarity = None
        if (R12differenceTop < R13differenceTop) and (R12differenceTop < R23differenceTop):
            topSimilarity = ('Top-12', R12differenceTop)
        if (R13differenceTop < R12differenceTop) and (R13differenceTop < R23differenceTop):
            topSimilarity = ('Top-13', R13differenceTop)
        if (R23differenceTop < R12differenceTop) and (R23differenceTop < R13differenceTop):
            topSimilarity = ('Top-23', R23differenceTop)
        if (R12differenceBottom < R13differenceBottom) and (R12differenceBottom < R23differenceBottom):
            bottomSimilarity = ('Bottom-12', R12differenceBottom)
        if (R13differenceBottom < R12differenceBottom) and (R13differenceBottom < R23differenceBottom):
            bottomSimilarity = ('Bottom-13', R13differenceBottom)
        if (R23differenceBottom < R12differenceBottom) and (R23differenceBottom < R13differenceBottom):
            bottomSimilarity = ('Bottom-23', R23differenceBottom)

        if topSimilarity != None and bottomSimilarity != None:
            if (topSimilarity[1]/numOfPix < self.SIMILAR_HALF) and (bottomSimilarity[1]/numOfPix < self.SIMILAR_HALF):
                splitBool = True
                topSimilarity = (topSimilarity[0], topSimilarity[1]/float(numOfPix))
                bottomSimilarity = (bottomSimilarity[0], bottomSimilarity[1]/float(numOfPix))

        return (splitBool, (topSimilarity, bottomSimilarity))    

    #TODO: check other diagonals for cross-check
    def specialDiagonalFigures(self, figure1, figure2, problem):
        width = figure1.size[0]
        height = figure1.size[1]
        numOfPix = width*height
        insideImg1 = Image.new('RGB', (width, height), 'white')
        insidePix1 = insideImg1.load()
        insideImg2 = Image.new('RGB', (width, height), 'white')
        insidePix2 = insideImg2.load()
        outsideImg1 = Image.new('RGB', (width, height), 'white')
        outsidePix1 = outsideImg1.load()
        outsideImg2 = Image.new('RGB', (width, height), 'white')
        outsidePix2 = outsideImg2.load()

        insideDifferences = 0.0
        outsideDifferences = 0.0
        insideSame = 0.0
        outsideSame = 0.0

        for x in range(0, width):
            for y in range(0, height):
                (R1, G1, B1, T1) = figure1.getpixel((x,y))
                (R2, G2, B2, T2) = figure2.getpixel((x,y))
                if (x > self.MIN_EDGE and x < self.MAX_EDGE and y > self.MIN_EDGE and y < self.MAX_EDGE):
                    insidePix1[x,y] = (R1, G1, B1)
                    insidePix2[x,y] = (R2, G2, B2)

                    if (R1 < self.COLOR_CUTOFF) ^ (R2 < self.COLOR_CUTOFF):
                        insideDifferences = insideDifferences + 1.0
                    else:
                        insideSame = insideSame + 1.0
                else:
                    outsidePix1[x,y] = (R1, G1, B1)
                    outsidePix2[x,y] = (R2, G2, B2)

                    if (R1 < self.COLOR_CUTOFF) ^ (R2 < self.COLOR_CUTOFF):
                        outsideDifferences = outsideDifferences + 1.0
                    else:
                        outsideSame = outsideSame + 1.0

        self.logger( ('inside difference', insideDifferences/numOfPix))
        self.logger( ('outside same', outsideDifferences/numOfPix))

        insidePercent = insideDifferences/numOfPix
        outsidePercent = outsideDifferences/numOfPix

        if (insidePercent < self.SIMILAR_NO_CHANGE) ^ (outsidePercent < self.SIMILAR_NO_CHANGE):

            insideSameOutsideDifferent = False
            outsideSameInsideDifferent = False
            if (insidePercent < self.SIMILAR_NO_CHANGE) and (outsidePercent > self.SIMILAR_NO_CHANGE):
                self.logger( 'inside-same, outside-different')
                insideSameOutsideDifferent = True
            elif (insidePercent > self.SIMILAR_NO_CHANGE) and (outsidePercent < self.SIMILAR_NO_CHANGE):
                self.logger( 'inside-different, outside-same')
                outsideSameInsideDifferent = True

            answerTransformation = {}
            for ans in range(1, self.NUM_OF_3x3_ANS + 1):
                figureImage = Image.open(problem.figures[str(ans)].visualFilename);
                figureImage.convert('RGB')
                outsideDiffs1 = 0
                outsideDiffs2 = 0
                insideDiffs1 = 0
                insideDiffs2 = 0

                for x in range(0, width):
                    for y in range(0, height):
                        (R1, G1, B1) = outsideImg1.getpixel((x, y))
                        (R2, G2, B2) = outsideImg2.getpixel((x, y))
                        (R3, G3, B3) = insideImg1.getpixel((x, y))
                        (R4, G4, B4) = insideImg2.getpixel((x, y))
                        (R5, G5, B5, T5) = figureImage.getpixel((x, y))
                        if (insideSameOutsideDifferent):
                            if (x > self.MIN_EDGE and x < self.MAX_EDGE and y > self.MIN_EDGE and y < self.MAX_EDGE):
                                if (R3 < self.COLOR_CUTOFF) ^ (R5 < self.COLOR_CUTOFF):
                                    insideDiffs1 = insideDiffs1 + 1;
                            else:
                                if (R1 < self.COLOR_CUTOFF) ^ (R5 < self.COLOR_CUTOFF):
                                    outsideDiffs1 = outsideDiffs1 + 1;
                                if (R2 < self.COLOR_CUTOFF) ^ (R5 < self.COLOR_CUTOFF):
                                    outsideDiffs2 = outsideDiffs2 + 1;
                        elif (outsideSameInsideDifferent):
                            if (x > self.MIN_EDGE and x < self.MAX_EDGE and y > self.MIN_EDGE and y < self.MAX_EDGE):
                                if (R3 < self.COLOR_CUTOFF) ^ (R5 < self.COLOR_CUTOFF):
                                    insideDiffs1 = insideDiffs1 + 1;
                                if (R4 < self.COLOR_CUTOFF) ^ (R5 < self.COLOR_CUTOFF):
                                    insideDiffs2 = insideDiffs2 + 1;
                            else:
                                if (R1 < self.COLOR_CUTOFF) ^ (R5 < self.COLOR_CUTOFF):
                                    outsideDiffs1 = outsideDiffs1 + 1;
                if(insideSameOutsideDifferent):
                    if (float(insideDiffs1)/numOfPix < self.SIMILAR_NO_CHANGE) and (float(outsideDiffs2)/numOfPix > self.SIMILAR_NO_CHANGE) and (float(outsideDiffs1)/numOfPix > self.SIMILAR_NO_CHANGE):
                        answerTransformation[str(ans)] = (float(insideDiffs1)/numOfPix, float(outsideDiffs1)/numOfPix, float(outsideDiffs2)/numOfPix)
                elif (outsideSameInsideDifferent):
                    if (float(insideDiffs1)/numOfPix > self.SIMILAR_NO_CHANGE) and (float(insideDiffs2)/numOfPix > self.SIMILAR_NO_CHANGE) and (float(outsideDiffs1)/numOfPix < self.SIMILAR_NO_CHANGE):
                        answerTransformation[str(ans)] = (float(outsideDiffs1)/numOfPix, float(insideDiffs1)/numOfPix, float(insideDiffs2)/numOfPix)
            self.logger( answerTransformation)
            if(len(answerTransformation) == 1):
                return answerTransformation.keys()[0]
            else:
                minPercent = 1.0
                answer = -1
                for d in answerTransformation:
                    (inside1, outside1, outside2) = answerTransformation[d];
                    if inside1 < minPercent:
                        minPercent = inside1
                        answer = d
                return answer

        # insideImg1.show()
        # outsideImg1.show()
        # insideImg2.show()
        # outsideImg2.show()
        return -1
  
    #TODO: write better code!
    def seperateImages(self, figure1, figure2, figure3, figure4, figure5, figure6, figure7, figure8):
        # figure1.show()
        # figure2.show()
        # figure3.show()
        width = figure1.size[0]
        height = figure1.size[1]
        numOfPix = width*height
        newImages = []
        insideImg1 = Image.new('RGB', (width, height), 'white')
        insidePix1 = insideImg1.load()
        insideImg2 = Image.new('RGB', (width, height), 'white')
        insidePix2 = insideImg2.load()
        insideImg3 = Image.new('RGB', (width, height), 'white')
        insidePix3 = insideImg3.load()
        insideImg4 = Image.new('RGB', (width, height), 'white')
        insidePix4 = insideImg4.load()
        insideImg5 = Image.new('RGB', (width, height), 'white')
        insidePix5 = insideImg5.load()
        insideImg6 = Image.new('RGB', (width, height), 'white')
        insidePix6 = insideImg6.load()
        insideImg7 = Image.new('RGB', (width, height), 'white')
        insidePix7 = insideImg7.load()
        insideImg8 = Image.new('RGB', (width, height), 'white')
        insidePix8 = insideImg8.load()
        outsideImg1 = Image.new('RGB', (width, height), 'white')
        outsidePix1 = outsideImg1.load()
        outsideImg2 = Image.new('RGB', (width, height), 'white')
        outsidePix2 = outsideImg2.load()
        outsideImg3 = Image.new('RGB', (width, height), 'white')
        outsidePix3 = outsideImg3.load()
        outsideImg4 = Image.new('RGB', (width, height), 'white')
        outsidePix4 = outsideImg4.load()
        outsideImg5 = Image.new('RGB', (width, height), 'white')
        outsidePix5 = outsideImg5.load()
        outsideImg6 = Image.new('RGB', (width, height), 'white')
        outsidePix6 = outsideImg6.load()
        outsideImg7 = Image.new('RGB', (width, height), 'white')
        outsidePix7 = outsideImg7.load()
        outsideImg8 = Image.new('RGB', (width, height), 'white')
        outsidePix8 = outsideImg8.load()

        for x in range(0, width):
            for y in range(0, height):
                (R1, G1, B1, T1) = figure1.getpixel((x,y))
                (R2, G2, B2, T2) = figure2.getpixel((x,y))
                (R3, G3, B3, T3) = figure3.getpixel((x,y))
                (R4, G4, B4, T4) = figure4.getpixel((x,y))
                (R5, G5, B5, T5) = figure5.getpixel((x,y))
                (R6, G6, B6, T6) = figure6.getpixel((x,y))
                (R7, G7, B7, T7) = figure7.getpixel((x,y))
                (R8, G8, B8, T8) = figure8.getpixel((x,y))
                if (x > self.MIN_EDGE and x < self.MAX_EDGE and y > self.MIN_EDGE and y < self.MAX_EDGE):
                    insidePix1[x,y] = (R1, G1, B1)
                    insidePix2[x,y] = (R2, G2, B2)
                    insidePix3[x,y] = (R3, G3, B3)
                    insidePix4[x,y] = (R4, G4, B4)
                    insidePix5[x,y] = (R5, G5, B5)
                    insidePix6[x,y] = (R6, G6, B6)
                    insidePix7[x,y] = (R7, G7, B7)
                    insidePix8[x,y] = (R8, G8, B8)
                else:
                    outsidePix1[x,y] = (R1, G1, B1)
                    outsidePix2[x,y] = (R2, G2, B2)
                    outsidePix3[x,y] = (R3, G3, B3)
                    outsidePix4[x,y] = (R4, G4, B4)
                    outsidePix5[x,y] = (R5, G5, B5)
                    outsidePix6[x,y] = (R6, G6, B6)
                    outsidePix7[x,y] = (R7, G7, B7)
                    outsidePix8[x,y] = (R8, G8, B8)

        listOfImages = [(insideImg1, outsideImg1), (insideImg2, outsideImg2), (insideImg3, outsideImg3)]
        listOfImages = listOfImages + [(insideImg4, outsideImg4)] + [(insideImg5, outsideImg5)] + [(insideImg6, outsideImg6)]
        listOfImages = listOfImages + [(insideImg7, outsideImg7)] + [(insideImg8, outsideImg8)]
        return listOfImages

    def seperateImage(self, figure):
        # figure.show()
        width = figure.size[0]
        height = figure.size[1]
        numOfPix = width*height
        insideImg = Image.new('RGB', (width, height), 'white')
        insidePix = insideImg.load()
        outsideImg = Image.new('RGB', (width, height), 'white')
        outsidePix = outsideImg.load()

        for x in range(0, width):
            for y in range(0, height):
                (R, G, B, T) = figure.getpixel((x,y))
                if (x > self.MIN_EDGE and x < self.MAX_EDGE and y > self.MIN_EDGE and y < self.MAX_EDGE):
                    insidePix[x,y] = (R, G, B)
                else:
                    outsidePix[x,y] = (R, G, B)
        # insideImg.show()
        # outsideImg.show()
        return (insideImg, outsideImg)

    def findInsideOutsideSimilarities(self, inFigure1, inFigure2, inFigure3, outFigure1, outFigure2, outFigure3):
        similarities = {}

        firstTwoInside = self.noChangeFigures(inFigure1, inFigure2)
        secondTwoInside = self.noChangeFigures(inFigure2, inFigure3)
        firstAndThirdInside = self.noChangeFigures(inFigure1, inFigure3)
        
        firstTwoOutside = self.noChangeFigures(outFigure1, outFigure2)
        secondTwoOutside = self.noChangeFigures(outFigure2, outFigure3)
        firstAndThirdOutside = self.noChangeFigures(outFigure1, outFigure3)

        if(firstTwoInside[0] and secondTwoInside[0] and not firstTwoOutside[0]):
            similarities['INSIDE'] = (firstTwoInside[1], secondTwoInside[1], firstAndThirdOutside[1], secondTwoOutside[1])
        if(firstTwoOutside[0] and secondTwoOutside[0] and not secondTwoInside[0]):
            similarities['OUTSIDE'] = (firstTwoOutside[1], secondTwoOutside[1], firstAndThirdInside[1], secondTwoInside[1])
        return similarities 

    #maybe add a point, but subtract for the "false"
    def compareTransformations(self, dict1, dict2):
        valueNum = 0.0
        if ('NO_CHANGE' in dict1) and ('NO_CHANGE' in dict2):
            (true, percent) = dict2['NO_CHANGE'];
            valueNum = 1.0 - percent
        if ('ADD' in dict1) and ('ADD' in dict2):
            valueNum = valueNum + (1- dict2['ADD']);
        if ('SUBTRACT' in dict1) and ('SUBTRACT' in dict2):
            valueNum = valueNum + 1.0
        if ('XOR' in dict1) and ('XOR' in dict2):
            valueNum = valueNum + 1.0
        if ('UNION' in dict1) and ('UNION' in dict2):
            valueNum = valueNum + 1.0
        if ('SPLIT_SIMILARITY' in dict1) and ('SPLIT_SIMILARITY' in dict2):
            (top1, bottom1) = dict1['SPLIT_SIMILARITY']
            (top2, bottom2) = dict2['SPLIT_SIMILARITY']
            if top1[0] == top2[0] and bottom1[0] == bottom2[0]:
                valueNum = valueNum + (1 - top2[1]) + (1 - bottom2[1])
            # self.logger(('SPLIT ONE: ', dict2))
        if ('INSIDE' in dict1) and ('INSIDE' in dict2):
            (samePercent12, samePercent23, diffPercent13, diffPercent23) = dict2['INSIDE']
            valueNum = valueNum + (1 - samePercent12 - samePercent23 + diffPercent13 + diffPercent23)
        if ('OUTSIDE' in dict1) and ('OUTSIDE' in dict2):
            (samePercent12, samePercent23, diffPercent13, diffPercent23) = dict2['OUTSIDE']
            valueNum = valueNum + (1 - samePercent12 - samePercent23 + diffPercent13 + diffPercent23)

        return valueNum

    def chooseAnswer(self, dict1):
        answer = -1
        maxValue = 0.0
        for ans in dict1:
            ansValue = dict1[ans]['Row1'] + dict1[ans]['Row2'] + dict1[ans]['Col1'] + dict1[ans]['Col2']
            if ansValue > maxValue:
                answer = ans
                maxValue = ansValue
        return answer

    def logger(self, message):
        if (self.logger_enabled):
            print message

    def hasSmallDiagonal(self, diagonal, awnsfig, figA, figB):
        compare1 = self.smallFigSameDif(figA,awnsfig)
        compare2 = self.smallFigSameDif(figB,awnsfig)

        return compare1["num"] == diagonal["num"] and compare2["num"] == diagonal["num"] and compare2["type"] == diagonal["type"] and compare1["type"] == diagonal["type"]

    def smallFigDiagonal(self, figure, problem):
        answerTransformation = {}
        diagonal = self.smallFigSameDif(figure['a'], figure['e'])

        for ans in range(1, self.NUM_OF_3x3_ANS + 1):
            figureImage = Image.open(problem.figures[str(ans)].visualFilename);
            awnsfig = self.parseImage(figureImage)
            if(awnsfig):
                awns = self.hasSmallDiagonal(diagonal,awnsfig,figure['a'],figure['e'])
                if(awns):
                    answerTransformation[ans] = awns

        if(len(answerTransformation) == 1):
            return answerTransformation.keys()[0]

        return -1
  

    def smallFigSameDif(self, fig1, fig2):
        awns = {}
        awns["num"] = (fig1["num"] == fig2["num"])

        Max = max(fig1["type"],fig2["type"])
        Min = min(fig1["type"],fig2["type"])

        awns["type"] =(Max - self.errorSmallFig <= Min)
        return awns
    #TODO: return a list [1st quad, 2nd quad, 3rd quad, 4th quad, total]
    def parseImage(self, figure):
        figure.convert('RGB');
        blackPix = 0;
        width = figure.size[0]
        height = figure.size[1]
        self.Hash = {}
        self.figCount = 0
        self.TotalBlack = 0

        for x in range(0, width):
            for y in range(0, height):
                (R, G, B, T) = figure.getpixel((x, y))
                point = str(x)+","+str(y)
                if R < self.COLOR_CUTOFF and not self.Hash.has_key(point):
                    self.BubleBack = 0
                    self.figCount = self.figCount + 1
                    if( not self.bubleUp(figure,x,y)):
                        return False
        return {"num" :self.figCount, "type" : float(self.TotalBlack)/self.figCount};

    def bubleUp(self, figure, x, y):
        point = str(x)+","+str(y)
        self.Hash[point] = True

        width = figure.size[0]
        height = figure.size[1]

        
        if self.BubleBack > self.maxSmallFig:
            return False

        self.TotalBlack = self.TotalBlack + 1
        self.BubleBack = self.BubleBack + 1


        for move in self.allDirections:
            next = (move[0] + x, move[1] + y)
            nextPoint = str(next[0])+","+str(next[1])
            if(self.canMove(next,width,height) and not self.Hash.has_key(nextPoint)):
                (R, G, B, T) = figure.getpixel((next[0], next[1]))
                if R < self.COLOR_CUTOFF:
                    awns = self.bubleUp(figure,next[0],next[1])
                    if(not awns):
                        return False

        return True

    def canMove(self, next, width,height):
        if(next[0] < 0 or next[0] > width -1 or next[1] < 0  or next[1] > height):
            return False
        else:
            return True

    def findBeggining(self, figure):
        figure.convert('RGB');

        width = figure.size[0]
        height = figure.size[1]
        
        for x in range(0, width):
            for y in range(0, height):
                ColorList = figure.getpixel((x, y))
                if ColorList[0] < self.COLOR_CUTOFF:
                    return {'x':x, 'y':y}
        return False

    def findEnd(self, figure):
        figure.convert('RGB');

        width = figure.size[0]
        height = figure.size[1]

        for x in range(width -1, -1, -1):
            for y in range(0, height):
                ColorList = figure.getpixel((x, y))
                if ColorList[0] < self.COLOR_CUTOFF:
                    return {'x':x, 'y':y}
        return False

    def findBegginingY(self, figure):
        figure.convert('RGB');

        width = figure.size[0]
        height = figure.size[1]
        
        
        for y in range(0, height):
            for x in range(0, width):
                ColorList = figure.getpixel((x, y))
                if ColorList[0] < self.COLOR_CUTOFF:
                    return {'x':x, 'y':y}
        return False

    def translateAndSub(self, fig1, fig2):
        fig1.save('temp/fig1.jpeg', "JPEG")
        fig2.save('temp/fig2.jpeg', "JPEG")

        width = fig1.size[0]
        height = fig1.size[1]
        numOfPix = width*height
        newImage = Image.new('RGB', (width, height), 'white')
        img = newImage.load()

        fig1Start = self.findBeggining(fig1)
        fig2Start = self.findBeggining(fig2)    

        delta = fig2Start['x'] - fig1Start['x']

        for x in range(0, width):
            for y in range(0, height):
                xn = 0
                if(x+delta < width):
                    xn = x + delta
                #print "THiS IS THE info: " + str(xn) + ",  " + str(width) + "," + str(delta)
                ColorList1 = fig1.getpixel((x,y))
                ColorList2 = fig2.getpixel((xn,y))

                if (ColorList1[0] < self.COLOR_CUTOFF) and not (ColorList2[0] < self.COLOR_CUTOFF):
                    img[x,y] = (ColorList1[0], ColorList1[0], ColorList1[0])
                
   
        newImage.save('temp/suboperation.jpeg', "JPEG")
        return newImage

    def subProblem(self, fig1, fig2, fig3):
        figSub = self.translateAndSub(fig1,fig2)
        return self.translateAndCompare(figSub, fig3)

    def translateAndCompare(self, figSub, fig3):
        width = fig3.size[0]
        height = fig3.size[1]
        numOfPix = width*height
        newImage = Image.new('RGB', (width, height), 'white')
        img = newImage.load()

        fig3Start = self.findBeggining(fig3)
        figSubStart = self.findBeggining(figSub)    

    
        delta = fig3Start['x'] - figSubStart['x']

        differences = 0
        sim = 0


        for x in range(0, width):
            for y in range(0, height):
                xn = 0
                if(x+delta < width and x+delta > 0):
                    xn = x + delta
                #print "THiS IS THE info: " + str(xn) + ",  " + str(width) + "," + str(delta)
                ColorList1 = fig3.getpixel((xn,y))
                ColorList2 = figSub.getpixel((x,y))

                R1 = ColorList1[0]
                R2 = ColorList2[0]

                if (R1 < self.COLOR_CUTOFF) and (R2 < self.COLOR_CUTOFF):
                    img[x,y] = (R1, R1, R1)
                    sim = sim + 1
                elif((R1 < self.COLOR_CUTOFF) ^ (R2 < self.COLOR_CUTOFF)):
                    differences = differences + 1
                    img[x,y] = (255, 0, 100)
                
   
        newImage.save('temp/end.jpeg', "JPEG")

        numOfPix = width * height

        noChangeBool = False
        if (float(differences)/numOfPix < self.SIMILAR_NO_CHANGE):
            noChangeBool = True;
        
        return (noChangeBool, float(differences)/numOfPix)
