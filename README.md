# PhotoDriver

Download Google Photos from your browser using Selenium Webdriver.

## Installation

```sh
pip install photodriver
```

Selenium requires [geckodriver](https://github.com/mozilla/geckodriver/releases) to be installed and on the PATH.

## Usage Examples

```sh
$ photodriver output_dir
   # Download all photos to "output_dir"

$ photodriver output_dir --start "Jan 2015" --stop "Feb 2015"
   # Download all photos taken in January 2015
```

## Development

Requires [Poetry](https://poetry.eustace.io/).

```sh
git clone https://github.com/sneakypete81/photodriver.git
poetry install
```

Then you can use the following:

```sh
  poetry run photodriver # Run your locally modified photodriver
  poetry run flake8      # Run the linter
  poetry run black .     # Run the autoformatter
  poetry run pytest      # Run unit tests

  # Not supported yet:
  #poetry run tox    # Run all checks across all Python versions
```

### PyTest Options

```sh
  --functional # Run functional tests as well as unit tests
  --seed       # Seed for random functional tests
  --headless   # Run in headless Firefox mode
```
