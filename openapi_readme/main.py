import typer

app = typer.Typer()


@app.command()
def main():
    print("Main program function.")


if __name__ == "__main__":
    app()
