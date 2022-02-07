# Py My Code

## A code analyzing tool written in python

### Supported languages:

* Java
* Python

## Usage

`python analyze.py [directory or file] -r -extensions .kt .java -o myDirectory/myFileResults.txt`

More will be added soon but language support requires writing regular expressions to detect comments in each language. This is where the delay comes from.

## Description

Py My Code (yes I actually thought of the name while in the shower) is a code analyzing tool that scans the provided diretory for files ending in the provided language's common extension. It then counts statistics such as number of code lines, blank lines, and comment lines.

A user may control many aspects about the program via the following arguments:

 -o is used to specify a directory/filename to create the results file to output the results to as opposed to the default `results.txt`.

-extensions is used to provide a list of extensions to scan. For example, when analyzing a Java code base, you may want to pass in both .java and .kt files. Thus, the user should specify `-extensions .kt .java`

-r is used to indicate recursion should be performed on the provided directory.
