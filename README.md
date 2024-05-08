# sequence-handler
Builds a database containing sequences extracted from a collection of paired-end FASTQ files and then filters sequences from other FASTQ files based on this database.

# query
1. https://trace.ncbi.nlm.nih.gov/Traces/index.html?view=study&acc=SRP056295

# fixed seq
- https://community.nanoporetech.com/technical_documents/chemistry-technical-document/v/chtd_500_v1_revaq_07jul2016/barcode-sequences

# Install
https://www.postgresql.org/download/

# Reference genome sequence
Human GRCh38 is used to create artificial db fastq files by ART.
- https://www.ncbi.nlm.nih.gov/genome/guide/human/

# Artificial db files
```shell
./art_illumina -ss HS25 -i GRCh38_latest_genomic.fna -p -l 100 -f 50 -m 400 -s 20 -o example
```
https://academic.oup.com/bioinformatics/article/28/4/593/213322?login=false
Art: A Next-Generation Sequencing Read Simulator

- ss HS25: Specify the sequencing system (HiSeq 2500)
- p: Generate paired-end reads.
- l 100: Set read length to 100 base pairs.
- f 400: Set mean fragment length to 400 base pairs.
- m 50: Set standard deviation of fragment length.
- s 200: Set minimum overlap length between paired reads to at least 200 base pairs.
- na: Disable any alignment information in the output FASTQ files.
- i reference: A Reference genome or sequence file.
- o example: Specify the output prefix for generated FASTQ files.

# Use
1. ```python scripts/create_db.py```
2. ```python scripts/populate_db.py```
3. ```sqlite3 seq_handler.db```
4. 
```
.mode csv
.output output.csv
SELECT * FROM seq;
.quit
```

# Levenshtein distance threshold
The threshold defines the maximum allowable difference (measured by edit distance) between sequences for them to be considered similar. If the edit distance between a sequence from the input data and any sequence in the database is less than or equal to this threshold, the sequences are deemed similar and the input sequence is skipped to ensure uniqueness based on the specified level of variation.