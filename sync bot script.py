from dotenv import load_dotenv
from notion_client import Client
import requests, os
import base64

load_dotenv(dotenv_path="C:\\Users\\Lakshya\\Desktop\\Random_Proj\\github sync bot\\.env")

notion = Client(auth=os.getenv("NOTION_TOKEN"))

# print(os.getenv("NOTION_TOKEN"))
db_id = os.getenv("NOTION_DATABASE_ID")

data = notion.databases.query(database_id=db_id)
# print(data["results"])

tasks = [
    item["properties"]["Bug bounty checklist"]["title"][0]["plain_text"]
    for item in data["results"]
    if item["properties"]["Bug bounty checklist"]["title"]
]

md_content = "\n".join([f"- [ ] {t}" for t in tasks])

# Push to GitHub
repo = os.getenv("GITHUB_REPO")
# print(repo)
token = os.getenv("GITHUB_TOKEN")
# print(token)

content_bytes = md_content.encode("utf-8")

url = f"https://api.github.com/repos/{repo}/contents/Bug_bounty_checklist.md"
headers = {"Authorization": f"Bearer {token}"}
r = requests.get(url, headers=headers)
sha = r.json().get("sha")
res = requests.put(url, headers=headers, json={
    "message": "update checklist",
    "content": base64.b64encode(content_bytes).decode("utf-8"),
    "sha": sha
})

# print(md_content.encode("utf-8"))
# print(res)