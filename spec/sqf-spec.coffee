describe "SQF grammar", ->
  [workspaceElement, grammar] = []

  beforeEach ->
    workspaceElement = atom.views.getView(atom.workspace)

    waitsForPromise ->
      Promise.all [
        atom.packages.activatePackage("language-arma-atom")
        atom.commands.dispatch workspaceElement, "language-arma-atom:toggle"
      ]

    runs ->
      grammar = atom.grammars.grammarForScopeName("source.sqf")

  it "parses the grammar", ->
    expect(grammar).toBeDefined()
    expect(grammar.scopeName).toBe "source.sqf"

  it "tokenizes multi-line strings", ->
    tokens = grammar.tokenizeLines('"12"')
    expect(tokens[0][0].value).toBe '"'
    expect(tokens[0][1].value).toBe '12'
    expect(tokens[0][2].value).toBe '"'
