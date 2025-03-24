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
iwr -useb https://astral.sh/uv/install.ps1 | iex

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
git clone https://github.com/yourusername/doi-finder.git
cd doi-finder

# Using uv
uv pip install -e .

# Or using regular pip
pip install -e .
```

### Direct Use Without Installation

If you encounter installation issues, you can use the package directly:

1. Install dependencies:
```bash
pip install requests bibtexparser beautifulsoup4
```

2. Run the provided script:
```bash
python run_doi_finder.py "Renewable energy and sustainable development: a crucial review"
```

## Command-Line Interface

DOI Finder includes a command-line interface for easy usage without writing Python code:

```bash
# Find DOI by article title (simplest form)
doi-finder "Renewable energy and sustainable development: a crucial review"

# With author for better matching
doi-finder "Renewable energy and sustainable development: a crucial review" --author "Dincer, Ibrahim"

# Explicitly using the doi command (same as above)
doi-finder doi "Renewable energy and sustainable development: a crucial review"

# Get detailed article information
doi-finder info "Renewable energy and sustainable development: a crucial review"

# Include full information with abstract
doi-finder info "Renewable energy and sustainable development: a crucial review" --full

# Find DOI from a BibTeX file
doi-finder bibtex references.bib

# Find DOI from stdin
cat references.bib | doi-finder bibtex -

# Get detailed article information from a BibTeX file
doi-finder bibtex-info references.bib

# Output in JSON format
doi-finder "Renewable energy and sustainable development: a crucial review" --json

# Using an email to improve CrossRef API rate limits
doi-finder "Renewable energy and sustainable development: a crucial review" --email "your.email@example.com"
```

### Alternative Execution Method

If the `doi-finder` command isn't available, you can also run the module directly:

```bash
python -m doi_finder "Renewable energy and sustainable development: a crucial review"
```

For help on available commands:
```bash
doi-finder --help
```

## Python API Usage

```python
from doi_finder import DOIFinder

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