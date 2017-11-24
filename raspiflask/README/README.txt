Raspissa käynnistetään app.py komennolla python3 app.py 

Python käynnistää Flask serverin porttiin 0.0.0.0:5000
0.0.0.0 varmistaa, että sivulle pääsee muistakin aliverkon koneista.

app.py toimii ohjelman runkona ja käynnistyessään käynnistää template-kansion index.html -tiedoston. 
Tiedosto hallinnoi SaunaVahtia

camera.py ottaa kuvan ja thermometer.py mittaa lämpötilan.

Laskenta ja tekstin liittäminen kuvaan tapahtuu app.py -tiedostossa.


Requirements

python3
pip3
Flask
picamera package for python3
image from pip3