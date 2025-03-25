from find_doi import DOIFinder

def main():
    # Initialize the DOI finder with an email for better CrossRef API rate limits
    # More info: https://github.com/CrossRef/rest-api-doc#good-manners--more-reliable-service
    finder = DOIFinder(mailto_email="your.email@example.com")  # Replace with your email or remove parameter
    
    # Example 1: Find DOI by title
    title = "Renewable energy and sustainable development: a crucial review"
    doi = finder.find_by_title(title)
    print(f"\nSearching for DOI by title: {title}")
    print(f"Found DOI: {doi}")
    
    # Example 2: Find DOI by title and author
    title = "Renewable energy and sustainable development: a crucial review"
    author = "Dincer, Ibrahim"
    doi = finder.find_by_title_and_author(title, author)
    print(f"\nSearching for DOI by title and author: {title} by {author}")
    print(f"Found DOI: {doi}")

    # Example 3: Find detailed article information by title
    print(f"\nSearching for detailed information about: {title}")
    article_info = finder.find_article_info(title)
    if article_info:
        print("\nArticle Information:")
        print(f"Title: {article_info.title}")
        print(f"Authors: {', '.join(article_info.authors) if article_info.authors else 'N/A'}")
        print(f"Year: {article_info.year}")
        print(f"Journal: {article_info.journal or 'N/A'}")
        print(f"Publisher: {article_info.publisher or 'N/A'}")
        print(f"DOI: {article_info.doi}")
        print(f"URL: {article_info.url or 'N/A'}")
        print(f"Type: {article_info.type or 'N/A'}")
        if article_info.abstract:
            print(f"Abstract: {article_info.abstract[:200]}...")  # Show first 200 chars
    else:
        print("No detailed information found")
    
    # Example 4: Find DOI from BibTeX, especially for those from Google Scholar which does not include the doi
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
    dois = finder.find_from_bibtex(bibtex)
    print(f"\nSearching for DOI from BibTeX entry")
    print(f"Found DOIs: {dois}")
    
    # Example 5: Find detailed article information from BibTeX
    print(f"\nSearching for detailed information from BibTeX")
    articles_info = finder.find_article_info_from_bibtex(bibtex)
    if articles_info:
        print("\nArticle Information from BibTeX:")
        for article_info in articles_info:
            print(f"Title: {article_info.title}")
            print(f"Authors: {', '.join(article_info.authors) if article_info.authors else 'N/A'}")
            print(f"Year: {article_info.year}")
            print(f"Journal: {article_info.journal or 'N/A'}")
            print(f"Publisher: {article_info.publisher or 'N/A'}")
            print(f"DOI: {article_info.doi}")
    else:
        print("No detailed information found from BibTeX")

if __name__ == "__main__":
    main() 