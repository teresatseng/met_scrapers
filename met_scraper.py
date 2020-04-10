#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import csv

MAX_ID = 844005 # Max obj ID number, from MetObjects.csv
URL = 'https://www.metmuseum.org/art/collection/search/'


with open('Met_displayLocation.csv', mode='w') as display_file:
    writer = csv.writer(display_file, delimiter=',')
    writer.writerow(['Object_ID', 'Location', 'Gallery'])

    for obj_id in range(1,MAX_ID + 1):
        print(obj_id) # just keep track of progress

        # request webpage
        page = requests.get(URL+str(obj_id))

        # parse page to understandable html with beautiful soup
        soup = BeautifulSoup(page.content, 'html.parser')

        locations = soup.find_all('p',class_='artwork__location gtm__artwork__location')

        for location in locations:

            # strip leading/trailing whitespace, remove unecessary text
            phrase = location.text.strip().replace('On view at ', '')
            place_gallery = phrase.split(' in ')

            # place_gallery format is either ['Not on view'] or ['Locaton, 'Gallery']
            try:
                gallery = place_gallery[1]
            except IndexError:
                gallery = ''

            writer.writerow([obj_id, place_gallery[0], gallery])
