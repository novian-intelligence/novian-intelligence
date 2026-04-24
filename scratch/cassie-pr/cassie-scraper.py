#!/usr/bin/env python3
"""
cassie-scraper.py — PR/Media Archive Scraper for DJ Cassandra (Cassie Shankman)
Novian Intelligence Client Tool | v1.0.0

Usage:
    python3 cassie-scraper.py [--output results.json] [--query "custom term"]

Requirements:
    pip install requests google-generativeai python-dateutil

Configuration:
    Set GEMINI_API_KEY env var or pass via --gemini-key flag.
    Optionally set GOOGLE_CSE_API_KEY and GOOGLE_CSE_ID for Custom Search Engine.
"""

import os
import json
import hashlib
import argparse
import datetime
import time
import re
from pathlib import Path
from urllib.parse import urlparse

# ── Third-party (install if missing) ──────────────────────────────────────────
try:
    import requests
except ImportError:
    print("[!] Missing: pip install requests")
    raise

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("[!] google-generativeai not installed — AI classification disabled. pip install google-generativeai")

# ── Configuration ─────────────────────────────────────────────────────────────

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyDP0c4c554HaQXwRmWG_BuHXA7WohrF49g")
GOOGLE_CSE_API_KEY = os.getenv("GOOGLE_CSE_API_KEY", "")  # Optional: Google Custom Search
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID", "")            # Optional: CSE ID

OUTPUT_PATH = Path(__file__).parent / "results.json"

# ── Search Terms ───────────────────────────────────────────────────────────────

SEARCH_TERMS = [
    # Core identity searches
    '"DJ Cassandra" Austin',
    '"DJ Cassandra" wedding',
    '"DJ Cassandra" Texas',
    '"Sounds by Cassandra"',
    '"Sounds by Cassandra" DJ',
    '"Cassie Shankman" DJ',
    '"Cassie Shankman" Austin',
    '"DJ Cassie Shankman"',
    '"CASS&RA" DJ Austin',
    '"CASS&RA" music',
    '"@djcassandra_"',
    '"Cassie F1"',
    # Geographic combos
    '"DJ Cassandra" Dallas',
    '"DJ Cassandra" DFW',
    '"DJ Cassandra" Southlake',
    '"Cassie Shankman" Texas',
    # Source-specific
    'site:theknot.com "DJ Cassandra"',
    'site:weddingwire.com "DJ Cassandra"',
    'site:weddingwire.com "Cassie Shankman"',
    'site:theknot.com "Sounds by Cassandra"',
    'site:instagram.com djcassandra_',
    'site:junebugweddings.com "DJ Cassandra"',
    # Press / editorial
    '"Cassie Shankman" "Teen Vogue"',
    '"Cassie Shankman" "Wall Street Journal"',
    '"Cassie Shankman" "New York Magazine"',
    '"Cassie Shankman" SXSW',
    '"DJ Cassandra" KVUE',
    '"Cassie Shankman" KXAN',
    '"Cassie Shankman" "Austin Business Journal"',
    '"Cassie Shankman" Lululemon',
]

# ── Tier Classification ────────────────────────────────────────────────────────

TIER1_DOMAINS = [
    "vogue.com", "teenvogue.com", "wsj.com", "thecut.com", "nytimes.com",
    "washingtonpost.com", "rollingstone.com", "billboard.com", "forbes.com",
    "glamour.com", "cosmopolitan.com", "brides.com", "marthastewartweddings.com",
    "theknot.com", "weddingwire.com", "people.com", "usweekly.com",
    "spotify.com", "recordingacademy.com", "grammy.com", "lululemon.com",
    "gucci.com", "google.com", "apple.com",
]

