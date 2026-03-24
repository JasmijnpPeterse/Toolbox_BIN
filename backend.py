import subprocess
import sys


def run(cmd, stap):
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        sys.exit(f"Analyse gefaald (exitcode {e.returncode}) tijdens: {stap}")


def minimap2(input_file):
    print("Stap 1: minimap2 alignment...")
    with open("output.sam", "w") as sam_file:
        subprocess.run(
            ["minimap2", "-a", "-x", "map-ont", "-t", "8", "-N", "5", "referentie.fa", input_file],
            check=True, stdout=sam_file
        )


def samtools_sort():
    print("Stap 2: samtools sort...")
    run(["samtools", "sort", "-o", "output.bam", "output.sam"], "samtools sort")


def samtools_index():
    print("Stap 3: samtools index...")
    run(["samtools", "index", "output.bam"], "samtools index")


def bcftools():
    print("Stap 4: bcftools variant calling...")
    mpileup = subprocess.Popen(
        ["bcftools", "mpileup", "-Ou", "-f", "referentie.fa", "output.bam"],
        stdout=subprocess.PIPE
    )
    call = subprocess.Popen(
        ["bcftools", "call", "-mv", "-Oz", "-o", "output.vcf.gz"],
        stdin=mpileup.stdout
    )
    mpileup.stdout.close()
    call.communicate()

    print("Stap 5: bcftools filter...")
    run(
        ["bcftools", "filter", "-i", "QUAL > 30 && DP > 10", "output.vcf.gz", "-Oz", "-o", "gefilterd.vcf.gz"],
        "bcftools filter"
    )

def main():
    if len(sys.argv) < 2:
        sys.exit("Gebruik: python pipeline.py <input.fastq>")

    minimap2(sys.argv[1])
    samtools_sort()
    samtools_index()
    bcftools()

    print("Klaar! Resultaat opgeslagen in: gefilterd.vcf.gz")

main()
