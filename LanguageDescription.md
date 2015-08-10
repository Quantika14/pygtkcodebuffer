# Syntax files #
This page describes how to write a syntax-file. These syntax-files are simple xml-files defining rules for the lexer. All these rules are assembled into regular-expressions so you may need to escape some of these patterns.

There 3 tags to define rules. `<pattern>` is the most basic one and defines a regular-expression to be matched. `<keywordlist>` defines a list of words (keywords) to be highlighted. And `<string>` defines a _range_ of the text marked by a start- and stop-pattern.

All these patterns were associated with a so called style. You _should_ use one of the DefaultStyles like keyword or string. Especially if you write a syntax-file for a programming language! Nobody wants to see keywords highlighted in different colours in different languages. There fore _use DefaultStyles_!

But since version 0.4.0 you may define language specific embedded styles. This makes sense if you like to provide a highlighting for wiki-like syntaxes for example. Using this feature you can define styles like "bold" or "underlined" which are not available by default.


### Document-root ###
All rules and styles are defined under the document-element `<syntax>`:
```
<?xml version="1.0"?>
<syntax>
   <!-- Add your rules here -->
</syntax>
```


### Define keywords ###
`<keywordlist>` is the simplest one, the example should be enough to get the idea.
The '

&lt;keywordlist&gt;

'-tag takes an optional argument to specify the [style](DefaultStyles.md) to be used. If omitted _keyword_ will be used.
```
...
   <!-- Keywords marked as keywords -->
   <keywordlist>
      <keyword>if</keyword>
      <keyword>else</keyword>
   </keywordlist>

   <!-- Keywords marked as "strings" -->
   <keywordlist style="string">
      <keyword>Another</keyword>
      <keyword>OrThis</keyword>
   </keywordlist>
...
```


### Define strings ###
A `<string>` is defined by start- and end-patterns. These patterns are regular-expressions so you may need to escape them. The `<string>`-tag also takes the optional argument `style` to specify the [style](DefaultStyles.md) which defaults to _string_. Also the `escape` argument is optional.
```
...
   <string escape="\">
      <starts>&quote;</starts>
      <ends>&quote;</ends>
   </string>
...
```


### Define patterns ###
The `<pattern>`-tag allows you to specify a regular-expression. This tag needs the `style` argument specifying the [style](DefaultStyles.md). It also takes the optional argument `group` to specify a sub-group of the regular-expression-match to be highlighted. This arguments defaults to _0_ meaning the string matched by the whole regexp will be highlighted. Additionally there is the optional argument `flags` specifying the regexp-flags used by this pattern.
```
...
   <pattern style="comment">#.*?$</pattern>
...
```
The `flags` argument specifies regular-expression flags. This argument may be a string of following characters.
| **I** | ignore case |
|:------|:------------|
| **L** | use current locale |
| **M** | multiline   |
| **S** | `.` matches even NL |
| **U** | use unicode |


### Define styles ###
Styles are defined by the `<style>`-element. Each style element needs the `name` attribute specifying the name of this style. Each style consists of any number of properties defined by the `<property>`-element. Each property-tag needs the `name` attribute specifying the name of the property to be setted. The content specifies the value of the property:

```
...
    <style name="bold">
        <property name="weight">bold</property>
    </style>
...
```

You can use embedded styles to overwrite the default styles. This is useful if you plan not to use a mono-spaced font. Please do not change any default styles for programming-languages! This may be confusing the user! Keywords should always be highlighted in the same way!

```
...
    <style name="DEFAULT">
        <property name="font">sans</property>
    </style>
...
```


#### Properties ####
Following table specifies which properties may be used to define a new style.

| _Name_ | _Description_ |
|:-------|:--------------|
| font   | A string defining the font to be used like: `sans` or `Sans Italic 12` |
| underline | One of `none`, `single` and `double`. |
| variant | One of `normal` or `smallcaps` |
| weight | One of `ultralight`, `light`, `normal`, `bold`, `ultrabold` or `heavy` |
| scale  | One of `xx_small`, `x_small`, `small`, `medium`, `large`, `x_large` or `xx_large` |
| style  | One of `normal`, `oblique` or `italic` |
