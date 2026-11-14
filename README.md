# kijkluister-epg

Dagelijkse tv-gids (XMLTV) voor de gratis Nederlandse en Belgische zenders in
[Kijkluister](https://github.com/firefly2008/bigscreen-host-windows).

**Adres voor apps:** `https://raw.githubusercontent.com/firefly2008/kijkluister-epg/main/guide.xml.gz`

- Elke nacht opnieuw opgehaald met [iptv-org/epg](https://github.com/iptv-org/epg)
  (bronnen: tvgids.nl, webtv.delta.nl, vrt.be, vtm.be, mon-programme-tv.be, pickx.be).
- Alleen de zenders uit de [iptv-org](https://github.com/iptv-org/iptv)-lijsten voor Nederland en België;
  `xmltv_id` is gelijk aan de `tvg-id` uit die lijsten, zodat de gids vanzelf aan de juiste zender koppelt.
- `channels.xml` laat zien welke zender uit welke bron komt.

De gidsgegevens zijn van de genoemde websites en alleen bedoeld voor eigen gebruik.
