# Table of Contents

1. [sequence-handler](#sequence-handler)
2. [How to use the tool](#how-to-use-the-tool)
   - [Installation and usage](#installation-and-usage)
     - [Levenshtein distance threshold](#levenshtein-distance-threshold)
3. [Information about the tool](#information-about-the-tool)
   - [Database files](#database-files)
     - [Art: A Next-Generation Sequencing Read Simulator](#art-a-next-generation-sequencing-read-simulator)
   - [Reference genome sequence](#reference-genome-sequence)
   - [Fixed sequences](#fixed-sequences)
   - [Query files](#query-files)
4. [My thinking process](#my-thinking-process)
   - [Database](#database)
     - [Database files](#database-files)
     - [Flanking sequences](#flanking-sequences)
     - [Database creation, population, and outputting](#database-creation-population-and-outputting)
   - [Filtering](#filtering)
   - [Updating the database](#updating-the-database)
   - [Tests](#tests)
   - [Error handling and logging](#error-handling-and-logging)

---

#  sequence-handler

This project is made for **DKMS Life Science Lab**, Bioinformatics Software Engineering Task. 

Sequencehandler is a Command Line Interface tool that builds a database from a collection of paired-end FASTQ files, flank the sequences with fixed sequences, and filters other input FASTQ files against the database.

Simply create a database with ```-c, --createDB``` flag, then configure the fixed sequences in ```config/fixed_sequences.yaml``` and populate the database using the files in the ```db/``` folder with ```-p, --populateDB``` flag. To output the SQL database as a csv file, simply run ```-o, --outputDB``` flag. 

To filter queries against the database, run ```-f, --filterQuery```. You can set the Levenshtein edit distance threshold using ```-t, --threshold```. It outputs the unique sequences with a date and time stamp in ```out/``` folder as a csv file. To update the database with newly found unique sequences, chose the csv file that is output and run ```-u, --updateDB```.


# How to use the tool
## Installation and usage
1. Install Poetry from its official website. (https://python-poetry.org/docs/)
2. Clone this repository.
3. Run ```poetry install``` and it will install the required packages in a separate environment.
4. Run ```poetry shell``` to activate the environment.
5. Run the commands as you wish. Initially, you should follow the order below.

-  ```poetry run sequencehandler -c```
-   ```poetry run sequencehandler -p```
-  ```spoetry run sequencehandler -o```
-  ```poetry run sequencehandler -f```
- ```poetry run sequencehandler -u```

If you would like to define the threshold, run ```poetry run sequencehandler -t {threshold}``` . Default is 51.

**Note:**
Default threshold is 51 because 24+24 is the length of flanking sequences. Plus 3 is an optional decision. If exact match is desired, then flanking sequences should be added to the query or removed from the database population, then threshold should set to 0.

###  Levenshtein distance threshold

The threshold defines the maximum allowable difference (measured by edit distance) between sequences for them to be considered similar. If the edit distance between a sequence from the input data and any sequence in the database is less than or equal to this threshold, the sequences are deemed similar and the input sequence is skipped to ensure uniqueness based on the specified level of variation.

# Information about the tool
 
##  Database files

### Art: A Next-Generation Sequencing Read Simulator

ART-MountRainier-2016-06-05 (the latest version) is used to generate database files including the settings that the overlap between paired-end reads is at least 200 base pairs, with amplicons being at least 400 base pairs long.

The code used to generate the data is below. Seed ```123``` is used to generate the data. If you run the same command, you will be able to generate the exact same data. 

```shell

./art_illumina  -ss  HS25  -i  GRCh38_latest_genomic.fna  -p  -l  100  -f  400  -m  50  -s  200  -rs  123  -na  -o  sequence-handler/db/example_

```

Detailed explanation of the settings:

- -ss HS25: Specify the sequencing system (HiSeq 2500)

- -p: Generate paired-end reads.

- -l 100: Set read length to 100 base pairs.

- -f 400: Set mean fragment length to 400 base pairs.

- -m 50: Set standard deviation of fragment length.

- -s 200: Set minimum overlap length between paired reads to at least 200 base pairs.

- -rs 123: Seed set to a specific number for reproducibility.

- -na: Disable any alignment information in the output FASTQ files.

- -i reference: A Reference genome or sequence file.

- -o example: Specify the output prefix for generated FASTQ files.

**Citation:**
Art: A Next-Generation Sequencing Read Simulator
[Weichun Huang, Leping Li, Jason R Myers, and Gabor T Marth. ART: a next-generation sequencing read simulator, Bioinformatics (2012) 28 (4): 593-594](https://doi.org/10.1093/bioinformatics/btr708)

###  Reference genome sequence

Human GRCh38 is used to create artificial database fastq files by ART.

https://www.ncbi.nlm.nih.gov/genome/guide/human/

##  Fixed sequences
Fixed sequences are chosen from Nanopore's barcode sequences. Please refer to the link below.

https://community.nanoporetech.com/technical_documents/chemistry-technical-document/v/chtd_500_v1_revaq_07jul2016/barcode-sequences

##  Query files
Query files are chosen to be human acute myeloid leukemia (AML) samples attributing to ***DKMS***'s mission. The files can be downloaded from the link below.

https://trace.ncbi.nlm.nih.gov/Traces/index.html?view=study&acc=SRP056295

# My thinking process
Here, I copy paste my e-mail for a brief explanation of my work and thinking process.

## Database
### Database files
I understood that I needed to create a database folder containing potentially hundreds of pairs of FASTQ files. I generated them by Art (A Next-Generation Sequencing Read Simulator) following the guideline that the overlap between paired-end reads is at least 200 base pairs, with amplicons being at least 400 base pairs long.

### Flanking sequences
I did not understand whether these samples were already barcoded or it was my responsibility to attach flanking sequences during the database creation. I assumed the first one but still went with the latter to show that I could program it. So, I created a config file where fixed sequences can be set. The tool fetches the sequences and attaches them at the ends of the database sequences. 

### Database creation, population, and outputting
![Populate db](https://github.com/mervebduman/sequence-handler/blob/main/res/populate_db.png?raw=true)
I used sqlite3 for the sake of simplicity. I believe there better options for such a large database but I didn’t want to complicate things for a technical interview.  With “—createDB” flag, tool creates a database file and an empty table in that. Running “—populateDB” populates this database fetching the database files and flanking them. There is an option to output this sql database as csv. Simply run “—outputDB”. 

## Filtering
![Filtering queries](https://github.com/mervebduman/sequence-handler/blob/main/res/filter_query.png?raw=true)

I understood that there should be an input folder where users can copy their pair-ended fastq files and search the database, output the unique and similar sequences. Therefore, I created a query folder. It doesn’t matter whether the files are zipped or unzipped, tool can handle it without specification. It runs through the database with a set edit distance threshold and finds unique sequences. Threshold can be set with “—threshold” flag. 

Here, I didn’t have time to finish outputting similar sequences and their frequences, although I added a note in the script where I would include it (sequencehandler/filter_query.py line 48). 

## Updating the database
![Update db](https://github.com/mervebduman/sequence-handler/blob/main/res/update_db.png?raw=true)
I quickly added a function to update the database, although I didn’t have time to thoroughly test it. It seems it works.

## Tests
I included tests initially, then I didn’t have time to update them as the function grew. I commented them out but let them stay there to show that I write tests.

## Error handling and logging
As you can see in the screenshots in the repository, I didn't forget to inform the user. I added date-time stamped information and error logs of the progress. 

