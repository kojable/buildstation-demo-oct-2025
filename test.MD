
You are refactoring the backend workflow.  
The goal is to replace the legacy metadata extraction logic 
(C:\Users\piush\Desktop\decoding-tool\backend\app\api\metadata.py) 
with a new context-based approach using `context_builder.py`. --- 
**  
Tasks to Perform:** 
1. **Replace `metadata.py` with `context_builder.py`:** - Remove all references to `metadata.py` and its API route 
`/api/metadata/extract`. - Integrate `context_builder.py` as the new backend module. 
2. **Update `url_analysis.py` workflow:** - Remove the call to `extract_url_metadata(url)` and any metadata 
confirmation logic. - Instead, use `extract_website_metadata(url)` from 
`context_builder.py` to gather initial context. - Ask the user for `country` and `language` (already implemented 
C:\Users\piush\Desktop\decoding-tool\backend\app\api\regions.py). - Use `build_people_also_ask_prompt(...)` from 
`context_builder.py` to generate prompts using: - Extracted metadata - Search snippets (from `search_google(...)` and 
`collect_snippets(...)`) - Country - Language - -                 
INput text from C:\Users\piush\Desktop\decoding
tool\frontend\src\pages\workflow\URLInputPage.tsx if provide 
(( <FormGroup role="group" aria-labelledby="description-label"> 
<Label id="description-label" htmlFor="description"> -                   
Tell us about your brand <OptionalBadge aria
label="optional field">(optional)</OptionalBadge> -                 
</Label> -                 
<TextareaWrapper> -                   
<Textarea -                     
id="description" -                     
placeholder="About your brand..." -                     
value={form.formData.description} 
-                     
onChange={(e) => 
form.handleFieldChange('description', e.target.value)} -                     
onBlur={() => form.handleFieldBlur('description')} -                     
$hasError={!!form.errors.description} -                     
disabled={isSubmitting} -                     
maxLength={DESCRIPTION_MAX_LENGTH + 50} -                     
aria-invalid={!!form.errors.description} -                     
aria-describedby="description-help" -                   
/> -                 
</TextareaWrapper> -                 
<HelpText id="description-help"> -                   
The more specific you are, the better the results 
we'll be able to provide. -                   
<ul> -                     
<li>What products or services do you offer?</li> -                     
<li>Do you serve any specific regions?</li> -                   
</ul> -                 
</HelpText> -                 
{form.errors.description && ( -                   
<ErrorMessage id="description-error" 
role="alert">{form.errors.description}</ErrorMessage> -                 
)} -               
</FormGroup> - 
)) 
3. **Update grounding logic:** - Ensure the grounding step uses the new context instead of 
legacy metadata. - Update 
`google_search_service.process_prompts_with_grounding(...)` to 
accept the new context format if needed. 
4. **Update response payload:** - Replace `"metadata"` with `"context"` if appropriate. - Ensure `"prompts_used"` and `"grounded_responses"` are still 
included. - Remove `"metadata_extraction_time"` or rename it to 
`"context_extraction_time"`. 
5. **Update dashboard integration:** - Ensure the dashboard payload reflects the new context 
structure. - Maintain compatibility with existing fields like `workflowId`, 
`email`, `prompts`, and `responses`. 
 --- 
 
**      New Workflow Structure:** 
 
URL → Extract Context → Ask Country & Language → Generate Prompts → Execute 
Grounded Searches → Aggregate Results → Dashboard 
**   Expectations:** - Maintain logging and error handling as shown in both files. -  
Ensure the new prompt generation logic aligns with the rules defined in 
`build_people_also_ask_prompt(...)`. - Preserve compatibility with existing frontend 
request formats and dashboard storage logic.  
 
Context_builder.py 
"""Utilities for extracting website context and building Gemini prompts."""

from __future__ import annotations

import logging
import textwrap
import unicodedata
from typing import Any, Dict, List, Optional

import requests
from bs4 import BeautifulSoup

LOGGER = logging.getLogger(__name__)


