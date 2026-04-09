# Geautomatiseerde Nanopore Analyse Pipeline

Bio-informatica project voor DNA variant detectie via Nanopore-sequencing.  
Ontwikkeld door: Lucas Bos, Jasmijn Peterse, Vani Rembet

---

## Vereisten

### Software
- Python 3.8 of hoger
- pip (Python pakketbeheer)
- Minimap2
- SAMtools
- BCFtools

### Python-pakketten
Installeer de benodigde Python-pakketten met:

```bash
pip install flask matplotlib werkzeug
```

---

## Installatie van tools

Zorg ervoor dat u een overzichtelijke map heeft voor het project. Plaats alle tools en data in dezelfde map.

### 1. Minimap2

Download via: https://github.com/lh3/minimap2

1. Klik op de groene knop **Code** → **Download ZIP**
2. Pak het ZIP-bestand uit
3. Verplaats de uitgepakte map naar uw projectmap
4. Compileer de tool via de terminal:

```bash
cd minimap2
make
```

### 2. SAMtools

Download via: https://github.com/samtools/samtools

1. Klik op de groene knop **Code** → **Download ZIP**
2. Pak het ZIP-bestand uit en verplaats naar uw projectmap
3. Compileer via de terminal:

```bash
cd samtools
./configure
make
make install
```

### 3. BCFtools

Download via: https://github.com/samtools/bcftools

1. Klik op de groene knop **Code** → **Download ZIP**
2. Pak het ZIP-bestand uit en verplaats naar uw projectmap
3. Compileer via de terminal:

```bash
cd bcftools
./configure
make
make install
```

> **Tip:** Controleer na installatie of de tools werken door `minimap2 --version`, `samtools --version` en `bcftools --version` in de terminal uit te voeren.

---

## Data instellen

Zorg dat de volgende bestanden aanwezig zijn in de `Data/` map:

```
Data/
├── ERR2165898.fastq              # Nanopore FASTQ-bestand
└── reference/
    └── GCF_000006945.2_ASM694v2_genomic.fna  # Referentiegenoom
```

De paden naar deze bestanden zijn ingesteld in `app.py`. Pas ze aan als u andere bestanden gebruikt:

```python
FASTQ_BESTAND = os.path.join(BASE_DIR, "Data", "ERR2165898.fastq")
REFERENCE = os.path.join(BASE_DIR, "Data", "reference", "GCF_000006945.2_ASM694v2_genomic.fna")
```

---

## De applicatie starten

Start de webapplicatie via de terminal:

```bash
python app.py
```

De applicatie is daarna bereikbaar via uw browser op: http://localhost:5002

---

## Projectstructuur

```
project/
├── app.py               # Flask webapplicatie
├── backend.py           # Pipeline-logica (Minimap2, SAMtools, BCFtools)
├── templates/
│   ├── header.html      # Gedeelde header en navigatie
│   ├── web.html         # Analysepagina
│   ├── Info_pagina.html # Informatiepagina
│   ├── tools_info.html  # Uitleg over de gebruikte tools
│   └── reference.html   # Referentiegenoom-links
├── static/
│   └── stylesheet.css   # Opmaak
└── Data/
    ├── ERR2165898.fastq
    └── reference/
        └── *.fna
```

---

## Gebruik

1. Open de browser en ga naar http://localhost:5002
2. Vul optioneel een chromosoom, startpunt en eindpunt in om een specifiek regio te analyseren
3. Kies de gewenste resultaten:
   - Tabel met SNP's
   - Plot van mutaties per positie
   - Plot van mutaties per chromosoom
4. Klik op **Start Analyse**

De analyse produceert de volgende tussenbestanden in de projectmap:

| Bestand | Beschrijving |
|---------|--------------|
| `output.sam` | Alignment-uitvoer van Minimap2 |
| `output.bam` | Gecomprimeerde versie van het SAM-bestand |
| `sorted_output.bam` | Gesorteerd BAM-bestand |
| `sorted_output.bam.bai` | Index van het BAM-bestand |
| `bcftools_mpileup.bcf` | Mpileup-uitvoer |
| `output.vcf` | Gefilterde varianten (QUAL ≥ 30) |

---

## Problemen oplossen

Als u problemen heeft met het runnen van van de website of eventuele erorrs die u tegenkomt, kunt u mailen naar l.bos.05@st.hanze.nl, adventa.christophany.rembet@st.hanze.nl of jrj.peterse@st.hanze.nl