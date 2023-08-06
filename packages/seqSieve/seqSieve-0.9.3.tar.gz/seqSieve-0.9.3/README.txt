seqSieve
===========

Installation:

    pip install seqSieve
    
This should also install numpy and matplotlib automatically if necessary.
If you have trouble installing dependencies via pip, try installing 
them with your distribution's package manager.

On debian do:

    apt-get install python-matplotlib python-numpy
    
It is also possible to run seqSieve without installation
    
    python seqSieve/seqSieve
    
    
    
**seqSieve** will try to remove sequences that cause misalignments from a multiple sequence alignment(MSA).
It reads a given MSA in multi-fasta format and removes sequences with the highest penalty scores, 
then builds the next MSA without those sequences. This process is repeated until a user-specified 
cut-off is reached or less than three sequences are left to be aligned.

In the default mode "Sites", sequences are penalized for both gaps and insertions by an amount proportional to the percentage of ungapped and gapped sequences, respectively.
The modes "Gaps", "uGaps","Insertions", "uInsertions","uInsertionsGaps" always assign a penalty of 1 for the named variation. "u" stands for unique, i.e. uGaps only penalizes unique gaps.
With mode "custom" the user sets the penalties for each variation. 

Usage:
    
    ######################################
    # seqSieve
    ######################################
    usage:
       seqSieve -f multifasta alignment
    options:
        -f, --fasta=FILE    multifasta alignment (eg. "align.fas")
        OR
        -F, --fasta_dir=DIR directory with multifasta files (needs -s SUFFIX)
        -s, --suffix=SUFFIX will try to work with files that end with SUFFIX (eg ".fas")

        -a, --msa_tool=STR  supported: "mafft", prank, prankf (= prank +F) [default:"mafft"]
        -i, --max_iterations=NUM    force stop after NUM iterations
        -n, --num_threads=NUM   max number of threads to be executed in parallel [default: 1]
        -m, --mode=MODE         set strategy to remove outlier sequences [default: "Sites"]
                                available modes (not case sensitive):
                                    "Sites", "Gaps", "uGaps","Insertions",
                                    "uInsertions","uInsertionsGaps", "custom"
        -q, --no-realign        don't realign with each iteration (not recommended)                        
        -l, --log       write logfile
        -h, --help      prints this

    only for mode "custom":
        -g, --gap_penalty=NUM        set gap penalty [default: 1.0]
        -G, --unique_gap_penalty=NUM set unique gap penalty [default: 10.0]
        -j, --insertion_penalty=NUM  set insertion penalty [default:1.0]
        -J, --unique_insertion_penalty=NUM set insertion penalty [default:1.0]
        -M, --mismatch_penalty=NUM   set mismatch penalty [default:1.0]
        -r, --match_reward=NUM       set match reward [default: -10.0]


Currently supported multiple sequence aligners:

- mafft (Katoh, Standley 2013 (Molecular Biology and Evolution 30:772-780) 
  MAFFT multiple sequence alignment software version 7: improvements in performance and usability. http://mafft.cbrc.jp/alignment/software/)
- prank (Loytynoja, Goldman  2005 (PNAS 102:10557-10562) 
  An algorithm for progressive multiple alignment of sequences with insertions. http://www.ebi.ac.uk/goldman-srv/prank/prank/

Requirements
============
* matplotlib
* numpy

External Programs
-----------------
* mafft and/or
* prank
