# forum-app

## Käynnistysohjeet

Kloonaa tämä repositorio omalle koneellesi ja siirry sen juurikansioon. Luo kansioon .env-tiedosto ja määritä sen sisältö seuraavanlaiseksi:

```
DATABASE_URL=<tietokannan-paikallinen-osoite>
SECRET_KEY=<salainen-avain>
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

## Sovelluksen tämänhetkinen tila
Valmiit ominaisuudet:
- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen
- Kaikki käyttäjät voivat luoda uusia alueita (topic), ketjuja (thread) sekä vastauksia ketjuihin (reply)
- UI toteutettu alkeellisella tasolla

Keskeneräistä:
- Käyttäjien nimimerkkien haku ketjujen ja vastausten yhteydessä
- Alueiden ja ketjujen listauksen lisätiedot
- Alueiden luomisen lukitseminen vain ylläpitäjien oikeudeksi
- Alueiden, ketjujen ja vastausten poistaminen ja niihin liittyvät oikeudet
- Salaiset alueet
- UI:n kaunistaminen

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
