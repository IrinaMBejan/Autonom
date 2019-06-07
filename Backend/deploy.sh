#! /usr/bin/env bash

version=$1
promote_flag="--no-promote"

if [[ -z "$version" ]]; then
    echo "[x] You must supply a version."
    exit 1
fi

gcloud app deploy *.yaml -v $version $promote_flag
