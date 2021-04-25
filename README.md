# Study Tracker

Study Tracker on opintojen suunnittelua ja seuraamista helpottava sovellus. 

Sovelluksessa opiskelija voi lisätä ja seurata eri kursseihin käytettyä aikaa. 
Lisäksi opiskelija voi asettaa tavoitteita ja seurata tavoitteissa pysymistä. Opiskelija voi myös nähdä kurssin suoritettuaan saamansa arvosanan kurssista.

Sovelluksessa voi tarkastella kaikkia kursseja ja nähdä kaikkien opiskelijoiden kurssin opiskeluun käytetyn ajan keskiarvon. 

Sovellukseen voi kirjautua myös opettajana ja lisätä opiskelijoilleen arvosanat. Lisäksi opettaja näkee omista opetetuista kursseistaan käytetyn ajan ja arvosanojen keskiarvon.

**Herokussa olevassa versiossa voi tällä hetkellä rekisteröityä ja kirjautua opiskelijana ja opettajana. Opiskelija voi selata ja lisätä kursseja sovellukseen, valita kursseja opiskeltavaksi, suunnnitella kurssin opiskeluun käytettävän ajan ja lisätä opiskeltuja tunteja. Lisäksi opiskelija voi muokata suunnitelmaa tai merkitä kurssin suoritetuksi. Opettaja voi lisätä kursseja sovellukseen.**

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

Kirjautumisen jälkeen opiskelija näkee oman sivun, jossa näkee käynnissä olevat kurssinsa ja tällä viikolla kursille käytetyn ajan ja paljonko saavutettu
viikottaisesta tavoitteesta prosentteina.
Lisäksi sivulta löytyy linkit sivuille: "opiskele", "suunnittele", "tilastot" ja "kurssit.

### Opiskele

Lisää kurssien opiskeluihin käytettyä aikaa.

### Suunnittele

Luo viikolle opintotavoite ja tarkasta miten tavoitteessa on pysytty. Lisää uusi kurssi, muokkaa suunnitelmaa tai merkitse käymäsi kurssi suoritetuksi. 

**Herokussa voi tällä hetkellä lisätä uuden kurssin ja sille opiskelutavoitteen ja seurata kurssin tavoitteen edistymistä. Kurssin tavoitetta voi myös muuttaa tai poistaa kurssisuunnitelmaa tai merkitä kurssin suoritetuksi. **

### Tilastot

Kurssikohtaiset tilastot eri ajanjaksoilta opiskelujen määristä. Arvosana näkyy täällä, kun kurssi on suoritettu.

**Tilastoissa näkyy kaikki opiskelija kurssit ja niiden suunnitelmat ja onko kurssit suoritettu.**

### Kurssit

Lista kaikista sovelluksessa olevista kursseista ja niihin käytettyjen opiskelutuntien keskiarvosta (kun kurssi on kokonaan suoritettu). Opiskelija tai opettaja voivat lisätä kurssin listaan.

**Herokussa tällä hetkellä voi selata kurssien nimiä ja lisätä uuden kurssin listaan.**

## Opettaja

### Rekisteröityminen

Opettajan tarvitsee antaa rekisteröityäkseen uniikki käyttäjätunnus, kursseissa näkyvä opettajan nimi, uusi salasana, sama salasana uudestaan ja vain opettajien tiedossa oleva koodi.

**Herokussa opettajan rekisteröitymistä varten koodi on 4278**

### Oma sivu

Sivulla näkyy opetettavat kurssit ja linkit sivuille: "arvostele", "tilastot" ja "kurssit"

**Herokussa näkyy tällä hetkellä vain linkit arvostele ja kurssit-sivulle**

### Arvostele

Lisää arvosanat opiskelijoille suoritetusta kurssista ja merkitse kurssi suoritetuksi. Tällöin kurssi poistuu opetettavista kursseista.

**Ei vielä toteutettu Herokussa**

### Tilastot

Arvosteltujen kurssien keskiarvoiset opiskelutuntimäärät ja arvosanat.

**Ei vielä toteutettu Herokussa**

### Kurssit

Lista kaikista sovelluksessa olevista kursseista ja niihin käytettyjen opiskelutuntien keskiarvosta (kun kurssi on kokonaan suoritettu). 

**Näkyy lista kursseista ja opettaja voi lisätä omia kursseja**


