---
title: Ho sistemato i metadati delle foto di Google Takeout
image: /posts/2025-03-31-sistemato-metadati-foto-google-takeout/image.jpg
description: Pensavo fosse piú semplice e invece no.
---
Dopo aver fatto l’upload di tutti i [video compressi](https://alorenzi.eu/2025/03/28/che-me-ne-faccio-dei-video.html) che avevo in giro su immich sono passato a richiedere a google tutto il mio archivio fotografico.


Ho fatto partire l’upload di qualche foto ma mi sono accorto che non tutte andavano nel posto giusto, qualcuna veniva caricata con la data in cui ho chiesto il takeout. 😱

Mi sono accorto che tutti i file foto e video avevano un file `.supplemental-metadata.json` associato. Ad esempio:

```
# ls -l ./Garda2020/DSC01374.jpg*                          
-rw-r--r--. 1 alorenzi alorenzi 160565 Aug 18  2020 ./Garda2020/DSC01374.jpg
-rw-r--r--. 1 alorenzi alorenzi    599 Mar 25 00:02 ./Garda2020/DSC01374.jpg.supplemental-metadata.json
```

Inoltre qualcuno aveva il nome di quel file tagliato, ad esempio  `./Photos from 2025/IMG_20250310_201005_380.webp.supplemental-meta.json` . Sicuramente volevano tenere il nome di una lunghezza massima, ma non ha sicuramente facilitato il lavoro di puliza.

## Che sono gli exif?

Gli exif sono metadati che la macchina fotografica (o il telefono) scrive all’interno del file della fotografia. Ci potete trovare il modello della macchina con cui é stata scattata la foto, i settaggi (tempi di esposizione, iso…), la posizione GPS e l’orario.

I software di gestione delle foto utilizzano queste informazioni per mettere la foto sulla mappa o appunto metterla correttamente nella timeline.

## Scriptiamo…

In questo caso ho utilizzato `exiftool` per estrarre la data dal file originale per evitare di processare inutilmente tutte le immagini, poi ho estratto dal json il timestamp con `jq` e infine ho settato l’exif usando ancora `exiftool` .

```bash
update_metadata(){
    FILENAME=$1
    # Extract the date from exif
    DATE=$(exiftool -d "%Y-%m-%d" -DateTimeOriginal -s3 "${FILENAME}")
    # if the date is valid return
    if [ -n "${DATE}" ]; then
        return 0
    fi
    JSON_FILE=$(ls "${FILENAME}".*.json)
    # Get the date from metadata json
    PHOTO_TAKEN_TIME=$(jq -r '.photoTakenTime.timestamp' "${JSON_FILE}")
    # Set exif
    exiftool -overwrite_original  -d "%s" \
      -DateTimeOriginal="${PHOTO_TAKEN_TIME}" \
      -FileCreateDate="${PHOTO_TAKEN_TIME}" \
      -FileModifyDate="${PHOTO_TAKEN_TIME}" \
      "${FILENAME}"
}
```

Una veloce modifica al codice e troviamo quali immagini non sono state configurate correttamente

```bash
check_date(){
    FILENAME=$1
    DATE=$(exiftool -d "%Y-%m-%d" -DateTimeOriginal -s3 "${FILENAME}")
    # if the date is valid return
    if [ -n "${DATE}" ]; then
        return 0
    fi
    echo "No date found for ${FILENAME}"
}
```

Entrambe le funzioni si possono lanciare con il comando `find` come fatto nell’[articolo precedente](https://alorenzi.eu/2025/03/28/che-me-ne-faccio-dei-video.html#lo-script).

Con `check_date` ho scoperto che una trentina di foto non avevano né gli exif settati e nemmeno un file json associato. Ma é anche vero che erano quasi tutte foto `NOMEFILE-edited.jpg` o simili.

Quindi l’ultimo giro di giostra é stato fare uno script che prendesse due immagini e copiasse la data di scatto da una all’altra:

```bash
lastfix(){
    FILENAME="$1"
    PHOTO_TAKEN_TIME=$(exiftool -d "%s" -DateTimeOriginal -s3 "$2")
    echo "Writing $PHOTO_TAKEN_TIME to $FILENAME"
    exiftool -overwrite_original \
        -d "%s" \
        -DateTimeOriginal="$PHOTO_TAKEN_TIME" \
        -FileCreateDate="$PHOTO_TAKEN_TIME" \
        -FileModifyDate="$PHOTO_TAKEN_TIME" \
        "$FILENAME"
}

lastfix photo-edited.jpg photo.jpg
```

## Upload

Alla fine ho caricato ben 3332 foto nuove al mio archivio unico 🤩

```bash
Crawling for assets...
Hashing files           | ████████████████████████████████████████ | 100% | ETA: 0s | 6280/6280 assets
Checking for duplicates | ████████████████████████████████████████ | 100% | ETA: 0s | 6280/6280 assets
Found 3832 new files and 2448 duplicates
Uploading assets | ███████████████████████████████████░░░░░ | 87% | ETA: NFs | 15.7 GB/15.7 GB
Successfully uploaded 3332 new assets (13.8 GB)
Skipped 500 duplicate assets (1.9 GB)
```
