#!/usr/bin/env python3
import re, sys

html = open("noest_raw.html", encoding="utf-8").read()

# Extract all member-info blocks
blocks = re.findall(r'<div class="member-info[^"]*"[^>]*>(.*?)</div>\s*</div>\s*</div>\s*</div>', html, re.DOTALL)

lines = ["# Noest Express — Bureaux (Stop Desks)\n", f"**Total: {len(blocks)} bureaux**\n\n---\n"]

for b in blocks:
    # Name
    name_m = re.search(r'<h4>(.*?)</h4>', b)
    name = name_m.group(1).strip() if name_m else "?"
    
    # Maps link + address
    maps_m = re.search(r'<a href="(https?://(?:maps\.app\.goo\.gl|goo\.gl/maps)[^"]+)"[^>]*>\s*(.*?)\s*</a>', b, re.DOTALL)
    if maps_m:
        maps_url = maps_m.group(1).strip()
        address = re.sub(r'\s+', ' ', maps_m.group(2)).strip()
    else:
        maps_url = None
        addr_m = re.search(r'<i class="bi bi-geo-alt-fill"></i>\s*(.*?)\s*</span>', b, re.DOTALL)
        address = re.sub(r'<[^>]+>', '', addr_m.group(1)).strip() if addr_m else "?"
        address = re.sub(r'\s+', ' ', address).strip()

    # Phones
    phones = re.findall(r'<a href="tel:([^"]+)">', b)
    phone_str = " / ".join(p.strip() for p in phones)

    # Wilaya = number part before dash
    wilaya_code = name.split(" - ")[0].strip() if " - " in name else name

    lines.append(f"## {name}\n")
    lines.append(f"- **Adresse:** {address}\n")
    if maps_url:
        lines.append(f"- **Maps:** [{maps_url}]({maps_url})\n")
    lines.append(f"- **Téléphone:** {phone_str}\n")
    lines.append("\n")

with open("offices.md", "w", encoding="utf-8") as f:
    f.writelines(lines)

print(f"Done! {len(blocks)} bureaux written to offices.md")
