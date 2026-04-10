"""
Bio-informatica nanopore sequencing analuse

Autors: Lucas Bos, Jasmijn Peterse, Vani Rembet
Version: 1.0
Date: 30/03 - 10/04
"""
from io import BytesIO
import base64
import subprocess
import matplotlib.pyplot as plt


class Tool:
    """
    Class om tools aan te maken
    """
    def __init__(self, tool, **configs):
        """
        __innit__ laat de gebruiker de naam van de tool + meerdere configuraties invullen
        """
        self.tool = tool
        self.configs = configs

    def __str__(self):
        return f"Tool: {self.tool}, configs: {self.configs}"

    def run(self, cmd):
        """
        Zorgt ervoor dat de tool in de terminal wordt gerunned
        """
        subprocess.run(f"{self.tool} {cmd}", shell=True)


def run(kwargs):
    """
    maakt tools aan en runt ze in de terminal
    """
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
    """
    Functie voor het inlezen van het output vcf file

    :return: mutaties(dict), snps_tabel_info(dict), chroms(dict)
    """
    mutaties = {}
    snps_tabel_info = {}
    chroms = {}
    with open("output.vcf", "r", encoding="utf-8") as f:
        for line in f:
            splitline = line.strip().split("\t")
            if line.startswith("#"):
                continue
            if splitline[4] and splitline[4] != ".":
                pos = splitline[1]
                chrom = splitline[0]
                mutaties[pos] = mutaties.get(pos, 0) + 1
                chroms[chrom] = chroms.get(chrom, 0) + 1
                snps_tabel_info[pos] = [splitline[3], splitline[4]]
    return mutaties, snps_tabel_info, chroms

class Plot:
    """
    Class voor het maken van een plot
    """
    def __init__(self, mutaties):
        """
        Initialiseert het object met een lijst van mutaties.

        :param mutaties: (list) lijst van mutaties
        """
        self.mutaties = mutaties

    def __str__(self):
        """
        Geeft een leesbare string representatie van het object.

        :return: (str) string met de mutaties
        """
        return f"Mutaties is dit:{self.mutaties}"


    def maken(self):
        """
        Functie voor het maken van het plot
        :return: Object(plot)
        """
        fig, ax = plt.subplots()

        keys = list(self.mutaties.keys())
        values = list(self.mutaties.values())

        ax.bar(keys, values)
        ax.set_xticks(range(len(keys)))
        ax.set_xticklabels(keys, rotation=90)

        ax.set_xlabel("Positie in genoom")
        ax.set_ylabel("Mutaties")
        ax.set_title("Mutaties in reads")
        fig.tight_layout()

        return self.opslaan_plot(fig)


    def opslaan_plot(self, fig):
        """
        Functie voor het opslaan van het plot
        :return website_png(str) string met base64 karakters van de plot
        """
        pltfile = BytesIO()
        plt.savefig(pltfile, format="png")
        pltfile.seek(0)  # rewind to beginning of file
        website_png = base64.b64encode(pltfile.getvalue()).decode("ascii")

        return website_png
