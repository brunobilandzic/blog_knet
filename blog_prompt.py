

prompt = """ZADATAK
Napiši opširan HTML blog post na hrvatskom jeziku na temu {self.theme}. Možeš prilagoditi fokus teme ciljanoj publici.

JEZIK I STIL

 Piši prirodnim hrvatskim (hr-HR), informativno i angažirano.
 Bez fraza tipa “u ovom poglavlju ćemo…”. Nikad ne obećavaj sadržaj koji ne isporučiš.
 Ne koristi riječi “poglavlje”, “tema”, “opis”, “podtema” u naslovima. Naslove piši kao u pravom blogu.
 Uključi bogat vokabular i duge, SEO-prijateljske rečenice, ali bez “keyword stuffing”-a.

STRUKTURA HTML-a (SAMO `<body>`!)
Ispiši isključivo element `<body>…</body>` bez `<html>`, `<head>`, `<title>`, CSS-a ili JS-a.

Unutar `<body>` koristi semantički HTML ovim redoslijedom:

1. <h1> – glavni naslov članka (privlačan, SEO-orijentiran).
2. Uvodni odlomak (sažeto postavite kontekst i vrijednost za čitatelja).
3. Opis bloga (dopunite i prilagodite publici ako postoji; inače za širu publiku) – jedan ili dva odlomka odmah ispod naslova.
4. Ciljana publika: Cijeli blog post mora biti izričito namijenjen publici {self.audience}; prilagodite ton, razinu detalja, primjere i terminologiju toj publici. Ako {self.audience} nije zadano, pišite za širu publiku.
5. Glavna tijela članka u sekcijama:
   - Za svaku temu iz {chapters_str} koristite <h2> za naziv sekcije (naslov možete promijeniti ako postoji prikladnija varijanta).
   - Ispod <h2> napišite opis sekcije (možete ga nadopuniti i prilagoditi publici).
   - Ako sekcija ima podpoglede, za svaki koristite <h3> i ispod njega sadržaj.
   - Svaki (pod)odjeljak mora imati najmanje 5 potpunih rečenica.
   - Dodajte dodatne sekcije ako doprinose jasnoći i potpunosti teme.
6. Zaključak s jasnim “takeaways” (ključni savjeti / koraci).


DULJINA
   750 riječi (više je poželjno ako je relevantno).

SEO ZAHTJEVI

 U tekstu prirodno koristi sinonime i long-tail fraze relevantne za {self.theme}.
 Uključi unutarnje mikro-FAQ odjeljak (2–4 česta pitanja s odgovorima po 3–5 rečenica) ako je prikladno.
 Ne izmišljaj resurse ni reference; ako ih spominješ, sadržaj zaista mora biti prisutan u članku.

SLIKE (OBAVEZNO)

 U svakoj većoj sekciji dodaj barem jednu relevantnu sliku.
 Format slike mora biti točno kao u primjeru {img_example} – zadrži isti hostname i path, zamijeni samo opis slike temom slike.
 Za svaku sliku koristi `<figure>`, unutar nje `<img>` i `<figcaption>`.
 U `<img>` obavezno stavi `alt` i `title` atribute s deskriptivnim, SEO-prijateljskim tekstom.
 Slike moraju biti konkretno vezane uz sekciju u kojoj se nalaze.

KVALITETA I ISTINITOST

 Ne ostavljaj prazne ili generičke odlomke; svaki mora dodati novu vrijednost.
 Ne obećavaj vodiče ili popise koje ne isporučiš. Ako nešto spomeneš, napiši.
 Izbjegavaj floskule i općenitosti – koristi praktične savjete, primjere i jasno objašnjenje “zašto” i “kako”.

IZLAZNI FORMAT (STROGO SE DRŽI REDOSLIJEDA)

1. Prvo ispiši kompletan HTML sadržaj isključivo u `<body>…</body>`.
2. Nakon `</body>` ispiši tri SEO linije bez ikakvih tagova ili dodatnog markup-a, točno ovim formatom (jedna stavka po liniji):

```
title - <meta title>
description - <meta description>
keywords - <meta keywords>
```

3. Također nakon `</body>`, ispiši sljedeće blokove teksta, bez HTML tagova i bez dodatnog markup-a, redom:

 Proizvodi (prijedlozi za kupnju): navedite 5–10 relevantnih proizvoda povezanih s temom članka. Za svaki proizvod u jednoj liniji upiši:
  `Naziv: …; Kratki opis: …; Za koga/što: …`
  (bez izmišljanja brendova; opisi i namjena moraju logično proizlaziti iz članka)
 Opisi slika (za lakše nalaženje na internetu): za svaku sliku korištenu u članku, u jednoj liniji upiši opis koji precizno opisuje sadržaj slike i kontekst sekcije (npr. “noževi od nehrđajućeg čelika za precizno sjeckanje luka – priprema mirepoixa”). Počni s: `Slika 1: …`, `Slika 2: …`, redom.

DODATNE NAPOMENE

 Ako je ciljna publika specificirana, ton i primjeri prilagodi njima; inače piši za širu publiku.
 Ako teme iz {chapters_str} nisu dovoljno sveobuhvatne, smiješ ih izmijeniti ili dodati nove da članak bude potpun.
 Ne uključuj nikakve napomene o tome da si AI ili kako generiraš sadržaj.
 Ne uključuj ništa osim traženog: `<body>…</body>`, zatim SEO linije, zatim blok s proizvodima, pa blok s opisima slika.

ULAZNI PODACI

 Tema: {self.theme}
 Opis bloga (dopuni i prilagodi publici): {self.blog_description}
 Predložene sekcije i podpoglavlja: {chapters_str}
 Primjer formata slike: {img_example}

"""
