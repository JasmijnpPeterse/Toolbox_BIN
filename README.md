# Toolbox_BIN

De tools die nodig zijn om ons programma te runnen zijn: Minimap2, Samtools en BCFtools.

Voordat u begint met het downloaden van de tools, zorg ervoor dat u een map hebt waar het programma in staat. Geef deze map een naam waarmee u de map makkelijk terug kunt vinden. Alle tools die u downloadt plaatst u uiteindelijk in dezelfde map als het programma.

Mininmap2 kunt u downloaden via deze link:
https://github.com/lh3/minimap2

Wanneer u de link opent, klikt u op de groene knop Code. Hier staat de optie Download ZIP. Klik hierop om Minimap2 te downloaden. Het bestand verschijnt in uw Downloads-map als een ZIP-bestand. Pak dit bestand uit door op Extract here of Alles uitpakken te klikken. Zorg ervoor dat u de uitgepakte map niet in uw Downloads laat staan, omdat dit onoverzichtelijk wordt. Verplaats de map naar dezelfde map waar uw programma staat.


Samtools kun je downloaden via deze link:
https://github.com/samtools/samtools

Wanneer u de link opent, klikt u op de groene knop Code. Hier staat de optie Download ZIP. Klik hierop om Minimap2 te downloaden. Het bestand verschijnt in uw Downloads-map als een ZIP-bestand. Pak dit bestand uit door op Extract here of Alles uitpakken te klikken. Zorg ervoor dat u de uitgepakte map niet in uw Downloads laat staan, omdat dit onoverzichtelijk wordt. Verplaats de map naar dezelfde map waar uw programma staat.


En de BCFtools kun je downloaden via deze link:
https://github.com/samtools/bcftools


Wanneer u de link opent, klikt u op de groene knop Code. Hier staat de optie Download ZIP. Klik hierop om Minimap2 te downloaden. Het bestand verschijnt in uw Downloads-map als een ZIP-bestand. Pak dit bestand uit door op Extract here of Alles uitpakken te klikken. Zorg ervoor dat u de uitgepakte map niet in uw Downloads laat staan, omdat dit onoverzichtelijk wordt. Verplaats de map naar dezelfde map waar uw programma staat.

Voor dit progamma moet je ook een referentie genoom bestand hebben dat geindext is.
Op de web pagina staan 3 linkjes naar NIH voor de referentie genomen, deze moeten nog geindext worden. Als u op de link van het refentie genoom dat u wilt gebruiken hebt geklikt, zou u een download knop moeten staan. Klik hierop en zorg ervoor dat alleen het vakje GENOME SEQUENCES (FASTA) is aangeklikt, en klik op download. 
Nu dat u het referentie genoom op uw apparaat heeft staan, plaats het in dezelfde map als waar de tools staan. 
Als de voorgaande stappen zijn gelukt kunt u naar de terminal gaan. Hier moet u via ``cd locatie`` naar de map gaan waar het referentie genoom staat. Zodra u hier bent moet u het volgende argument in plaatsen om het referentie genoom te indexen:

``minimap2 -d naam_reference_genome.mmi nieuwe_naam_voor_document_met_index.fa``


