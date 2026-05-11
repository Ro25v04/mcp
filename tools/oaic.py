from bs4 import BeautifulSoup
from mcp.server.fastmcp import FastMCP
from utils.scraper import session

BASE_URL = "https://www.oaic.gov.au"

KNOWN_TOPICS = {
    "data breach": "/privacy/notifiable-data-breaches",
    "australian privacy principles": "/privacy/australian-privacy-principles",
    "privacy impact assessment": "/privacy/privacy-impact-assessments",
    "credit reporting": "/privacy/credit-reporting",
}


def _fetch_oaic(topic: str) -> str:
    key = topic.lower().strip()

    path = None
    for known_name, known_path in KNOWN_TOPICS.items():
        if known_name in key or key in known_name:
            path = known_path
            break

    if not path:
        return f"Could not find OAIC guidance for: {topic}. Known topics: {', '.join(KNOWN_TOPICS.keys())}"

    url = BASE_URL + path
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        return f"Failed to fetch OAIC guidance from {url}: {e}"

    soup = BeautifulSoup(response.text, "lxml")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    main = soup.find("main") or soup.find("div", class_="content") or soup.body
    text = main.get_text(separator="\n", strip=True) if main else soup.get_text(separator="\n", strip=True)
    lines = [line for line in text.splitlines() if line.strip()]
    cleaned = "\n".join(lines[:200])

    return f"[oaic.gov.au - {topic}]\n\n{cleaned}"


def register(mcp: FastMCP):
    @mcp.tool()
    def fetch_oaic_guidance(topic: str) -> str:
        """Fetch privacy guidance from oaic.gov.au for a given topic."""
        return _fetch_oaic(topic)
