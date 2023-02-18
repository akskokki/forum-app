# forum-app

## Käynnistysohjeet

Kloonaa tämä repositorio omalle koneellesi ja siirry sen juurikansioon. Luo kansioon .env-tiedosto ja määritä sen sisältö seuraavanlaiseksi:

```
DATABASE_URL=<tietokannan-paikallinen-osoite>
SECRET_KEY=<salainen-avain>
ADMIN_USERNAME=<ylläpitäjän-käyttäjänimi>
```

Seuraavaksi aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r ./requirements.txt
```

Määritä vielä tietokannan skeema komennolla

```
$ psql < schema.sql
```

Nyt voit käynnistää sovelluksen komennolla

```
$ flask run
```

Ylläpitäjä-tili luodaan samalla tavalla kuin tavallinen käyttäjä; tili saa ylläpitäjä-oikeudet kunhan käyttäjätunnus on sama kuin .env-tiedostoon kirjattu.

## Sovelluksen tämänhetkinen tila
Valmiit ominaisuudet:
- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen
  - Ylläpitäjän luominen onnistuu .env-tiedoston avulla
- Ylläpitäjä voi luoda alueita, ja kaikki käyttäjät uusia ketjuja alueiden sisällä
- Aluelistalla näkyy niiden sisältämät ketju- ja viestimäärät, sekä uusimman viestin tiedot
  - Ketjulistalla näkyy samoin ketjun viestimäärä ja uusin viesti
- Kaikki käyttäjät voivat lisätä ketjuihin uusia viestejä
  - Ketjun aloittajan viestit ovat sinisellä korostettuja
  - Ketjua sekä viestejä voivat niiden omistajat muokata sekä poistaa ketjunäkymässä
- UI toteutettu bootstrapilla

Puuttuvat ominaisuudet:
- Viestihaku
- Salaiset alueet (uusi tietokantataulu tätä varten)

## Täysi vaatimusmäärittely

Sovelluksessa näkyy keskustelualueita, joista jokaisella on tietty aihe. Alueilla on keskusteluketjuja, jotka muodostuvat viesteistä. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

Sovelluksen ominaisuuksia:

- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- Käyttäjä näkee sovelluksen etusivulla listan alueista sekä jokaisen alueen ketjujen ja viestien määrän ja viimeksi lähetetyn viestin ajankohdan.
- Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön.
- Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun.
- Käyttäjä voi muokata luomansa ketjun otsikkoa sekä lähettämänsä viestin sisältöä. Käyttäjä voi myös poistaa ketjun tai viestin.
- Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana.
- Ylläpitäjä voi lisätä ja poistaa keskustelualueita.
- Ylläpitäjä voi luoda salaisen alueen ja määrittää, keillä käyttäjillä on pääsy alueelle.
