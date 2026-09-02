---
title: Cloud vs In House
description: Il viaggio di due aziende tra cloud e server personali
image: /posts/2025-04-15-cloud-vs-in-house/meme.jpg
---

Sto scrivendo un altro articolo che mi sta uscendo un rant lunghissimo. Visto che ci sto mettendo tre giorni causa deficit visivo (chi mi conosce sa), ho deciso di staccare e ampliare questo pezzo di storia.

Parliamo di **Cloud**, quella cosa che gli europei non riescono proprio a fare. 

I tre maggiori cloud provider sono americani (*AWS*, *GCP*, *Azure*); gli altri hanno numeri irrilevanti. Forse spicca la cinese *Alibaba* ma più per motivazioni politiche che tecnologiche.

In **Europa** tutto tace, le grosse aziende sono piú orientate all'*hosting web* e di *macchine virtuali* che ai servizi cloud e si muovono alla rinfusa. Ogni tanto escono notizie che mi fanno ben sperare ([il cloud della LIDL](https://www.wired.it/article/lidl-cloud-schwarz-digit/), [gaia x](https://www.gaiax-italia.eu/cosa-facciamo)) ma nella relata non vedo una corsa alla cloudizzazione europea.  
Nemmeno le varie [**sentenze Shrems**](https://it.wikipedia.org/wiki/Sentenze_Schrems) hanno mai scosso le coscienze delle aziende verso il passaggio all'autarchia europea del cloud. 
## Ma il cloud serve davvero?

Ultimamente mi sto facendo spesso questa domanda.

Vengo da un background di **sistemista unix**, il mio primo lavoro é stato su macchine [Solaris](https://en.wikipedia.org/wiki/Oracle_Solaris) e [HP-UX](https://en.wikipedia.org/wiki/HP-UX), ho seguito tutte le evoluzioni del ruolo e ad oggi lavoro principalmente su AWS come **platform engineer**.

Ho sempre avuto un server personale, prima un "server" in casa (un vecchio computer con la ventola costantemente accesa fuori dalla porta della camera da letto), poi una vps, e oggi sono tornato ad ospitare un mini-pc fanless in casa.

Un paio di anni fa ho iniziato ad **abbattere i costi** del cloud nella mia azienda. Mi sono accorto di quanti sprechi avevamo e - nonostante il lavoro fatto - ancora oggi ci sono costi intrinsechi non eliminabili.
Ho quindi pensato a quanto ci costerebbe oggi l'infrastruttura se fossero state fatte scelte diverse e a quali sarebbero i costi di una migrazione.

![Meme Left Exit 12 Off Ramp. Testo 1: "Cloud", Testo 2 "In House"]({{ site.media_url }}/posts/2025-04-15-cloud-vs-in-house/meme.jpg)

## Il viaggio di Alpha e Sigma

Per questo viaggio  prenderemo ad esempio le aziende Alpha e Sigma. Entrambe vogliono "andare veloce" ma in modi diversi.

L'azienda **Alpha** é all'avanguardia, va sul cloud, scrive microservizi che fa girare su kubernetes gestito, il database gestito, e magari fa anche il vibe coding. 

L'azienda **Sigma** invece sceglie una via minimalista: un servizio monolite, un database e poco altro.

⚠️ queste due aziende sono un il mischione di decine di aziende per le quali ho lavorato direttamente o in consulenza. Spero che nessun (ex)collega si ritrovi pienamente in nessuna delle due.

### Fase 1: startup

In questa fase le aziende vogliono validare la propria idea, aprirsi al mercato e gettare le basi dell'impero economico che ne nascerà.

In **Alpha** gli sviluppatori vanno su microservizi e AWS: EKS, RDS, S3, VPC, GW e qualche altra sigla.

In locale ogni sviluppatore crea il proprio microservizio isolato. Inizia a scrivere con il proprio linguaggio di programmazione preferito sul framework preferito. Lo fa girare in locale con docker compose e fa deploy su kubernetes. Poche persone full-stack che iniziano a tirare su il proprio pezzo di [dominio](https://en.wikipedia.org/wiki/Domain-driven_design), fare meeting per decidere come interfacciare i pezzi e incastrare i pezzi del puzzle. 

In **Sigma** si sviluppa sullo stesso monolite in sessioni di pair o mud programming. Ognuno installa il database sul proprio computer ed esegue il monolite, si prende una VPS su hetzner e si installa il database e l'applicativo esattamente come gira sulla propria macchina di sviluppo.  

#### I costi

Per **Alpha** calcolo un eks, rds, un po' di nodi kubernetes, il gateway per la vpc privata, siamo tra i 200$ e i 300$ mensili.

**Sigma** fa girare tutto su una macchina hetzner CPX31, 13.60€ mensili.

### Fase 2: Scale up

La startup é diventata **scale up**! L'idea funziona, ha preso fondi dagli investitori, si cresce, si assumono piú persone. 

In **Alpha** creano team specializzati (hanno letto [team topology](https://www.instagram.com/p/CP-9cVjghmU/)), hanno sempre piú microservizi da gestire perché ogni funzionalità del sistema ha un microservizio, aumentano i nodi del cluster kubernetes. I microservizi sono tanti, non é facilmente ricreabile localmente l'ambiente di sviluppo per intero quindi anche i cluster diventano due, viene aggiunto un ambiente di test con cui interfacciarsi durante lo sviluppo del microservizio. 
In seguito si crea anche uno di staging dove poter testare tutto in un ambiente un po' piú stabile prima di mandare in produzione.

In pratica bisogna **triplicare l'aumento** delle risorse richiesto ad ogni sviluppo fatto.

Nel frattempo si accumula debito tecnico, alcuni servizi non sono piú toccati da mesi. Molti hanno versioni del framework vecchi, non aggiornati con patch di sicurezza non applicate, altri sono scritti in linguaggi di programmazione che piacevano tanto a qualche sviluppatore che ora lavora in altre aziende e ora non c'é piú nessuno che li padroneggia.

In **Sigma** si continua a lavorare in maniera minimale e pulita. Vengono assunte persone che conoscono quel linguaggio di programmazione e quel framework o che sono interessati a studiarli. Tutti sono in grado di mettere mano a quel codice, viene mantenuto e aggiornato perché é piú facile mantenere un singolo servizio. Anche quando viene diviso il servizio in sito pubblico e backoffice si mantengono le stesse tecnologie.

Il software non dovendo fare chiamate ad altri microservizi é veloce e non avendo overhead per ogni servizio é anche efficiente in termini di memoria. Quindi gli sviluppatori continuano a poter eseguire "*tutta l'azienda*" sul proprio computer, non servono particolari ambienti di sviluppo.

Per scalare l'infrastruttura di produzione si decide nel tempo di mettere il database su un VPS separato, di scalare verticalmente prendendo una macchina virtuale piú grossa per il servizio e alla fine di scalare orizzontalmente prendendo tre macchine virtuali piú una piccola macchina varnish che fa da server proxy e cache.

Database e le immagini vengono backuppate ad ogni ora sul nas aziendale (il primo pezzo di hardware acquistato) e settimanalmente viene fatto uno snapshot di tutto su un disco cifrato tenuto offline in una sede diversa.

Per il disaster recovery viene realizzato un sito statico su un diverso provider su cui puntare i dns in caso di problemi seri. Gli utenti non possono acquistare i servizi direttamente ma possono esplorare il catalogo e fare ordini via mail. 

#### I costi

**Alpha** quindi ormai avrà tre cluster kubernetes, tre cluster postgres, tutto in reti isolate e qualche bucket s3. Spannometricamente spenderemo 10k$/mo per produzione e 5k$ a testa per dev e staging, arrotondiamo 250k$/anno su AWS.

Invece **Sigma** utilizza ben 6 macchine CPX41 per prodotto e database e una CPX31, per un totale di 158€. Arrotondiamo a 200€ mensili su hetzner includendo anche storage aggiuntivo e 1000€ per un qnap e dischi. 3400€ all'anno, fiscalmente 2.6k ammortizzando l'hardware.

### Fase 3: La maturità

Siamo arrivati al famoso break even point, il punto in cui i profitti superano i costi, iniziamo a fare i big money.

Come sta il nostro reparto tech?

**Alpha** usa tutti i servizi che AWS propone, salvo poi non ricordarsi per quale motivo un servizio é acceso, intanto il billing aumenta.

**Sigma** si é mantenuta ai principi fondamentali. Vengono adottate nuove tecnologie solo se rispondono a precise esigenze non coperte da tecnologie giá adottate e per ognuna si calcola i costi di mantenimento sul lungo periodo. Il team rimane piccolo e focalizzato sullo sviluppo di  un prodotto solido.
L'infrastruttura passa al ferro. Con tre server "carrozzati" in colocation e un sistema di virtualizzazione il servizio é stabile. L'acquisto dei server é stato visto non come un costo ma come investimento e il canone della colocation é contenuto rispetto ai costi che avevano prima sul provider (i nodi con GPU iniziavano a costare parecchio).

Non sto piú nemmeno a calcolare **i costi** che possono avere in questa fase le aziende. Ci sono aziende che hanno billing milionari sul cloud e altre che costruiscono interi datacenter, e altri ancora che hanno un rack nello sgabuzzino.

## Conclusioni

Sicuramente sto passando in un momento di **disillusione** del cloud, ci sono aspetti **positivi** che ho tralasciato, ad esempio le availability zone sono una cosa stupenda per l'uptime, e amplificato aspetti **negativi** che non sono propri del "cloud" in quanto tale ma conseguenza di scelte di design che comunque il cloud non ostacola. 

D'altra parte forse sto dimenticando i **dolori del giovane sistemista**: le repliche postgres che si de-sincronizzano e bisogna ricreare, l'aggiornamento delle macchine, le sudate fredde quando il riavvio impiega piú di 30 secondi.

Non so dove mi porterà il futuro, gli scenari aperti dalle nuove tecnologie e come io le accoglierò. Come dico ogni tanto, il ruolo che ho ora non esisteva nemmeno quando mi sono laureato, per non parlare di quando ho scritto la prima riga in GW Basic a fine anni 90; chissà cosa farò da grande.
