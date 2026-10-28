#!/usr/bin/env python3
"""Google Maps public-transport directions link. Usage: maps.py "<origin>" "<destination>" """
import sys
from urllib.parse import urlencode


def maps_link(origin, dest):
    return "https://www.google.com/maps/dir/?" + urlencode(
        {"api": 1, "origin": origin, "destination": dest, "travelmode": "transit"})


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    print(maps_link(sys.argv[1], sys.argv[2]))
