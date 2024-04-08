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
# This script generates a set of artifacts for a given SAMM model in a ttl-file.
# Preconditiions:
# -internet connection to download specified SAMM CLI provided in $SAMMCLI folder and Catena-X CSS style

# Usage:
# Apply script to a single file
# ./generate.sh io.catenax.vehicle.product_description/2.0.0/ProductDescription.ttl
# To generate files for all models in repo
# find ./ -type f -name "*.ttl" -exec ./generate.sh "{}" \;



# Adjust if SAMM CLI version changes
JARNAME=samm-cli-2.6.0.jar
SAMMFOLDER=.SAMMCLI/
SAMMCLI=$SAMMFOLDER$JARNAME
# Adjust if SAMM CLI version changes
SAMMCLIURL=https://github.com/eclipse-esmf/esmf-sdk/releases/download/v2.6.0/samm-cli-2.6.0.jar

CATENAXCSS=$SAMMFOLDER/catena-template.css
CATENAXCUSTOMCSSURL=https://raw.githubusercontent.com/eclipse-tractusx/sldt-semantic-hub/main/backend/src/main/resources/catena-template.css

echo "Check availability of SAMM CLI"
if [ ! -f "$SAMMCLI" ]; then
  echo "$SAMMCLI does not exist. Will download"
  mkdir $SAMMFOLDER

  cd $SAMMFOLDER && { curl -LJO $SAMMCLIURL ; cd -; }
fi

if [ ! -f "$CATENAXCSS" ]; then
  echo "$CATENAXCSS does not exist. Will download"
  mkdir $SAMMFOLDER

  cd $SAMMFOLDER && { curl -LJO $CATENAXCUSTOMCSSURL ; cd -; }
fi

echo "Generate artifacts for $1"
MODELNAME="$(basename $1 .ttl)"
DIR="$(dirname "$1")"
PATHTEMPLATE=$DIR"/gen/"$MODELNAME

commands=(aas aas schema json openapi html)
endings=(-aas.xml .aasx -schema.json .json .yml .html)
toggles=("-f xml" "-f aasx" "" "" "-b=catenax.io" "-c $CATENAXCSS")

for i in ${!commands[@]}; do
    echo "generate ${commands[$i]} into $PATHTEMPLATE${endings[$i]}"
    java -jar $SAMMCLI aspect "$1" to ${commands[$i]} ${toggles[$i]} -o $PATHTEMPLATE${endings[$i]}
done
