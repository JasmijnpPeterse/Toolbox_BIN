import subprocess
import time

class Tools():
    def __init__(self, chrom, pos, ref, alt, qual):
        self.chrom = chrom
        self.pos = pos
        self.ref = ref
        self.alt = alt
        self.qual = float(qual)

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
                #qual = regel[5]
            )
            lijst.append(mutatie)
    return lijst

def relevante_mutatie(self):
    """
    hier wordt bepaald wanneer een mutatie relevant is door midden van kwaliteitscontrole.
    straks wordt het zo:
    return self.qual >= (een getal)
    """

def filter_mutaties(mutatie_lijst):
    relevante_mutaties = []
    ruis = []
    for mutatie in mutatie_lijst:
        if mutatie.relevante_mutatie():
            relevante_mutaties.append(mutatie)
        else:
            ruis.append(mutatie)
    return relevante_mutaties, ruis

def aantal_mutaties(aantal_mut_lijst):
    locatie_bijhouden = {}
    frequentie = []

    for mutatie in aantal_mut_lijst:
        locatie = (mutatie.chrom, mutatie.pos)

        if locatie in locatie_bijhouden:
            locatie_bijhouden[locatie] += 1
        else:
            locatie_bijhouden[locatie] = 1

    for (chrom, pos), count in locatie_bijhouden.items():
        locatie_data = {
            'chrom': chrom,
            'pos': pos,
            'frequentie': count,
        }
        frequentie.append(locatie_data)

    return frequentie


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
        "bcftools call -m -O v -o out.vcf bcftools_mpileup.bcf",
        shell=True
    )

    print(f"Tools done!")

    mutatie_obj = vcf_naar_lijst("out.vcf")
    print(f"Mutatie gevonden: {len(mutatie_obj)}")

    nodige_mutatie, onnodige_mutatie = filter_mutaties(mutatie_obj)
    print(f"Relevante mutatie: {len(nodige_mutatie)}")
    print(f"Ruis mutatie: {len(onnodige_mutatie)}")

    mutatie_frq = aantal_mutaties(mutatie_obj)
    print(f"Mutatie frequntie: {len(mutatie_frq)}")


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

