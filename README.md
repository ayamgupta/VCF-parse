# VCF-parse
Simple Python code to parse VEP annotated VCF files 


    gunzip -c <input_file_name>_indels_VEP.ann.vcf.gz
    gunzip -c <input_file_name>_snvs_VEP.ann.vcf.gz
    gunzip -c <input_file_name>_VEP.ann.vcf.gz

# Requires "picard MergeVcfs 2.18.29"
    picard MergeVcfs I=<input_file_name>_snvs_VEP.ann.vcf.gz I=<input_file_name>_indels_VEP.ann.vcf.gz O=merge.vcf
*VCF files should be from the same samples. 

# Custom parsers
    python parser.py --input <input_file_name>_VEP.ann.vcf --output <input_file_name>_VEP.ann.csv
    python parse_snv_indel_merged.py --input merge.vcf --output merged_complete_vcf.csv

# Nextflow 
Entire workflow can be executed using nextflow

    nextflow run main.nf

The workflow currently uses 2 VCF files as input for parse_snv_indel_merged.py but this can be modified by editing the "main.nf" file to accomodate more vcf files.
If merging of files from different samples is required bcftools merge can be used. 
