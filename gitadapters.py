
def gitHub_hookshot(payload):
    ssh_url = payload["repository"]["ssh_url"]
    branch = payload["ref"].split("/")[2]
    name = "origin"
    return ssh_url, name, branch
