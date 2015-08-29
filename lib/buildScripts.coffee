spawn = require('child_process').spawn

module.exports =
	build: ->
    	buildProcess = spawn 'python', [atom.config.get('language-arma-atom.buildScript').replace /%([^%]+)%/g, (_,n) -> process.env[n]]
      	buildProcess.stdout.on 'data', console.log
        buildProcess.stderr.on 'data', console.log

    make: ->
		spawn 'python', [atom.config.get('language-arma-atom.makeScript').replace /%([^%]+)%/g, (_,n) -> process.env[n]]
