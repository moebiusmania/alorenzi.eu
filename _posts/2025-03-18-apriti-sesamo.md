---
title:  "Apriti Sesamo"
image: /posts/2025-03-18-apriti-sesamo/schema.jpg
description: "Ovvero, come fa il cancello di casa ad aprirsi quando torno dalla passeggiata."
---

Da quando ho la cana faccio avanti e indietro casa per passeggiare almeno quattro volte al giorno: la mattina appena svegli, pausa caffè, pranzo, post lavoro, prima di nanna. Non tutti sempre, ma insomma, mi piace sgranchirmi le gambe di tanto in tanto.

E ogni volta che ritorno a casa parte la ricerca le chiavi nelle tasche dei pantaloni, giacca, felpa, zaino. Tutto questo con il guinzaglio in mano. Il telefono invece chissà perché so sempre dove sta.

## Domotizziamo cancelletto e portoncino

Un po' di tempo fa ho preso un oggettino che si attacca al citofono, si collega al wifi e con l'app apri da dove ti pare. Cosí mentre cammino ho tutto il tempo di cercare il telefono e trovarmi con cancello e portoncino aperto. 

Siamo nel 3000, circa.

L'app e il widget sono carucci, non sempre peró super reattivi. Ogni tanto se tento di aprire dal widget si blocca, dice che non puó raggiungere il dispositivo, poi apri l'app, ci mette un po' a svegliarsi e va tutto.

## Piú automazione!

L'altro giorno mi é venuta questa idea, ma se si aprisse in automatico quando mi avvicino?

![schema]({{ site.media_url }}/posts/2025-03-18-apriti-sesamo/schema.jpg)

> Si puó fare!

Ho reinstallato HomeAssistant dopo molti molti anni che non lo usavo, ho importato tutti gli aggegi domocosi vari che ho in casa e installato l'app sul telefono.

Da qui é stato abbastanza semplice configurare un trigger:

* When: il mio telefono entra in zona "Casa"
* And if: (niente)
* Then do: premi il bottone di ingresso

![schema]({{ site.media_url }}/posts/2025-03-18-apriti-sesamo/screenshot.jpg)

## Come sta andando

Per sicurezza ho attivato le notifiche dell'app di quando si apre il cancello. Nel giro di tre giorni non ho avuto né falsi positivi né falsi negativi.

* Non mi ha mai aperto il cancello "a caso", se non ha la posizione gps e poi la ritrova passa da stato "unknown" a localizzato, ma non apre il cancello. E questa era la cosa piú critica.
* Arrivato davanti casa il cancello era sempre aperto.

Installeró un aggeggio simile anche per la porta di casa? Per ora non penso, finché é il cancelletto e il portone ci pensano giá i miei vicini a lasciarli aperti a caso, quindi un'apertura accidentale non sarebbe grave. Ma per la porta di casa ho qualche remora in piú.

Sono decisamente soddisfatto della cosa.
