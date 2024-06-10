"""CLI app to generate Markdown from an OpenAPI schema."""

import json
from importlib import metadata
from pathlib import Path
from typing import Any, NoReturn

import typer
from rich import print as rprint
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

OPENAPI_FILENAME = Path("openapi.json")
README_FILENAME = Path("README.md")


def handle_error(message: str, exit_code: int) -> NoReturn:
    """Print an error message and exit."""
    rprint(f"[red]ERROR: {message}")
    raise typer.Exit(exit_code)


def get_api_data(filename: Path) -> dict[str, Any]:
    """Return a python dictionary containing the API data from schema file.

    Fail if the file is not found or has an unexpected format.
    """
    try:
        with filename.open(encoding="utf-8") as file:
            data = json.load(file)
            if not isinstance(data, dict):
                handle_error(
                    "Expected JSON data to be a dictionary", exit_code=3
                )
            return data
    except FileNotFoundError:
        handle_error(
            "No openapi.json file found in this location!", exit_code=1
        )
    except json.JSONDecodeError:
        handle_error("Failed to decode JSON from the file!", exit_code=2)


def process_path(
    route: str, route_data: dict[str, Any], route_level: int
) -> str:
    """Process the specific API route.

    Args:
        route (str): The API route.
        route_data (dict[str, Any]): The data for the route.
        route_level (int): The heading level for Markdown.

    Returns:
        str: The formatted Markdown string for the route.
    """
    output = [""]

    for verb, verb_data in route_data.items():
        description = verb_data.get("description", "")
        heading_level = "#" * route_level
        output.append(f"{heading_level} **`{verb.upper()}`** _{route}_\n")
        if description:
            first_line, *desc = description.splitlines()
            output.append(f"> {verb_data['summary']} : _{first_line}_".strip())
            if desc:
                output.extend(f"> {line}".strip() for line in desc)
        else:
            output.append(
                f"> {verb_data['summary']} : _No Description Given_".strip()
            )

    return "\n".join(output) + "\n"


def get_markdown(route_level: int) -> str:
    """Return the full OpenAPI Markdown as a string."""
    schema_path = Path() / OPENAPI_FILENAME
    output = ""
    all_paths: dict[str, Any] = get_api_data(schema_path)["paths"]
    for route, data in all_paths.items():
        output += process_path(route, data, route_level)

    return output


def print_header() -> None:
    """Print the header for the CLI."""
    rprint(
        "\n[cyan][underline]OpenAPI Readme Generator[/underline][/cyan] "
        f"version [bold]{__version__}[/bold] (c) Grant Ramsay 2022-2024.\n",
    )


@app.command()
def main(
    route_level: int = typer.Option(4, help="Number of heading levels to use."),
    *,
    inject: bool = typer.Option(
        False,
        "--inject",
        help="Inject generated output into a README file.",
    ),
) -> None:
    """Generate Markdown from an OpenAPI schema."""
    output = get_markdown(route_level)

    print_header()
    if inject:
        try:
            with README_FILENAME.open("r+", encoding="utf-8") as file:
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
                        rprint(
                            "[gold3]"
                            "-> Existing API schema found in this file, "
                            "[bold]Replacing.\n"
                        )
                        del contents[placeholder + 1 : end_placeholder + 2]

                    except ValueError:
                        rprint(
                            "[green]"
                            "-> No Existing API schema found in this file, "
                            "[bold]Inserting.\n"
                        )

                    output += "<!-- openapi-schema-end -->\n"

                    contents.insert(placeholder, output)

                    file.seek(0)
                    file.write("".join(contents))
                except ValueError:
                    rprint(
                        "[red]ERROR: No placeholder has been found in the "
                        "README. Please check the documentation before using "
                        "the '--inject' option."
                    )
        except FileNotFoundError as exc:
            rprint(
                "[red]ERROR: No [green]README.md[/green] file found in "
                "this location!"
            )
            raise typer.Exit(2) from exc
    else:
        rprint(output, "\n")


if __name__ == "__main__":
    app()
