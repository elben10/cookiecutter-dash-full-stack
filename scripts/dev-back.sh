#! /usr/bin/env bash

# Run this script from outside the project, to integrate a dev-fsfp project with changes and review modifications

# Exit in case of error
set -e

rm -fr ./\{\{cookiecutter.project_slug\}\}/app

rsync -a --exclude=./dev-project/{.env} ./dev-project/* ./\{\{cookiecutter.project_slug\}\}/