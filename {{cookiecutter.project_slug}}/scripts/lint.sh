#!/usr/bin/env bash

set -e

black app --check
isort --check-only app
flake8