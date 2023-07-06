# Data processing utils

Alguns codis útils per a processar dades de [Twarc].

## get\_counts_\jsonl.py

```
python3 get_counts_jsonl.py --granularity [day|hour|minute] INFILE OUTFILE
```

Aquest codi rep d'entrada (`INFILE`)
un fitxer de tweets jsonl
obtingut amb alguna consulta de Twarc com `search`, `searches` o `stream`
i et retorna un fitxer CSV (`OUTFILE`)
on la primera columna és la finestra temporal
i la segona és el nombre de tweets (i retweets) del jsonl escrits en aquella finestra.
La granularitat de la finestra és per defecte un dia,
però pot canviar-se amb l'opció `--granularity`.

## get\_counts\_twarc.py

```
python3 get_counts_twarc.py --granularity [day|hour|minute] INFILE OUTFILE
```

Aquest codi et converteix un fitxer json (`INFILE`)
que tingui el format de configuració del [recollector]
en una consulta `twarc2 searches --counts-only`.
Aquesta consulta desa un fitxer CSV a `OUTFILE`
on les columnes són el mot clau, la finestra temporal
i el nombre de tweets escrits en la finestra temporal que continguin el mot clau.
La granularitat de la finestra és per defecte un dia,
però pot canviar-se amb l'opció `--granularity`.

Ara mateix, aquest codi només funciona per fitxers de configuració molt senzills,
que només continguin una finestra temporal.
Es podria millorar per fer que funcionés amb qualsevol nombre.
També crea un fitxer `tmp.txt` que es pot esborrar.

## get\_most\_common\_words.py

```
python3 get_most_common_words.py INFILE OUTFILE
```

Aquest codi rep d'entrada (`INFILE`)
un fitxer de tweets jsonl obtingut amb alguna consulta de Twarc
i et retorna un fitxer CSV (`OUTFILE`)
on la primera columna és un mot
i la segona és quants cops apareix aquest mot en tweets o retweets del jsonl.
Les files estan ordenades decreixentment per aquesta segona columna.
Els accents són ignorats (seguint el criteri definit a `strip_accents.py`)
tal com fa l'API de Twitter a l'hora de descarregar tweets que continguin algun mot clau.

## get\_network\_communities.py

```
python3 get_network_communities.py --weight TEXT --cutoff INT --best_n INT [INFILES]... OUTDIR
```
Aquest codi rep d'entrada (`INFILES`)
diversos fitxers gml de xarxes obtingudes amb [twarc-network].
De cada una d'aquestes xarxes se'n calcularan les comunitats i es desaran a `OUTDIR`.

L'algorisme utilitzat és l'algorisme voraç de maximització de la modularitat de [Clauset-Newman-Moore].
L'opció `--cutoff` marca el nombre mínim de comunitats que s'han de retornar (per defecte, 1)
i l'opció `--best_n` marca el nombre màxim de comunitats a retornar (per defecte, tantes com en trobi).
Les arestes de les xarxes d'usuaris de Twarc són pesades.
Per defecte, es fa servir el pes `weight`,
que correspon al nombre total d'interaccions d'un usuari a l'altre
(retweets, citacions, respostes i mencions).
Si es vol usar un pes concret, com per exemple els retweets,
es pot fer amb l'opció `--weight retweet`.

L'argument `OUTDIR` és senzillament un string que es posa a l'inici del fitxer de sortida.
És a dir, si voleu posar els fitxers de sortida en un directori anomenat `dir`,
l'argument haurà de ser `dir/`.
Però no cal que sigui un directori, si voleu pot ser `xarxa-`
i els fitxers es desaran al directori on s'executi, però tots començaran per aquest string.
La resta del nom del fitxer serà el nom de la xarxa utilitzada,
canviant l'extensió de `.gml` per `.json`.
El format d'aquests fitxers és un json senzill on la clau és el nom d'usuari
i el valor és la comunitat,
on la comunitat més gran és la 0, la segona més gran és la 1 i així successivament.

## get\_network\_layout.py

```
python3 get_network_layout.py --component [weak|strong] --layout [sfdp|arf|fr] --weight TEXT [INFILES]... OUTDIR
```

Aquest codi rep d'entrada (`INFILES`)
diversos fitxers gml de xarxes obtingudes amb [twarc-network].
De cada una d'aquestes xarxes se'n farà el layout i es desarà a `OUTDIR`.

L'algorisme usat per defecte és l'SFDP spring-block layout,
però també es poden fer servir altres algorismes de la llibreria [graph-tool]
amb l'opció `--layout`.
El pes de les arestes utilitzat per defecte és `weight`.
Es pot usar un altre pes amb l'opció `--weight`.
Si es vol obtenir el layout únicament de la component feblement o fortament connexa més gran
es pot usar l'opció `--component`.

L'argument `OUTDIR` és senzillament un string que es posa a l'inici del fitxer de sortida.
És a dir, si voleu posar els fitxers de sortida en un directori anomenat `dir`,
l'argument haurà de ser `dir/`.
Però no cal que sigui un directori, si voleu pot ser `xarxa-`
i els fitxers es desaran al directori on s'executi, però tots començaran per aquest string.
La resta del nom del fitxer serà el nom de la xarxa utilitzada,
canviant l'extensió de `.gml` per `.json`.
El format d'aquests fitxers és un json senzill on la clau és el nom d'usuari
i el valor és una llista de les dues coordenades.

A part de les dependències que hi ha a `requeriments.txt`,
també cal [instal·lar] graph-tool per a fer servir aquest codi.

## merge.py

```
python3 merge.py [INFILES]... OUTFILE
```

Aquest codi fusiona diversos fitxers de tweets jsonl (`INFILES`)
obtinguts amb alguna consulta de Twarc
en un únic fitxer `OUTFILE`.
Si un mateix tweet aparesqués en més d'un fitxer,
només s'inclouria un cop en el fitxer final.

## network.sh

```
network.sh
```

Aquest codi converteix tots els fitxers jsonl del directori on s'executa,
obtinguts amb alguna consulta de Twarc,
en xarxes en format gml, utilitzant Twarc Network.
Els fitxers obtinguts tenen el mateix nom,
però amb l'extensió `.gml` en comptes de `.jsonl`.

[Clauset-Newman-Moore]: https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.community.modularity_max.greedy_modularity_communities.html
[graph-tool]: https://graph-tool.skewed.de/static/doc/draw.html#layout-algorithms
[instal·lar]: https://git.skewed.de/count0/graph-tool/-/wikis/installation-instructions
[recollector]: https://github.com/remiss-project/recollector
[Twarc]: https://github.com/DocNow/twarc
[twarc-network]: https://github.com/DocNow/twarc-network
