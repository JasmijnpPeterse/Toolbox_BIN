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
        "bcftools call -m -O v -o output.vcf bcftools_mpileup.bcf",
        shell=True
    )
    subprocess.run(
        "bcftools filter -i QUAL>=30' output.vcf -o output.vcf",
        shell=True
    )

    print(f"done!")


def lezen_vcf():
    mutaties = {}
    snip_tabel_info = {}
    with open('testoutput.vcf', 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("#"):
                continue
            else:
                splitline = line.split('\t')
                if splitline[4]:
                    qual = splitline[5]
                    if splitline[4] != '.':
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
    plt.savefig("static/mutaties.png")

    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)  # rewind to beginning of file
    website_png = base64.b64encode(figfile.getvalue()).decode('ascii')
