import requests
import os
import json

BASE_URL = "https://Oishii-Udon.github.io/LCSource"
APPS_DIR = "apps"
STATE_FILE = "state.json"

os.makedirs(APPS_DIR, exist_ok=True)

# 讀取歷史版本
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        state = json.load(f)
else:
    state = {}

with open("apps.json") as f:
    config = json.load(f)

new_state = {}
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

    # 找 IPA
    ipa_url = None
    for asset in data.get("assets", []):
        if keyword in asset["name"]:
            ipa_url = asset["browser_download_url"]
            break

    if not ipa_url:
        print(f"No IPA found for {name}")
        continue

    filename = f"{name}.ipa"
    path = os.path.join(APPS_DIR, filename)

    new_state[name] = version

    # 判斷是否需要更新
    if state.get(name) != version or not os.path.exists(path):
        print(f"Updating {name} → {version}")

        ipa_data = requests.get(ipa_url).content
        with open(path, "wb") as f:
            f.write(ipa_data)
    else:
        print(f"{name} is up to date")

    result.append({
        "name": name,
        "bundleIdentifier": f"auto.{name.lower()}",
        "version": version,
        "downloadURL": f"{BASE_URL}/{APPS_DIR}/{filename}",
        "iconURL": "",
    })

# 保存版本記錄
with open(STATE_FILE, "w") as f:
    json.dump(new_state, f, indent=2)

# 生成 index.json
with open("index.json", "w") as f:
    json.dump({
        "name": "My Source",
        "apps": result
    }, f, indent=2)

print("Done.")