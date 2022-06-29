#!/bin/bash

file='/etc/nginx/conf.d/default.conf'

if [ ! $LL_API ]; then
    echo "Backend API is empty! please set an environment variable named {LL_API}."
    exit
else
    echo "Backend API is: "$LL_API
    LL_API=${LL_API//\//\\\/}
    if [ "$(uname)" == "Darwin" ];
    then
        sed -i '' 's/proxy_pass localhost/proxy_pass '$LL_API'/g' $file
    elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ];
    then
        sed -i 's/proxy_pass localhost/proxy_pass '$LL_API'/g' $file
    fi
    echo "Start Nginx..."
    nginx -g "daemon off;"
fi