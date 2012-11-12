#filterbank

**filterbank** is a tool for generating datasets at multiple resolutions. The resulting files then allow for quick summarisation and viewing.

##Installation

    pip install http://github.com/malariagen/filterbank/raw/master/dist/filterbank-0.1.0.tar.gz

## Usage

    filterbank [-h] [--verbose] input_file output_directory -c yaml_config

A set of files (one data file and one yaml describing the data file for each channel at each resolution level) will be produced in the output directory. The input file is a tab-delimted file with a header row naming the columns.


## Config
The config is a yaml file with several sections:
    block_sizes:  #The resolution levels at which to output files
      start:      #Integer of smallest block size - e.g. 1 will output 1 line for each line in the input file
      end:        #Integer of largest allowed block size
      mult:       #Integer that is the ratio between successive block sizes
    #For example 1,16,4 for these numbers would produce block sizes of 1,4,16

    channels:     #A associative array defining the outputs
      LONG NAME:    #Name of this channel
        ANYTHING:     #Arbitary metadata that is passed through to the output YAML files
        short_name:   #short name used in output file name
        value:        #Python expression that gives the value of the channel, available variables
                      #are the column names
        accumulators: #A list of classes that determine how to reduce a block of values to one.
                      #Currently avaliable: [LastVal, ArithmeticMean, GeometricMean, Median, 
                      #Percentile, Min, Max] Specify the class with a string, if it needs args 
                      #specify the class with an associative array.
                      #E.g. [{'Percentile': {'percent':0.25}}, 'Max', 'Min'] would give you the
                      # 1st quartile, max and min as output.
                      #Note that for a block size of 1 only the LastVal accumulator will be used.
        encoder:      #Specify the class used to output the channel. Either FixedWidthBase64 (for
                      #DQX webapp) or TabDelimited. Again either as a string or associative array
                      #with args.
 
###Example config:

        block_sizes:
          start: 1
          end: 1048576
          mult: 8

        defaults: &defaults
          accumulators: [Min, GeometricMean, Max]
          encoder:
            FixedLengthB64:
              length: 3
              range: [0,100]

        channels:
        ##### CORE CHANNELS #####
            Number of reads:
              short_name: num_reads
              value: reads
              encoder:
                FixedLengthB64:
                  length: 3
                  range: [0,2000]
              <<: *defaults
            Percent of reads on forward strand:
              short_name: reads_fwd
              value: reads_fwd * 100. / reads
              <<: *defaults
            Percent of reads properly paired:
              short_name: reads_paired
              value: reads_pp * 100. / reads
              <<: *defaults
            Percent of reads with mate unmapped:
              short_name: singletons
              value: reads_mate_unmapped * 100. / reads
              <<: *defaults
            Percent of reads with mate mapped to another chomosome:
              short_name: mate_other_chrom
              value: reads_mate_other_chr * 100. / reads
              <<: *defaults
            Percent of reads where mate is mapped to the same strand:
              short_name: mate_same_strand
              value: reads_mate_same_strand * 100. / reads
              <<: *defaults
            Percent of reads faceaway:
              short_name: faceaway
              value: reads_faceaway * 100. / reads
              <<: *defaults
            Percent of reads softclipped:
              short_name: softclipped
              value: reads_softclipped * 100. / reads
              <<: *defaults
            Percent of reads with edit distance zero:
              short_name: edit_dist_zero
              value: reads_edit0 * 100. / reads
              <<: *defaults
