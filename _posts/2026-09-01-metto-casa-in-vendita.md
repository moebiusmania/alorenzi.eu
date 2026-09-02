---
title: Metto casa in vendita!
description: Vendo il trilocale di Viale Sicilia 4 a Busto Arsizio, e ovviamente mi sono fatto il sito da solo
image: /immobili/viale-sicilia/carosello/esterno-IMG_20260824_143244466_HDR.jpg
---

Dopo 39 anni passati a Busto Arsizio è arrivato il momento di cambiare aria!

**Metto in casa in vendita!!!**

## L'annuncio

Trilocale di 83 mq, cucina a vista, due camere (di cui una é lo studio da cui lavoro e mi diletto a suonare), box auto e cantina. Se cercate casa a Busto Arsizio zona San Michele, o conoscete qualcuno che la cerca, questo è il posto giusto per guardare tutto nel dettaglio:

👉 **[Casa in Vendita - Viale Sicilia 4](/viale-sicilia.html)**

Ci ho messo dentro anche un **[virtual tour](/viale-sicilia-virtual-tour.html)** navigabile stanza per stanza.

## Il making-of

### Le foto

Il primo tentativo l'ho fatto sul serio: Sony Alpha 7 II, obiettivo grandangolare 7Artisans, treppiede robusto. Ci ho messo un'eternità a studiare ogni inquadratura stanza per stanza, e alla fine le foto non erano granché - complice anche un obiettivo tutt'altro che eccelso.

Nel frattempo, per il virtual tour, stavo già girando casa con la Osmo 360 montata su un mini treppiede Manfrotto e un'asta telescopica: bastava piazzarla nel punto giusto e spostarla da una stanza all'altra in pochi secondi, molto più agile di rincorrere l'inquadratura perfetta con la reflex.

A un certo punto mi sono chiesto perché mai stessi portandomi dietro due macchine fotografiche quando una faceva già il lavoro sporco. Ho ricominciato da capo usando solo la Osmo 360: stessi punti strategici per il tour, più qualche scatto in più nelle posizioni dove volevo anche una foto "normale". Dall'app sul telefono ho poi esportato i singoli fotogrammi 2D, scegliendo con calma l'inquadratura a schermo invece che a occhio nudo in stanza. Risultato: foto molto più convincenti, con la metà della fatica.

### Il sito

Il sito con foto e tour lo ho prototipizzato come pagina statica a sé stante, poi integrarto qui su alorenzi.eu invece di tenerlo su un dominio separato: un layout [Jekyll](https://jekyllrb.com/) (`immobile`) legge tutti i dati — prezzo, caratteristiche, foto, coordinate del tour - da un unico file YAML in `_data/`, e lo stesso file alimenta anche la pagina del tour a schermo intero. Foto e panorami sono su git-lfs, come il resto dei media del sito.

### Il virtual tour

Avendo lavorato su [realisti.co](https://realisti.co/) (poi acquisita da [Floorfy](https://floorfy.com/)) sapevo che un virtual tour avrebbe fatto la differenza rispetto al solito annuncio con quattro foto in croce, quindi volevo assolutamente aggiungerlo.

Con [pannellum](https://pannellum.org/) è stato tutto piuttosto semplice: gli passi le foto panoramiche e definisci gli hotspot che collegano una scena all'altra, cioè i punti cliccabili nell'inquadratura che ti spostano da una stanza alla successiva. La parte noiosa era trovare le coordinate giuste (yaw e pitch) per posizionare quegli hotspot esattamente sopra la porta o il corridoio che dovevano rappresentare: all'inizio andavo a tentativi dalla console di debug del browser, leggendo a mano i valori con `tourViewer.getYaw()` e `getPitch()`.

Poi mi sono stancato e ho aggiunto una modalità debug: aggiungendo `#debug` all'URL del tour compare un overlay con yaw, pitch e hfov aggiornati in tempo reale, più un mirino al centro dello schermo per allineare l'hotspot mentre giro la vista. Da lì in poi posizionare i collegamenti tra le stanze è diventato questione di minuti invece che di tentativi random.

## Conclusione

Mettere in ordine casa, ripulirla da cima a fondo, sistemare quelle cosette un po' tralasciate, vedere le foto fatte bene della casa... tutto questo lavoro mi ha ricollegato un po' a queste mura e già so che mi mancherà. Un po' come un senso di nostalgia in anticipo per una casa che mi ha visto crescere quando c'era nonna, che poi ho acquistato grazie all'aiuto della mia famiglia, ristrutturato e vissuto per quasi 10 anni.

Se avete letto fin qui solo per il retroscena tecnico e non per comprare casa, yay! Ma se conoscete qualcuno interessato, fatemi un fischio: **me@alorenzi.eu**.
