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
var fs = require('fs')
var https = require('node:https');

try {
    console.log("Welcome to the Upload Action");
    const token = getInput('TOKEN');
    const hub = getInput("SEMANTIC_HUB_URL");
    const output = JSON.parse(fs.readFileSync("output.json", 'utf8'));

    for (let aspect of output.upload) {
        console.log("About to upload: " + aspect.model)
        uploadAspect(aspect, hub, token)
    }
    for  (let urn of output.delete) {
        console.log("About to delete: " + urn)
        deleteAspect(urn, hub, token)
    }
} catch (error) {
    console.log(error)
}

function uploadAspect(aspect, hub, token) {
        
        console.log(hub)
        if (token == "") {
            console.log("Token is empty")
        }
        var options = {
            'method': 'POST',
            'host': hub,
            'path': '/hub/api/v1/models?type=SAMM&status=' + aspect.status,
            'headers': {
              'Authorization': 'Bearer ' + token, 
              'Content-Type': 'text/plain'
            },
          };
          
          var req = https.request(options, function (res) {
            var chunks = [];
          
            res.on("data", function (chunk) {
              chunks.push(chunk);
            });
          
            res.on("end", function (chunk) {
              var body = Buffer.concat(chunks);
              console.log(body.toString());
            });
          
            res.on("error", function (error) {
              console.error(error);
            });
          });
            
          req.write(aspect.model);
          
          req.end()
}

function deleteAspect(urn, hub, token) {
var options = {
    'method': 'DELETE',
    'hostname': hub,
    'path': '/hub/api/v1/models/' + urn,
    'headers': {
        'Authorization': 'Bearer ' + token,
    },
    'maxRedirects': 20
    };
    
    var req = https.request(options, function (res) {
    var chunks = [];
    
    res.on("data", function (chunk) {
        chunks.push(chunk);
    });
    
    res.on("end", function (chunk) {
        var body = Buffer.concat(chunks);
        console.log(body.toString());
    });
    
    res.on("error", function (error) {
        console.error(error);
    });
    });
    
    req.end();
}

function getInput(name) {
    const val = process.env[`INPUT_${name.replace(/ /g, '_').toUpperCase()}`] || '';
    return val.trim();
}
