import requests, random
import xml.etree.ElementTree as ET

# Get full list of Pokémon
url = "https://pokeapi.co/api/v2/pokemon?limit=1025"
resp = requests.get(url).json()

# Pick one random Pokémon
random_pokemon = random.choice(resp["results"])
data = requests.get(random_pokemon["url"]).json()

name = data["name"].capitalize()

# Use crisp sprite (PokeAPI pixel sprite repo has consistent IDs)
id = data["id"]
sprite = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id}.png"

# Types (just plain text, e.g. "Grass, Poison")
types = [t["type"]["name"] for t in data["types"]]
type_str = ", ".join(types).title()

# Build RSS
rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = "Pokémon of the Hour"
ET.SubElement(channel, "link").text = "https://pokeapi.co/"
ET.SubElement(channel, "description").text = "One random Pokémon every hour"

item = ET.SubElement(channel, "item")
ET.SubElement(item, "title").text = name
ET.SubElement(item, "link").text = sprite
ET.SubElement(item, "description").text = type_str

# Output XML
rss_xml = ET.tostring(rss, encoding="unicode")
print(rss_xml)
