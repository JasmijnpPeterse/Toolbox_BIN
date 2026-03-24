import subprocess, sys

file_location = sys.argv[1]




def minimap2():
    try:
        output = subprocess.run(
            ["minimap2", "-d", "ref.mmi", file_location], check=True, text=True)
        return output

    except subprocess.CalledProcessError as e:
        sys.exit(f"poging tot analyse gefaald {e.returncode} tijdens het indexen van je genoom via minimap2")


def samtools_sort(minimap2_output):
    try:
        output = subprocess.run(
            ["samtools", "sort", "-o", 'output_samtools_sorted', minimap2_output], check=True, text=True)[3]
        return output

    except subprocess.CalledProcessError as e:
        sys.exit(f"poging tot analyse gefaald {e.returncode} tijdens het sorten van je genoom via samtools")

def samtools_index(samtools_sort_output):
    try:
        output = subprocess.run(
            ["samtools", "index", samtools_sort_output], check=True, text=True)
        return output

    except subprocess.CalledProcessError as e:
        sys.exit(f"poging to analyse gefaald {e.returncode} tijdens het indexen van je genoom via samtools")

def


def main():
    minimap2_output = minimap2()
    samtools_sort_output = samtools_sort(minimap2_output)
    samtools_index(samtools_sort_output)
