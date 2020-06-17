import requests
import os
import json
import re
from github import Github

def main():
    url = "https://git.hcqis.org/api/v3/user/repos?type=all"
    #url = "https://git.hcqis.org/api/v3/orgs/iQIES/repos"

    payload = {}
    headers = {'Authorization': 'token ' + os.getenv('GITHUB_TOKEN')}

    response = requests.request("GET", url, headers=headers, data = payload)
    if(response.status_code == 200):
        services = filter_services(response.text)
        service_names = list(l['name'] for l in services)
        write_services(service_names) #writes out a txt file with all service names
        write_openapis(service_names)
        #print(services)
    else:
        print('Something bad happened: ' + response.text)


def filter_services(input):
    RPATTERN = '^iqies.*service$'
    lrepos = json.loads(input)
    services = list(filter(lambda enum: re.match(RPATTERN, enum['name']), lrepos))
    return services
    

def write_services(input = ()):
    dir = "/swagger"
    f = open(os.getcwd() + dir + "/services.txt", "w")
    for i in input:
        name = i#.replace('iqies', '').replace('service', '').replace('-','').strip()
        print(name)
        f.write(name + os.linesep)

def write_openapis(input = ()):
    #kongToken=`curl 'https://test2-iqies.hcqis.org/api/auth/v1/public/login' -H 'Content-Type: application/json' --data '{"username":"ro-region1","password":"sdfsdff"}' | 
    # #python3.5 -c "import sys, json; print(json.load(sys.stdin)['kongToken'])"`
    for i in input:
        service = i.replace('iqies', '').replace('service', '').replace('-','').strip()
        print(service)
        url = "https://test2-iqies.hcqis.org/api/{}/openapi.json".format(service)
        print(url)
        payload = {}
        kongToken = authenticate()
        headers = {'Content-Type': 'application/json'}
        cookies = {'iqies-token':kongToken}
        response = requests.request("GET", url, headers=headers, data = json.dumps(payload), cookies= cookies)
        #print(response)
        if(response.status_code == 200):
            print(response.text)
            f = open("{}/swagger/{}.json".format(os.getcwd(),service), "w")
            f.write(response.text)


def authenticate():
    url = "https://test2-iqies.hcqis.org/api/auth/v1/public/login"
    payload = {"username":"ro-region1","password":"sdfsdff"}
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data = json.dumps(payload))
    if(response.status_code == 200):
        kongToken = json.loads(response.text)['kongToken']
        return kongToken
    else:
        exit()


if __name__ == "__main__":
    # execute only if run as a script
    main()


"""

    url="https://test2-iqies.hcqis.org/api/${ii}/openapi.json";
	echo $url;
	output_file_tmp=$(dirname $0)/"${ii}.tmp";
	output_file_json=$(dirname $0)/"${ii}.json";
	echo "Writing json to " $output_file_tmp;
	#echo $kongToken
	curl -H "Cookie:iqies-token=${kongToken}" $url > $output_file_tmp
	python3.5 -mjson.tool $output_file_tmp 
	if [ $? -eq 0 ]
	then
		echo $output_file_tmp " is json format"
		mv $output_file_tmp $output_file_json
	else
		echo $output_file_tmp " was not json" >&2
	fi

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


class Service(object):
    def __init__(self, name, full_name, created_at, updated_at, git_url, openapi):
        self.name = name
        self.full_name = full_name
        self.created_at = created_at
        self.updated_at = updated_at
        self.git_url = git_url
        self.openapi = openapi
        
 """