TIER2_DOMAINS = [
    "kvue.com", "kxan.com", "studio512.com", "statesman.com", "bizjournals.com",
    "austinchamber.com", "do512.com", "junebugweddings.com", "lovestories.tv",
    "sxsw.com", "kmfa.org", "texasperformingarts.org", "austinmonthly.com",
    "dallasnews.com", "dmagazine.com", "fort-worth.com", "culturemap.com",
    "benkweller.com", "soundcloud.com", "youtube.com", "tiktok.com",
    "reddit.com", "twitter.com", "x.com",
]

CATEGORY_PATTERNS = {
    "Press/Editorial": [
        r"(article|feature|profile|interview|story|news|award|finalist|governor|panelist|speaker)",
        r"(magazine|journal|newspaper|media|press|editorial|publication)",
    ],
    "Wedding Feature": [
        r"(wedding|bride|groom|nuptial|ceremony|reception|marriage|matrimon)",
        r"(theknot|weddingwire|junebug|zola|bridal|venue)",
    ],
    "Event Listing": [
        r"(sxsw|event|concert|festival|show|performance|live|set|gig|tour|opening)",
        r"(venue|stage|lineup|ticket|booking)",
    ],
    "Social Mention": [
        r"(instagram|twitter|tiktok|facebook|social|mention|tag|post|playlist|spotify)",
        r"(ambassador|lululemon|brand|partnership|collab)",
    ],
    "Review/Testimonial": [
        r"(review|testimonial|rating|stars|couple|client|feedback|recommend)",
    ],
    "Photo Feature": [
        r"(photo|photography|image|gallery|lookbook|styled|shoot)",
        r"(lovestories|visual|editorial photo)",
    ],
}

# ── Helper Functions ───────────────────────────────────────────────────────────

def classify_tier(url: str) -> tuple[str, str]:
    """Classify a URL into Tier 1, 2, or 3."""
    domain = urlparse(url).netloc.lower().lstrip("www.")
    for d in TIER1_DOMAINS:
        if d in domain:
            return "Tier 1", f"Major publication/platform ({domain})"
    for d in TIER2_DOMAINS:
        if d in domain:
            return "Tier 2", f"Regional/industry source ({domain})"
    return "Tier 3", f"Blog/social/other ({domain})"


def classify_category(title: str, snippet: str, url: str) -> str:
    """Rule-based category classification."""
    text = f"{title} {snippet} {url}".lower()
    scores = {}
    for category, patterns in CATEGORY_PATTERNS.items():
        score = sum(1 for p in patterns if re.search(p, text, re.I))
        scores[category] = score
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "Press/Editorial"


def classify_sentiment(title: str, snippet: str) -> str:
    """Simple rule-based sentiment."""
    positive_words = [
        "award", "finalist", "feature", "ambassador", "recognized", "named",
        "best", "top", "leading", "talented", "incredible", "love", "amazing",
        "honored", "elected", "curated", "spotlight", "celebrated", "prestigious"
    ]
    negative_words = [
        "complaint", "problem", "issue", "fail", "bad", "wrong", "poor"
    ]
    text = f"{title} {snippet}".lower()
    pos = sum(1 for w in positive_words if w in text)
    neg = sum(1 for w in negative_words if w in text)
    if neg > pos:
        return "Negative"
    elif pos > 0:
        return "Positive"
    return "Neutral"


def classify_with_gemini(title: str, snippet: str, url: str) -> dict:
    """Use Gemini to classify a result if available."""
    if not GEMINI_AVAILABLE or not GEMINI_API_KEY:
        return {}
    
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""You are classifying press mentions for DJ Cassandra (Cassie Shankman), an Austin-based DJ/producer.

Result:
Title: {title}
URL: {url}
Snippet: {snippet}

Respond with ONLY a JSON object with these fields:
- category: one of ["Press/Editorial", "Wedding Feature", "Social Mention", "Event Listing", "Review/Testimonial", "Photo Feature"]
- sentiment: one of ["Positive", "Neutral", "Negative"]
- relevance_note: one sentence explaining why this matters for her PR

