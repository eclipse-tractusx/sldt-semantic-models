const core = require('@actions/core');
const github = require('@actions/github');
const https = require('https');
const fs = require('fs');
const path = require('path')
const { exec } = require("child_process");
const { TIMEOUT } = require('dns');


var bulk = JSON.parse(core.getInput('bulk'))
var bammVersion = core.getInput('bamm_version')
var bammSdkPath = `${__dirname}/samm-cli-${bammVersion}.jar`;

var added = JSON.parse(core.getInput('added'))
var modified = JSON.parse(core.getInput('modified'))
var prNumber = core.getInput('pr_number')

main()

async function main() {
    try {
        await asyncBammSdkDownload(`https://github.com/eclipse-esmf/esmf-sdk/releases/download/v${bammVersion}/samm-cli-${bammVersion}.jar`)

        if(bulk === false){
            validateChanges(added, modified, prNumber)
        } else {
            validateAllModels()
        }
    } catch (error) {
        core.setFailed(error.message)
    }
}

async function validateAllModels() {
    var validationResultPromises = []

    gatherValidationResults('./', '.ttl', validationResultPromises)

    var validationResults = await Promise.all(validationResultPromises)

    var formattedOutput = await produceValidationMarkdown(validationResults)

    var fullReport = `# Validation report for all models

    `

    formattedOutput.forEach((report) => {
        fullReport += '\n\n' + report + '\n'
    })

    writeOutputToFilesystem(fullReport, 'full-validation-report.md')
}

async function gatherValidationResults(startPath, fileEnding, returnValue) {
    var allFiles = fs.readdirSync(startPath)

    for (file of allFiles) {
        var fileName = path.join(startPath, file)

        if(fs.lstatSync(fileName).isDirectory()) {
            gatherValidationResults(fileName, fileEnding, returnValue)
        } else if(fileName.endsWith(fileEnding)) {
            returnValue.push(validateModel(fileName))
        }
    }
}


async function validateChanges(added, modified, prNumber) {
    var validationOutput = []

    added = added.filter(fileName => fileName.endsWith('.ttl'))
    modified = modified.filter(fileName => fileName.endsWith('.ttl'))

    await validateAllInputs(added, modified, validationOutput)

    console.log(validationOutput)
    
    var output = await produceValidationMarkdown(validationOutput)

    writeOutputToFilesystem(JSON.stringify({
        comments: output,
        prNumber: prNumber
    }), 'validation-output.json')
}

function writeOutputToFilesystem(output, filename) {
    const archiveDir = "output"
    if (!fs.existsSync(archiveDir)){
        fs.mkdirSync(archiveDir);
    }

    fs.writeFileSync(`${archiveDir}/${filename}`, output)
}

function produceValidationMarkdown(validationOutput) {
    return Promise.all(validationOutput.map(async (model) => {
        var lines = model.response.split('\n')

        var firstLine = lines[0]
    
        lines.splice(0,2)
        lines.splice(-3)
    
        var remainingLines = lines.join('\n')
        
        var body = `### Validation Report for ${model.file}

#### ${firstLine}`
        
        if(remainingLines !== '') {
            body = body + `\n\`\`\`ttl\n${remainingLines}\n\`\`\``
        }

        return body
    }))
}

async function validateAllInputs(added, modified, validationOutput) {
    return Promise.all(
        added.concat(modified).map((file) => {
            return validateModel(file)
                .then(result => {
                    validationOutput.push(result)
                })
        })
    )
}

async function validateModel(file) {
    return new Promise((resolve, reject) => {
        console.log(`Validating TTL file ${file}`)

        exec(`java -Dpolyglot.engine.WarnInterpreterOnly=false -jar ${bammSdkPath} aspect ${file} validate`, (error, stdout, stderr) => {
            if (stderr) {
                reject(stderr)
            }

            resolve({
                file: file,
                response: stdout
            })
        })
    })

}

async function asyncBammSdkDownload(url) {
    return new Promise((resolve, reject) => {
        downloadBammSdk(url, resolve, reject)
    })
}

async function downloadBammSdk(url, resolve, reject) {
    https.get(url, (response) => {
        if (response.statusCode >= 400) {
            reject("Could not download SAMM SDK v${bammVersion}")
        }

        if (response.statusCode > 300 && response.statusCode < 400 && !!response.headers.location) {
            downloadBammSdk(response.headers.location, resolve, reject)
        } else {
            console.log(`Starting download of SAMM SDK v${bammVersion}`)

            const filePath = fs.createWriteStream(bammSdkPath);

            response.pipe(filePath)
            filePath.on('finish', () => {
                filePath.close()
                console.log(`Downloaded SAMM SDK v${bammVersion}`)
                resolve(`Downloaded SAMM SDK v${bammVersion}`)
            })
        }
    })
}
