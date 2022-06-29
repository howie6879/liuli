#!/bin/bash

file='/etc/nginx/conf.d/default.conf'

if [ ! $BA_API ]; then
    echo "Backend API is empty! please set an environment variable named {BA_API}."
    exit
else
    echo "Backend API is: "$BA_API
    BA_API=${BA_API//\//\\\/}
    if [ "$(uname)" == "Darwin" ];
    then
        # command="sed -i '' 's/proxy_pass localhost/proxy_pass '$BA_API'/g' "$file
        # echo $command
        sed -i '' 's/proxy_pass localhost/proxy_pass '$BA_API'/g' $file
    elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ];
    then
        sed -i 's/proxy_pass localhost/proxy_pass '$BA_API'/g' $file
    fi
    echo "Start Nginx..."
    nginx -g "daemon off;"
fi