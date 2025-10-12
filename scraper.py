"""Web scraping utilities."""

import time
from typing import Any
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


def fetch_page(
    url: str,
    timeout: int = 30,
    headers: dict[str, str] | None = None,
) -> BeautifulSoup:
    """Fetch a webpage and return parsed BeautifulSoup.

    Args:
        url: URL to fetch
        timeout: Request timeout in seconds
        headers: Optional headers dict

    Returns:
        Parsed BeautifulSoup object
    """
    default_headers = {
        "User-Agent": "Mozilla/5.0 (compatible; DataKit/1.0)"
    }
    if headers:
        default_headers.update(headers)

    response = requests.get(url, timeout=timeout, headers=default_headers)
    response.raise_for_status()

    return BeautifulSoup(response.content, "lxml")


def extract_text(soup: BeautifulSoup, selector: str) -> str:
    """Extract text from first element matching CSS selector.

    Returns empty string if no match.
    """
    element = soup.select_one(selector)
    return element.get_text(strip=True) if element else ""


def extract_texts(soup: BeautifulSoup, selector: str) -> list[str]:
    """Extract text from all elements matching CSS selector."""
    elements = soup.select(selector)
    return [el.get_text(strip=True) for el in elements]


def extract_attr(soup: BeautifulSoup, selector: str, attr: str) -> str | None:
    """Extract attribute value from first element matching CSS selector.

    Returns None if no match or attribute missing.
    """
    element = soup.select_one(selector)
    return element.get(attr) if element else None


def extract_attrs(soup: BeautifulSoup, selector: str, attr: str) -> list[str]:
    """Extract attribute values from all elements matching CSS selector.

    Skips elements where the attribute is missing.
    """
    elements = soup.select(selector)
    return [el.get(attr) for el in elements if el.get(attr)]


def extract_links(soup: BeautifulSoup, base_url: str = "") -> list[str]:
    """Extract all href values from anchor tags.

    If base_url provided, converts relative links to absolute.
    """
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if base_url:
            href = urljoin(base_url, href)
        links.append(href)
    return links


def extract_table(soup: BeautifulSoup, selector: str = "table") -> list[dict[str, str]]:
    """Extract table data into list of dicts.

    Args:
        soup: BeautifulSoup object
        selector: CSS selector for table

    Returns:
        List of dicts, one per row
    """
    table = soup.select_one(selector)
    if not table:
        return []

    # Get headers
    headers = []
    header_row = table.find("thead")
    if header_row:
        headers = [th.get_text(strip=True) for th in header_row.find_all(["th", "td"])]
    else:
        first_row = table.find("tr")
        if first_row:
            headers = [th.get_text(strip=True) for th in first_row.find_all(["th", "td"])]

    if not headers:
        return []

    # Get data rows
    result = []
    tbody = table.find("tbody") or table
    for row in tbody.find_all("tr")[1 if not table.find("thead") else 0:]:
        cells = [td.get_text(strip=True) for td in row.find_all(["td", "th"])]
        if cells:
            row_dict = dict(zip(headers, cells))
            result.append(row_dict)

    return result


class RateLimitedScraper:
    """Scraper with rate limiting.

    Automatically delays between requests to avoid hammering servers.
    """

    def __init__(self, delay: float = 1.0):
        """Initialize with delay between requests.

        Args:
            delay: Seconds to wait between requests
        """
        self.delay = delay
        self.last_request = 0.0

    def fetch(self, url: str, **kwargs) -> BeautifulSoup:
        """Fetch page, sleeping if needed to respect rate limit."""
        elapsed = time.time() - self.last_request
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)

        result = fetch_page(url, **kwargs)
        self.last_request = time.time()
        return result


def get_domain(url: str) -> str:
    """Extract domain (netloc) from URL.

    Example: "https://example.com/path" -> "example.com"
    """
    parsed = urlparse(url)
    return parsed.netloc
