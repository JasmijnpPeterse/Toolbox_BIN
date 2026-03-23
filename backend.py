import subprocess, sys

file_location = sys.argv[1]
class Run_program():



def minimap2():
    try:
        output = subprocess.run(
            ["minimap2", "-d", "ref.mmi", file_location], check=True, text=True)
        return output

    except subprocess.CalledProcessError as e:
        sys.exit(f"poging tot analyse gefaald {e.returncode} tijdens het indexen van je genoom via minimap2")


def samtools_sort():
    try:
        output = subprocess.run(
            ["minimap2", "-d", "ref.mmi", file_location], check=True, text=True)
        return output

    except subprocess.CalledProcessError as e:
        sys.exit(f"poging tot analyse gefaald {e.returncode} tijdens het indexen van je genoom via samtools")


#minimap2 -d ref.mmi reference.fasta
#samtools index your_file.bam
def main():
    minimap2_output = minimap2()
    samtools_sort(minimap2_output)
