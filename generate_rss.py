import requests
import xml.etree.ElementTree as ET

# Get Pokémon (adjust limit if you want more)
url = "https://pokeapi.co/api/v2/pokemon?limit=50"
resp = requests.get(url).json()

rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = "Pokémon Sprites & Types"
ET.SubElement(channel, "link").text = "https://pokeapi.co/"
ET.SubElement(channel, "description").text = "Pokémon names with their sprites and types"

for p in resp["results"]:
    data = requests.get(p["url"]).json()
    name = data["name"].capitalize()
    sprite = data["sprites"]["front_default"]
    types = [t["type"]["name"] for t in data["types"]]
    type_str = ", ".join(types).title()

    item = ET.SubElement(channel, "item")
    ET.SubElement(item, "title").text = name
    ET.SubElement(item, "link").text = sprite
    ET.SubElement(item, "description").text = (
        f'{name} – Type: {type_str}<br>'
        f'<img src="{sprite}" alt="{name}"/>'
    )

# Print the XML (this is what will become feed.xml)
rss_xml = ET.tostring(rss, encoding="unicode")
print(rss_xml)
