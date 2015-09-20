spawn = require('child_process').spawn

module.exports =

  dev: ->
    # Start notification
    startNotification = atom.notifications.addInfo 'Development Build Started', dismissable: true, detail: 'Stand by...'

    # Get Config Path
    path = atom.config.get('language-arma-atom.buildDevScript')
    if /<current-project>/.test(path)
      path = atom.project.getPaths() + '\\tools\\build.py'

    # Spawn development build process
    buildProcess = spawn 'python', [path.replace(/%([^%]+)%/g, (_,n) -> process.env[n])]
    buildProcess.stdout.on 'data', (data) -> atom.notifications.addSuccess 'Development Build Passed', dismissable: true, detail: data
    buildProcess.stderr.on 'data', (data) -> atom.notifications.addError 'Development Build Failed', dismissable: true, detail: data

    # Hide start notification
    buildProcess.stdout.on 'close', => startNotification.dismiss()

  release: ->
    # Start notification
    startNotification = atom.notifications.addInfo 'Release Build Started', dismissable: true, detail: 'Stand by, this may take some time...'

    # Get Config Path
    path = atom.config.get('language-arma-atom.buildReleaseScript')
    if /<current-project>/.test(path)
      path = atom.project.getPaths() + '\\tools\\make.py'

    # Spawn release build process
    buildProcess = spawn 'python', [path.replace /%([^%]+)%/g, (_,n) -> process.env[n]]
    buildProcess.stdout.on 'data', (data) -> atom.notifications.addSuccess 'Release Build Passed', dismissable: true, detail: data
    buildProcess.stderr.on 'data', (data) -> atom.notifications.addError 'Release Build Failed', dismissable: true, detail: data

    #@todo consolidate into 1 notification, it gets split currently, if not possible a workaround to display final "passed" notification should be added

    # Hide start notification, check output to determine if finished as make.py does not close automatically
    buildProcess.stdout.on 'data', (data) ->
      if /Press Enter to continue.../.test(data)
        startNotification.dismiss()
