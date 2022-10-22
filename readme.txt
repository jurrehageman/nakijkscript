Handleiding 'nakijkscript'

Antwoorden worden via Microsoft Forms ingeleverd. Deze bestanden zijn te vinden in Microsoft Teams als Excel-bestand.

Download het bestand met de antwoorden van de studenten en sla het vervolgens op als csv-bestand (het script leest alleen csv-bestanden). Gebruik duidelijke namen voor de bestanden en lessen, bijvoorbeeld les1_ncbi_protein.csv

Zet het bestand in dezelfde map als het script. In deze map staan ook de bestanden met de antwoorden

Open een terminal en navigeer naar de map met het script.

Het commando voor het script verwacht 3 argumenten:
- het te lezen csv-bestand
- de naam van het bestand waar het nagekeken wel naartoe wordt geschreven
- het bestand met de antwoorden

Type: python3 nakijkscript_les_bioinf2.py argument1 argument2 argument3

Bijvoorbeeld:
python3 nakijkscript_les_bioinf2.py les1_ncbi_protein.csv les1_results.xlsx antwoorden_les1.txt

Het bestand met het nagekeken werk staat nu in les1_results.xlsx. De output is zo opgemaakt dat het letterlijk gekopieerd kan worden in het Excel-bestand en daar verder verwerkt wordt. Gebruik hier altijd copy -> paste values

