import json
from pathlib import Path

import typer

app = typer.Typer()

OPENAPI_FILENAME = "openapi.json"


def get_api_data(filename: str) -> dict:
    """Return a python dictionary containing the API data from schema file."""
    with open(filename) as f:
        return json.load(f)


def process_path(route: str, route_data: dict, route_level: int) -> None:
    """Process the specific API route."""
    for verb, verb_data in route_data.items():
        first_line, *desc = verb_data["description"].splitlines()
        heading_level = "#" * route_level
        print(f"{heading_level} **`{verb.upper()}`** _{route}_")
        print(f"> {verb_data['summary']} : _{first_line}_")

        if desc:
            for line in desc:
                print(f"> {line}")


@app.command()
def main(route_level: int = 4) -> None:
    schema_path = Path(".") / OPENAPI_FILENAME

    all_paths = get_api_data(schema_path)["paths"]
    for route, data in all_paths.items():
        process_path(route, data, route_level)


if __name__ == "__main__":
    app()
