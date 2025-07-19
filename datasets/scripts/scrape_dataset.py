from typing import List
from bs4 import BeautifulSoup


def get_urls_for_other_cve_descriptions() -> List[str]:
    """
    Returns a list of sample URLs pointing to CVE description pages for scraping.
    """
    # Example: URLs from NVD or MITRE. In production, this could scrape an index or be dynamically generated.
    cve_urls = [
        "https://nvd.nist.gov/vuln/detail/CVE-2023-12345",
        "https://nvd.nist.gov/vuln/detail/CVE-2023-67890",
        "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-12345",
    ]
    return cve_urls


def get_content_from_url(url: str, timeout: int = 10) -> str:
    """
    Fetches and parses the main CVE description content from the given URL.
    Returns the extracted text or an empty string if failed.
    """
    import requests
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, "html.parser")
        # NVD example: description in <p data-testid="vuln-description">
        desc = soup.find("p", attrs={"data-testid": "vuln-description"})
        if desc:
            return desc.text.strip()
        # MITRE example: description in <td valign="top"> after 'Description'
        for td in soup.find_all("td", valign="top"):
            if "Description" in td.text:
                next_td = td.find_next_sibling("td")
                if next_td:
                    return next_td.text.strip()
        # Fallback: return all visible text
        return soup.get_text(separator=" ", strip=True)
    except Exception as e:
        print(f"[ERROR] Failed to fetch or parse {url}: {e}")
        return ""
