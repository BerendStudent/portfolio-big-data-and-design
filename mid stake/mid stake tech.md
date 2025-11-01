# Mid Stake Tech

## Inhoud

1. [Feedback](#feedback)
2. [Ontwikkeling](#ontwikkeling)
3. [Uitvoering](#uitvoering)
4. [Wat ging er goed](#wat-ging-er-goed)
5. [Uitdagingen](#uitdagingen)
6. [Tegenslagen](#tegenslagen)
7. [Doelen](#doelen)

## Feedback
### Feedback Luuc
Ik heb van Luuc als feedback ontvangen dat mijn graphing tool technisch gezien erg indrukwekkend is, maar dat deze weinig toegevoegde waarde biedt boven bestaande tools die veel minder tijd hadden gekost. Deze feedback vond ik interessant, omdat het me liet nadenken over de balans tussen technische complexiteit en functionele relevantie. Vaak ben ik geneigd om mezelf technisch uit te dagen en iets ‘from scratch’ te bouwen, maar dit kost soms zoveel tijd dat het uiteindelijke doel – het vertellen van een duidelijk data-verhaal – naar de achtergrond verdwijnt. Door deze feedback ben ik me bewuster geworden van het belang van pragmatisme binnen een project: niet alles hoeft vanaf nul geschreven te worden als er al bewezen oplossingen bestaan.

### Feedback Pete
Van Pete kreeg ik feedback dat mijn technische opdrachten netjes en gestructureerd waren, maar dat er nog meer aandacht mocht zijn voor kleine details, zoals consistente comments en uitleg bij code. Dit leek in eerste instantie een klein punt, maar ik realiseer me dat dit juist belangrijk is voor de leesbaarheid en overdraagbaarheid van mijn werk. Ik heb daarom geprobeerd om in latere opdrachten mijn code beter te documenteren en mijn gedachtengang toe te lichten, zodat ook anderen mijn redeneringen kunnen volgen.

## Ontwikkeling
Ik begon deze minor met een stevige technische basis, omdat ik een achtergrond heb in technische informatica. Daardoor had ik bij de meeste Python-opdrachten relatief weinig moeite. Toch heb ik geprobeerd om mezelf te blijven uitdagen, onder andere door eigen projecten op te pakken die verder gingen dan de standaard opdrachten. Een goed voorbeeld daarvan is mijn graphing tool.

Hoewel de meeste studenten gebruikmaakten van bestaande visualisatielibraries zoals Matplotlib, besloot ik om zelf een eenvoudige graphing library te schrijven. Ik deed dit niet omdat het moest, maar omdat ik wilde begrijpen hoe zulke tools werken op een laag niveau. Door dit te doen, heb ik beter inzicht gekregen in hoe visualisatiepakketten omgaan met schaalverdeling, coördinaten, en rendering in HTML5-canvas.

Daarnaast heb ik tijdens de workshops veel geleerd over Natural Language Processing (NLP). Hoewel ik hier al theoretische kennis over had, was het waardevol om te zien hoe deze technieken praktisch worden toegepast in data-analyse en tekstmining. Dit heeft mijn interesse in taalmodellen en machine learning verder versterkt.

## Uitvoering
Het eerste deel van dit semester heb ik alle tech opdrachten volledig afgerond. Dit heb ik zonder problemen kunnen doen, doordat ik de voorkennis al had die deze opdrachten bedoeld waren om aan te leren. Ik heb wel erg veel van de workshop kunnen leren, omdat er voor text mining veel gebruik gemaakt wordt van Natural Language Processing. Dit was puur theoretische kennis, maar ik denk dat dit wel erg handig wordt voor mijn toekomstige werk.

Verder heb ik voor mijn data story mijn eigen graphing library geschreven. Dit heb ik in Javascript gedaan, omdat ik Python al erg goed ken, en ik meer wil weten over Javascript. De tool werkt in een html bestand, door pixels aan te passen op een canvas gebaseerd op de ingevoerde data. Hier heb ik erg veel van geleerd, en ik ben blij dat ik dit heb gedaan, ondanks dat het uitendelijk niet relevant was voor mijn data story. 


Voorbeeld:
```
    var line_data = [[1989, 8.89], [1990, 8.7], [1991, 8.62], [1992, 8.41], [1993, 8.51], [1994, 8.56], [1995, 8.8], [1996, 9.03], [1997, 8.98], [1998, 8.74], [1999, 8.86], [2000, 9.2], [2001, 9.26], [2002, 9.68], [2003, 10.52], [2004, 10.87], [2005, 11.55], [2006, 12.19], [2007, 12.78], [2008, 13.2], [2009, 13.05], [2010, 13.95], [2011, 14.74], [2012, 14.91], [2013, 15], [2014, 15.02], [2015, 14.67], [2016, 14.34], [2017, 14.51], [2018, 14.75], [2019, 14.69], [2020, 14.21], [2021, 15.13], [2022, 15.19], [2023, 15.4]];
    var line_graph = new Graph('frame2', 500, 'line', {
        title: "CO2 uitstoot door steenkoolverbranding",
        xLabel: "Jaar",
        yLabel: "Miljard ton co2",
        showPointLabels: true,
        font: "10px Arial",
        fontColor: "black"
    });
    line_graph.createFrame(line_data);
```
![alt text](<../design/data story/images/co2 uitstoot door steenkool.png>)

## Wat ging er goed
De opdrachten gingen erg goed. Ik heb de opdrachten over data visualization, data cleanup, en algemene python skills, zonder problemen kunnen afronden.

## Uitdagingen
De grootste uitdaging op het gebied van tech was het uitzoeken van uitdagingen op het gebied van tech. Ik heb dit blok specifiek gekozen voor moeilijkere opdrachten, zoals met mijn graphing tool en met de data wrangling opdrachten, omdat ik daar voor de air disasters pdf koos.

## Tegenslagen
Een van de grootste tegenslagen was dat ik veel tijd heb geïnvesteerd in mijn graphing tool, terwijl deze uiteindelijk weinig bijdroeg aan mijn data story. Met de kennis van nu had ik waarschijnlijk beter een bestaande library kunnen gebruiken, zodat ik meer tijd had gehad voor de inhoudelijke kant van mijn visualisatie. Toch zie ik het niet als verspilde moeite: het project heeft me geholpen om mijn JavaScript-kennis te verdiepen en beter te begrijpen hoe visualisatie werkt op technisch niveau.

## Doelen
In het volgende blok krijgen wij les over UX design, Natural Language Processing, en data visualization. Dit zijn onderwerpen waar ik al wel een technische achtergrond in heb, maar waar ik niet ver ontwikkeld in ben. Ik hoop vooral meer te leren over UX design, omdat dit echt een gebied is waar ik niet veel over weet.

Daarnaast wil ik meer leren over het combineren van data-analyse met storytelling. Mijn doel is om niet alleen iets te maken dat werkt, maar ook iets dat mensen begrijpend en interessant vinden. Ik denk dat de volgende modules mij zullen helpen om die brug te slaan tussen techniek en communicatie.