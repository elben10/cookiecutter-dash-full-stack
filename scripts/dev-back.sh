#! /usr/bin/env bash

# Run this script from outside the project, to integrate a dev-fsfp project with changes and review modifications

# Exit in case of error
set -e

rm -fr ./\{\{cookiecutter.project_slug\}\}/app
rm -fr ./\{\{cookiecutter.project_slug\}\}/tests

rsync -a --exclude=README.md ./dev-project/* ./\{\{cookiecutter.project_slug\}\}/
rsync -a ./dev-project/.flake8 ./\{\{cookiecutter.project_slug\}\}/