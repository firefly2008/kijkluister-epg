#!/usr/bin/env python3
"""Maak een channels.xml voor iptv-org/epg met precies de zenders uit de gratis
Kijkluister-lijsten (iptv-org, Nederland en België).

Per zender wordt de eerste bron gekozen die de zender kent (volgorde in SITES).
Het xmltv_id in de uitvoer is altijd de tvg-id uit de zenderlijst, zodat
Kijkluister de gids zonder zoeken aan de juiste zender koppelt.

Gebruik: epg-channels.py <epg-repo> <uitvoer.xml> <lijst.m3u> [<lijst.m3u> ...]
"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# Voorkeursvolgorde: Nederlandse bronnen eerst, dan Belgische
SITES = ["tvgids.nl", "webtv.delta.nl", "vrt.be", "vtm.be", "mon-programme-tv.be", "pickx.be"]


def base(tvg_id: str) -> str:
    return tvg_id.split("@", 1)[0].lower()


def main() -> int:
    epg_repo, output, playlists = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3:]

    wanted: dict[str, str] = {}  # tvg-id -> zendernaam
    for playlist in playlists:
        text = Path(playlist).read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r'#EXTINF[^\n]*?tvg-id="([^"]+)"[^\n]*,([^\n]*)', text):
            wanted.setdefault(m.group(1).strip(), m.group(2).strip())
    print(f"Zenders met tvg-id in de lijsten: {len(wanted)}")

    # Alle bekende zenders per site, op volledige id en op basis-id (zonder @SD/@HD)
    exact: dict[str, ET.Element] = {}
    by_base: dict[str, ET.Element] = {}
    for site in SITES:
        path = epg_repo / "sites" / site / f"{site}.channels.xml"
        if not path.exists():
            print(f"  bron ontbreekt: {site}")
            continue
        for ch in ET.parse(path).getroot().iter("channel"):
            xid = ch.get("xmltv_id") or ""
            if not xid:
                continue
            exact.setdefault(xid, ch)
            by_base.setdefault(base(xid), ch)

    root = ET.Element("channels")
    found = 0
    for tvg_id, name in sorted(wanted.items()):
        ch = exact.get(tvg_id)
        if ch is None:
            ch = by_base.get(base(tvg_id))
        if ch is None:
            continue
        el = ET.SubElement(root, "channel", {
            "site": ch.get("site"),
            "site_id": ch.get("site_id"),
            "lang": ch.get("lang") or "nl",
            "xmltv_id": tvg_id,
        })
        el.text = ch.text or name
        found += 1

    ET.indent(root)
    output.write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding="unicode") + "\n",
                      encoding="utf-8")
    per_site: dict[str, int] = {}
    for el in root:
        per_site[el.get("site")] = per_site.get(el.get("site"), 0) + 1
    print(f"Met gids: {found} zenders  {per_site}")
    return 0 if found else 1


if __name__ == "__main__":
    sys.exit(main())
