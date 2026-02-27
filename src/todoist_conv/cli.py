import pathlib

from click import Choice, Path, argument, command, open_file, option

from todoist_conv.formats import FORMAT_NAMES, get_format


@command()
@option(
    "-i",
    "--input-format",
    required=True,
    type=Choice(FORMAT_NAMES, case_sensitive=False),
)
@option(
    "-f",
    "--output-format",
    required=True,
    type=Choice(FORMAT_NAMES, case_sensitive=False),
)
@option(
    "-o",
    "--output-file",
    default="-",
    show_default=True,
    type=Path(dir_okay=False, writable=True, readable=False, allow_dash=True),
)
@argument(
    "file",
    type=Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        path_type=pathlib.Path,
    ),
    required=True,
)
def cli(input_format, output_format, output_file, file):
    """Converts Todoist FILE from input_format to output_format"""

    parser = get_format(input_format)
    serializer = get_format(output_format)

    parsed = parser.parse(file)
    output = serializer.serialize(parsed)

    with open_file(output_file, mode="wb") as output_file_obj:
        output_file_obj.write(output)


if __name__ == "__main__":
    cli()
