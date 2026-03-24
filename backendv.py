import subprocess
import time

class Tools():
    def __init__(self, chrom, pos, ref, alt):
        self.chrom = chrom
        self.pos = pos
        self.ref = ref
        self.alt = alt

def vcf_naar_lijst(vcf_bestand):
    with open(vcf_bestand, 'r') as vcf:
        lijst = []
        for line in vcf:
            if line.startswith('#'):
                continue
            regel = line.strip().split('\t')
            mutatie = Tools(
            chrom = regel[0],
            pos = regel[1],
            ref = regel[3],
            alt = regel[4]
            )
            lijst.append(mutatie)
    return lijst

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

    subprocess.run(
        f"bcftools mpileup sorted_output.bam -f {kwargs['reference']} > bcftools_mpileup.bcf",
        shell=True
    )

    subprocess.run(
        "bcftools call -m -O v -o out.vcf bcftools_mpileup.bcf",
        shell=True
    )

    print(f"Tools done!")

    mutatie_obj = vcf_naar_lijst("out.vcf")
    print(f"Mutatie gevonden: {len(mutatie_obj)}")


"""
dit hieronder is voor het later aanroepen van de code thx oscar papito
kwargs = {
    "fastq_bestand": "reads.fastq",
    "reference": "referentie.fa",
    "threads": 8,
    "N": 5
}

main(kwargs)
"""

