import csv  #Importing Libraries
import argparse


#Defining Headers
csq_headers = [
    "Allele", "Consequence", "IMPACT", "SYMBOL", "Gene", "Feature_type", "Feature", 
    "BIOTYPE", "EXON", "INTRON", "HGVSc", "HGVSp", "cDNA_position", "CDS_position", 
    "Protein_position", "Amino_acids", "Codons", "Existing_variation", "DISTANCE", 
    "STRAND", "FLAGS", "VARIANT_CLASS", "SYMBOL_SOURCE", "HGNC_ID", "CANONICAL", 
    "MANE_SELECT", "MANE_PLUS_CLINICAL", "TSL", "APPRIS", "CCDS", "ENSP", 
    "SWISSPROT", "TREMBL", "UNIPARC", "UNIPROT_ISOFORM", "GENE_PHENO", "SIFT", 
    "PolyPhen", "DOMAINS", "miRNA", "AF", "AFR_AF", "AMR_AF", "EAS_AF", "EUR_AF", 
    "SAS_AF", "gnomADe_AF", "gnomADe_AFR_AF", "gnomADe_AMR_AF", "gnomADe_ASJ_AF", 
    "gnomADe_EAS_AF", "gnomADe_FIN_AF", "gnomADe_NFE_AF", "gnomADe_OTH_AF", 
    "gnomADe_SAS_AF", "gnomADg_AF", "gnomADg_AFR_AF", "gnomADg_AMI_AF", "gnomADg_AMR_AF", 
    "gnomADg_ASJ_AF", "gnomADg_EAS_AF", "gnomADg_FIN_AF", "gnomADg_MID_AF", 
    "gnomADg_NFE_AF", "gnomADg_OTH_AF", "gnomADg_SAS_AF", "MAX_AF", "MAX_AF_POPS", 
    "FREQS", "CLIN_SIG", "SOMATIC", "PHENO", "PUBMED", "MOTIF_NAME", "MOTIF_POS", 
    "HIGH_INF_POS", "MOTIF_SCORE_CHANGE", "TRANSCRIPTION_FACTORS" # Headers for annotations extracted from the info field
]

main_headers = ["#CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "FORMAT", "NORMAL", "TUMOR"] #Main headers

def parse_csq(csq_string):
    annotations = csq_string.split(',') #Spliting the CSQ string by commas to get individual annotation
    parsed_annotations = []
    for annotation in annotations:
        fields = annotation.split('|') # For each annotation, split by '|' to get the individual fields
        if len(fields) != len(csq_headers):
            fields.extend([''] * (len(csq_headers) - len(fields)))  #preventing spill of dp etc to Transcription_factors column if the number of fields is less than csq_headers it pad the list with empty string
        parsed_annotations.append(dict(zip(csq_headers, fields)))
    return parsed_annotations

def process_merged_vcf(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    data = []
    for line in lines:
        if line.startswith("#"): #skipping lines starting with "#" to avoid metadata headers altogether
            continue
        else:
            columns = line.strip().split('\t')
            info = columns[7]
            csq_data = []
            if 'CSQ=' in info:
                csq_info = info.split('CSQ=')[1].split(';')[0] 
                csq_data = parse_csq(csq_info)
            
            for csq_entry in csq_data:
                row = columns[:7] + columns[8:] # Extracts the INFO column (index 7)
                row.extend([csq_entry.get(header, '') for header in csq_headers])
                data.append(row)

    with open(output_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(main_headers + csq_headers)
        csvwriter.writerows(data)

#to work with commandline
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process merged VCF files to CSV')
    parser.add_argument('--input', required=True, help='Input merged VCF file')
    parser.add_argument('--output', required=True, help='Output CSV file')
    args = parser.parse_args()

    process_merged_vcf(args.input, args.output)
