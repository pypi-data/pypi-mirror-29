pivotal2pdf
===========

Create a pdf document from an exported csv of Pivotal Tracker

## Setup

```
pip install pivotal2pdf
```

## How it works

Select your stories from Pivotal Tracker. Export them to a csv file.
Run the Python script to convert them into a pdf. The stories will be split into chunks
of 4 per page.

`pivotal2pdf yourproject_20140820_1036.csv`

## Usage

```
pivotal2pdf [-h] [-m MARGIN] [-o OUTPUT] [-n] [-t] [-c] csv

positional arguments:
  csv                   the file path to the csv file

optional arguments:
  -h, --help            show this help message and exit
  -m MARGIN, --margin MARGIN
                        margin of the page in mm (default: 5)
  -o OUTPUT, --output OUTPUT
                        file path to the generated pdf (default: None)
  -n, --show-number     shows the story number on the bottom left (default:
                        False)
  -t, --show-tasks      shows the tasks for each story (default: False)
  -c, --collate         collate stories for easier sorting after cutting all
                        pages (default: False)
```
