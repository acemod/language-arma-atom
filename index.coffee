{CompositeDisposable} = require 'atom'

buildScripts = require './lib/buildScripts'
rptfile = require './lib/rptfile'

module.exports =
    subscriptions: null

    config:
        buildScript:
            title: "Build Script File",
            description: "Localtion of the Build File",
            type: "string",
            default: "p:\\z\\ace\\tools\\build.py"
        makeScript:
            title: "Make Script File"
            description: "Localtion of the Make File"
            type: "string"
            default: "p:\\z\\ace\\tools\\make.py"
        appDataFolder:
            title: "Arma 3 AppData Folder",
            description: "Location of the Arma 3 Application Data Folder (location of RPT files)",
            type: "string",
            default: "%localappdata%\\Arma 3\\"

    activate: ->
        @subscriptions = new CompositeDisposable
        @subscriptions.add atom.commands.add 'atom-workspace',
            'language-arma-atom:Build': => buildScripts.build()
        @subscriptions.add atom.commands.add 'atom-workspace',
            'language-arma-atom:Make': => buildScripts.make()
        @subscriptions.add atom.commands.add 'atom-workspace',
            'language-arma-atom:open-rpt-file': => rptfile.open()

    deactivate: ->
        @subscriptions.dispose()
