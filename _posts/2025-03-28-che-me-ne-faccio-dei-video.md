---
title:  "Che me ne faccio dei video?"
image: /posts/2025-03-28-che-me-ne-faccio-dei-video/server_stats.jpg
description: "Uno script per comprimere tutti i video e mandarli a immich"
---

Nelle ultime settimane sto risistemando tutte le foto e i video che ho in giro e sto caricando tutto su immich, un servizio self-hosted che rimpiazza Google Photos.

Visto che dei video in alta qualità non me ne faccio assolutamente nulla, e anzi ne sto eliminando un po', ho deciso di comprimerli tutti in locale e poi caricarli sul mio serverino.

È vero che immich stesso fa una compressione all'upload, ma il serverino stesso è piccolino, poco potente e impiegherebbe più tempo. Inoltre, la conversione avverrebbe dopo l'upload, e anche i tempi di upload si allungherebbero inutilmente.

E poi è possibile usare questo script anche per altri archivi, non necessariamente per immich.

## I requisiti

- Devo comprimere i video in modo da risparmiare spazio
- Posso lanciare il comando più volte e, se già esiste il video compresso, vado avanti
- Voglio che ci sia una verifica del file compresso
    - nei test mi sono capitati dei file fallati
- Il file compresso deve avere gli stessi metadata del sorgente
- al primo upload su immich avevano tutti la data del giorno in cui ho fatto l’upload, mancando i metadati di quando sono stati girati

## Try this at home, ma con calma

⚠️ Testate il funzionamento in una directory con qualche video di test e/o abbiate i backup prima di fare qualsiasi cosa

### **Lo script**

La funzione si genera un nome file del nome esistente, ad esempio `example.ext` → `example_compressed.mp4`.

Poi controlla se il file di destinazione esiste e se è valido utilizzando [`ffprobe`](https://ffmpeg.org/ffprobe.html).

Infine utilizza ffmpeg per generare il video finale.

Utilizzo `find` per cercare tutte le estensioni video che mi vengono in mente ed eseguire la funzione compress.

```bash
#!/usr/bin/bash
set -euo pipefail

compress () {
    ORIGIN=$1
    FILENAME=$(basename "$ORIGIN")
    OUTPUT_FILE="$(dirname "$ORIGIN")/${FILENAME%.*}_compressed.mp4"

    echo "☑️ Task TODO: $ORIGIN -> $OUTPUT_FILE"

    # Check if destination already exists and is corrupted
    if [ -f "$OUTPUT_FILE" ]; then
        if ffprobe -v error -i "$OUTPUT_FILE"; then
            echo "✅ Task completed: $OUTPUT_FILE already exists" 
            return
        fi
        echo "⚠️  File corrupted, removing and recreating: $OUTPUT_FILE"
        rm "$OUTPUT_FILE"
    fi

    # Compress at 720p, 30fps, H.265 video coding
    ffmpeg -i "$ORIGIN" -map_metadata 0 -movflags use_metadata_tags -vf "scale=-2:720,fps=30" -c:v libx265 -crf 28 -preset slow -c:a aac -b:a 128k "$OUTPUT_FILE" 
    echo "✅ Task completed: $OUTPUT_FILE done"
}

export -f compress

find . -type f -name "*.MP4" -exec bash -c 'compress "$0"' '{}' \;
find . -type f -name "*.MOV" -exec bash -c 'compress "$0"' '{}' \;
find . -type f -name "*.MTS" -exec bash -c 'compress "$0"' '{}' \;
find . -type f -name "*.mp4" ! -name "*_compressed.mp4" -exec bash -c 'compress "$0"' '{}' \;
```

### Decluttering digitale

Facciamo qualche prova random, testiamo che tutti i video siano felicemente compressi e possiamo gettare il cuore oltre l’ostacolo: eliminiamo tutti i video vecchi.

```bash
find . -type f -name "*.MP4" -delete
# tutte le estensioni video che avete in mente
find . -type f -name "*.mp4" ! -name "*_compressed.mp4" -delete
```

Come nello script sopra dobbiamo distinguere gli  `*.mp4` originali da quelli compressi. Nei due esempi usiamo il punto esclamativo (`! -name “*_compressed.mp4`) per escludere le foto compresse.

### Mass import

Bene ora che abbiamo il nostro archivio molto piú leggero possiamo fare l’upload di tutto.

Usiamo [immich-cli](https://immich.app/docs/features/command-line-interface/) per fare l’upload di massa. Non é necessario essere sulla stessa macchina di immich per usare la cli, ci basta installarla sulla macchina in cui ci sono le foto(`npm i -g @immich/cli` ) e fare login (`immich login https://photos.example.com key-from-account-settings`). 

```bash
immich upload . -r
```

## That’s it

Adesso potete decidere cosa farne di foto volanti e backup vari.

Io sto tenendo immich come servizio primario, ho dismesso shotwell dopo 10+ anni e relativi backup e faccio backup di immich.

<a data-fslightbox href="{{ site.media_url }}/posts/2025-03-28-che-me-ne-faccio-dei-video/server_stats.jpg">
![Schermata delle statistiche]({{ site.media_url }}/posts/2025-03-28-che-me-ne-faccio-dei-video/server_stats.jpg)
</a>