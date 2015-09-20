spawn = require('child_process').spawn

module.exports =

  build: ->
    # start Hint
    atom.notifications.addInfo 'Build Started', dismissable: true, detail: 'Please do not load the project folder.'

    # get Config Path
    path = atom.config.get('language-arma-atom.buildScript')
    if path is 'PROJECTFOLDER'
      path = atom.project.getPaths() + '\\tools\\build.py'

    buildProcess = spawn 'python', [path.replace(/%([^%]+)%/g, (_,n) -> process.env[n])]
    buildProcess.stdout.on 'data', (data) -> atom.notifications.addSuccess 'Build Passed' , dismissable: true, detail: data
    buildProcess.stderr.on 'data', (data) -> atom.notifications.addError 'Build Failed' , dismissable: true, detail: data

  make: ->
    atom.notifications.addInfo 'Make Started', dismissable: true, detail: 'This may take some time.'

    # get Config Path
    path = atom.config.get('language-arma-atom.buildScript')
    if path is 'PROJECTFOLDER'
      path = atom.project.getPaths() + '\\tools\\make.py'

    buildProcess = spawn 'python', [path.replace /%([^%]+)%/g, (_,n) -> process.env[n]]
    buildProcess.stdout.on 'data', (data) -> atom.notifications.addSuccess 'Make Passed', dismissable: true, detail: data
    buildProcess.stderr.on 'data', (data) -> atom.notifications.addError 'Make Failed', dismissable: true, detail: data