def extract_website_metadata(url: str, *, timeout: int = 10) -> Dict[str, Any]:
    """Scrape basic metadata and headings from a website."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome Safari"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException as exc:  # noqa: BLE001
        LOGGER.error("Failed to fetch %s: %s", url, exc)
        return {}

    soup = BeautifulSoup(response.content, "html.parser")
    metadata: Dict[str, Any] = {
        "title": _text_or_empty(soup.find("title")),
        "description": _meta_content(soup, {"name": "description"}),
        "keywords": _split_keywords(_meta_content(soup, {"name": "keywords"})),
        "og_title": _meta_content(soup, {"property": "og:title"}),
        "og_description": _meta_content(soup, {"property": "og:description"}),
        "twitter_title": _meta_content(soup, {"name": "twitter:title"}),
        "twitter_description": _meta_content(soup, {"name": "twitter:description"}),
        "headings": _collect_headings(soup),
    }

    combined = [
        metadata["title"],
        metadata["description"],
        ", ".join(metadata["keywords"]),
    ]
    if metadata["og_description"] and metadata["og_description"] != metadata["description"]:
        combined.append(metadata["og_description"])
    if metadata["twitter_description"] and metadata["twitter_description"] not in {
        metadata["description"],
        metadata["og_description"],
    }:
        combined.append(metadata["twitter_description"])
    metadata["combined_text"] = " ".join(filter(None, combined))
    return metadata


def build_search_query(
    query: str,
    *,
    site: Optional[str] = None,
    prefix: str = "",
    suffix: str = "",
    exact: bool = False,
    normalize: bool = True,
    exclude_site: Optional[str] = None,  # NEW
    competitors_mode: bool = False,  # NEW
    autodetect_competitors: bool = True,  # NEW: auto-enable competitor discovery for brand-like queries
) -> str:
    """Construct a search query with optional site restriction, prefix/suffix and exact phrase.

    - site: if provided, prepends "site:<site>" to the query
    - exclude_site: if provided, adds "-site:<site>" to exclude results from that domain
    - exact: wrap the query in quotes for exact phrase match
    - prefix/suffix: arbitrary strings to add before/after the core query
    - normalize: runs normalize_query() to strip non-ASCII by default
    - competitors_mode: optimizes query for finding competitor brand names
    - autodetect_competitors: if True, automatically enables competitors_mode for queries that look like brand names
    """
    q = query.strip() or ""

    def _looks_like_brand(name: str) -> bool:
        """Quick heuristic to detect if a query looks like a brand name.

        Rules:
        - 1-3 tokens
        - At least one token starts with an uppercase letter
        - Not all tokens are common stopwords (like 'best', 'top')
        """
        if not name:
            return False
        tokens = [t for t in name.split() if t.strip()]
        if len(tokens) == 0 or len(tokens) > 3:
            return False
        stopwords = {
            "the",
            "a",
            "an",
            "best",
            "top",
            "cheapest",
            "buy",
            "reviews",
            "review",
            "compare",
            "comparison",
        }
        cap_tokens = sum(1 for t in tokens if t and t[0].isupper())
        if cap_tokens < 1:
            return False
        if all(t.lower() in stopwords for t in tokens):
            return False
        return True

    # Autodetect brand-like queries and set competitor mode if not explicitly provided
    if autodetect_competitors and not competitors_mode and q:
        try:
            if _looks_like_brand(q):
                competitors_mode = True
        except Exception:
            # If anything goes wrong, continue without changing mode
            pass
    
    if competitors_mode and q:
        # Enhance query for competitor discovery
        competitor_terms = ["competitors", "alternatives", "vs", "similar to"]
        if not any(term in q.lower() for term in competitor_terms):
            q = f"{q} competitors OR alternatives"
    
    if exact and q:
        q = f'"{q}"'
    
    if site:
        q = f"site:{site} {q}" if q else f"site:{site}"
    
    if exclude_site:
        exclusion = f"-site:{exclude_site}"
        q = f"{q} {exclusion}".strip() if q else exclusion
    
    if prefix:
        q = f"{prefix} {q}".strip()
    
    if suffix:
        q = f"{q} {suffix}".strip()
    
    return normalize_query(q) if normalize else q


def search_google(
    query: str,
    *,
    api_key: Optional[str] = None,
    engine_id: Optional[str] = None,
    num: int = 10,
    timeout: int = 10,
    site: Optional[str] = None,
    prefix: str = "",
    suffix: str = "",
    exact: bool = False,
    normalize: bool = True,
    exclude_site: Optional[str] = None,  # NEW
    competitors_mode: bool = False,  # NEW
    autodetect_competitors: bool = True,  # NEW
    debug: bool = False,
) -> Optional[Dict[str, Any]]:
    """Call Google Custom Search and return JSON results.

    New optional arguments allow modifying the search query:
    - site: restrict results to a domain (adds 'site:domain' to query)
    - exclude_site: exclude results from a domain (adds '-site:domain')
    - prefix/suffix: prefix/suffix text to include
    - exact: wrap the main query in quotes for exact match
    - normalize: run normalize_query to produce ASCII-only text
    - competitors_mode: optimize query for finding competitor brands
    - autodetect_competitors: if True, automatically enables competitor discovery for brand-like queries
    - debug: when True prints and logs the final query & params for debugging
    """
    api_key = api_key or _get_env("GOOGLE_API_KEY") or _get_env("GEMINI_API_KEY")
    engine_id = engine_id or _get_env("SEARCH_ENGINE_ID")

    if not api_key or not engine_id:
        LOGGER.error("Missing GOOGLE_API_KEY/GEMINI_API_KEY or SEARCH_ENGINE_ID")
        return None

    q = build_search_query(
        query,
        site=site,
        prefix=prefix,
        suffix=suffix,
        exact=exact,
        normalize=normalize,
        exclude_site=exclude_site,
        competitors_mode=competitors_mode,
        autodetect_competitors=autodetect_competitors,
    )
    params = {"key": api_key, "cx": engine_id, "q": q, "num": min(num, 10)}

    # debug output - logs at DEBUG level and optionally prints to stdout
    LOGGER.debug("Search query: %s", q)
    LOGGER.debug("Search params: %s", params)
    if debug:
        print("SEARCH QUERY:", q)
        print("SEARCH PARAMS:", params)

    try:
        response = requests.get(
            "https://www.googleapis.com/customsearch/v1",
            params=params,
            timeout=timeout,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:  # noqa: BLE001
        LOGGER.error("Google search failed: %s", exc)
        return None


def collect_snippets(search_results: Optional[Dict[str, Any]], *, dedupe: bool = True) -> List[str]:
    """Extract snippet text from search results.

    By default, duplicates are removed while preserving order. Set `dedupe=False`
    to keep duplicates if you need them for some downstream reason.
    """
    if not search_results:
        return []

    snippets: List[str] = []
    for item in search_results.get("items", []):
        snippet = item.get("snippet")
        if snippet:
            snippets.append(snippet.strip())

    if not dedupe:
        return snippets

    # De-duplicate while preserving order
    seen = set()
    unique_snippets: List[str] = []
    for s in snippets:
        norm = " ".join(s.split())  # normalize whitespace
        if norm not in seen:
            seen.add(norm)
            unique_snippets.append(s)
    return unique_snippets



def build_people_also_ask_prompt(
    *,
    website_url: str,
    country: str,
    language: str,
    metadata: Dict[str, Any],
    snippets: List[str],
    question_count: int = 20,
) -> str:
    """Generate the instruction prompt for People Also Ask discovery."""
    headings = metadata.get("headings", [])[:5] or ["None"]
    keywords = metadata.get("keywords", [])[:10] or ["None"]
    snippets_text = "\n".join(snippets)

    prompt = textwrap.dedent(
f"""
Based on the provided information about a brand or website—including headings, keywords, and search snippets—generate {question_count} Google-style 'People Also Ask' questions that focus on brand-level comparisons. 
Ensure questions reflect realistic user search intent and include a mix of direct, indirect, and alternative brand comparisons. 

