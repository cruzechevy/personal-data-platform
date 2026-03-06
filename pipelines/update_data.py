import requests
import json

def update_github():

    username = "cruzechevy"

    url = f"https://api.github.com/users/{username}"

    response = requests.get(url)

    data = response.json()

    stats = {
        "public_repos": data["public_repos"],
        "followers": data["followers"],
        "following": data["following"]
    }

    with open("data/github_stats.json","w") as f:
        json.dump(stats,f)

if __name__ == "__main__":
    update_github()