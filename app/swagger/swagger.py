import requests
import os
import json
import re

# from github import Github

DIR = ""
# DIR = "./static/assets/json"
# uploads_dir = os.path.join(app.instance_path, 'uploads')

def main():
  run_job()


def run_job():
    # Need to work out the proper repo for this, as each repo gives different results (user or org)
    # url = "https://git.hcqis.org/api/v3/user/repos?"
    url = "https://qnetgit.cms.gov/api/v3/orgs/iQIES/repos?per_page=3000"

    payload = {}
    GH_PAT = os.getenv("GH_PAT") # Pulls in local env GH_PAT, ensure this is set (#> export GH_PAT=<PAT>)
    headers = {"Authorization": f"token {GH_PAT}"}

    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        services = filter_services(response.text)
        service_names = list(l["name"] for l in services)
        # writes out a txt file with all service names
        write_services(service_names)
        # writes out <service_name>.json openapi files
        write_openapis(service_names)
        write_service_json(
            services
        )  # writes out service.json with details on the services
        # print(services)
    else:
        print(f"Something bad happened: {response.text}")


def filter_services(input):
    RPATTERN = "^iqies.*service$"
    lrepos = json.loads(input)
    services = list(filter(lambda enum: re.match(RPATTERN, enum["name"]), lrepos))
    return services


def write_service_json(input=()):
    services = []
    for s in input:
        service_name = (
            s["name"]
            .replace("iqies", "")
            .replace("service", "")
            .replace("-", "")
            .strip()
        )
        service = {
            "name": s["name"],
            "created_at": s["created_at"],
            "updated_at": s["updated_at"],
            "github": s["html_url"],
            "openapi": f"https://test2-iqies.hcqis.org/api/{service_name}/openapi.json",
            "openapi_cache": f"http://10.137.177.242:4500/{service_name}.json",
        }
        # print(service)
        services.append(service)

    with open("{}{}services.json".format(os.getcwd(), DIR), "w") as json_file:
        json.dump(services, json_file)


def write_services(input=()):
    f = open(os.getcwd() + DIR + "/services.txt", "w")
    for i in input:
        name = i.replace("iqies", "").replace("service", "").replace("-", "").strip()
        # print(name)
        f.write(name + os.linesep)


def write_openapis(input=()):
    for i in input:
        service = i.replace("iqies", "").replace("service", "").replace("-", "").strip()
        # print(service)
        url = f"https://test2-iqies.hcqis.org/api/{service}/openapi.json"
        # print(url)
        payload = {}
        authCookie = authenticate()
        headers = {"Content-Type": "application/json"}
        cookies = authCookie #{"iqies-token": kongToken}
        response = requests.request(
            "GET", url, headers=headers, data=json.dumps(payload), cookies=cookies
        )
        # print(response)
        if response.status_code == 200:
            # print(response.text)
            f = open("{}{}/{}.json".format(os.getcwd(), DIR, service), "w")
            f.write(response.text)


def authenticate():
    url = "https://test2-iqies.hcqis.org/api/auth/v1/public/login"
    payload = {"username": "ro-region1", "password": "sdfsdff"}
    headers = {"Content-Type": "application/json"}
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        #print(response.text)
        #kongToken = json.loads(response.text)["kongToken"]
        return response.cookies
    else:
        exit()


if __name__ == "__main__":
    # execute only if run as a script
    main()


# Tried a different path using the PyGithub library, but it was making
# writing back out difficult.

"""
def main():
    RPATTERN = '^iqies.*service$'
    TIME_FORMAT = "%m/%d/%y, %H:%M:%S"

    g = Github(base_url="https://git.hcqis.org/api/v3", login_or_token=os.getenv('GITHUB_TOKEN'))


    repos = list(filter(lambda enum: re.match(RPATTERN, enum.name), g.get_user().get_repos()))
    jsonx = json.dumps(repos)
    services = {}
    for s in repos:
        service = dict(Service(s.name, s.full_name, s.created_at.strftime(TIME_FORMAT), s.updated_at.strftime(TIME_FORMAT), s.git_url, 'https://test2-iqies.hcqis.org/api/'+ s.name.replace('iqies','').replace('service','').replace('-','').strip() + '/openapi.json'))

        services += service

    jsonServices = json.dumps(services)
    print(jsonServices)
"""
