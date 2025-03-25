# Find DOI

A Python package to find Digital Object Identifiers (DOIs) for academic articles based on their title, authors, or BibTeX entries.

## Features

- Find DOI by article title
- Find DOI by title and author
- Parse BibTeX entries and extract DOIs
- Command-line interface (CLI)
- JSON output for integration with other tools

## Installation

### Development Installation

#### Installing uv (Optional)

#### Windows
```bash
# PowerShell (recommended)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or using pip
pip install uv
```

#### macOS/Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Installing from Source

Clone the repository and install:

```bash
git clone https://github.com/weigao-123/find-doi.git
cd find-doi

# Using uv
uv pip install -e .

# Or using regular pip
pip install -e .
```

### Direct Use Without Installation

If you encounter installation issues, you can use the package directly:

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Command-Line Interface

DOI Finder includes a command-line interface for easy usage without writing Python code:

```bash
# Find DOI by article title (simplest form)
find-doi "Renewable energy and sustainable development: a crucial review"

# With author for better matching
find-doi "Renewable energy and sustainable development: a crucial review" --author "Dincer, Ibrahim"

# Explicitly using the doi command (same as above)
find-doi doi "Renewable energy and sustainable development: a crucial review"

# Get detailed article information
find-doi info "Renewable energy and sustainable development: a crucial review"

# Include full information with abstract
find-doi info "Renewable energy and sustainable development: a crucial review" --full

# Find DOI from a BibTeX file
find-doi bibtex references.bib

# Find DOI from stdin
cat references.bib | find-doi bibtex -

# Get detailed article information from a BibTeX file
find-doi bibtex-info references.bib

# Output in JSON format
find-doi "Renewable energy and sustainable development: a crucial review" --json

# Using an email to improve CrossRef API rate limits
find-doi "Renewable energy and sustainable development: a crucial review" --email "your.email@example.com"
```

### Alternative Execution Method

If the `find-doi` command isn't available, you can also run the module directly:

```bash
python -m find-doi "Renewable energy and sustainable development: a crucial review"
```

For help on available commands:
```bash
find-doi --help
```

## Python API Usage

```python
from find_doi import DOIFinder

# Initialize the DOI finder
finder = DOIFinder()

# Find DOI by title
doi = finder.find_by_title("Renewable energy and sustainable development: a crucial review")
print(f"Found DOI: {doi}")

# Find DOI by title and author
doi = finder.find_by_title_and_author("Renewable energy and sustainable development: a crucial review", "Dincer, Ibrahim")
print(f"Found DOI: {doi}")

# Parse BibTeX and find DOI
bibtex = """
  @article{dincer2000renewable,
    title={Renewable energy and sustainable development: a crucial review},
    author={Dincer, Ibrahim},
    journal={Renewable and sustainable energy reviews},
    volume={4},
    number={2},
    pages={157--175},
    year={2000},
    publisher={Elsevier}
  }
"""
doi = finder.find_from_bibtex(bibtex)
print(f"Found DOI: {doi}")
```

## Requirements

- Python 3.8+
- requests
- bibtexparser (>=2.0.0b8)

## Troubleshooting

If you encounter any issues during installation or execution, please refer to the [Troubleshooting Guide](TROUBLESHOOTING.md).

## License

MIT License 