JSON only, no markdown:"""
        
        response = model.generate_content(prompt)
        text = response.text.strip()
        # Strip markdown code fences if present
        text = re.sub(r'^```json?\s*', '', text).rstrip('`').strip()
        return json.loads(text)
    except Exception as e:
        print(f"  [Gemini] Classification failed: {e}")
        return {}


def search_google_cse(query: str) -> list[dict]:
    """Search using Google Custom Search Engine API."""
    if not GOOGLE_CSE_API_KEY or not GOOGLE_CSE_ID:
        return []
    
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_CSE_API_KEY,
        "cx": GOOGLE_CSE_ID,
        "q": query,
        "num": 10,
    }
    
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data.get("items", [])
    except Exception as e:
        print(f"  [CSE] Search failed for '{query}': {e}")
        return []


def search_fallback_fetch(query: str) -> list[dict]:
    """Fetch results from DuckDuckGo lite as fallback (no API key needed)."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        url = "https://html.duckduckgo.com/html/"
        resp = requests.post(url, data={"q": query}, headers=headers, timeout=15)
        
        # Parse results from HTML
        results = []
        # Simple regex to extract results (DDG HTML is predictable)
        pattern = r'class="result__a"[^>]*href="([^"]+)"[^>]*>([^<]+)<.*?class="result__snippet"[^>]*>([^<]+)<'
        matches = re.findall(pattern, resp.text, re.DOTALL)
        
        for href, title, snippet in matches[:5]:
            # DDG wraps links — extract actual URL
            actual_url = href
            if "uddg=" in href:
                from urllib.parse import unquote, parse_qs, urlparse
                parsed = urlparse(href)
                qs = parse_qs(parsed.query)
                actual_url = unquote(qs.get("uddg", [href])[0])
            
            results.append({
                "link": actual_url,
                "title": title.strip(),
                "snippet": snippet.strip(),
            })
        
        return results
    except Exception as e:
        print(f"  [DDG] Fallback search failed for '{query}': {e}")
        return []


def generate_id(url: str, title: str) -> str:
    """Generate a stable ID from URL + title."""
    raw = f"{url}{title}"
    return "r" + hashlib.md5(raw.encode()).hexdigest()[:8]


def process_result(raw: dict) -> dict:
    """Convert a raw search result into a classified PR entry."""
    url = raw.get("link", raw.get("url", ""))
    title = raw.get("title", "")
    snippet = raw.get("snippet", raw.get("description", ""))
    date = raw.get("date", raw.get("pagemap", {}).get("metatags", [{}])[0].get("date", ""))
    
    tier, tier_reason = classify_tier(url)
    category = classify_category(title, snippet, url)
    sentiment = classify_sentiment(title, snippet)
    
    # Attempt AI enhancement
    ai_data = classify_with_gemini(title, snippet, url)
    if ai_data:
        category = ai_data.get("category", category)
        sentiment = ai_data.get("sentiment", sentiment)
    
    domain = urlparse(url).netloc.lower().lstrip("www.")
    source_name = domain.replace(".com", "").replace(".org", "").replace(".tv", "").replace("-", " ").title()
    
    return {
        "id": generate_id(url, title),
        "url": url,
        "title": title,
        "source": source_name,
        "source_domain": domain,
        "date": date or "",
        "date_display": date or "Unknown",
        "snippet": snippet,
        "category": category,
        "sentiment": sentiment,
        "tier": tier,
        "tier_reason": tier_reason,
        "verified": False,
        "ai_note": ai_data.get("relevance_note", ""),
        "source_logo_initial": source_name[:2].upper(),
        "source_color": "#888888",
    }


def deduplicate(results: list[dict]) -> list[dict]:
    """Remove duplicate URLs, keeping first occurrence."""
    seen = set()
    unique = []
    for r in results:
        if r["url"] not in seen:
            seen.add(r["url"])
            unique.append(r)
    return unique


# ── Main Scraper ───────────────────────────────────────────────────────────────

