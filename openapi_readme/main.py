"""CLI app to generate Markdown from an OpenAPI schema."""
import json
from pathlib import Path

try:
    from importlib import metadata
except ImportError:  # for Python<3.8
    import importlib_metadata as metadata

import typer
from rich import print
from single_source import get_version

path_to_pyproject_dir = Path(__file__).parent.parent
__version__ = get_version(__name__, path_to_pyproject_dir, default_return=None)

if __version__ is None:
    __version__ = metadata.version("openapi-readme")

app = typer.Typer(
    pretty_exceptions_show_locals=False,
    add_completion=False,
    no_args_is_help=True,
)

OPENAPI_FILENAME = "openapi.json"
README_FILENAME = "README.md"


def get_api_data(filename: Path) -> dict:
    """Return a python dictionary containing the API data from schema file."""
    try:
        with open(filename, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError as exc:
        print(
            "[red]ERROR: No [green]openapi.json[/green] file found in "
            "this location!"
        )
        raise typer.Exit(1) from exc


def process_path(route: str, route_data: dict, route_level: int) -> str:
    """Process the specific API route."""
    output = [""]

    for verb, verb_data in route_data.items():
        description = verb_data.get("description", "")
        heading_level = "#" * route_level
        output.append(f"{heading_level} **`{verb.upper()}`** _{route}_\n")
        if description:
            first_line, *desc = description.splitlines()
            output.append(f"> {verb_data['summary']} : _{first_line}_".strip())
            if desc:
                for line in desc:
                    output.append(f"> {line}".strip())
        else:
            # output.append(f"{heading_level} **`{verb.upper()}`** _{route}_\n")
            output.append(
                f"> {verb_data['summary']} : _No Description Given_".strip()
            )

    return "\n".join(output) + "\n"


def get_markdown(route_level: int) -> str:
    """Return the full OpenAPI Markdown as a string."""
    schema_path = Path(".") / OPENAPI_FILENAME
    output = ""
    all_paths = get_api_data(schema_path)["paths"]
    for route, data in all_paths.items():
        output += process_path(route, data, route_level)

    return output


def print_header() -> None:
    """Print the header for the CLI."""
    print(
        "[cyan][underline]openapi-readme[/underline] "
        f"version [bold]{__version__}[/bold] (c) Grant Ramsay 2023.\n",
    )


@app.command()
def main(
    route_level: int = typer.Option(4, help="Number of heading levels to use."),
    inject: bool = typer.Option(
        False,
        "--inject",
        help="Inject generated output into a README file.",
    ),
) -> None:
    """Generate Markdown from an OpenAPI schema."""
    output = get_markdown(route_level)

    if inject:
        print_header()
        try:
            with open(README_FILENAME, "r+", encoding="utf-8") as file:
                contents = file.readlines()
                try:
                    placeholder = (
                        contents.index("<!-- openapi-schema -->\n") + 1
                    )

                    # delete any existing data inside the tags.
                    try:
                        end_placeholder = contents.index(
                            "<!-- openapi-schema-end -->\n"
                        )
                        print(
                            "[gold3]"
                            "-> Existing API schema found in this file, "
                            "[bold]Replacing.\n"
                        )
                        del contents[placeholder + 1 : end_placeholder + 2]

                    except ValueError:
                        print(
                            "[green]"
                            "-> No Existing API schema found in this file, "
                            "[bold]Inserting.\n"
                        )

                    output += "<!-- openapi-schema-end -->\n"

                    contents.insert(placeholder, output)

                    file.seek(0)
                    file.write("".join(contents))
                except ValueError:
                    print(
                        "[red]ERROR: No placeholder has been found in the "
                        "README. Please check the documentation before using "
                        "the '--inject' option."
                    )
        except FileNotFoundError as exc:
            print(
                "[red]ERROR: No [green]README.md[/green] file found in "
                "this location!"
            )
            raise typer.Exit(2) from exc
    else:
        print(output, "\n")


if __name__ == "__main__":
    app()
