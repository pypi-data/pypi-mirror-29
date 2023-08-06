# README #
### Shoelaces ###

This is an open source program for processsing ribosome profiling data written in Python3

### Requirements ###
* Python3
* pysam
* numpy
* pyqt5
* pyopengl

(all Python3 packages are installable with pip3)


## RUN ##
To start the window application, run the `run.sh` script

To start the console application, run `python shoelaces/main.py -h`

## GUI ##

* Load sequence alignment data (BAM format, note that the index BAI file needs to be in the same directory) and gene annotations (GTF format).
* In the 'Resources' window, select one GTF and one BAM file (they will turn blue).
* Press the 'Set Offset' button to create metaplots around transript start and stop per read length. The number of transcripts used for creating metaplots can be adjusted in the drop-down menu (default is top 10% most expressed transcripts).
* The footprint lengths with 3-nucleotide periodicity appear in the 'Common' tab (footprints stemming from translating ribosomes).
* The offsets are calibrated automatically, you can adjust the positions by dragging the plots left/right ('0' in 'Start/Stop codon' plots are the first nucleotides of start/stop codons respectively.
* Export your selected data into WIG format by pressing the 'Export Wig' button (you can either create single file or one per each selected footprint length).

Noise regions can be defined by a separate transcript file. Right click on the desired to resource and select set as noise (it will turn red).

Single transcripts or genes in your current transcript file can be excluded from processing, by right clicking and select toggle usage (they will be grayed out).

To store your current project, select save button. This stores and xml with your current offsets, selected files, disabled transcripts.

In the 'Data Overview' you can click 'Refresh' button to calculate global statistics of your library.
Double-clicking on the gene/transcript names in the panels on the left plots the sequence data in a genome browser-like fashion, with corresponding statistics.

For processing multiple alignment files in the same way, go to File -> Batch... and add BAM files with 'Add' button.

## Console ##
See the `run-console.sh` for an example.

Using specified offsets (config file):

`python3 shoelaces/main.py -o -files Data/offsets.xml Data/example.bam Data/example.gtf out.wig`

Split output for fragment lengths specified in offsets.xml:

`python3 shoelaces/main.py -o -s -files Data/offsets.xml Data/example.bam Data/example.gtf out.wig`

Overwrite fragment lengths for which to create wig output:

`python3 shoelaces/main.py -o -lengths 28 29 -files Data/offsets.xml Data/example.bam Data/example.gtf out.wig`

Automatic offset detection:

`python3 shoelaces/main.py -a -files Data/example.bam Data/example.gtf out.wig`


### Who do I talk to? ###

* Asmund.Birkeland@uib.no