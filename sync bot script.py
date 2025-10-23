from dotenv import load_dotenv
from notion_client import Client
import requests, os

load_dotenv(dotenv_path="C:\\Users\\Lakshya\\Desktop\\Random_Proj\\.env")

notion = Client(auth=os.getenv("NOTION_TOKEN"))

# print(os.getenv("NOTION_TOKEN"))
db_id = os.getenv("NOTION_DATABASE_ID")

data = notion.databases.query(database_id=db_id)
tasks = [item["properties"]["name"]["title"][0]["plain_text"] for item in data["results"]]         # here the name field is not there , we have to figure out a way to make this point to the plain text.
print("done 3")
md_content = "\n".join([f"- [ ] {t}" for t in tasks])
print("done 4")
# Push to GitHub
repo = os.getenv("GITHUB_REPO")
print(repo)
token = os.getenv("GITHUB_TOKEN")
print(token)


url = f"https://api.github.com/repos/{repo}/contents/BugBountyChecklist.md"
headers = {"Authorization": f"token {token}"}
r = requests.get(url, headers=headers)
sha = r.json().get("sha")

requests.put(url, headers=headers, json={
    "message": "update checklist",
    "content": md_content.encode("utf-8").decode("utf-8"),
    "sha": sha
})
