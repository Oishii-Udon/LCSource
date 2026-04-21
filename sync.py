import requests
import json

BASE_URL = "https://Oishii-Udon.github.io/LCSource"

with open("apps.json") as f:
    config = json.load(f)

result = []

for app in config["apps"]:
    name = app["name"]
    repo = app["repo"]
    keyword = app["asset_keyword"]

    print(f"Checking {name}...")

    url = f"https://api.github.com/repos/{repo}/releases/latest"
    r = requests.get(url)

    if r.status_code != 200:
        print(f"Failed to fetch {repo}")
        continue

    data = r.json()
    version = data.get("tag_name", "unknown")

    ipa_url = None

    for asset in data.get("assets", []):
        if keyword in asset["name"]:
            ipa_url = asset["browser_download_url"]
            break

    if not ipa_url:
        print(f"No IPA found for {name}")
        continue

    result.append({
        "name": name,
        "bundleIdentifier": f"auto.{name.lower()}",
        "version": version,
        "downloadURL": ipa_url,
        "iconURL": "",
    })

# 生成 index.json
with open("index.json", "w") as f:
    json.dump({
        "name": "My Source",
        "apps": result
    }, f, indent=2)

print("Done.")