Brand/Website: {website_url}
Country/Region: {country}
Language: {language}

Headings from the website:
{textwrap.indent(chr(10).join(headings), '  - ')}

Keywords from the website:
{', '.join(keywords)}

Search Result Snippets:
{snippets_text}

Instructions:

🔹 **Primary Objective**  
Generate 20 natural, realistic questions that reflect "People Also Ask" intent for a brand.
Focus on how the brand compares to others in the market.

🔹 **Mandatory Requirements**  
- **Named Competitors:** At least **18 out of 20 questions** must include a **specific named competitor or alternative brand**.  
  - Use specific brand names in at least 18 of the 20 questions. Do not use vague phrases like “other brands”, “similar products”, or “alternatives”.  
  - Do not include questions that only describe the brand’s products unless they are part of a comparison. Use actual brand names (e.g., “American Crew”, “Google”, “BMW”).  
  - If competitor names are missing, infer 12–15 credible competitors in the same industry and region.

- **Brand-Level Framing:** All questions must be framed around the brand’s positioning, reputation, or comparative value—not just product descriptions.

🔹 **Required Comparison Types**  
Include a diverse mix of the following question types:

1. **Direct Competition** – e.g., “Is [Brand] better than [Competitor]?”
2. **Indirect Competition** – e.g., “Is [Brand] worth it compared to [Budget Brand]?”
3. **Complementary Competition** – Include **at least 2 questions** comparing the brand to adjacent categories (e.g., salons, barbershops, retailers like Boots or Superdrug).
4. **Alternative Brands** – e.g., “Best alternatives to [Brand] in [Country]?”
5. **Brand Differentiation** – e.g., “What makes [Brand] different from [Competitor]?”
6. **Consumer Choice** – e.g., “Should I choose [Brand] or [Competitor] for [use case]?”

