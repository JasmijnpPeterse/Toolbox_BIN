import matplotlib.pyplot as plt
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
    bcftools.run("call -m -O v -o output.vcf bcftools_mpileup.bcf")
    bcftools.run("filter -i 'QUAL>=30' output.vcf -o output.vcf")


def lezen_vcf():
    mutaties = {}
    snip_tabel_info = {}
    with open('output.vcf', 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("#"):
                continue
            else:
                splitline = line.split('\t')
                if splitline[3]:
                    qual = splitline[5]
                    if splitline[4] != '.' and float(qual) >= 30:  # <-- fix here
                        if splitline[1] not in mutaties:
                            mutaties[splitline[1]] = 1
                        else:
                            mutaties[splitline[1]] += 1
                if splitline[4] != '.':
                    snip_tabel_info[splitline[1]] = [splitline[3], splitline[4]]
    return mutaties, snip_tabel_info

def maken_plot(mutaties):
    plt.bar(mutaties.keys(), mutaties.values())
    plt.xticks(rotation=90)
    plt.ylabel("Aantal mutaties")
    plt.title("Mutaties met QUAL ≥ 30")
    plt.tight_layout()
    plt.savefig("mutaties.png")
