# OpenAPI Readme Generator

Generates Markdown suitable for a README file from a local `openapi.json` file.

## Usage

Run this in the same directory as your `openapi.json` file. By default the
Markdown output will be printed to the console, but you can redirect it out to
a file too.

The particular styling of the generated Markdown is currently hardcoded, though
plans are afoot to implement some sort of themeing.

## Options

### --help

Show application usage hints and help.

### --route-level

Specify the heading level for each Route in the generated documentation. This
defaults to **4** if not specified, ie:

```Markdown
#### **`GET`** _/user/list_
```

### --inject

Injects the new Markdown directly into a `README.md` file in the current
directory, if it is found.
You need to add the placeholder comment `<!--
openapi-schema -->` to your markdown where you want it to be injected:

```Markdown
This is some preceeding text

### API Schema description
<!-- openapi-schema -->

### Next section
The document continues unaffected after the injection.
```

<!-- openapi-schema -->
