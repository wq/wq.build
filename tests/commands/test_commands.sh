#!/bin/bash
set -e;

function test_command {
    echo
    if [ -z "$2" ]; then
        CMD=$1;
        ARG="";
        echo Testing wq $CMD...;
    else
        CMD=$1;
        ARG=$2;
        echo "Testing wq $CMD $ARG...";
    fi;

    cd $CMD;
    rm -rf output/;
    mkdir output;
    wq $CMD $ARG;
    diff -r expected/ output/
    cd ..;
}

test_command collectjson;
test_command serviceworker 0.0.0;
