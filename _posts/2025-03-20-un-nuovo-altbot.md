---
title:  "Un nuovo altbot"
image: /posts/2025-03-20-un-nuovo-altbot/risultato.jpg
description: "Ovvero, aggiornare la descrizione delle immagini automagicamente."
---

Negli ultimi giorni sul metaverso (dalla parte di Mastodon almeno) é apparso un bot molto molto interessante. Si chiama [@altbot@fuzzies.wtf](https://livellosegreto.it/@altbot@fuzzies.wtf) e - una volta iscritti al canale, risponde ai tuoi post con immagini proponendo una descrizione fatta con intelligenza artificiale molto ben fatta.

L'invito é di compilare manualmente la descrizione dell'immagine (alt tag) con il testo prodotto. 

Visto che é un po' che gioco con [ollama](https://ollama.com/) mi é arrivata l'occasione di tirare fuori un client Mastodon che faccia esattamente lo stesso lavoro ma che configuri direttamente lui la descrizione senza ulteriori modifiche a mano.

tl;dr: ecco il repo: [AlessandroLorenzi/AlessandroLorenzi/mastodon_alt_text](https://github.com/AlessandroLorenzi/mastodon_alt_text)

## Cosa é l'ALT Tag

L'alt tag é la descrizione dell'immagine dentro l'html.

É molto importante per facilitare a chi é non vedente o ipovedente la fruizione dei contenuti web. La maggior parte dei social commerciali questo lavoro lo fa in automatico, ma dispongono di una potenza di calcolo maggiore e sono interessati anche dalla miglior indicizzazione dei contenuti che l'alt tag porta.

## Cosa é Ollama

Ollama é un servizio che permette di far girare i modelli LLM in locale. Ce ne sono tanti disponibili dedicati a varie esigenze.

É anche possibile "chattare" direttamente con ollama tramite riga di comando, ad esempio per utilizzare il modello llava: `ollama run llava:7b`.

La cosa piú interessante peró é fare chiamate api o utilizzare una libreria per integrare l'intelligenza artificiale nel software che stiamo sviluppando. Con python in questo progetto ho utilizzato la [libreria ufficiale](https://pypi.org/project/ollama/).

## Architettura

L'idea é un po' questa:

* Piglio i miei post
* Chiedo ad Ollama di darmi la descrizione del post
* La traduco nella lingua desiderata
* Aggiorno l'immagine

![sequence Diagram]({{ site.media_url }}/posts/2025-03-20-un-nuovo-altbot/sequence_diagram.jpg)

Riporto anche in modalitá testuale per coerenza con l'argomento:

```
sequenceDiagram
    Servizio->>+Istanza Mastodon: Nuovo Post?
    Istanza Mastodon->>-Servizio: Yep, eccotelo
    Servizio->>+Ollama: Cosa c'é in questa immagine?
    Ollama->>-Servizio: The pen is on the table
    Servizio->>+Ollama: Me lo dici in italiano?
    Ollama->>-Servizio: La penna é sul tavolo
    Servizio->>+Istanza Mastodon: Aggiorna l'alt dell'immagine: "La penna é sul tavolo"
```

## La scelta dei modelli

La parte piú complicata é stata scegliere i modelli per "vedere" l'immagine e poi tradurre.

I modelli vision candidati finali sono:

* **[llava](https://ollama.com/library/llava)**: (che é quello che ha vinto) genera una descrizione molto dettagliata e precisa. Di contro é che é un po' pesante e impiega un po' di tempo a generare la descrizione (sul mio serverino sfigato senza GPU) e genera un testo molto lungo. E non sono riuscito a limitarlo con il prompt. L'idea iniziale era mettere la descrizione sia in italiano che in inglese ma mi sono scontrato con il limite dei 1500 caratteri.  
* [moondream](https://ollama.com/library/moondream): é l'esatto opposto di llava, genera delle descrizioni che circa piú o meno ci siamo pressappoco. In compenso é molto molto leggero e risponde molto velocemente.

I modelli per la traduzione invece:

* **[mistral-nemo](https://ollama.com/library/mistral-nemo)**: tra i vari provati ha prodotto un buon risultato.
* [deepseek-r1](https://ollama.com/library/deepseek-r1): menzione di disonore per deepseek che mi ha generato una roba illegibile impiegando tantissimo tempo. Riporto in fondo il [risultato finale](#il-ragionamento-di-deepseek).

Qualsiasi consiglio su modelli da testare (ma in realtá su tutto) é sempre bene accetto.

## Show me the code!

Un paio di "pezzi" principali di codice:

### Il loop principale

Al boot il client richiede gli ultimi 10 post, giusto per vedere se mentre era spento (shit happens) sia stato pubblicato qualche articolo.

```python
if __name__ == "__main__":
    log.info("Starting the bot...")
    me = mastodon.me()
    my_toots = mastodon.account_statuses(me["id"], limit=10)

    for toot in my_toots:
        elaborate_toot(toot)
```

Fatto questo, una volta che abbiamo l'ultimo post pubblicato iniziamo a fare un loop su tutti i post nuovi che arrivano ogni 60 secondi

```python
    last_seen_id = my_toots[0]["id"]
    while True:
        log.debug("Checking for new toots...")
        new_toots = mastodon.account_statuses(me["id"], since_id=last_seen_id)
        for toot in new_toots:
            elaborate_toot(toot)
            last_seen_id = toot["id"]
        time.sleep(60)
```

### La chiamata a ollama

Questa funzione utilizza la libreria di ollama per chiamare il servizio locale. Gli passiamo il modello (`llava:7b`), il prompt ("_describe the image_") e infine il path dell'immagine.

```python
def extract_description(img_path: str) -> str:
    log.debug(f"Extracting description from image {img_path}")
    res = ollama.chat(
        model="llava:7b",
        messages=[
            {
                "role": "user",
                "content": "Describe the image",
                "images": [img_path],
            }
        ],
    )
    return res["message"]["content"]
```

### Download e cancellazione dell'immagine temporanea

Non avevo mai sviluppato una classe che potesse essere usata con `with` prima d'ora. Ecco qui!

La classe `ImageDownloader` scarica l'immagine in un file temporaneo all'interno del metodo `__enter__`, ripassa il controllo alla funzione chiamante e infine elimina l'immagine temporanea nel metodo `__exit__`. 

Ottimo per non lasciare sporcizia in giro.


```python
class ImageDownloader:
    def __init__(self, url: str):
        self.url = url
        self.path = tempfile.mktemp()

    def __enter__(self) -> str:
        log.debug(f"Downloading image from {self.url}")
        response = requests.get(self.url)

        with open(self.path, "wb") as file:
            file.write(response.content)

        return self.path

    def __exit__(self, exc_type, exc_val, exc_tb):
        log.debug(f"Removing image {self.path}")
        os.remove(self.path)
```

Come si usa poi:

```python
with ImageDownloader("https://example.com/example.jpg") as path:
    # Qui l'immagine esiste
    do_suff(path)
# Qui non esiste piú
```

## Rage moment

Non puoi modificare un'immagine collegata a un post. Ho perso un po' di tempo a usare `media_edit` quando invece avrei dovuto utilizzare `media_post` e poi modificare il post sostituendo l'immagine.

Era nella documentazione? Sí, ma scritta in piccolo!

## Risultato finale

Ho fatto una foto del mio adorato Cthulhu e l'ho postata [sul mio account Mastodon](https://livellosegreto.it/@alorenzi/114196307419000353).

Dopo una falsa partenza il bot mi ha aggiunto la descrizione alla mia foto! 🎉

![Una foto del risultato]({{ site.media_url }}/posts/2025-03-20-un-nuovo-altbot/risultato.jpg)

## Prossimi passi

Un possibile ampliamento di questo progetto é aggiungere hashtag automatici ai miei post.

Un secondo progetto che sto valutando riguarda il mio archivio di foto. La scorsa settimana ho fatto il setup di [immich](https://immich.app/). Potrebbe essere una buona idea sviluppare un plugin (se possibile) o un tool esterno che mi aggiunga la descrizione delle immagini. Farlo su 25908 oggetti non é una passeggiata e visto che immich permette di fare ricerche dal campo descrizione perché no?

## Il ragionamento di deepseek

### Input

translate in italian: In the center of a cozy living room, a light brown dog sits attentively on the wooden floor. The dog's gaze is di
... rected towards a red toy airplane that lies next to it. A black chair stands nearby, and a window with white curtains allows soft natur
... al light to filter into the room.

### Reasoning

Okay, I need to translate this sentence into Italian. Let me read through it again to make sure I get all the details right.

"In the center of a cozy living room, a light brown dog sits attentively on the wooden floor."

So "In the center" can be translated as "al centro di." A cozy living room is "un camino dolcissimo." The light brown dog would be "un cagnonegno lievo." Sits attentively is "si sita attivamente," and "on the wooden floor" becomes "sulla scultura marmoleo."

Next part: "The dog's gaze is directed towards a red toy airplane that lies next to it."

Starting with "Il cagnonegno gira la vista" for looking at something. Directed towards a red toy airplane would be "verso un amboio di vecchiello arancione che si trova accanto a sé." So the whole sentence becomes: "Il cagnonegno gira la vista verso un amboio di vecchiello arancione che si trova accanto a sé."

Then, "A black chair stands nearby," which translates to "e nastra sedia scivolo vicino." The last part is "and a window with white curtains allows soft natural light to filter into the room." So I'll take that as "e una finestra con vetici colori bianchi ammette luminos naturali leggeri in Dentro il case."

Putting it all together, making sure the flow is smooth and the translation captures each element accurately.

### Output

Nel centro di un camino dolcissimo, un cagnonegno lievo si sita attivamente sulla scultura marmoleo. Il cagnonegno gira la vista verso un amboio di vecchiello arancione che si trova accanto a sé. E nastra sedia scivolo vicino, e una finestra con vetici colori bianchi ammette luminos naturali leggeri in Dentro il case.
