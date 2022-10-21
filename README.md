# OpenAPI Readme Generator

Generates Markdown suitable for a README file from a local `openapi.json` file.

## Usage

Run this in the same directory as your `openapi.json` file. By default the
Markdown output will be printed to the console, just you can redirect it out to
a file too.

## Options

`--route-level`
: Specify the heading level for each Route in the generated documentation. This
defaults to **4** if not specified, ie `#### Heading`
