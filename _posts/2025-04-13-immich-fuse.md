---
title: Immich-FUSE
description: Un progettino per montare immich come filesystem
image: /posts/2025-04-13-immich-fuse/graph.jpg
---

tl;dr: ho creato un filesystem in userspace (FUSE) per montare le immagini di Immich in una directory locale. [Questo é il repo](https://github.com/AlessandroLorenzi/immich-fuse).

Sto usando Immich da un mese, ho spostato lì tutti i miei archivi ([Google Photos](https://alorenzi.eu/2025/03/31/sistemato-metadati-foto-google-takeout.html), foto di Shotwell, backup vari) e penso che sia un software fantastico.

C'è solo un problema: rompe il mio solito flusso di lavoro di editing delle foto che avevo con Shotwell: scaricare tutte le foto dalla fotocamera su Shotwell -> rivedere le foto più interessanti dello shooting -> modificare con GIMP/Darktable/qualsiasi altro software -> profit.

Ora, con Immich, utilizzo il comando `immich upload -r /var/media/[....]/DCIM` per caricare le immagini sul server, ed è persino più comodo rispetto a Shotwell che ogni tanto si imballava. MA ora devo scaricare le immagini per modificarle.

L'idea è: perché non montare Immich direttamente in una directory locale?

![Grafico che spiega la mia idea]({{ site.media_url }}/posts/2025-04-13-immich-fuse/graph.jpg)

Questo progetto è un Proof of Concept (POC), è in sola lettura, ma funziona! È possibile sfogliare le immagini di Immich per data, solo preferiti e cercando persone taggate.

Peró funziona, questo é uno screenshot di Nautilus che mostra le foto di Immich:

![screen delle foto in nautilus]({{ site.media_url }}/posts/2025-04-13-immich-fuse/nautilus.jpg)


Nel [README](https://github.com/AlessandroLorenzi/immich-fuse) ci sono più dettagli implementativi.

In futuro mi piacerebbe implementare una sorta di caricamento diretto. Ad esempio, salvando un'immagine da GIMP, questa verrebbe caricata automaticamente su Immich.

