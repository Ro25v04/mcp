from bs4 import BeautifulSoup
from mcp.server.fastmcp import FastMCP
from utils.scraper import session

LIVE_SOURCES = {
    "fair work act 2009": "https://www.austlii.edu.au/au/legis/cth/consol_act/fwa2009114/",
    "national employment standards": "https://www.austlii.edu.au/au/legis/cth/consol_act/fwa2009114/",
    "unpaid internship": "https://www.austlii.edu.au/au/legis/cth/consol_act/fwa2009114/",
    "privacy act 1988": "https://www.oaic.gov.au/privacy/australian-privacy-principles",
    "australian privacy principles": "https://www.oaic.gov.au/privacy/australian-privacy-principles",
    "notifiable data breach": "https://www.oaic.gov.au/privacy/notifiable-data-breaches",
    "work health and safety act 2011": "https://www.austlii.edu.au/au/legis/cth/consol_act/whaas2011218/",
    "australian consumer law": "https://www.austlii.edu.au/au/legis/cth/consol_act/caca2010265/",
    "competition and consumer act 2010": "https://www.austlii.edu.au/au/legis/cth/consol_act/caca2010265/",
    "superannuation guarantee act 1992": "https://www.austlii.edu.au/au/legis/cth/consol_act/sgaa1992237/",
    "spam act 2003": "https://www.austlii.edu.au/au/legis/cth/consol_act/sa200386/",
}

STATIC_FALLBACK = {
    "fair work act 2009": """Fair Work Act 2009 - Key provisions for internships and employment:
- Unpaid work is only lawful as a genuine vocational placement authorised by an educational institution
- Interns performing productive work that benefits the employer must be paid minimum wage
- The primary benefit must flow to the intern (training/learning), not the employer
- National Employment Standards (NES) apply to all employees regardless of contract terms
- Labelling an arrangement as 'internship' does not override employee entitlements if the substance is employment
- Employers cannot contract out of minimum wage, leave entitlements, or superannuation obligations
- Minimum wage as of 2024: $23.23 per hour""",

    "privacy act 1988": """Privacy Act 1988 - Australian Privacy Principles (APPs):
- APP 1: Open and transparent management of personal information
- APP 3: Collection of solicited personal information — only collect what is necessary
- APP 5: Notification of collection — individuals must be notified of collection and purpose
- APP 6: Use or disclosure — only use information for the purpose it was collected
- APP 11: Security of personal information — must take reasonable steps to protect from misuse
- APP 12: Access to personal information — individuals have right to access their information
- Notifiable Data Breaches: must notify OAIC and affected individuals of eligible breaches within 30 days""",

    "work health and safety act 2011": """Work Health and Safety Act 2011 - Key duties:
- Primary duty of care: ensure health and safety of workers, including volunteers and interns
- Must eliminate or minimise risks so far as reasonably practicable
- Provide safe systems of work, adequate facilities, information, training, and supervision
- Workers must be consulted on health and safety matters
- Serious incidents must be reported to the regulator immediately
- Officers must exercise due diligence to ensure compliance
- Applies to all persons at a workplace, not just employees""",

    "australian consumer law": """Australian Consumer Law (Competition and Consumer Act 2010):
- Prohibits misleading or deceptive conduct in trade or commerce
- Unfair contract terms in standard form consumer contracts are void
- Consumer guarantees cannot be excluded by contract
- Prohibition on unconscionable conduct
- Mandatory remedies: repair, replacement, or refund
- Liability limitation clauses may be unenforceable if they constitute unfair contract terms""",

    "superannuation guarantee act 1992": """Superannuation Guarantee (Administration) Act 1992:
- Employers must contribute 11.5% of ordinary time earnings (2024-25 rate)
- Applies to employees and some contractors paid wholly for labour
- Contributions must be made quarterly to a complying fund
- Genuine unpaid interns are not employees and not entitled to superannuation
- If internship is found to be employment, super obligations apply retrospectively
- Failure to pay attracts Superannuation Guarantee Charge payable to ATO""",

    "spam act 2003": """Spam Act 2003 - Key requirements:
- Commercial emails must only be sent with recipient consent (express or inferred)
- Messages must clearly identify the sender with accurate contact details
- Must include a functional unsubscribe mechanism
- Unsubscribe requests must be honoured within 5 business days
- Applies to emails, SMS, and instant messages with Australian links
- Penalties up to $2.2 million per day for serious or repeated breaches""",
}

_cache: dict[str, str] = {}


def _scrape_url(url: str) -> str:
    response = session.get(url, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    main = soup.find("main") or soup.find("article") or soup.find("div", class_="content") or soup.body
    text = main.get_text(separator="\n", strip=True) if main else soup.get_text(separator="\n", strip=True)
    lines = [line for line in text.splitlines() if line.strip()]
    return "\n".join(lines[:300])


def _fetch_legislation(act_name: str) -> str:
    key = act_name.lower().strip()

    if key in _cache:
        return _cache[key]

    url = None
    matched_key = None
    for known_name, known_url in LIVE_SOURCES.items():
        if known_name in key or key in known_name:
            url = known_url
            matched_key = known_name
            break

    if not url:
        return f"Could not find legislation for: {act_name}. Known acts: {', '.join(set(LIVE_SOURCES.keys()))}"

    try:
        text = _scrape_url(url)
        result = f"[Live data - {matched_key} from {url}]\n\n{text}"
        _cache[key] = result
        return result
    except Exception:
        pass

    for fallback_key, fallback_text in STATIC_FALLBACK.items():
        if fallback_key in key or key in fallback_key:
            result = f"[Legislation summary - {fallback_key}]\n\n{fallback_text}"
            _cache[key] = result
            return result

    return f"Could not fetch legislation for {act_name}. Please try again later."


def register(mcp: FastMCP):
    @mcp.tool()
    def fetch_legislation_tool(act_name: str) -> str:
        """Fetch Australian legislation summaries from legislation.gov.au and other government sources."""
        return _fetch_legislation(act_name)
