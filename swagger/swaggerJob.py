import requests
import os
import json
import re
from config import Config

# from github import Github
DIR = "/swagger/output"
STATIC = "/app/static/assets"


class SwaggerJob:
    @staticmethod
    def run_job():
        # Need to work out the proper repo for this, as each repo gives different results (user or org)
        # url = "https://git.hcqis.org/api/v3/user/repos?"
        url = "https://git.hcqis.org/api/v3/orgs/iQIES/repos?per_page=3000"

        payload = {}
        headers = {"Authorization": os.getenv("GITHUB_TOKEN")}

        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code == 200:
            services = SwaggerJob.filter_services(response.text)
            service_names = list(l["name"] for l in services)
            SwaggerJob.write_services_txt(
                service_names, STATIC
            )  # writes out a txt file with all service names
            SwaggerJob.write_services_csv(
                service_names, STATIC
            )  # writes out a csv file with all service names
            SwaggerJob.write_openapis(
                service_names, DIR
            )  # writes out <service_name>.json openapi files
            SwaggerJob.write_service_json(
                services, DIR
            )  # writes out service.json with details on the services
            # print(services)
        else:
            print("Something bad happened: " + response.text)

    @staticmethod
    def filter_services(input):
        RPATTERN = "^iqies.*service$"
        lrepos = json.loads(input)
        services = list(filter(lambda enum: re.match(RPATTERN, enum["name"]), lrepos))
        return services

    @staticmethod
    def write_service_json(input=(), out_dir=DIR):
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
                "openapi": "https://test2-iqies.hcqis.org/api/{}/openapi.json".format(
                    service_name
                ),
                "openapi_cache": "http://10.137.177.242:4500/{}.json".format(
                    service_name
                ),
            }
            # print(service)
            services.append(service)

        with open("{}{}services.json".format(os.getcwd(), out_dir), "w") as json_file:
            json.dump(services, json_file)

    @staticmethod
    def write_services_txt(input=(), out_dir=DIR):
        f = open(os.getcwd() + out_dir + "/services.txt", "w")
        for i in input:
            name = (
                i.replace("iqies", "").replace("service", "").replace("-", "").strip()
            )
            # print(name)
            f.write(name + os.linesep)

    @staticmethod
    def write_services_csv(input=(), out_dir=DIR):
        f = open(os.getcwd() + out_dir + "/services.csv", "w")
        for i in input:
            name = (
                i.replace("iqies", "").replace("service", "").replace("-", "").strip()
            )
            # print(name)
            f.write(name + ",")

    @staticmethod
    def write_openapis(input=(), out_dir=DIR):
        for i in input:
            service = (
                i.replace("iqies", "").replace("service", "").replace("-", "").strip()
            )
            # print(service)
            url = "https://test2-iqies.hcqis.org/api/{}/openapi.json".format(service)
            # print(url)
            payload = {}
            kongToken = SwaggerJob.authenticate()
            headers = {"Content-Type": "application/json"}
            cookies = {"iqies-token": kongToken}
            response = requests.request(
                "GET", url, headers=headers, data=json.dumps(payload), cookies=cookies
            )
            # print(response)
            if response.status_code == 200:
                # print(response.text)
                f = open("{}{}/{}.json".format(os.getcwd(), out_dir, service), "w")
                f.write(response.text)

    @staticmethod
    def authenticate():
        url = "https://test2-iqies.hcqis.org/api/auth/v1/public/login"
        payload = {"username": "ro-region1", "password": "sdfsdff"}
        headers = {"Content-Type": "application/json"}
        response = requests.request(
            "POST", url, headers=headers, data=json.dumps(payload)
        )
        if response.status_code == 200:
            kongToken = json.loads(response.text)["kongToken"]
            return kongToken
        else:
            exit()
