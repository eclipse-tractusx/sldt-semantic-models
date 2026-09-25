#!/bin/bash
#######################################################################
# Copyright (c) 2023 Robert Bosch Manufacturing Solutions GmbH
# Copyright (c) 2026 Catena-X Automotive Network e.V.
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

# Usage (always run from the repository root, e.g. as ./scripts/generate.sh
# - the .SAMMCLI/ cache and every model path are resolved relative to the
# current working directory, not to this script's own location):
# Apply script to a single file
# ./scripts/generate.sh io.catenax.vehicle.product_description/2.0.0/ProductDescription.ttl
# To generate files for all models in repo
# find ./ -type f -name "*.ttl" -exec ./scripts/generate.sh "{}" \;



# SAMM CLI version comes from .github/scripts/config.json - the same file
# model-validation/config.py reads for the MS2 criteria check - so this
# can't silently drift from what CI validates models against.
SAMM_CLI_VERSION="$(jq -r '.settings.samm_cli_version' .github/scripts/config.json 2>/dev/null)"
if [ -z "$SAMM_CLI_VERSION" ] || [ "$SAMM_CLI_VERSION" = "null" ]; then
  echo "Could not read settings.samm_cli_version from .github/scripts/config.json" >&2
  exit 1
fi

JARNAME=samm-cli-$SAMM_CLI_VERSION.jar
SAMMFOLDER=.SAMMCLI/
SAMMCLI=$SAMMFOLDER$JARNAME
SAMMCLIURL=https://github.com/eclipse-esmf/esmf-sdk/releases/download/v$SAMM_CLI_VERSION/samm-cli-$SAMM_CLI_VERSION.jar

# samm-cli 2.16.0's class files require JDK 25 to even load, and on JDK 25
# it triggers two harmless-but-noisy JVM warnings on every invocation: one
# from a native library load (jansi) that newer JDKs warn about by
# default, one from a terminally-deprecated sun.misc.Unsafe call inside
# its GraalVM/Truffle internals. Both have a dedicated suppression flag,
# but only on JDK 23+ - moot here since this jar won't run on anything
# older anyway.
JAVA_FLAGS="--enable-native-access=ALL-UNNAMED --sun-misc-unsafe-memory-access=allow"

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

echo "Validate $1 with SAMM CLI"
if ! java $JAVA_FLAGS -jar $SAMMCLI aspect "$1" validate; then
  echo "$1 does not validate - skipping artifact generation" >&2
  exit 1
fi

echo "Generate artifacts for $1"
MODELNAME="$(basename $1 .ttl)"
DIR="$(dirname "$1")"
PATHTEMPLATE=$DIR"/gen/"$MODELNAME

commands=(aas aas schema json openapi html parquet)
endings=(-aas.xml .aasx -schema.json .json .yml .html .parquet)
toggles=("-f xml" "-f aasx" "" "" "-b=catenax.io" "-c $CATENAXCSS")

# A model can validate but still fail to generate one of the artifact
# types below (SAMM CLI bug/limitation for that particular structure).
# That's not fatal: keep whichever artifact types succeeded, warn on
# whichever didn't (removing any partial/corrupt output that type's
# failed attempt may have left behind), and still exit 0 - a caller
# should commit the artifacts that could be built rather than getting
# none of them over one format that can't.
for i in ${!commands[@]}; do
    out="$PATHTEMPLATE${endings[$i]}"
    echo "generate ${commands[$i]} into $out"
    if ! java $JAVA_FLAGS -jar $SAMMCLI aspect "$1" to ${commands[$i]} ${toggles[$i]} -o "$out"; then
      echo "::warning::could not generate '${commands[$i]}' artifact for $1 ($out) - skipping" >&2
      rm -f "$out"
    fi
done
