spawn = require('child_process').spawn

module.exports =
	build: ->
        buildProcess = spawn 'python', [atom.config.get('language-arma-atom.buildScript').replace(/%([^%]+)%/g, (_,n) -> process.env[n])]
        buildProcess.stdout.on 'data', (data) -> console.log '' + data
        buildProcess.stderr.on 'data', (data) -> console.log '' + data

    make: ->
        buildProcess = spawn 'python', [atom.config.get('language-arma-atom.makeScript').replace /%([^%]+)%/g, (_,n) -> process.env[n]]
        buildProcess.stdout.on 'data', (data) -> console.log '' + data
        buildProcess.stderr.on 'data', (data) -> console.log '' + data
