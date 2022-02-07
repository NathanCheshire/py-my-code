import sys
import os

from numpy import block

def main():
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

    #todo keep track of running totals here

    for file in findFiles(startingPlace, extensions = extensions, recursive = recursive):
        countComments(file)

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

def countComments(file):
    print('On file: ' + file)

    numComments = 0
    lines = 0
    blockMode = False
    blankLines = 0

    if not os.path.exists(file):
        print('Error: provided file does not exist: ', file)
        return

    for line in open(file,'r').readlines():
        if len(line.strip()) > 0:
            lines = lines + 1

            if line.strip().startswith('/*'):
                blockMode = True
            elif line.strip().endswith('*/'):
                blockMode = False

            if line.strip().startswith('//') and file.endswith('.java'):
                numComments = numComments + 1
            elif blockMode:
                numComments = numComments + 1
            elif (line.strip()) == 0:
                blankLines = blankLines + 1
            elif line.strip().startswith('/*') and line.strip().endswith('*/'):
                numComments = numComments + 1
        else:
            blankLines = blankLines + 1

    print('Comments found: ' + str(numComments))
    print('Lines found: ' + str(lines))
    print('Blank lines found: ' + str(blankLines))

if __name__ == '__main__':
    main()
