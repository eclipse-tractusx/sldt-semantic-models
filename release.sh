#!/bin/bash
#######################################################################
# Copyright (c) 2023 Robert Bosch Manufacturing Solutions GmbH
# Copyright (c) 2023 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This work is made available under the terms of the
# Creative Commons Attribution 4.0 International (CC-BY-4.0) license,
# which is available at
# https://creativecommons.org/licenses/by/4.0/legalcode.
#
# SPDX-License-Identifier: CC-BY-4.0
#######################################################################


# REMARKS:
# ========
# This script create release notes for a given period. Be advised that the script manipulates the currrent state of your local git repository.
# i.e. it switches branches, checks out specific commits and assumes you are on main. So please make sure you have not uncommitted change and
# that you are on main.

# Usage:
# ./release.sh '10/01/2022' '12/15/2022'

HEADLINES=("Added" "Deprecated" "Standardized")
STATUS=("release" "deprecate" "standardize")

for str in ${myArray[@]}; do
  echo $str
done

for i in ${!HEADLINES[@]}; do
  printf "\n## ${HEADLINES[$i]}\n"
  git checkout `git rev-list -n 1  --before="$2" main` >/dev/null 2>&1
  git whatchanged --since $1 --until $2 --pretty=format: --name-only | grep '\metadata.json$'| xargs grep -l "${STATUS[$i]}" | sed  -e "s/\metadata.json$//"
  git checkout main >/dev/null 2>&1
done


printf "\n## Removed\n"
git whatchanged --since $1 --until $2 --diff-filter D --pretty="format:" --name-only | grep '\metadata.json$'| sed '/^$/d'| grep '\metadata.json$'

printf "\n--------------------------------\n"
