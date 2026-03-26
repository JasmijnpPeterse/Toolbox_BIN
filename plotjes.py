"""
Bio-Informatica project met toolbox

Auteurs: Vani Rembant, Lucas Bos en Jasmijn Peterse
Datum: 25/03 -
Versie: 1.0
"""
import matplotlib.pyplot as plt

def lezen_vcf():
    mutaties = {}
    with open('empty.vcf', 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("#"):
                continue
            else:
                index_line = line.split()
                if index_line[4]:
                    if float(index_line[5]) >= 30:
                        if index_line[1] not in mutaties:
                            mutaties[index_line[1]] = 1
                        if index_line[1] in mutaties:
                            mutaties[index_line[1]] =+1

    return mutaties

def maken_plot(mutaties):
    plt.bar(mutaties.keys(), mutaties.values())
    plt.xticks(rotation=90)
    plt.ylabel("Aantal mutaties")
    plt.title("Mutaties met QUAL ≥ 30")
    plt.tight_layout()
    plt.show()


def main():
    mutaties = lezen_vcf()
    maken_plot(mutaties)

if __name__ == '__main__':
    main()