🔹 **Additional Rules**  
- Use brand names only—not retailers or marketplaces unless used for complementary comparison.
- Avoid including influencers, stockists, or unrelated product lines as competitors.
- If a product is mentioned, include its **parent brand** (e.g., “Galaxy (Samsung)”).
- Use each competitor no more than twice.
- Keep comparisons factual and neutral.
- Do not include questions that only describe or list the brand’s products without any competitive or comparative framing.

🔹 **Output Format**  
People Also Ask Questions:  
(Return exactly {question_count} questions, one per line, no numbering.)
"""
                ).strip()
    return prompt


def normalize_query(text: str) -> str:
    """Normalize text to ASCII-only for search queries."""
    normalized = unicodedata.normalize("NFKD", text or "")
    return normalized.encode("ascii", "ignore").decode("ascii")


def _meta_content(soup: BeautifulSoup, attrs: Dict[str, str]) -> str:
    tag = soup.find("meta", attrs=attrs)
    return tag.get("content", "").strip() if tag else ""


def _text_or_empty(tag: Optional[Any]) -> str:
    return tag.get_text(strip=True) if tag else ""


def _collect_headings(soup: BeautifulSoup) -> List[str]:
    headings: List[str] = []
    for level in ("h1", "h2", "h3"):
        for element in soup.find_all(level):
            text = element.get_text(strip=True)
            if text:
                headings.append(text)
    return headings


def _split_keywords(raw: str) -> List[str]:
    return [keyword.strip() for keyword in (raw or "").split(",") if keyword.strip()]


def _get_env(key: str) -> Optional[str]:
    import os

    return os.getenv(key)


__all__ = [
    "extract_website_metadata",
    "search_google",
    "build_search_query",
    "collect_snippets",
    "build_people_also_ask_prompt",
    "normalize_query",
]
## gemini_grounded_search.py
"""Grounded Gemini search utilities."""

from __future__ import annotations

import logging
import textwrap
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

from google import genai
from google.genai import types

LOGGER = logging.getLogger(__name__)


class GeminiGroundedSearchProcessor:
    """Gemini processor with Google Search grounding support."""

    def __init__(self, api_key: str, model_id: str = "gemini-2.5-flash-lite") -> None:
        self.client = genai.Client(api_key=api_key)
        self.model_id = model_id
        LOGGER.info("Initialized GeminiGroundedSearchProcessor with model %s", self.model_id)

    def process_prompts_with_grounding(
        self,
        prompts: List[str],
        *,
        url: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
        rate_limit_per_minute: int = 10,
        sleep_seconds: int = 60,
    ) -> List[Dict[str, Any]]:
        """Run Gemini with Google Search grounding across multiple prompts."""
        if not prompts:
            return []

        grounding_tool = types.Tool(google_search=types.GoogleSearch())
        config = types.GenerateContentConfig(
            tools=[grounding_tool],
            temperature=0.7,
            response_modalities=["TEXT"],
        )

        LOGGER.info("Processing %s prompts with Google Search grounding", len(prompts))
        LOGGER.info("Context URL: %s", url or "N/A")

        context_prefix = ""
        if url and metadata:
            context_prefix = textwrap.dedent(
                f"""
                Context: Analyzing the website {url}
                Website Title: {metadata.get('title', 'N/A')}
                Description: {metadata.get('description', 'N/A')}
                """
            ).strip()

        results: List[Dict[str, Any]] = []
        for idx, prompt in enumerate(prompts, 1):
            if idx > 1 and (idx - 1) % rate_limit_per_minute == 0:
                LOGGER.warning("Rate limit reached. Sleeping for %s seconds", sleep_seconds)
                time.sleep(sleep_seconds)

            start_time = time.time()
            try:
                formatted_prompt = f"{context_prefix}\n\nQuestion: {prompt}\n\n" \
                    "Please provide a comprehensive, well-researched answer using current information " \
                    "from the web. Focus on factual, actionable insights and cite the most relevant sources."

                response = self.client.models.generate_content(
                    model=self.model_id,
                    contents=formatted_prompt,
                    config=config,
                )

                response_text = getattr(response, "text", "")
                web_queries: List[str] = []
                grounding_sources: List[Dict[str, str]] = []
                grounding_metadata: Dict[str, Any] = {}

                if getattr(response, "candidates", None):
                    candidate = response.candidates[0]
                    grounding_meta = getattr(candidate, "grounding_metadata", None)

                    if grounding_meta:
                        web_queries_data = getattr(grounding_meta, "web_search_queries", [])
                        web_queries = [str(query) for query in web_queries_data]

                        grounding_chunks = getattr(grounding_meta, "grounding_chunks", [])
                        for chunk in grounding_chunks:
                            if hasattr(chunk, "web"):
                                web = chunk.web
                                source = {
                                    "title": getattr(web, "title", "N/A"),
                                    "url": getattr(web, "uri", "N/A"),
                                }

                                retrieved_context = getattr(grounding_meta, "retrieved_context", None)
                                snippet = getattr(retrieved_context, "text", "") if retrieved_context else ""
                                if snippet:
                                    source["snippet"] = snippet[:200]
                                grounding_sources.append(source)

                        if hasattr(grounding_meta, "search_entry_point"):
                            grounding_metadata["search_entry_point"] = str(
                                grounding_meta.search_entry_point
                            )

                processing_time = round(time.time() - start_time, 2)
                results.append(
                    {
                        "prompt": prompt,
                        "response": response_text,
                        "web_search_queries": web_queries,
                        "grounding_sources": grounding_sources,
                        "grounding_metadata": grounding_metadata,
                        "url": url,
                        "metadata": metadata,
                        "model": self.model_id,
                        "processing_time": processing_time,
                        "success": True,
                        "timestamp": datetime.now().isoformat(),
                    }
                )
                LOGGER.info(
                    "Prompt %s/%s completed in %ss (queries=%s, sources=%s)",
                    idx,
                    len(prompts),
                    processing_time,
                    len(web_queries),
                    len(grounding_sources),
                )

            except Exception as exc:  # noqa: BLE001
                processing_time = round(time.time() - start_time, 2)
                LOGGER.exception("Prompt %s/%s failed: %s", idx, len(prompts), exc)
                results.append(
                    {
                        "prompt": prompt,
                        "response": "",
                        "web_search_queries": [],
                        "grounding_sources": [],
                        "grounding_metadata": {},
                        "url": url,
                        "metadata": metadata,
                        "model": self.model_id,
                        "processing_time": processing_time,
                        "success": False,
                        "error": str(exc),
                        "timestamp": datetime.now().isoformat(),
                    }
                )

        LOGGER.info("Completed processing %s prompts", len(results))
        return results


__all__ = ["GeminiGroundedSearchProcessor"]

How I am using the code : 
# Web context helpers (refactored into backend/services) 
from backend.services.context_builder import ( 
    extract_website_metadata, 
    search_google, 
    collect_snippets, 
    build_people_also_ask_prompt, 
    normalize_query, 
) 
 
from typing import Any, Dict 
def display_metadata(metadata: Dict[str, Any], *, max_items: int = 5) -> None: """Pretty
print metadata fields returned from extract_website_metadata.""" print("=== Website 
Metadata ===") for key, value in metadata.items(): if key == "combined_text" or not 
value: continue label = key.replace('_', ' ').title() if isinstance(value, list): display_value = 
', '.join(value[:max_items]) else: display_value = value print(f"{label}: {display_value}") 
 
# Extract metadata from the website 
 
website_url = "https://fabuwellness.com/" 
 
metadata = extract_website_metadata(website_url) 
 
 
 
if metadata: 
 
    display_metadata(metadata) 
 
    print("\n" + "=" * 50) 
 
    print("\n=== Combined Text for Analysis ===") 
 
    print(metadata.get("combined_text", "")) 
 
else: 
 
    print("No metadata could be fetched for the website") 
 
 
 
country = "Ireland" 
 
language = "English" 
 
 
 
search_query = metadata.get("title") or "fabuwellness" 
 
search_query_cleaned = normalize_query(search_query) 
 
 
 
print(f"\nOriginal query: {search_query}") 
 
print(f"Cleaned query: {search_query_cleaned}\n") 
 
 
 
# Debug: reload service module to ensure latest edits are picked up (Jupyter 
kernel may have stale imports) 
 
search_results = None 
 
try: 
 
    import importlib 
 
    import backend.services.context_builder as cb 
 
    importlib.reload(cb) 
 
    print("Reloaded module:", cb.__file__) 
 
    # Print function signature to confirm autodetect arg is present 
 
    import inspect 
 
    print("search_google signature:", inspect.signature(cb.search_google)) 
 
    # Use the module alias explicitly to call the updated function 
 
    search_results = cb.search_google(search_query_cleaned, 
competitors_mode=True, debug=True) 
 
    print("Used cb.search_google (reloaded module)") 
 
except Exception as exc: 
 
    print("Could not reload/re-run search_google from module; falling back to 
local import:", exc) 
 
    # Fallback: call previously imported function from notebook 
 
    try: 
 
        search_results = search_google(search_query_cleaned, 
competitors_mode=True, debug=True) 
 
        print("Used search_google from notebook import (fallback)") 
 
    except Exception as exc2: 
 
        print("Fallback also failed:", exc2) 
 
 
 
# Now collect snippets and print once 
 
snippets = collect_snippets(search_results) 
 
 
 
print(f"Extracted {len(snippets)} snippets from search results\n") 
 
if snippets: 
 
    print("Combined snippets text:") 
 
    print("=" * 80) 
 
    print("\n".join(snippets)) 
 
    print("=" * 80) 
 
else: 
 
    print("No snippets available from search results") 
 
 
 
prompt = build_people_also_ask_prompt( 
 
    website_url=website_url, 
 
    country=country, 
 
    language=language, 
 
    metadata=metadata, 
 
    snippets=snippets, 
 
    question_count=20, 
 
) 
 
 
Initialize Gemini client with the new SDK 
from google import genai 
from google.genai import types 
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY")) 
GEMINI_MODEL = "gemini-2.5-flash-lite" 
print(f"✓ Gemini client initialized with model: {GEMINI_MODEL}") 
print("\n" + "=" * 80) 
print("Sending prompt to Gemini to generate questions...") 
print("=" * 80) 
response = gemini_client.models.generate_content( 
model=GEMINI_MODEL, 
 
contents=prompt 
  
) 
Response text extraction — use what the 
SDK returns in .text (older versions of the 
SDK) 
prompts = [] 
if response is not None: 
if hasattr(response, "text") and response.text: 
 
    response_text = response.text 
 
elif hasattr(response, "content") and response.content: 
 
    try: 
 
        response_text = response.content 
 
    except Exception: 
 
        response_text = None 
 
else: 
 
    response_text = None 
  
if not response_text: 
print("    No text output from Gemini. Response object:") 
 
print(response) 
 
prompts = [] 
  
else: 
# Split into lines & sanitize 
 
lines = [q.strip() for q in response_text.strip().splitlines() if 
q.strip()] 
 
 
 
# Remove common header lines inserted by LLMs, e.g. 'People Also 
Ask', and strip numbering 
 
import re 
 
 
 
def _clean_line(line: str) -> Optional[str]: 
 
    # ignore header lines 
 
    if re.match(r'(?i)^(people also ask( questions)?[:\s]*)$', 
line.strip()): 
 
        return None 
 
    # strip leading numbers/bullets like '1.' '1)' '•' 
 
    cleaned = re.sub(r'^\s*\d+[\.)]\s*', '', line).strip() 
 
    cleaned = re.sub(r'^\s*[\u2022\*\-]\s*', '', cleaned).strip() 
 
    # drop lines that are very short and not questions 
 
    if len(cleaned) < 5: 
 
        return None 
 
    return cleaned 
 
 
 
cleaned_lines = [] 
 
for l in lines: 
 
    cl = _clean_line(l) 
 
    if cl: 
 
        cleaned_lines.append(cl) 
 
 
 
# Keep only lines that look like questions (contain ?), but fallback 
to all if none 
 
question_lines = [l for l in cleaned_lines if '?' in l] 
 
if not question_lines: 
 
    question_lines = cleaned_lines 
 
 
 
# De-duplicate while preserving order 
 
seen_q = set() 
 
unique_questions = [] 
 
for q in question_lines: 
 
    norm = ' '.join(q.split()) 
 
    if norm not in seen_q: 
 
        seen_q.add(norm) 
 
        unique_questions.append(norm) 
 
# Enforce the expected count if available in prompt builder 
(defaults to 20 here) 
EXPECTED_PROMPTS = 20 
if 'question_count' in globals() and isinstance(question_count, 
int): 
EXPECTED_PROMPTS = question_count 
prompts = unique_questions[:EXPECTED_PROMPTS] 
# Log if the model returned more or fewer prompts than expected 
if len(unique_questions) != EXPECTED_PROMPTS: 
print(f"    
Model returned {len(unique_questions)} items 
(requested {EXPECTED_PROMPTS}). Using first {len(prompts)} items.") 
print(f"\nGenerated {len(prompts)} questions as prompts:\n") 
for i, question in enumerate(prompts, 1): 
print(f"{i}. {question}") 
print(f"\n✓ {len(prompts)} prompts stored in 'prompts' variable for further processing") 
===================================
 ===================================
 ====== 
EXECUTE: Process prompts with Gemini 
===================================
 ===================================
 ====== 
Initialize the Gemini processor and 
process the prompts 
Gemini grounded search processor 
(refactored into backend/services) 
from backend.services.gemini_grounded_search import 
GeminiGroundedSearchProcessor processor = 
GeminiGroundedSearchProcessor(api_key=os.getenv("GEMINI_API_KEY")) 
gemini_results = processor.process_prompts_with_grounding( prompts=prompts, 
url=website_url, metadata=metadata ) 
Save results to JSON 
gemini_filename = 
f"gemini_responses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json" with 
open(gemini_filename, "w", encoding="utf-8") as f: json.dump(gemini_results, f, 
ensure_ascii=False, indent=2) 
print(f"✓ Saved Gemini responses to {gemini_filename}") print(f"     
Variable 
'gemini_filename' is now available for subsequent cells") 
The example above has 20 prompts. Please make sure you change the code to 10. 

