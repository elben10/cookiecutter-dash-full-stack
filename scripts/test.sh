#! /usr/bin/env bash

# Exit in case of error
set -e

rm -rf ./test

cookiecutter --no-input -f . project_name="Test"

cd test

poetry install

poetry run bash scripts/lint.sh
poetry run bash scripts/test.sh $@

cd ..
rm -rf ./test
