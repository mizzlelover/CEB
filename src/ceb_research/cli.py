from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from .format import CebFormatError
from .pipeline import convert_file

app = typer.Typer(no_args_is_help=True)
console = Console()
DEFAULT_OUTPUT_DIR = Path("ceb-output")


@app.callback()
def main() -> None:
    """Expose the CEB conversion commands."""
    return


def iter_ceb_files(input_dir: Path, recursive: bool) -> tuple[Path, ...]:
    """Return CEB files in stable path order, optionally including subdirectories."""
    pattern = "**/*.ceb" if recursive else "*.ceb"
    return tuple(sorted(path for path in input_dir.glob(pattern) if path.is_file()))


@app.command()
def convert(
    input_path: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            resolve_path=True,
        ),
    ],
    output_dir: Annotated[
        Path,
        typer.Option("--output-dir", "-o", file_okay=False),
    ] = DEFAULT_OUTPUT_DIR,
) -> None:
    try:
        report = convert_file(input_path, output_dir)
    except CebFormatError as exc:
        console.print(str(exc), style="red")
        raise typer.Exit(code=2) from exc
    console.print(
        " ".join(
            (
                f"Converted {report.source} -> {report.page_count} pages,",
                f"{report.text_chars} text characters",
            )
        )
    )
    console.print(report.pdf)
    console.print(report.markdown)
    console.print(report.text)
    console.print(report.report)


@app.command()
def batch(
    input_dir: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=False,
            dir_okay=True,
            readable=True,
            resolve_path=True,
        ),
    ],
    output_dir: Annotated[
        Path,
        typer.Option("--output-dir", "-o", file_okay=False),
    ] = DEFAULT_OUTPUT_DIR,
    recursive: Annotated[
        bool,
        typer.Option("--recursive/--no-recursive"),
    ] = True,
) -> None:
    """Convert every .ceb file and preserve its relative input directories."""
    sources = iter_ceb_files(input_dir, recursive)
    if not sources:
        console.print(f"No .ceb files found in {input_dir}", style="yellow")
        raise typer.Exit(code=1)

    succeeded = 0
    failed = 0
    for source in sources:
        relative_parent = source.relative_to(input_dir).parent
        destination = output_dir / relative_parent
        try:
            report = convert_file(source, destination)
        except CebFormatError as exc:
            failed += 1
            console.print(f"Failed: {exc}", style="red")
        else:
            succeeded += 1
            message = f"Converted {source} -> {report.page_count} pages, "
            message += f"{report.text_chars} text characters"
            console.print(message)

    console.print(f"Batch complete: {succeeded} succeeded, {failed} failed.")
    if failed:
        raise typer.Exit(code=2)


if __name__ == "__main__":
    app()
