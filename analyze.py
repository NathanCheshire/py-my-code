import sys
import os

from numpy import block

def main():
    global lineSep
    lineSep = '---------------------------------'

    startingPlace = None
    extensions = []
    recursive = False
    output = None

    global usageString
    usageString = 'Usage: analyze.py [directory or file] [arguments (-r, -extensions .kt .java, -o myDirectory/myFileResults.txt)]'

    global paramsFor
    paramsFor = None

    for argIndex in range(1, len(sys.argv)):
        arg = sys.argv[argIndex]

        if startingPlace == None:
            startingPlace = arg

            if not os.path.exists(startingPlace):
                print(f'Error: provided starting point does not exist: {startingPlace}')
                return
        else:
            if arg.startswith('-'):
                if arg == '-r' or arg == '-R':
                    if recursive == True:
                        print('Error: Recursive argument already passed')
                        return
                    recursive = True
                elif arg == '-extensions':
                    if len(extensions) != 0:
                        print('Error: Extensions argument already passed')
                        return
                    paramsFor = 'extensions'
                elif arg == '-o':
                    if output != None:
                        print('Error: Output argument already passed')
                        return
                    paramsFor = 'output'
                else:
                    print('Error: Invalid argument: ' + arg)
                    print(usageString)
                    return
            else:
                if paramsFor == None:
                    print(usageString)
                    return
                elif paramsFor == 'extensions':
                    if arg.startswith('.'):
                        extensions.append(arg)
                    else:
                        print('Error: Invalid extension: ' + arg + "\nExtensions must begin with '.'")
                        return
                elif paramsFor == 'output':
                    output = arg

    #if no output provided, default
    if output == None:
        output = 'Results.txt'

    if len(extensions) == 0:
        print('Error: must provide at least one extension')
        return

    totalLines = 0
    totalComments = 0
    totalBlankLines = 0

    #todo how to detect what extensions go with which analyze?
    #todo maybe an annotation
    for file in findFiles(startingPlace, extensions = extensions, recursive = recursive):
        print('On file: ' + file)

        tuple = javaFileAnalyze(file)

        print('Files lines, comments, blank lines: ' + str(tuple[0]) + ',' + str(tuple[1]) + ',' + str(tuple[2]))
        print(lineSep)

        totalLines = totalLines + tuple[0]
        totalComments = totalComments + tuple[1]
        totalBlankLines = totalBlankLines + tuple[2]

    print("Total lines: " + str(totalLines))
    print("Total comments: " + str(totalComments))
    print("Total blank lines: " + str(totalBlankLines))
    print("Code to comment ratio: " + str(float(totalLines - totalComments) / float(totalComments)))

def findFiles(startingDirectory, extensions = [], recursive = False):
    ret = []

    if len(extensions) == 0:
        print('Error: must provide valid extensions')
        return

    if os.path.isdir(startingDirectory):
        for subDir in os.listdir(startingDirectory):
            if recursive:
                ret = ret + findFiles(os.path.join(startingDirectory, subDir), extensions, recursive)
            else:
                ret.append(os.path.join(startingDirectory, subDir))
    else:
        for extension in extensions:
            if startingDirectory.endswith(extension):
                ret.append(startingDirectory)
                
    return ret

def javaFileAnalyze(file):
    """Returns a tuple of the number of lines, comments, and blank lines in that order"""

    numComments = 0
    numLines = 0
    blockMode = False
    numBlankLines = 0

    if not os.path.exists(file):
        print('Error: provided file does not exist: ', file)
        return

    for line in open(file,'r').readlines():
        if len(line.strip()) > 0:
            numLines = numLines + 1

            if line.strip().startswith('/*'):
                blockMode = True
            elif line.strip().endswith('*/'):
                blockMode = False

            if line.strip().startswith('//') and file.endswith('.java'):
                numComments = numComments + 1
            elif blockMode:
                numComments = numComments + 1
            elif (line.strip()) == 0:
                numBlankLines = numBlankLines + 1
            elif line.strip().startswith('/*') and line.strip().endswith('*/'):
                numComments = numComments + 1
        else:
            numBlankLines = numBlankLines + 1

    return (numLines, numComments, numBlankLines)

if __name__ == '__main__':
    main()
