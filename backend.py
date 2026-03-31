import subprocess
import time
import matplotlib.pyplot as plt
from io import BytesIO
import base64

class Tools():
    def __init__(self, chrom, pos, ref, alt, qual):
        self.chrom = chrom
        self.pos = pos
        self.ref = ref
        self.alt = alt
        self.qual = float(qual) if qual != '.' else 0.0


def run(kwargs):
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
    "bcftools call -m -O v bcftools_mpileup.bcf | bcftools filter -i 'QUAL>=30' -o output.vcf",
    shell=True
    )

    print(f"done!")

def lezen_vcf():
    mutaties = {}
    snps_tabel_info = {}
    chroms = {}
    with open('output.vcf', 'r') as f:
        for line in f:
            splitline = line.strip().split('\t')
            if line.startswith("#"):
                continue
            if splitline[4] and splitline[4] != '.':
                pos = splitline[1]
                chrom = splitline[0]
                mutaties[pos] = mutaties.get(pos, 0) + 1
                chroms[chrom] = chroms.get(chrom, 0) + 1
                snps_tabel_info[pos] = [splitline[3], splitline[4]]
    return mutaties, snps_tabel_info, chroms

class Plot:
    def __init__(self, mutaties):
        self.mutaties = mutaties

    def __str__(self):
        return f"Hoi HOI{self.mutaties}"

    def maken(self):
        fig, ax = plt.subplots()
        ax.bar(self.mutaties(), self.mutaties.values())
        ax.set_xticklabels(self.mutaties.keys(), rotation=90)
        ax.set_ylabel("Aantal mutaties")
        ax.set_title("Mutaties met QUAL ≥ 30")
        fig.tight_layout()
        return self.maken_plot(fig)


    def maken_plot(self, mutaties):
        pltfile = BytesIO()
        plt.savefig(pltfile, format='png')
        pltfile.seek(0)  # rewind to beginning of file
        website_png = base64.b64encode(pltfile.getvalue()).decode('ascii')

        return website_png
