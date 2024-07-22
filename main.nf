#!/usr/bin/env nextflow


//launch dir should contain the unzipped vcf files and the python scripts to process the files
// Nextflow script
nextflow.enable.dsl=2

// parameters for input files Change As per the file names
// More files can be added
params.input_vcf1 = "<input_vcf_1>"
params.input_vcf2 = "input_vcf_2"
// params.input_vcf2 = "input_vcf_3"
// params.input_vcf2 = "input_vcf_4"
// ..
// ..

params.input_filtered_vcf = "<vcf_file>"
params.output_filtered_csv = "<file.csv>"
params.output_merged_csv = "<snv_indel_merged.csv>"

// channels for input files
Channel.fromPath(params.input_vcf1).set { vcf1 }
Channel.fromPath(params.input_vcf2).set { vcf2 }
// Channel.fromPath(params.input_vcf2).set { vcf3 }
// Channel.fromPath(params.input_vcf2).set { vcf4 }

Channel.fromPath(params.input_filtered_vcf).set { filtered_vcf }

// workflow process to merge VCF files using Picard
process mergeVcfs {
    input:
    path vcf1
    path vcf2
    // path vcf3
    // path vcf4
    output:
    path "merge.vcf"

    script: // if more vcf files are added add I=$vcf3 I=vcf4 ...
    """
    picard MergeVcfs I=$vcf1 I=$vcf2 O=merge.vcf
    """
}

// workflow process to parse VCF to CSV
process parseVcf {
    input:
    path filtered_vcf
    output:
    path params.output_filtered_csv

    script:
    """
    python ${launchDir}/parser.py --input ${filtered_vcf} --output ${params.output_filtered_csv}
    """
}

// workflow process to process the merged VCF
process processMergedVcf {
    input:
    path "merge.vcf"
    output:
    path params.output_merged_csv

    script:
    """
    python ${launchDir}/process_merged.py --input merge.vcf --output ${params.output_merged_csv}
    """
}

// workflow
workflow {
    mergeVcfs(vcf1, vcf2) // pass vcf3 and vcf4 ... as per requirement
    merge_vcf = mergeVcfs.out // Avoiding ERROR ~ No such variable: merge_vcf
    parseVcf(filtered_vcf)
    processMergedVcf(merge_vcf)
}
