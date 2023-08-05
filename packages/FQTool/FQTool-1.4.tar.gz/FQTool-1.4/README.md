# FQTool

## Introduction
This lightweight tool, written in Python, is designed to allow a simple -yet powerful- way to manipulate FASTQ files. 
The purpose of this tool is to filter those reads, taken from one or more FASTQ files, that satisfy all the constrains selected when running the tool. Some simple flags are used to set the constraints.

## Installation
We decided to publish the package on PyPI to make the process of installing and upgrading FQTool easier for anyone.
You need to have `pip3` installed.

Just type `sudo -H pip3 install fqtool` in your terminal and you're ready to go! Check the [examples](#examples) and the [flags](#which-flags-are-available) to understand how to use FQTool.

## Which flags are available?
`fqtool -h` &nbsp; prints all the flags supported by FQParse. Here's the list:
* `-i, --input-filenames filename1 [filename2 filename3 ...]`
    * Input file name(s). Usually in the form *.fastq, *.fq

* `-l, --length length` 
    * Minimum length of the reads' substrings to be extracted.

*  `-q, --probability-of-correctness quality` 
    * Minimum probabilty of correctness of the reads to be extracted. Ranges between 0 and 1. You can also write the Phread Quality Value directly (e.g. 35)

*  `-f, --ascii-conversion-function function`
    * Function to be used to switch bewteen ASCII and Phred Value.Choose between: S = Sanger, X = Solexa, I = Illumina 1.3+, J = Illumina 1.5+, L = Illumina 1.8+. Default = L
*  `-a, --accuracy accuracy`
    * The average probability of correctness of the reads must be *at least* this value. If it is not, the read will be ignored. Default = 0

*  `-v, --version`         
    * Shows the program version and exits
*  `-h, --help`
    * List of the flags you can use with FQTool


## Examples
Some examples showing how to use FQTool can be found in the *Examples* directory. All the FASTQ files in that folder are taken from http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase3/data/


### Documentation
In this repository you will find a Doxyfile. Just type `doxygen Doxyfile` in a terminal to generate the project's documentation. You need to have `doxygen` installed.