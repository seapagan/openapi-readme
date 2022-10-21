import json
from pathlib import Path

import typer
from rich import print

app = typer.Typer()

OPENAPI_FILENAME = "openapi.json"
README_FILENAME = "README.md"


def get_api_data(filename: str) -> dict:
    """Return a python dictionary containing the API data from schema file."""
    try:
        with open(filename) as f:
            return json.load(f)
    except FileNotFoundError:
        print(
            "[red]ERROR: No [green]openapi.json[/green] file found in "
            "this location!"
        )
        raise typer.Exit(1)


def process_path(route: str, route_data: dict, route_level: int) -> str:
    """Process the specific API route."""
    output = [""]

    for verb, verb_data in route_data.items():
        first_line, *desc = verb_data["description"].splitlines()
        heading_level = "#" * route_level
        output.append(f"{heading_level} **`{verb.upper()}`** _{route}_\n")
        output.append(f"> {verb_data['summary']} : _{first_line}_".strip())

        if desc:
            for line in desc:
                output.append(f"> {line}".strip())

    return "\n".join(output) + "\n"


def get_markdown(route_level: int):
    """Return the full OpemAPI Markdown as a string."""
    schema_path = Path(".") / OPENAPI_FILENAME
    output = ""
    all_paths = get_api_data(schema_path)["paths"]
    for route, data in all_paths.items():
        output += process_path(route, data, route_level)

    return output


@app.command()
def main(route_level: int = 4, inject: bool = False) -> None:
    output = get_markdown(route_level)

    if inject:
        try:
            with open(README_FILENAME, "r+") as f:
                contents = f.readlines()
                try:
                    placeholder = (
                        contents.index("<!-- openapi-schema -->\n") + 1
                    )
                    output += "<!-- openapi-schema-end -->"
                    output += "\n"
                    contents.insert(placeholder, output)
                    f.seek(0)
                    # f.truncate()
                    f.write("".join(contents))
                except ValueError:
                    print(
                        "[red]ERROR: No placeholder has been found in the "
                        "README. Please check the documentation before using "
                        "the '--inject' option."
                    )
        except FileNotFoundError:
            print(
                "[red]ERROR: No [green]README.md[/green] file found in "
                "this location!"
            )
            raise typer.Exit(2)
    else:
        print(output, "\n")


if __name__ == "__main__":
    app()
