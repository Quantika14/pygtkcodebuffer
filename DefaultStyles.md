# Default styles #
Following table shows all styles defined by default. You may use them in LanguageDefinition to specify how a particular lexical element ie. a keyword should be highlighted. Note, that you may specify your own styles using the `update_styles()` method of the CodeBuffer-class.

| **style-name** | **properties** |
|:---------------|:---------------|
| DEFAULT        | monospaced, black (all other styles derives these properties) |
| comment        | blue           |
| preprocessor   | violet         |
| keyword        | darkred, bold  |
| special        | turquoise      |
| string         | magenta        |
| number         | magenta        |
| datatype       | sea green      |