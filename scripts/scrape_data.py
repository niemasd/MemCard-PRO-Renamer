#! /usr/bin/env python3
'''
Scrape PSX/PS2/PSP serial numbers and titles from psxdatacenter.com
'''
from bs4 import BeautifulSoup
from json import dump as jdump
from urllib.request import urlopen
from warnings import warn

# psxdatacenter.com console URLs
URLS = {
    'PSX': [
        'https://psxdatacenter.com/ulist.html', # NTSC-U
        'https://psxdatacenter.com/jlist.html', # NTSC-J
        'https://psxdatacenter.com/plist.html', # PAL
    ],
    'PS2': [
        'https://psxdatacenter.com/psx2/ulist2.html', # NTSC-U
        'https://psxdatacenter.com/psx2/jlist2.html', # NTSC-J
        'https://psxdatacenter.com/psx2/plist2.html', # PAL
    ],
    'PSP': [
        'https://psxdatacenter.com/psp/ulist.html', # NTSC-U
        'https://psxdatacenter.com/psp/jlist.html', # NTSC-J
        'https://psxdatacenter.com/psp/plist.html', # PAL
    ],
}

# main program
if __name__ == "__main__":
    for console, urls in URLS.items():
        out_fn = '%s.json' % console
        print("Scraping %s data to: %s" % (console, out_fn))
        curr_data = dict() # keys = serials, values = titles
        for url in urls:
            print("Currently scraping: %s" % url)
            raw_data = urlopen(url).read().decode(errors='replace')
            raw_data = raw_data.replace('</</td>', '</td>')
            raw_data = raw_data.replace('</td)>', '</td>')
            soup = BeautifulSoup(raw_data, 'html.parser')
            for row in soup.find_all('tr'):
                serials = row.find_all('td', class_='col2')
                if len(serials) == 1:
                    serials = [v for v in serials[0].contents if getattr(v, 'name', None) != 'br']
                    serials = {v.text.strip() for v in serials}
                title = row.find_all('td', class_='col3')
                if len(title) == 1:
                    title = title[0].text.strip()
                    if 'PLASMALITE' in title:
                        print(row.find_all('td', class_='col2'))
                    if len(serials) == 1:
                        serial = serials.pop()
                        if len(serial) == 0:
                            continue
                        if serial in curr_data:
                            warn("Duplicate serial (%s): %s" % (serial, row))
                        else:
                            curr_data[serial] = title
                    else:
                        num_discs = len(serials)
                        title = ' '.join(title.split()).split(' - [ %d DISCS ]' % num_discs)[0].strip()
                        for i, serial in enumerate(serials):
                            if len(serial) == 0:
                                raise ValueError("Empty serial: %s" % row)
                            if serial in curr_data:
                                warn("Duplicate serial (%s): %s" % (serial, row))
                            else:
                                curr_data[serial] = '%s - DISC %d' % (title, i+1)
        f = open(out_fn, 'w'); jdump(curr_data, f); f.close(); print()
