#!/usr/bin/env python3

# export toilettespubliques.com points into gps file

import json
import requests
from lxml import etree

src_website = "https://api.v2.toilettespubliques.com/toilettes"
authToken = '837pNgtH9wQ7nXUU44bp'
headers = {
    'Authorization': 'Bearer ' + authToken,
    'Content-Type': 'application/json'
}

request = requests.get(src_website, headers=headers, timeout=60)
data = request.content

jsonContent = json.loads(data)

root_elem_gpx = etree.Element('gpx', version="1.1")
root_elem_kml = etree.Element('kml', version="1.1")

wp_processed = 0

for wp in jsonContent.get('Toilettes'):

    # GPX
    wpt_elem_gpx = etree.SubElement(root_elem_gpx, 'wpt')
    wpt_elem_gpx.set("lat", str(wp.get('latitude')))
    wpt_elem_gpx.set("lon", str(wp.get('longitude')))
    src_elem_gpx = etree.SubElement(wpt_elem_gpx, 'src')
    src_elem_gpx.text = wp.get('id')
    name_elem_gpx = etree.SubElement(wpt_elem_gpx, 'name')
    name_elem_gpx.text = wp.get('adresse')
    desc_elem_gpx = etree.SubElement(wpt_elem_gpx, 'desc')
    desc_elem_gpx.text = wp.get('horaires')

    # KML
    pm_elem_kml = etree.SubElement(root_elem_kml, 'Placemark')
    pt_elem_kml = etree.SubElement(pm_elem_kml, 'Point')
    cdt_elem_kml = etree.SubElement(pt_elem_kml, 'coordinates')
    cdt_elem_kml.text = str(wp.get('longitude')) + "," + str(wp.get('latitude'))
    name_elem_kml = etree.SubElement(pm_elem_kml, 'name')
    name_elem_kml.text = wp.get('id')
    dsc_elem_kml = etree.SubElement(pm_elem_kml, 'description')
    dsc_elem_kml.text = wp.get('horaires')
    addr_elem_kml = etree.SubElement(pm_elem_kml, 'address')
    addr_elem_kml.text = wp.get('adresse')

    wp_processed += 1

print(str(wp_processed) + " wp processed")
# print(etree.tostring(root_elem_gpx, pretty_print=True).decode("utf-8"))
tree_gpx = etree.ElementTree(root_elem_gpx)
tree_kml = etree.ElementTree(root_elem_kml)
tree_gpx.write('toilettespubliques.gpx', pretty_print=True)
tree_kml.write('toilettespubliques.kml', pretty_print=True)