def run_scrape(output_path: Path, custom_query: str | None = None):
    """Run the full scrape and save results."""
    print("=" * 60)
    print("  Cassie PR Scraper — Novian Intelligence")
    print(f"  {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    terms = [custom_query] if custom_query else SEARCH_TERMS
    all_raw = []
    
    for i, term in enumerate(terms):
        print(f"\n[{i+1}/{len(terms)}] Searching: {term}")
        
        # Try Google CSE first, fall back to DDG
        results = search_google_cse(term)
        if not results:
            print("  → Falling back to DuckDuckGo...")
            results = search_fallback_fetch(term)
        
        print(f"  → Found {len(results)} results")
        all_raw.extend(results)
        
        # Rate limiting
        time.sleep(1.5)
    
    print(f"\n[Processing] {len(all_raw)} total raw results → classifying...")
    
    processed = []
    for raw in all_raw:
        try:
            entry = process_result(raw)
            processed.append(entry)
        except Exception as e:
            print(f"  [!] Failed to process result: {e}")
    
    processed = deduplicate(processed)
    print(f"[Dedup] {len(processed)} unique results after deduplication")
    
    # Load existing results and merge (preserving verified entries)
    existing = []
    if output_path.exists():
        try:
            with open(output_path) as f:
                data = json.load(f)
                existing = data.get("results", [])
                # Keep verified/manually added entries
                existing_verified = [r for r in existing if r.get("verified")]
                existing_ids = {r["id"] for r in existing_verified}
                new_entries = [r for r in processed if r["id"] not in existing_ids]
                final = existing_verified + new_entries
                print(f"[Merge] {len(existing_verified)} existing verified + {len(new_entries)} new = {len(final)} total")
        except Exception:
            final = processed
    else:
        final = processed
    
    output = {
        "meta": {
            "client": "DJ Cassandra (Cassie Shankman)",
            "scraped_at": datetime.datetime.now().isoformat(),
            "scraper_version": "1.0.0",
            "search_terms_used": terms,
            "sources_checked": list(set(
                urlparse(r.get("url", "")).netloc for r in all_raw if r.get("url")
            )),
            "total_results": len(final),
        },
        "results": final,
    }
    
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    print(f"\n✅ Saved {len(final)} results to: {output_path}")
    
    # Summary
    by_tier = {}
    by_category = {}
    for r in final:
        t = r.get("tier", "Unknown")
        c = r.get("category", "Unknown")
        by_tier[t] = by_tier.get(t, 0) + 1
        by_category[c] = by_category.get(c, 0) + 1
    
    print("\n📊 Summary by Tier:")
    for t, count in sorted(by_tier.items()):
        print(f"   {t}: {count}")
    
    print("\n📁 Summary by Category:")
    for c, count in sorted(by_category.items()):
        print(f"   {c}: {count}")
    
    return output


# ── CLI Entry Point ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="DJ Cassandra PR/Media Scraper — Novian Intelligence"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=OUTPUT_PATH,
        help="Output JSON file path (default: results.json in script directory)"
    )
    parser.add_argument(
        "--query", "-q",
        type=str,
        default=None,
        help="Single custom query to run (skips all default terms)"
    )
    parser.add_argument(
        "--gemini-key",
        type=str,
        default=None,
        help="Gemini API key (overrides env var GEMINI_API_KEY)"
    )
    parser.add_argument(
        "--cse-key",
        type=str,
        default=None,
        help="Google CSE API key (overrides env var GOOGLE_CSE_API_KEY)"
    )
    parser.add_argument(
        "--cse-id",
        type=str,
        default=None,
        help="Google CSE ID (overrides env var GOOGLE_CSE_ID)"
    )
    
    args = parser.parse_args()
    
    if args.gemini_key:
        GEMINI_API_KEY = args.gemini_key
    if args.cse_key:
        GOOGLE_CSE_API_KEY = args.cse_key
    if args.cse_id:
        GOOGLE_CSE_ID = args.cse_id
    
    run_scrape(args.output, args.query)
