# OpenAPI Readme Generator  <!-- omit in toc -->

Generates Markdown suitable for a README file from a local `openapi.json` file.

I still plan to add more features to this tool, but it is already useful for
generating basic API documentation in Markdown from an OpenAPI schema.

- [Installation](#installation)
- [Usage](#usage)
- [Options Summary](#options-summary)
- [Options in Detail](#options-in-detail)
  - [--route-level](#--route-level)
  - [--inject](#--inject)
- [TODO](#todo)
- [Contributing](#contributing)
- [License](#license)

## Installation

This tool can be installed via `uv`, `poetry` or `pip` depending on your needs:

This tool is usually only needed during development, so it is recommended to
install it as a development dependency.

uv:

```console
uv add --dev openapi-readme
```

Poetry:

```console
poetry add openapi-readme --group dev
```

Or Pip:

```console
pip install openapi-readme
```

This will install the `openapi-readme` command line tool.

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

## Contributing

All PRs to add features of fix bugs are very welcome!

Please read the [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) and
[CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the
process for submitting pull requests to us.

## License

This project is licensed under the MIT License as reproduced below:

```pre
    Copyright (c) 2022-2024 Grant Ramsay

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
```
