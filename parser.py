#importing libs
import csv
import argparse

def parse_vcf_to_csv(input_file, output_file):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()
    
    headers = []
    data = []
    
    for line in lines:
        line = line.strip()
        if line.startswith('##INFO=<ID=CSQ'):
            headers_line = line.split('Format: ')[1].strip('">')
            csq_headers = headers_line.split('|') #Splitting the CSQ field
        elif line.startswith('#CHROM'):
            vcf_headers = line.lstrip('#').split('\t')
        elif not line.startswith('#'):
            fields = line.split('\t')
            chrom, pos, vid, ref, alt, qual, filt, info, form, sample = fields
            
            info_dict = dict(item.split('=') for item in info.split(';') if '=' in item)
            if 'CSQ' in info_dict:
                csq_entries = info_dict['CSQ'].split(',')
                for entry in csq_entries:
                    data_fields = entry.split('|')
                    while len(data_fields) < len(csq_headers):
                        data_fields.append('')
                    data.append([chrom, pos, vid, ref, alt, qual, filt, info, form, sample] + data_fields)
    
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(vcf_headers + csq_headers)
        writer.writerows(data)

#for working with commandline
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse VCF to CSV')
    parser.add_argument('--input', required=True, help='Input VCF file')
    parser.add_argument('--output', required=True, help='Output CSV file')
    args = parser.parse_args()

    parse_vcf_to_csv(args.input, args.output)
