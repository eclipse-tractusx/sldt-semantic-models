/*
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
*/

var cp = require('child_process')
var path = require('path')
var fs = require('fs');
const { error } = require('console');

var output = {
    upload: [],
    delete: []
}

try {
    is_main_input = getInput('IS_MAIN')
    console.log("added: " + is_main_input)
    deploySingleAspect(is_main_input,"release")
    setOutput()

} catch (error) {
    console.log(error)
}


function deploySingleAspect(file, status) {
        console.log("Adding model to upload list for model file: " + file)
        hubStatus = metadataStatusToHubStatus(status)
  
        modelContent = fs.readFileSync(file, "utf-8");
        aspect = {
            model : modelContent,
            status : hubStatus
        }
        output.upload.push(aspect)
}

function metadataStatusToHubStatus(status) {
    var hubStatus = "DRAFT"
    switch(status) {
        case "draft": 
            break;
        case "release":
            hubStatus = "RELEASED";
            break;
        case "deprecate":
            hubStatus = "DEPRECATED";
            break
        default:
            console.log("The status " + status + " found in the metadata.json is not know. Using the status DRAFT instead")
    } 
    return hubStatus;
}

/*
    When working on the main-branch, some of the deletion might fail because models in state RELEASED cannot be deleted from the Semantic Hub. However, when deleting a model in Git, most likeley the corresponding metadata.json will be deleted too. 
    So to retrieve the status of the model before the deletion in Git one could 
    request the state of the model from the Semantic Hub which is an additional HTTP call compared to directly sending the deletion request. There is also no good 
    recovery solution if the model cannot be deleted from the Semantic Hub, because 
    it would be not intuitive to restore the model in Git then. As a consequence, the 
    current synchronization simply tries to delete the model without further logic. 
    The outlined issues thus need to be prevented as part of the governance process. 

    Another edge case is the deletion of the metadata.json file while the model file remains in the Git repository.
    The current design decision is to ignore this deletion and keep the latest set status for the model and not change the status back to RELEASED which would be the default status for a model without a metadata.json file. The underlying assumption
    is that the metadata.json should not be deleted in the first place and that hence the deletion should not be used as indicator for a status change of the model. However, this may lead to a confusing situation where a model without a metadata.json is not in status "RELEASED" which can be resolved by re-adding a metadata.json file.
*/

function deleteAspects(files) {
    files.forEach((file) =>  {
        if (isModelFile(file)) {
            
            splitted = file.split("/")
            urn = "urn:samm:" + splitted[0] + ":" + splitted[1] + '%23'
            console.log("Urn is" + urn)
            output.delete.push(urn)
        }
    }
    );
}

function getInput(name) {
    const val = process.env[`INPUT_${name.replace(/ /g, '_').toUpperCase()}`] || '';
    return val.trim();
}

function setOutput() {
   try {
    const archiveDir = "toArchive"
    if (!fs.existsSync(archiveDir)){
        fs.mkdirSync(archiveDir);
    }
    fs.writeFileSync("output.json", JSON.stringify(output)) 
       console.log("File added to:" +"output.json")
   } catch(err) {
    console.log("Error writing file: " + error.message)
   }
  }
