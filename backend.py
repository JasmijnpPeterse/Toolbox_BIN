import subprocess
import time

class Tools():
    pass


def main(kwargs):
    print(kwargs)
    print(kwargs["threads"])
    print(kwargs["fastq_bestand"])
    time.sleep(1)

    subprocess.run(
        f"minimap2 -a -x map-ont -t {kwargs['threads']} -N {kwargs['N']} {kwargs['reference']} {kwargs['fastq_bestand']} > output.sam",
        shell=True
    )

    print("Minimap2")

    subprocess.run(
        "samtools view -b -o output.bam output.sam",
        shell=True
    )

    subprocess.run(
        "samtools sort output.bam > sorted_output.bam",
        shell=True
    )

    subprocess.run(
        "samtools index sorted_output.bam",
        shell=True
    )

    mpileup_cmd = f"bcftools mpileup sorted_output.bam -f {kwargs['reference']}"

    if kwargs.get("region"):
        mpileup_cmd += f" -r {kwargs['region']}"

    mpileup_cmd += " > bcftools_mpileup.bcf"

    subprocess.run(
        mpileup_cmd,
        shell=True
    )

    subprocess.run(
        "bcftools call -m -O v -o output.vcf bcftools_mpileup.bcf",
        shell=True
    )

    print(f"done!")


"""
dit hieronder is voor het later aanroepen van de code thx oscar papito
kwargs = {
    "fastq_bestand": "/homes/lbos5/ERR2165898.fastq",
    "reference": "/homes/lbos5/Downloads/reference/ncbi_dataset/data/GCF_000006945.2/GCF_000006945.2_ASM694v2_genomic.fna",
    "threads": 8,
    "N": 5
}

main(kwargs)

dit hieronder is voor het later aanroepen van de code thx oscar papito

"""