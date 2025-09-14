import requests, random, base64
import xml.etree.ElementTree as ET
from PIL import Image
from io import BytesIO

# Get full list of Pokémon
url = "https://pokeapi.co/api/v2/pokemon?limit=1025"
resp = requests.get(url).json()

# Pick one random Pokémon
random_pokemon = random.choice(resp["results"])
data = requests.get(random_pokemon["url"]).json()

name = data["name"].capitalize()

# Download the small default sprite
id = data["id"]
sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id}.png"
sprite_resp = requests.get(sprite_url)
img = Image.open(BytesIO(sprite_resp.content))

# Upscale 4x with nearest-neighbour to keep pixels crisp
scale = 4
img = img.resize((img.width * scale, img.height * scale), Image.NEAREST)

# Encode as base64 so it’s embedded directly in the XML
buffered = BytesIO()
img.save(buffered, format="PNG")
sprite_base64 = base64.b64encode(buffered.getvalue()).decode()
sprite_html = f'<img src="data:image/png;base64,{sprite_base64}" alt="{name}"/>'

# Types
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
ET.SubElement(item, "description").text = type_str
ET.SubElement(item, "link").text = sprite_html  # embed the upscaled image

# Output XML
rss_xml = ET.tostring(rss, encoding="unicode")
print(rss_xml)
