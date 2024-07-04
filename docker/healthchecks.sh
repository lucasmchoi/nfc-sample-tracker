#!/bin/bash

checks=()

if [ "$SERVER" == "True" ]; then
    if [ "$STOP_API" != "True" ]; then
        curl -f http://localhost:8081; checks+=($?)
    fi
    if [ "$STOP_GUI_MAIN" != "True" ]; then
        curl -f http://localhost:8082; checks+=($?)
    fi
    if [ "$STOP_GUI_ADMIN" != "True" ]; then
        curl -f http://localhost:8083; checks+=($?)
    fi
fi

# if [ "$HARDWARE" == "True" ]; then
    
# fi

for check in "${checks[@]}"; do
    if [ "$check" -gt 0 ]; then
        exit 1
    fi
done

exit 0
