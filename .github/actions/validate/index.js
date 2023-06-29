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

const mainBranch = 'refs/heads/main';

var output = {
    upload: [],
    delete: []
}

try {
    const added = JSON.parse(getInput('ADDED'))
    const modified = JSON.parse(getInput('MODIFIED'))
    const removed = JSON.parse(getInput('REMOVED'))

    is_main_input = getInput('IS_MAIN')
    const is_main = JSON.parse(getInput('IS_MAIN'))

    if (is_main) {
        deployAddedFilesOnMain(added)
        deployModifiedFilesOnMain(modified);
        deleteAspects(removed);
    } else {
        console.log("The action sets the changed models to the status 'DRAFT' and does not consider potential metadata.json files because it runs on a branch which is not the main-branch.")
        deployAspects(added);
        deployAspects(modified);
    }
    setOutput()

} catch (error) {
    console.log(error)
}

function deployAddedFilesOnMain(files) {
    files.forEach((file) => {
        if (path.basename(file) === 'metadata.json') {
            console.log("Found added metadata file: " + file);
            const metadata = JSON.parse(fs.readFileSync(file, 'utf8'));
            console.log("The new status is: " + metadata.status);
            if (metadata.status !== "draft" ) {
                baseDir = path.dirname(file)
                const filesInDirectory = fs.readdirSync(baseDir, 'utf8', true).map((file) => { return baseDir + "/" + file });
                modelFilesInDirectory = filesInDirectory.filter(isModelFile)
                if (modelFilesInDirectory.length === 0) {
                    console.log("Warning: Did not find any model file corresponding to metadata in: " + file)
                } else if (modelFilesInDirectory.length > 1) {
                    console.log("Warning: Did find more than one model file corresponding to one metadata file. The Semantic Hub currently only supports the addition of a single model file for each versioned namespace")
                    console.log("Metadata: " + file + ", Models in Directory: " + modelFilesInDirectory)
                }
                deployAspects(modelFilesInDirectory, metadata.status)
            } else {
                console.log("Ignoring Aspect with metadata " + file + " because it is in status 'DRAFT' which is not a valid state on the main branch")
            }    
        }
        if (isModelFile(file)) {
            let status = "release"
            const metaDataPath = path.dirname(file) + "/metadata.json";
            console.log("Metadata Path: " + metaDataPath)
            /*
            Do not need to add the model here if the metadata.json is part of the added
            files too, because the model will be already added once the metadata.json for the model is found. 
            */
            if (!files.includes(metaDataPath)) {
                try {
                    const metadata = JSON.parse(fs.readFileSync(metaDataPath));
                    status = metadata.status;
                } catch (err) {
                    console.log("Unable to load valid metadata for the model file " + file + " . Assuming the status RELEASED now.")
                } 
                deploySingleAspect(file, status)
            }
        }
    })
}

function isModelFile(file) {
    return path.extname(file) === ".ttl";
}

function deployModifiedFilesOnMain(files) {
    files.forEach((file) => {
        if (isModelFile(file)) {
            console.log("Warning: Detected a modification on main-branch for the model: " + file + " . Models on the main-branch should only change the status and not the content. Because of that, the model will be ignored for the upload.")
        }
        /*
        Only upload changes to the status found in the metdata.json since all other (model) files on the main branch are in state RELEASED or later and thus not supposed to change unless there is a state change. Thus these model deployment would be rejected by the Semantic Hub.
        There is the edge case that a model is changed while its status is changed too, for example, from 'RELEASED' to 'DEPRECATED'. This should be handled in the semantic hub.
        */
        if (path.basename(file) === 'metadata.json') {
            console.log("Modified metadata file: " + file);
            const metadata = JSON.parse(fs.readFileSync(file, 'utf8'));
            console.log("Modified new status: " + metadata.status);
            baseDir = path.dirname(file)
            const filesInDirectory = fs.readdirSync(baseDir, 'utf8', true).map((file) => { return baseDir + "/" + file });
            console.log(filesInDirectory)
            deployAspects(filesInDirectory, metadata.status)
        }
    })
}

function deploySingleAspect(file, status) {
    if (isModelFile(file)) {
        console.log("Adding model to upload list for model file: " + file)
        hubStatus = metadataStatusToHubStatus(status)
  
        modelContent = fs.readFileSync(file, "utf-8");
        aspect = {
            model : modelContent,
            status : hubStatus
        }
        output.upload.push(aspect)
        
    } else {
        console.log("Did not add file to upload list, because it is not a model file: " + file) 
    }
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

function deployAspects(files, status) {
    if(typeof status === 'undefined') {
        files.forEach((file) => {
            deploySingleAspect(file, "draft")
        });
    } else {
        files.forEach((file) => {
            deploySingleAspect(file, status)
        });
    }
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
    fs.writeFileSync(archiveDir + "/output.json", JSON.stringify(output)) 
   } catch(err) {
    console.log("Error writing file: " + error.message)
   }
  }
