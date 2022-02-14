import sys
import os
from matplotlib import pyplot as plt

def parseArgs():
    '''
    Parses the provided command line arguments and outputs 
    the py-my-code results to the user.
    '''

    global lineSep
    lineSep = '---------------------------------'

    startingPlace = None
    extensions = []
    recursive = False
    output = None

    global usageString
    usageString = 'Usage: analyze.py [directory or file] [arguments (-r, -extensions .kt .java, -o path/to/my/directory/results)]'

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
    totalCodeLines = 0

    print(lineSep)

    for file in findFiles(startingPlace, extensions = extensions, recursive = recursive):
        print('On file: ' + file)

        tuple = analyzeFile(file)

        print('Files lines, comments, blank lines: ' + str(tuple[0]) + ',' + str(tuple[1]) + ',' + str(tuple[2]))
        print(lineSep)

        totalLines = totalLines + tuple[0]
        totalComments = totalComments + tuple[1]
        totalBlankLines = totalBlankLines + tuple[2]

    if totalLines == 0:
        print('No valid files with the provided extensions were found')
    else:
        totalCodeLines = totalLines - totalBlankLines - totalComments

        print("Total lines: " + str(totalLines))
        print("Total comments: " + str(totalComments))
        print("Total blank lines: " + str(totalBlankLines))
        print("Code to comment ratio: " + str(float(totalLines - totalComments) / float(totalComments)))

        labels = ['Code lines (' + str(totalCodeLines) + ')',
        'Comments (' + str(totalComments) + ')',
        'Blank lines (' + str(totalBlankLines) + ')']
        sizes= [totalCodeLines, totalComments, totalBlankLines]

        plt.pie(sizes, labels = labels, startangle = 90,
            explode=(0.1, 0.1, 0.1), autopct='%1.3f%%')
        plt.title(startingPlace)
        plt.axis('equal')

        print(lineSep)

        if output != None:
            outputDirectory = output[:output.find('/')]

            if not os.path.exists(outputDirectory):
                os.makedirs(outputDirectory)

            print('Saved master output to ', output, '.txt', sep = '')

            print('Saved master chart to ', output, '.png', sep = '')
            plt.savefig( output + '.png')


def findFiles(startingDirectory, extensions = [], recursive = False):
    '''
    Finds all files within the provided directory that 
    end in one of the provided extensions.
    '''

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

def analyzeFile(file):
    """
    Returns a tuple of the number of lines, comments, 
    and blank lines in that order
    """

    numComments = 0
    numLines = 0
    blockMode = False
    numBlankLines = 0

    if not os.path.exists(file):
        print('Error: provided file does not exist: ', file)
        return

    fileLines = open(file,'r').readlines()

    if file.endswith('.java') or file.endswith('.kt'):
        for line in fileLines:
            if len(line.strip()) > 0:
                numLines = numLines + 1

                # starts with //
                line = line.strip()

                #multiline
                if line.startswith('/*') and line.endswith('*/'):
                    numComments = numBlankLines + 1
                elif line.startswith('/*'):
                    blockMode = True
                elif line.endswith('*/'):
                    blockMode = False

                if blockMode:
                    numComments = numComments + 1
                elif line.startswith('//'):
                    numComments = numComments + 1
            else:
                numBlankLines = numBlankLines + 1
    elif file.endswith('.py') or file.endswith('.gdscript'):
         for line in fileLines:
            if len(line.strip()) > 0:
                numLines = numLines + 1

                line = line.strip()

                if line.startswith('"""') and line.endswith('"""'):
                    numComments = numComments + 1
                elif line.startswith("'''") and line.endswith("'''"):
                    numComments = numComments + 1
                elif line.startswith('"""'):
                    blockMode = True
                elif line.startswith("'''"):
                    blockMode = True
                elif line.endswith('"""'):
                    blockMode = False
                elif line.endswith("'''"):
                    blockMode = False

                if blockMode:
                    numComments = numComments + 1
                elif line.startswith('#'):
                    numComments = numComments + 1
            else:
                numBlankLines = numBlankLines + 1
    elif '.' not in file:
        print('File has no extension: ' + file)
        return
    else:
        print('Unsupported language: ' + file)
        return

    return (numLines, numComments, numBlankLines)
    
# todo comment, add arg to just count lines and blank lines if specified extension has no function

if __name__ == '__main__':
    '''
    Parses the providec arguments and attempts to begin the py-my-code functionality.
    '''
    parseArgs()
