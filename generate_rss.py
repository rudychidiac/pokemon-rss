import requests, random
import xml.etree.ElementTree as ET

# Map each type to your custom icon URL
type_icons = {
    "normal": "https://res.cloudinary.com/dmeqm1nlf/image/upload/v1757973947/Normal_tod4gd.png",
    "fire": "https://res.cloudinary.com/dmeqm1nlf/image/upload/v1757973943/Fire_txnblx.png",
    "water": "https://res.cloudinary.com/dmeqm1nlf/image/upload/v1757973950/Water_dplgc2.png",
    "electric": "https://res.cloudinary.com/dmeqm1nlf/image/upload/v1757973942/Electric_sftubb.png",
    "grass": "https://res.cloudinary.com/dmeqm1nlf/image/upload/v1757973945/Grass_x092di.png",
    "ice": "https://res.cloudinary.com/dmeqm1nlf/image/upload/v1757973947/Ice_zaiudy.png",
    "fighting": "https://res.cloudinary.com/dmeqm1nlf/image/upload/v1757973943/Fighting_oxz9p0.png",
    "poison": "https://res.cloudinary.com/dmeqm1nlf/image/upload/v1757973948/Poison_okdpvl.png",
    "ground": "https://res.cloudinary.com/dmeqm1nlf/image/upload/v1757973946/Ground_mwkdu3.png",
    "flying": "https://res.cloudinary.com/dmeqm1nlf/image/upload/v1757973944/Flying_cjgyqz.png",
    "psychic": "https://res.cloudinary.com/dmeqm1nlf/image/upload/v1757973948/Psychic_ne6wr5.png",
    "bug": "https://res.cloudinary.com/dmeqm1nlf/image/upload/v1757973941/Bug_hadxnh.png",
    "rock": "https://res.cloudinary.com/dmeqm1nlf/image/upload/v1757973949/Rock_qvrjcw.png",
    "ghost": "https://res.cloudinary.com/dmeqm1nlf/image/upload/v1757973944/Ghost_g6mr2p.png",
    "dragon": "https://res.cloudinary.com/dmeqm1nlf/image/upload/v1757973942/Dragon_mzawbu.png",
    "dark": "https://res.cloudinary.com/dmeqm1nlf/image/upload/v1757973942/Dark_lts8vq.png",
    "steel": "https://res.cloudinary.com/dmeqm1nlf/image/upload/v1757973950/Steel_r5hsqv.png",
    "fairy": "https://res.cloudinary.com/dmeqm1nlf/image/upload/v1757973943/Fairy_eot8cn.png"
}

# Get all Pokémon
url = "https://pokeapi.co/api/v2/pokemon?limit=1025"
resp = requests.get(url).json()

# Pick one random Pokémon
random_pokemon = random.choice(resp["results"])
data = requests.get(random_pokemon["url"]).json()

name = data["name"].capitalize()
sprite = data["sprites"]["other"]["official-artwork"]["front_default"]

# Build type string with icons
types = [t["type"]["name"] for t in data["types"]]
type_str = ", ".join(
    f'<img src="{type_icons[t]}" height="16" style="vertical-align:middle"/> {t.title()}'
    for t in types
)

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
