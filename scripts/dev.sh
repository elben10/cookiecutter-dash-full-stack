#! /usr/bin/env bash

# Exit in case of error
set -e

rm -rf ./dev-project

cookiecutter --no-input -f . project_name="Dev Project"