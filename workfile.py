import json
from pprint import pprint


s = """{"Andromeda": "Princess of Ethiopia", "Antlia": "Air pump", "Apus": "Bird of Paradise", "Aquarius": "Water bearer", "Aquila": "Eagle", "Ara": "Altar", "Aries": "Ram", "Auriga": "Charioteer", "Bootes": "Herdsman", "Caelum": "Graving tool", "Camelopardalis": "Giraffe", "Cancer": "Crab", "Canes Venatici": "Hunting dogs", "Canis Major": "Big dog", "Canis Minor": "Little dog", "Capricornus": "Sea goat", "Carina": "Keel of Argonauts\" ship", "Cassiopeia": "Queen of Ethiopia", "Centaurus": "Centaur", "Cepheus": "King of Ethiopia", "Cetus": "Sea monster (whale)", "Chamaeleon": "Chameleon", "Circinus": "Compasses", "Columba": "Dove", "Coma Berenices": "Berenice's hair", "Corona Australis": "Southern crown", "Corona Borealis": "Northern crown", "Corvus": "Crow", "Crater": "Cup", "Crux": "Cross (southern)", "Cygnus": "Swan", "Delphinus": "Porpoise", "Dorado": "Swordfish", "Draco": "Dragon", "Equuleus": "Little horse", "Eridanus": "River", "Fornax": "Furnace", "Gemini": "Twins", "Grus": "Crane", "Hercules": "Hercules, son of Zeus", "Horologium": "Clock", "Hydra": "Sea serpent", "Hydrus": "Water snake", "Indus": "Indian", "Lacerta": "Lizard", "Leo": "Lion", "Leo Minor": "Little lion", "Lepus": "Hare", "Libra": "Balance", "Lupus": "Wolf", "Lynx": "Lynx", "Lyra": "Lyre or harp", "Mensa": "Table mountain", "Microscopium": "Microscope", "Monoceros": "Unicorn", "Musca": "Fly", "Norma": "Carpenter's Level", "Octans": "Octant", "Ophiuchus": "Holder of serpent", "Orion": "Orion, the hunter", "Pavo": "Peacock", "Pegasus": "Pegasus, the winged horse", "Perseus": "Perseus, hero who saved Andromeda", "Phoenix": "Phoenix", "Pictor": "Easel", "Pisces": "Fishes", "Piscis Austrinus": "Southern fish", "Puppis": "Stern of the Argonauts' ship", "Pyxis": "Compass on the Argonauts' ship", "Reticulum": "Net", "Sagitta": "Arrow", "Sagittarius": "Archer", "Scorpius": "Scorpion", "Sculptor": "Sculptor's tools", "Scutum": "Shield", "Serpens": "Serpent", "Sextans": "Sextant", "Taurus": "Bull", "Telescopium": "Telescope", "Triangulum": "Triangle", "Triangulum Australe": "Southern triangle", "Tucana": "Toucan", "Ursa Major": "Big bear", "Ursa Minor": "Little bear", "Vela": "Sail of the Argonauts\" ship", "Virgo": "Virgin", "Volans": "Flying fish", "Vulpecula": "Fox"}"""

print(json.loads(s))