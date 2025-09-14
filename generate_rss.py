import requests, random
import xml.etree.ElementTree as ET

# Get all Pokémon (change limit if needed — 1025 covers all)
url = "https://pokeapi.co/api/v2/pokemon?limit=1025"
resp = requests.get(url).json()

# Pick one random Pokémon
random_pokemon = random.choice(resp["results"])
data = requests.get(random_pokemon["url"]).json()

name = data["name"].capitalize()
sprite = data["sprites"]["front_default"]
types = [t["type"]["name"] for t in data["types"]]
type_str = ", ".join(types).title()

# Build RSS feed
rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = "Pokémon of the Day"
ET.SubElement(channel, "link").text = "https://pokeapi.co/"
ET.SubElement(channel, "description").text = "One random Pokémon every 6 hours"

item = ET.SubElement(channel, "item")
ET.SubElement(item, "title").text = name
ET.SubElement(item, "link").text = sprite
ET.SubElement(item, "description").text = type_str

# Output XML
rss_xml = ET.tostring(rss, encoding="unicode")
print(rss_xml)
