spawn = require('child_process').spawn

module.exports =

  build: (type, text, script) ->
    # Start notification
    startNotification = atom.notifications.addInfo (text + ' Build Started'), dismissable: true, detail: 'Stand by ...'

    # Get Script Path
    path = atom.config.get('language-arma-atom.build' + type + 'Script')
    if /<current-project>/.test(path)
      path = atom.project.getPaths() + '\\tools\\' + script

    # Spawn build process and add Error notification handler
    buildProcess = spawn 'python', [path.replace(/%([^%]+)%/g, (_,n) -> process.env[n])]
    buildProcess.stderr.on 'data', (data) -> atom.notifications.addError (text + ' Build Error'), dismissable: true, detail: data

    return [buildProcess, startNotification]

  dev: ->
    [buildProcess, startNotification] = @build("Dev", "Development", "build.py")

    # Add Success notification handler
    buildProcess.stdout.on 'data', (data) -> atom.notifications.addSuccess 'Development Build Passed', dismissable: true, detail: data

    # Hide start notification
    buildProcess.stdout.on 'close', => startNotification.dismiss()

  release: ->
    [buildProcess, startNotification] = @build("Release", "Release", "make.py")

    # Add Info notification handler
    buildProcess.stdout.on 'data', (data) -> atom.notifications.addInfo 'Release Build Progress', dismissable: true, detail: data

    # Hide start notification, check output to determine if finished as make.py does not close automatically
    buildProcess.stdout.on 'data', (data) ->
      if /Press Enter to continue.../.test(data)
        startNotification.dismiss()
        # Display final Success notification as notificatons from make.py get splitted for some reason
        atom.notifications.addSuccess 'Release Build Passed', dismissable: true, detail: 'Release build finished successfully, refer to above progress/error notifications for more information.'
