import matplotlib.pyplot as plt
from io import BytesIO
import base64
import subprocess


class Tool:
    def __init__(self, tool, **configs):
        self.tool = tool
        self.configs = configs

    def run(self, cmd):
        subprocess.run(f"{self.tool} {cmd}", shell=True)


def run(kwargs):
    minimap2 = Tool("minimap2", threads=kwargs["threads"], N=kwargs["N"], reference=kwargs["reference"], fastq=kwargs["fastq_bestand"])
    samtools = Tool("samtools")
    bcftools = Tool("bcftools", reference=kwargs["reference"], region=kwargs.get("region"))

    minimap2.run(f"-a -x map-ont -t {minimap2.configs['threads']} -N {minimap2.configs['N']} {minimap2.configs['reference']} {minimap2.configs['fastq']} > output.sam")

    samtools.run("view -b -o output.bam output.sam")
    samtools.run("sort output.bam > sorted_output.bam")
    samtools.run("index sorted_output.bam")

    mpileup_cmd = f"mpileup sorted_output.bam -f {bcftools.configs['reference']}"
    if bcftools.configs.get("region"):
        mpileup_cmd += f" -r {bcftools.configs['region']}"
    mpileup_cmd += " > bcftools_mpileup.bcf"

    bcftools.run(mpileup_cmd)
    bcftools.run("call -m -O v -o output.vcf bcftools_mpileup.bcf| bcftools filter -i 'QUAL>=30' -o output.vcf")

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
