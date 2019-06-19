# PhotoDriver

Download Google Photos from your browser using Selenium Webdriver.

## Installation

```sh
pip install photodriver
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

  # Not supported yet:
  
  #poetry run pytest # Run all unit tests
  #poetry run tox    # Run all checks across all supported Python versions
```