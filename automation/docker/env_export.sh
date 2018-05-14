#!/bin/sh
set -e 

# Read environment variables from file and export them.

file="/app/environment_vars"

#if file exists then export enviroment variables
if [ -f $file ]; then
    while IFS= read line
        do
            # export $line 
	        export "$line"
    done <"$file"
    rm $file
fi

exec "$@"
