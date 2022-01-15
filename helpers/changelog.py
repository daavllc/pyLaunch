import json
import urllib.error
import urllib.parse
import urllib.request

class Changelog:
    def __init__(self, org: str, repo: str):
        self.org = org
        self.repo = repo

    def Get(self):
        response = None
        try:
            response = urllib.request.urlopen(f"https://api.github.com/repos/{self.org}/{self.repo}/commits")
        except urllib.error.HTTPError as e:
            return False
        content = response.read().decode("UTF-8")
        data = json.loads(content)
        
        changelog = []
        for item in data:
            changelog.append(dict(
                sha = item['sha'],
                date = item['commit']['author']['date'][:-1],
                author = dict(
                    name = item['commit']['author']['name'],
                    email = item['commit']['author']['email']
                ),
                message = item['commit']['message']
            ))
        return changelog

if __name__ == '__main__':
    cl = Changelog("daavofficial", "pyLaunch")
    changelog = cl.Get()
    for item in changelog:
        print(item['sha'])
        print(item['date'])
        print(f"{item['author']['name']} - {item['author']['email']}")
        print(item['message'])
        input("Press enter to continue...")