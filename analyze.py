import sys
import os

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
        
    print('Staring place: ', startingPlace)
    print('Recursive: ' + str(recursive))
    print('Extensions: ' + str(extensions))
    print('Output: ' + output)

if __name__ == '__main__':
    main()
