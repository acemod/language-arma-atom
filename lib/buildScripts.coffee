{CompositeDisposable} = require 'atom'
spawn = require('child_process').spawn

module.exports =

    build: ->
        # start Hint
        atom.notifications.addInfo 'Build started', dismissable: true

        # get Config Path
        path = atom.config.get('language-arma-atom.buildScript')
        if path is 'PROJECTFOLDER'
            path = atom.project.getPaths() + '\\tools\\build.py'
            #atom.notifications.addInfo '' + path, dismissable: true

        buildProcess = spawn 'python', [path.replace(/%([^%]+)%/g, (_,n) -> process.env[n])]
        buildProcess.stdout.on 'data', (data) -> atom.notifications.addSuccess 'Build is Done: ' + data , dismissable: true
        buildProcess.stderr.on 'data', (data) -> atom.notifications.addError 'Build cant Finish:' + data , dismissable: true

    make: ->
        notifications.addInfo 'Make started', dismissable: true

        # get Config Path
        path = atom.config.get('language-arma-atom.buildScript')
        if path is 'PROJECTFOLDER'
            path = atom.project.getPaths() + '\\tools\\make.py'
            #atom.notifications.addInfo '' + path, dismissable: true


        buildProcess = spawn 'python', [path.replace /%([^%]+)%/g, (_,n) -> process.env[n]]
        buildProcess.stdout.on 'data', (data) -> atom.notifications.addSuccess 'Make is Done: ' + data , dismissable: true
        buildProcess.stderr.on 'data', (data) -> atom.notifications.addError 'Make cant Finish: ' + data , dismissable: true
