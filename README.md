# Toolbox_BIN

De tools die nodig zijn om ons programma te runnen zijn: Minimap2, Samtools en BCFtools.

Voordat u begint met het downloaden van de tools, zorg ervoor dat u een map hebt waar het progamma in staat. 
Geef dit een naam waarmee u de map makkelijk terug kan vinden.

Mininmap2 kunt u downloaden via deze link:
https://github.com/lh3/minimap2

Als u de link opent moet u klikken op de button code, hierin staat de optie downloud zit, hier klikt u op. Zodra u Minimap2 hebt gedownload staat het in uw downloads als een zip, deze pakt u uit door op exstract here te klikken. 
Zorg ervoor dat u deze niet in je downloads map laat staan, hierdoor wordt het slordig en moeilijk te vinden. Zet deze map in dezelfde map waar u het progamma in hebt staan.

Samtools kun je downloaden via deze link:
https://github.com/samtools/samtools

Als u de link opent moet u klikken op de button code, hierin staat de optie downloud zit, hier klikt u op. Zodra u Minimap2 hebt gedownload staat het in uw downloads als een zip, deze pakt u uit door op exstract here te klikken. 
Zorg ervoor dat u deze niet in je downloads map laat staan, hierdoor wordt het slordig en moeilijk te vinden. Zet deze map in dezelfde map waar u het progamma in hebt staan.


En de BCFtools kun je downloaden via deze link:
https://github.com/samtools/bcftools

Als u de link opent moet u klikken op de button code, hierin staat de optie downloud zit, hier klikt u op. Zodra u Minimap2 hebt gedownload staat het in uw downloads als een zip, deze pakt u uit door op exstract here te klikken. 
Zorg ervoor dat u deze niet in je downloads map laat staan, hierdoor wordt het slordig en moeilijk te vinden. Zet deze map in dezelfde map waar u het progamma in hebt staan.

Voor dit progamma moet je ook een referentie genoom bestand hebben dat geindext is.
Op de web pagina staan 3 linkjes naar NIH voor de referentie genomen, deze moeten nog geindext worden. Als u op de link van het refentie genoom dat u wilt gebruiken hebt geklikt, zou u een download knop moeten staan. Klik hierop en zorg ervoor dat alleen het vakje GENOME SEQUENCES (FASTA) is aangeklikt, en klik op download. 
Nu dat u het referentie genoom op uw apparaat heeft staan, plaats het in dezelfde map als waar de tools staan. 
Als de voorgaande stappen zijn gelukt kunt u naar de terminal gaan. Hier moet u het volgende argument in plaatsen om het referentie genoom te indexen:

minimap2 -d naam_reference_genome nieuwe_naam_voor_document_met_index

Dit moet je doen doormiddel van Minimap2. Als u het referentie genoom 
