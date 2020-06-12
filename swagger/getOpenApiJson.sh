#!/bin/bash

echo $(dirname $0)

kongToken=`curl 'https://test2-iqies.hcqis.org/api/auth/v1/public/login' -H 'Content-Type: application/json' --data '{"username":"ro-region1","password":"sdfsdff"}' | python3.5 -c "import sys, json; print(json.load(sys.stdin)['kongToken'])"`

#kongToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InJvLXJlZ2lvbjEiLCJpc3MiOiJIcmY0OHFaeGlYWG8zV2xwR2lFZTJxS2tUTzdQcTdMQSIsIm8iOnsiMDQiOnsiMSI6WzE0XX19LCJ1c2VySWQiOjc1NTksImV4cCI6MTU5MTgyMTk5MC40ODIsInNlc3Npb25JZCI6IjYxNzkxMjg2OTAwMjY2OSIsImlhdCI6MTU5MTgwNzU5MCwic3ViIjoicm8tcmVnaW9uMSJ9.ROdkLWDgyLiLmV2Eu9P98wOuOt-Sefc_E3UiDh0VJ5A

#services=(intake)
services=(auth intake location myreports patientassessment patients provider regulation reportdatastreaming reportfilters reportgeneration reports reportscheduler survey virusscan enforcement grouper grouperhha letters objectauthorizer patientassessmenthha patientassessmentirf stateapi stateapinotification vut)
#services=(patients)

for ii in "${services[@]}";
do
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
done
