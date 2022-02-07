import sys
import os

def main():
    extensions = []
    recursive = False
    output = 'Results.txt'

    lookingFor = 'starting_place'

    for argIndex in range(1, len(sys.argv)):
        arg = sys.argv[argIndex]
        
        if arg.startswith('-'):
            print('argument found: ', arg)
        else:
            print('argument param found: ', arg)

def validateFile(filename):
    """
    Validates whether the provided filename exists
    """
    pass

if __name__ == '__main__':
    main()
