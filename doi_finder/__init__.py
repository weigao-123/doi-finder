"""
DOI Finder - A package to find Digital Object Identifiers for academic articles using CrossRef API.
"""

import requests
import bibtexparser
import re
from typing import Optional, List
from dataclasses import dataclass

@dataclass
class ArticleInfo:
    """Data class to store article information."""
    doi: Optional[str] = None
    title: Optional[str] = None
    authors: Optional[List[str]] = None
    year: Optional[int] = None
    journal: Optional[str] = None
    publisher: Optional[str] = None
    url: Optional[str] = None
    abstract: Optional[str] = None
    citation_count: Optional[int] = None
    type: Optional[str] = None  # article, book, conference paper, etc.

class DOIFinder:
    def __init__(self, mailto_email=None):
        """
        Initialize the DOI Finder with necessary configurations.
        
        Args:
            mailto_email (str, optional): Email to send to CrossRef API for improved rate limits.
                                         See: https://github.com/CrossRef/rest-api-doc#good-manners--more-reliable-service
        """
        self.headers = {
            'User-Agent': 'DOIFinder/0.1.0 (https://github.com/yourusername/doi_finder; mailto:{})'.format(
                mailto_email if mailto_email else "anonymous@example.com"
            )
        }
        
    def find_by_title(self, title: str, clean_title: bool = True) -> Optional[str]:
        """
        Find DOI for an article by its title.
        
        Args:
            title (str): The title of the article
            clean_title (bool): Whether to clean/normalize the title before searching
            
        Returns:
            Optional[str]: The DOI if found, None otherwise
        """
        doi = self.find_by_metadata(title, clean_title=clean_title)
        if doi:
            return doi
        return None
    
    def find_by_title_and_author(self, title: str, author: str, clean_title: bool = True) -> Optional[str]:
        """
        Find DOI for an article by its title and author.
        """
        doi = self.find_by_metadata(title, author=author, clean_title=clean_title)
        if doi:
            return doi
        return None
    
    def find_by_metadata(self, title: str, author: Optional[str] = None, clean_title: bool = True) -> Optional[str]:
        """
        Find DOI for an article by its title and author.
        """
        # Try CrossRef API first
        if clean_title:
            title = title.lower().strip()
            # remove extra spaces
            title = re.sub(r'\s+', ' ', title)
        doi = self._search_crossref_by_metadata(title, author)
        if doi:
            return doi
        return None
    
    def find_article_info(self, title: str, author: Optional[str] = None) -> Optional[ArticleInfo]:
        """
        Find detailed article information by title.
        
        Args:
            title (str): The title of the article
            
        Returns:
            Optional[ArticleInfo]: Article information if found, None otherwise
        """
        # Try CrossRef API first
        article_infos = self._search_crossref_detailed(title, author)
        if article_infos:
            return article_infos
    
    def find_from_bibtex(self, bibtex_str: str, use_metadata: bool = True) -> Optional[List[str]]:
        """
        Find DOIs from a BibTeX entry.
        
        Args:
            bibtex_str (str): The BibTeX entry as a string
            use_metadata (bool): Whether to use metadata (beside title) to help find the DOI

        Returns:
            Optional[List[str]]: The DOIs if found, None otherwise
        """
        try:
            bib_database = bibtexparser.parse_string(bibtex_str)
        except Exception as e:
            print(f"Error parsing BibTeX: {e}")
            return None
            
        if not bib_database.entries:
            return None

        dois = []
        for entry in bib_database.entries:
            # First check if DOI is directly in the BibTeX
            if 'doi' in entry:
                dois.append(entry['doi'])
                
            # If no DOI, try to find it using the title
            if 'title' in entry:
                author = None
                year = None
                if use_metadata:
                    if 'author' in entry:
                        author = entry['author']
                    if 'year' in entry:
                        year = entry['year']
                dois.append(self.find_by_metadata(entry['title'], author=author))
        return dois
    
    def find_article_info_from_bibtex(self, bibtex_str: str) -> Optional[List[ArticleInfo]]:
        """
        Find detailed article information from a BibTeX entry.
        
        Args:
            bibtex_str (str): The BibTeX entry as a string
            
        Returns:
            Optional[List[ArticleInfo]]: Article information if found, None otherwise
        """
        try:
            bib_database = bibtexparser.parse_string(bibtex_str)
        except Exception as e:
            print(f"Error parsing BibTeX: {e}")
            return None
            
        if not bib_database.entries:
            return None
                
        article_infos = []
        for entry in bib_database.entries:
            # First check if DOI is directly in the BibTeX
            if 'doi' in entry:
                # Use the DOI to get detailed information
                article_infos.append(self._search_crossref_by_doi(entry['doi']))
                
            # If no DOI, try to find it using the title
            if 'title' in entry:
                article_infos.append(self.find_article_info(entry['title']))
            
        return article_infos
    
    def _search_crossref_by_metadata(self, title: str, author: Optional[str] = None) -> Optional[str]:
        """Search CrossRef API for the DOI."""
        url = "https://api.crossref.org/works"

        params = {
            "query.title": title,
            "rows": 5,  # Increased rows for better matching
            "sort": "score",  # Sort by relevance score
            "order": "desc"
        }

        if author:
            params["query.author"] = author
        
        try:
            response = requests.get(url, params=params, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                if data['message']['items']:
                    # Look through the top results to find the best title match
                    for item in data['message']['items']:
                        if 'title' in item and item['title']:
                            # if title is exactly the same, return the DOI
                            _sanitized_title = self._get_sanitized_title(title)
                            _sanitized_item_title = self._get_sanitized_title(item['title'][0])
                            if _sanitized_title == _sanitized_item_title:
                                return item['DOI']
                    
        except Exception as e:
            print(f"Error searching CrossRef: {e}")
            
        return None
    
    def _search_crossref_by_doi(self, doi: str) -> Optional[ArticleInfo]:
        """Search CrossRef API for detailed article information using DOI."""
        try:
            url = f"https://api.crossref.org/works/{doi}"
            
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                item = data['message']
                
                # Extract authors
                authors = []
                if 'author' in item:
                    for author in item['author']:
                        if 'given' in author and 'family' in author:
                            authors.append(f"{author['given']} {author['family']}")
                        elif 'family' in author:
                            authors.append(author['family'])
                
                # Extract year
                year = None
                if 'published-print' in item:
                    year = item['published-print']['date-parts'][0][0]
                elif 'published-online' in item:
                    year = item['published-online']['date-parts'][0][0]
                elif 'created' in item:
                    year = item['created']['date-parts'][0][0]
                
                return ArticleInfo(
                    doi=item.get('DOI'),
                    title=item.get('title', [None])[0],
                    authors=authors,
                    year=year,
                    journal=item.get('container-title', [None])[0] if item.get('container-title') else None,
                    publisher=item.get('publisher'),
                    url=item.get('URL'),
                    abstract=item.get('abstract'),
                    type=item.get('type')
                )
                    
        except Exception as e:
            print(f"Error searching CrossRef by DOI: {e}")
            
        return None
    
    def _search_crossref_detailed(self, title: str, author: Optional[str] = None) -> Optional[ArticleInfo]:
        """Search CrossRef API for detailed article information."""
        url = "https://api.crossref.org/works"
        params = {
            "query.title": title,
            "rows": 5,  # Increased rows for better matching
            "sort": "score",  # Sort by relevance score
            "order": "desc"
        }

        if author:
            params["query.author"] = author

        try:
            response = requests.get(url, params=params, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                if data['message']['items']:
                    # Look through the top results to find the best title match
                    for item in data['message']['items']:
                        if 'title' in item and item['title']:
                            # Exact match but only characters are important
                            _sanitized_title = self._get_sanitized_title(title)
                            _sanitized_item_title = self._get_sanitized_title(item['title'][0])
                            if _sanitized_title == _sanitized_item_title:
                                # Extract authors
                                authors = []
                                if 'author' in item:
                                    for author in item['author']:
                                        if 'given' in author and 'family' in author:
                                            authors.append(f"{author['given']} {author['family']}")
                                        elif 'family' in author:
                                            authors.append(author['family'])
                                
                                # Extract year
                                year = None
                                if 'published-print' in item:
                                    year = item['published-print']['date-parts'][0][0]
                                elif 'published-online' in item:
                                    year = item['published-online']['date-parts'][0][0]
                                elif 'created' in item:
                                    year = item['created']['date-parts'][0][0]
                                
                                return ArticleInfo(
                                    doi=item.get('DOI'),
                                    title=item.get('title', [None])[0],
                                    authors=authors,
                                    year=year,
                                    journal=item.get('container-title', [None])[0] if item.get('container-title') else None,
                                    publisher=item.get('publisher'),
                                    url=item.get('URL'),
                                    abstract=item.get('abstract'),
                                    type=item.get('type')
                                )
                    
        except Exception as e:
            print(f"Error searching CrossRef: {e}")
            
        return None
    
    def _get_sanitized_title(self, title: str) -> str:
        """Sanitize the title by removing special characters and converting to lowercase."""
        _sanitized_title = title.lower().strip()
        # remove special characters using regex
        _sanitized_title = re.sub(r'[^\w\s]', '', _sanitized_title)
        # remove all spaces
        _sanitized_title = re.sub(r'\s+', '', _sanitized_title)
        return _sanitized_title

# Export the classes
__all__ = ['DOIFinder', 'ArticleInfo']