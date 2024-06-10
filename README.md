# OpenAPI Readme Generator  <!-- omit in toc -->

Generates Markdown suitable for a README file from a local `openapi.json` file.

This tool is still under development, progress so far is only a days work so
there is a lot to do with extra functionality and refactoring.

- [Usage](#usage)
- [Options Summary](#options-summary)
- [Options in Detail](#options-in-detail)
  - [--route-level](#--route-level)
  - [--inject](#--inject)
- [TODO](#todo)

## Usage

```console
openapi-readme [OPTIONS]
```

Run this in the same directory as your `openapi.json` file. By default the
Markdown output will be printed to the console, but you can redirect it out to
a file too.

The particular styling of the generated Markdown is currently hardcoded, though
plans are afoot to implement some sort of themeing.

## Options Summary

- `--route-level INTEGER`: Number of heading levels to use.  [default: 4]
- `--inject / --no-inject`: Inject generated output into a README file.
  [default: False]
- `--install-completion`: Install completion for the current shell.
- `--show-completion`: Show completion for the current shell, to copy it or
  customize the installation.
- `--help`: Show this message and exit.

## Options in Detail

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

Existing (previously injected) Schemas will be **replaced** by this new data.

## TODO

Future improvement plans

- Take more info from the `openapi.json` file
