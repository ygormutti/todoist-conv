# todoist-conv

Converts Todoist CSVs to/from other formats to integrate with other tools, like mind mappers.

## Usage

```shell
$ todoist-conv --help
Usage: todoist-conv [OPTIONS] FILE

  Converts Todoist FILE from input_format to output_format

Options:
  -i, --input-format [csv|opml|json]
                                  [required]
  -f, --output-format [csv|opml|json]
                                  [required]
  -o, --output-file FILE          [default: -]
  --help                          Show this message and exit.
```