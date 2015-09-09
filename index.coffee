{CompositeDisposable} = require 'atom'

buildScripts = require './lib/buildScripts'
rptfile = require './lib/rptfile'

module.exports =
    subscriptions: null

    config:
        buildScript:
            title: "Build Script",
            description: "Location of the Build File (if PROJECTFOLDER then it uses the path: projectfolder/tools/build.py)",
            type: "string",
            default: "PROJECTFOLDER"
        makeScript:
            title: "Make Script"
            description: "Location of the Make File (if PROJECTFOLDER then it uses the path: projectfolder/tools/build.py)"
            type: "string"
            default: "PROJECTFOLDER"
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
