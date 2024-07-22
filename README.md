# VCF-parse
Simple Python code to parse VEP annotated VCF files 


    gunzip -c <input_file_name>_indels_VEP.ann.vcf.gz
    gunzip -c <input_file_name>_snvs_VEP.ann.vcf.gz
    gunzip -c <input_file_name>_VEP.ann.vcf.gz

# Requires "picard MergeVcfs 2.18.29"
picard MergeVcfs I=<input_file_name>_snvs_VEP.ann.vcf.gz I=<input_file_name>_indels_VEP.ann.vcf.gz O=merge.vcf

# Custom parsers
python parser.py --input <input_file_name>_VEP.ann.vcf --output <input_file_name>_VEP.ann.csv
python process_merged.py --input merge.vcf --output merged_complete_vcf.csv
