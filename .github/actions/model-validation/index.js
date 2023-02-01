const core = require('@actions/core');
const github = require('@actions/github');
const https = require('https');
const fs = require('fs');
const path = require('path')
const { exec } = require("child_process");


try {
    var added = JSON.parse(core.getInput('added'))
    var modified = JSON.parse(core.getInput('modified'))
    var bammVersion = core.getInput('bamm_version')
    var prNumber = core.getInput('pr_number')

    var bammSdkPath = `${__dirname}/bamm-cli-${bammVersion}.jar`;
    var validationOutput = []

    main()
} catch (error) {
    core.setFailed(error.message)
}

async function main() {
    await asyncBammSdkDownload(`https://github.com/eclipse-esmf/esmf-sdk/releases/download/v${bammVersion}/bamm-cli-${bammVersion}.jar`)

    await validateAllInputs()

    console.log(validationOutput)
    
    var output = await produceValidationMarkdown()

    writeOutputToFilesystem({
        comments: output,
        prNumber: prNumber
    })
}

function writeOutputToFilesystem(output) {
    const archiveDir = "output"
    if (!fs.existsSync(archiveDir)){
        fs.mkdirSync(archiveDir);
    }

    fs.writeFileSync(`${archiveDir}/validation-output.json`, JSON.stringify(output))
}

function produceValidationMarkdown() {
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

async function validateAllInputs() {
    return Promise.all(
        added.concat(modified).map((file) => {
            return validateModel(file)
                .then(result => {
                    validationOutput.push({
                        file: file,
                        response: result
                    })
                })
        })
    )
}

async function validateModel(file) {
    return new Promise((resolve, reject) => {
        if (path.extname(file) === ".ttl") {
            console.log(`Validating TTL file ${path.basename(file)}`)

            exec(`java -jar ${bammSdkPath} aspect ${file} validate`, (error, stdout, stderr) => {
                if (stderr) {
                    reject(stderr)
                }

                resolve(stdout)
            })
        }
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
            reject("Could not download BAMM SDK v${bammVersion}")
        }

        if (response.statusCode > 300 && response.statusCode < 400 && !!response.headers.location) {
            downloadBammSdk(response.headers.location, resolve, reject)
        } else {
            console.log(`Starting download of BAMM SDK v${bammVersion}`)

            const filePath = fs.createWriteStream(bammSdkPath);

            response.pipe(filePath)
            filePath.on('finish', () => {
                filePath.close()
                console.log(`Downloaded BAMM SDK v${bammVersion}`)
                resolve(`Downloaded BAMM SDK v${bammVersion}`)
            })
        }
    })
}