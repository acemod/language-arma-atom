describe "SQF grammar", ->
  grammar = null

  beforeEach ->
    atom.project.setPaths([path.join(__dirname, 'sample')])
    workspaceElement = atom.views.getView(atom.workspace)

    ## Open our sample init.sqf file
    waitsForPromise ->
      atom.workspace.open('init.sqf')

    ## active our sqf package
    #waitsForPromise ->
    #  atom.packages.activatePackage("language-arma-atom")

    runs ->
      activationPromise = atom.packages.activatePackage('language-arma-atom')
      activationPromise.fail (reason) ->
        throw reason

      grammar = atom.grammars.grammarForScopeName("source.sqf")

  it "parses the grammar", ->
    expect(grammar).toBeTruthy()
    expect(grammar.scopeName).toBe "source.sqf"

  it "tokenizes multi-line strings", ->
    tokens = grammar.tokenizeLines('"1\\\n2"')

    expect(tokens[0][0].value).toBe '"'
    expect(tokens[0][0].scopes).toEqual ['source.sqf', 'string.quoted.double.single-line.sqf', 'punctuation.definition.string.begin.sqf']
    expect(tokens[0][1].value).toBe '1'
    expect(tokens[0][1].scopes).toEqual ['source.sqf', 'string.quoted.double.single-line.sqf']
    expect(tokens[0][2].value).toBe '\\'
    expect(tokens[0][2].scopes).toEqual ['source.sqf', 'string.quoted.double.single-line.sqf', 'constant.character.escape.newline.sqf']
    expect(tokens[0][3]).not.toBeDefined()
