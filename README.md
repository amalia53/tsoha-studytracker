# Study Tracker

Study Tracker on opintojen suunnittelua ja seuraamista helpottava sovellus. 

Sovelluksessa opiskelija voi lisätä ja seurata eri kursseihin käytettyä aikaa. 
Lisäksi opiskelija voi asettaa tavoitteita ja seurata tavoitteissa pysymistä. Opiskelija voi myös nähdä kurssin suoritettuaan saamansa arvosanan kurssista.

Sovelluksessa voi tarkastella kaikkia kursseja ja nähdä kaikkien opiskelijoiden kurssin opiskeluun käytetyn ajan keskiarvon. 

Sovellukseen voi kirjautua myös opettajana ja lisätä opiskelijoilleen arvosanat. Lisäksi opettaja näkee omista opetetuista kursseistaan käytetyn ajan ja arvosanojen keskiarvon.

## Sovelluksen käyttö

Pääset käyttämään sovellusta osoitteesta [https://tsoha-studytracker.herokuapp.com/](https://tsoha-studytracker.herokuapp.com/)

### Etusivu

Etusivulla esitellään sovelluksen toiminta ja voidaan kirjautua palveluun. Lisäksi löytyy linkki opiskelijan ja opettajan rekisteröitymiseen. 

Mikäli käyttäjä on rekisteröitynyt, hän voi kirjautua käyttäjätunnuksellaan ja salasanalla sovellukseen.

## Opiskelija

### Rekisteröityminen

Uusi opiskelija voi luoda tunnuksen antamalla uuden käyttäjätunnuksen, salasanan ja saman salasanan uudestaan. Käyttäjätunnus täytyy olla
uniikki, tähän sopii hyvin esimerkiksi opiskelijanumero.

### Oma sivu

Kirjautumisen jälkeen opiskelija näkee oman sivun, jossa näkee käynnissä olevat kurssinsa ja kursille käytetyn ajan ja paljonko saavutettu tavoitteesta prosentteina.
Lisäksi sivulta löytyy valikko, josta voi siirtyä sivuille: "opiskele", "suunnittele", "tilastot" ja "kurssit. Valikosta voi möys kirjautua ulos.

### Opiskele

Lisää kurssien opiskeluihin käytettyä aikaa tunteina.

### Suunnittele

Lisää uusi kurssi ja sille opiskelutavoite, muokkaa suunnitelmaa tai merkitse käymäsi kurssi suoritetuksi.Lisäksi kurssin voi poistaa käynnissä olevista kursseista

### Tilastot

Kurssikohtaiset tilastot opiskelijan kaikista kursseista, myös suoritetuista. Arvosana näkyy täällä, kun kurssi on suoritettu ja arvosteltu opettajan toimesta.

### Kurssit

Lista kaikista sovelluksessa olevista kursseista ja opiskelija voi lisätä kurssin listaan. Mikäli opiskelija lisää kurssin, kurssille ei merkitä opettajaa.

## Opettaja

### Rekisteröityminen

Opettajan tarvitsee antaa rekisteröityäkseen uniikki käyttäjätunnus, kursseissa näkyvä opettajan nimi, uusi salasana, sama salasana uudestaan ja vain opettajien tiedossa oleva koodi.

**Opettajan rekisteröitymistä varten koodi on 4278**

### Oma sivu

Sivulla näkyy opetettavat kurssit ja valikko, josta voi siirtyä sivuille: "arvostele", "tilastot" ja "kurssit". Valikosta voi myös kirjautua ulos.

### Arvostele

Lisää arvosanat opiskelijoille kurssista.

### Tilastot

Opettajan kurssien keskiarvoiset opiskelutuntimäärät ja arvosanat.

### Kurssit

Lista kaikista sovelluksessa olevista kursseista ja opettaja voi lisätä oman kurssinsa listaan. Mikäli opettaja lisää kurssin, kurssille merkitään automaattisesti lisännyt opettaja opettajaksi.

## Jatkokehitysideoita

Opiskelutavoitteita voisi tehdä eri ajanjaksoille ja opiskelusessioihin merkattaisiin päivämäärä.
