{CompositeDisposable} = require 'atom'

buildProject = require './lib/build-project'
openLatestRptFile = require './lib/open-latest-rpt-file'

module.exports =
  subscriptions: null

  config:
    buildDevScript:
      title: "Development Build Script",
      description: "Location of the Development Build Script (requires a compatible script, such as CBA's or ACE3's build.py)",
      type: "string",
      default: "<current-project>/tools/build.py"
    buildReleaseScript:
      title: "Release Build Script"
      description: "Location of the Release Build Script (requires a compatible script, such as CBA's or ACE3's make.py)"
      type: "string"
      default: "<current-project>/tools/make.py"
    appDataFolder:
      title: "Arma 3 AppData Folder",
      description: "Location of the Arma 3 Application Data Folder (location of RPT files)",
      type: "string",
      default: "%localappdata%\\Arma 3\\"

  activate: ->
    @subscriptions = new CompositeDisposable
    @subscriptions.add atom.commands.add 'atom-workspace',
      'language-arma-atom:build-dev': => buildProject.dev()
    @subscriptions.add atom.commands.add 'atom-workspace',
      'language-arma-atom:build-release': => buildProject.release()
    @subscriptions.add atom.commands.add 'atom-workspace',
      'language-arma-atom:open-latest-RPT-file': => openLatestRptFile.open()

  deactivate: ->
    @subscriptions.dispose()
