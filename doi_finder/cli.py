#!/usr/bin/env python
"""
Command-line interface for DOI Finder
"""
import argparse
import json
import sys
from typing import Dict, Any, List, Optional
from . import DOIFinder, ArticleInfo


def format_article_info(article_info: ArticleInfo) -> Dict[str, Any]:
    """Convert ArticleInfo to a dictionary for JSON output."""
    if article_info is None:
        return {}
    
    result = {
        "doi": article_info.doi,
        "title": article_info.title,
        "authors": article_info.authors,
        "year": article_info.year,
        "journal": article_info.journal,
        "publisher": article_info.publisher,
        "url": article_info.url,
        "type": article_info.type
    }
    
    # Include abstract if --full flag is set
    if getattr(article_info, 'abstract', None):
        result["abstract"] = article_info.abstract
    
    return result


def find_by_title(args: argparse.Namespace) -> None:
    """Find DOI by title."""
    finder = DOIFinder(mailto_email=args.email)
    
    if args.author:
        doi = finder.find_by_title_and_author(args.title, args.author)
    else:
        doi = finder.find_by_title(args.title)
    
    if args.json:
        # JSON output
        result = {"doi": doi}
        print(json.dumps(result, indent=2))
    else:
        # Plain text output
        if doi:
            print(f"DOI: {doi}")
        else:
            print("No DOI found")


def find_info_by_title(args: argparse.Namespace) -> None:
    """Find article information by title."""
    finder = DOIFinder(mailto_email=args.email)
    
    article_info = finder.find_article_info(args.title, args.author)
    
    if args.json:
        # JSON output
        result = format_article_info(article_info)
        print(json.dumps(result, indent=2))
    else:
        # Plain text output
        if article_info:
            print(f"Title: {article_info.title}")
            print(f"Authors: {', '.join(article_info.authors) if article_info.authors else 'N/A'}")
            print(f"Year: {article_info.year}")
            print(f"Journal: {article_info.journal or 'N/A'}")
            print(f"Publisher: {article_info.publisher or 'N/A'}")
            print(f"DOI: {article_info.doi}")
            print(f"URL: {article_info.url or 'N/A'}")
            print(f"Type: {article_info.type or 'N/A'}")
            if args.full and article_info.abstract:
                print(f"Abstract: {article_info.abstract}")
        else:
            print("No article information found")


def find_from_bibtex(args: argparse.Namespace) -> None:
    """Find DOI from BibTeX."""
    finder = DOIFinder(mailto_email=args.email)
    
    # Read BibTeX from file or stdin
    if args.input_file == '-':
        bibtex = sys.stdin.read()
    else:
        try:
            with open(args.input_file, 'r', encoding='utf-8') as file:
                bibtex = file.read()
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    
    dois = finder.find_from_bibtex(bibtex)
    
    if args.json:
        # JSON output
        result = {"dois": dois}
        print(json.dumps(result, indent=2))
    else:
        # Plain text output
        if dois:
            for doi in dois:
                if doi:
                    print(f"DOI: {doi}")
        else:
            print("No DOIs found")


def find_info_from_bibtex(args: argparse.Namespace) -> None:
    """Find article information from BibTeX."""
    finder = DOIFinder(mailto_email=args.email)
    
    # Read BibTeX from file or stdin
    if args.input_file == '-':
        bibtex = sys.stdin.read()
    else:
        try:
            with open(args.input_file, 'r', encoding='utf-8') as file:
                bibtex = file.read()
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    
    articles_info = finder.find_article_info_from_bibtex(bibtex)
    
    if args.json:
        # JSON output
        results = [format_article_info(ai) for ai in articles_info if ai]
        print(json.dumps(results, indent=2))
    else:
        # Plain text output
        if articles_info:
            for i, article_info in enumerate(articles_info):
                if article_info:
                    if i > 0:
                        print("\n" + "-" * 50 + "\n")
                    
                    print(f"Title: {article_info.title}")
                    print(f"Authors: {', '.join(article_info.authors) if article_info.authors else 'N/A'}")
                    print(f"Year: {article_info.year}")
                    print(f"Journal: {article_info.journal or 'N/A'}")
                    print(f"Publisher: {article_info.publisher or 'N/A'}")
                    print(f"DOI: {article_info.doi}")
                    print(f"URL: {article_info.url or 'N/A'}")
                    print(f"Type: {article_info.type or 'N/A'}")
                    if args.full and article_info.abstract:
                        print(f"Abstract: {article_info.abstract}")
        else:
            print("No article information found")


def main() -> None:
    """Main entry point for the CLI."""
    # Define valid commands
    commands = ['doi', 'info', 'bibtex', 'bibtex-info']
    
    # Check if first argument is not a recognized command and doesn't start with hyphen
    if len(sys.argv) > 1 and not sys.argv[1].startswith('-') and sys.argv[1] not in commands:
        # Insert 'doi' command before the first argument
        sys.argv.insert(1, 'doi')
    
    # Create the top-level parser
    parser = argparse.ArgumentParser(
        description="DOI Finder - Find Digital Object Identifiers for academic articles",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Create subparsers for commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Common arguments for all subparsers
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument("--email", help="Email to send to CrossRef API for better rate limits")
    common_parser.add_argument("--json", action="store_true", help="Output in JSON format")
    
    # Subparser for 'doi' command (renamed from 'title')
    doi_parser = subparsers.add_parser("doi", help="Find DOI by article title", parents=[common_parser])
    doi_parser.add_argument("title", help="Article title")
    doi_parser.add_argument("--author", help="Author name (optional)")
    doi_parser.set_defaults(func=find_by_title)
    
    # Subparser for 'info' command
    info_parser = subparsers.add_parser("info", help="Find article information by title", parents=[common_parser])
    info_parser.add_argument("title", help="Article title")
    info_parser.add_argument("--author", help="Author name (optional)")
    info_parser.add_argument("--full", action="store_true", help="Include full information (abstract)")
    info_parser.set_defaults(func=find_info_by_title)
    
    # Subparser for 'bibtex' command
    bibtex_parser = subparsers.add_parser("bibtex", help="Find DOI from BibTeX", parents=[common_parser])
    bibtex_parser.add_argument("input_file", help="BibTeX file (use '-' for stdin)")
    bibtex_parser.set_defaults(func=find_from_bibtex)
    
    # Subparser for 'bibtex-info' command
    bibtex_info_parser = subparsers.add_parser("bibtex-info", help="Find article information from BibTeX", parents=[common_parser])
    bibtex_info_parser.add_argument("input_file", help="BibTeX file (use '-' for stdin)")
    bibtex_info_parser.add_argument("--full", action="store_true", help="Include full information (abstract)")
    bibtex_info_parser.set_defaults(func=find_info_from_bibtex)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Execute the appropriate function or show help
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main() 