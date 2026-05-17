import re
import json

with open("offices.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

desks = []
current_desk = {}

for line in lines:
    line = line.strip()
    if line.startswith("## "):
        if current_desk:
            desks.append(current_desk)
        
        name = line[3:].strip()
        
        # Extract wilaya name, assuming format "01A - Adrar" or "16A - Alger « Bir mourad Rais »"
        # We can extract the part after the dash and before any quotes
        parts = name.split(" - ", 1)
        if len(parts) > 1:
            wilaya_full = parts[1].strip()
            wilaya = wilaya_full.split("«")[0].split(" (")[0].strip()
        else:
            wilaya = name

        current_desk = {
            "wilaya": wilaya,
            "name": name,
            "address": "",
            "phone": "",
            "maps": ""
        }
    elif line.startswith("- **Adresse:** "):
        current_desk["address"] = line[15:].strip()
    elif line.startswith("- **Maps:** "):
        # e.g. - **Maps:** [https://maps.app...](https://maps.app...)
        maps_link = line[12:].strip()
        if maps_link.startswith("[") and "](" in maps_link:
            maps_link = maps_link.split("](")[1].strip(")")
        current_desk["maps"] = maps_link
    elif line.startswith("- **Tel:** ") or line.startswith("- **Téléphone:** "):
        prefix_len = 11 if line.startswith("- **Tel:** ") else 17
        current_desk["phone"] = line[prefix_len:].strip()

if current_desk:
    desks.append(current_desk)

# Generate JSON string with proper formatting
json_str = "[\n"
for d in desks:
    json_str += f"            {json.dumps(d, ensure_ascii=False)},\n"
json_str = json_str.rstrip(",\n") + "\n        ]"

# Read index.html
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace desksRawData
pattern = re.compile(r'const desksRawData = \[.*?\];', re.DOTALL)
html_new = pattern.sub(f"const desksRawData = {json_str};", html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_new)

print(f"Updated index.html with {len(desks)} desks.")
