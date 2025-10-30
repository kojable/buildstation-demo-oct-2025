import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

ENV_KEY = "ANTHROPIC_API_KEY"
api_key = os.getenv(ENV_KEY)
if api_key is None:
    raise EnvironmentError(
        f"Set the {ENV_KEY} environment variable with your Anthropic API key before calling Claude."
    )

client = Anthropic(api_key=api_key)

all_text = """
 "Content-Type: application/json"   -d '{"url":"https://www.arcium.com/team/"}'
{"url":"https://www.arcium.com/team/","timestamp":"2025-10-29T16:32:15.001Z","original_content_hash":"sha256:efc80ac2d692b1b9b68d50b7072e5d1e3236e3f48c191ae9f2a4758ab7afa62f","anonymization_applied":true,"pii_detected":10,"content":{"title":"Our Team","body":"Road to MainnetLearnBuildCommunityOur TeamHomeRoad to MainnetWhat is Arcium?News & InsightsResearch PapersDocsOur TeamExplore TestnetJoin the CommunityRead our DocsRoad to MainnetLearnBuildCommunityOur TeamHomeRoad to MainnetWhat is Arcium?News & InsightsResearch PapersDocsOur TeamExplore TestnetJoin the CommunityRead our DocsEmpowering the decentralized internet.AboutWhat is Arcium?Road to MainnetOur TeamPrivacy PolicyTerms & ConditionsResourcesNews & InsightsMediaResearch PapersBrand AssetsDocsElsewhereXDiscordGithubYouTubeAll rights reservedThank you! We've added you to our mailing list.Oops! Something went wrong in the submission process. Try again.ARX-9316cd4d881e21d7 TeamMeetYannik SchradeCo-founder & CEOYannik SchradeCo-founder & CEOTwitterInstagramLinkedInYannik has been deeply involved in the cryptography space, driven by a passion for engineering since childhood. His early success with shiftscreen, an iOS app with over 100,000 paying users, combined with his expertise in computer science and mathematics, positions him as a pivotal force in Arcium's technical strategy, particularly in the realm of MPC (Multi-ARX-f76cb18c0cfdb069). Having also studied law, Yannik brings a unique, multifaceted perspective to the table. As CEO, his leadership and visionary approach drive Arcium's mission to revolutionize confidential computing.ARX-645610e51672062d BelSenior Cryptography EngineerNicolas Le BelSenior Cryptography EngineerTwitterInstagramLinkedInNicolas ARX-1befae6fa3074d09 holds a Master’s degree in physics from ETH Zürich, specializing in theoretical and computational physics, with a thesis focused on the fractal properties of certain phase transitions. This led him to work on various projects, from bioinformatics to smart contract design, before being introduced to cryptography through the ZK realm. Since joining Arcium in 2023, Nicolas has been leading the development of async-mpc, Arcium's multiparty computation Rust library.Dr. Sergiu CarpovSenior Cryptography EngineerDr. Sergiu CarpovSenior Cryptography EngineerTwitterInstagramLinkedInSergiu hold a PhD in operations research applied to optimization problems in parallel processing systems. Shortly after graduating, he started working on compilation tools for ARX-c5c4f246e705eaf8 Encryption (FHE) and applied cryptography. He was the main contributor to Cingulata, the first compilation chain for FHE. His current interests are cryptography techniques for privacy-preserving computations (FHE, MPC among others) and optimization methods for privacy-preserving algorithms.Julian DeschlerCo-founder & CSOJulian DeschlerCo-founder & CSOTwitterInstagramLinkedInJulian began his entrepreneurial journey during his engineering and economics studies at the ARX-e92aa427747d5983 of Munich. After discovering Bitcoin and Ethereum in 2016, he became deeply passionate about decentralized technologies. Before fully diving into the Web3 space, Julian gained valuable experience working for two years in finance and banking. His background also includes serving on the board of START Munich and earning a scholarship from UnternehmerTUM. ARX-c1a27e526fb59037 ARX-0a2d15c2b94e656a, Julian is instrumental in shaping Arcium's strategic direction and driving its growth in the decentralized computing space.Nico SchapelerCo-founder & CTONico SchapelerCo-founder & CTOTwitterInstagramLinkedInNico Schapeler has a background in math and computer science from TUM and has been working at the intersection of cryptography and blockchains for nearly a decade. Some of his previous work includes TEEs for blockchain key material (before transitioning to MPC at Arcium), high-performance implementations of hash algorithms, and zk tech for onchain privacy tooling with Elusiv. ARX-a8e1b878b8eabe22, Nico leads all technical aspects, ranging from cryptography research to protocol implementation.Dr. Marius VuilleSenior ARX-f1d350bc82145878 EngineerDr. Marius VuilleSenior Machine Learning EngineerTwitterInstagramLinkedInMarius studied mathematics at EPFL and earned a PhD in algebraic geometry, focusing on the computation of isogenies between Jacobian varieties of hyperelliptic curves. He then spent five years as a Machine Learning Engineer at Inpher, where he developed novel MPC algorithms for a range of data science and machine learning problems. In the summer of 2024, Marius joined Arcium, where he works on both machine learning and cryptography-related topics.Lukas SteinerCo-founder & COOLukas SteinerCo-founder & COOTwitterInstagramLinkedInLukas joined the team after meeting Yannik, Nico, and Julian at a hacker house, bringing with him a rich blend of operational and development experience. Following his commercial apprenticeship, Lukas worked for two and a half years at a fintech startup in Zurich, where he reported to the former McKinsey CFO of Switzerland. This role honed his operations, finance, and recruiting skills. His interest in AI led him to develop a GPT-3 based SaaS application that was later acquired. As COO of Arcium, Lukas drives operational excellence, over"},"anonymization_map":[{"position":661,"type":"person_name","token":"ARX-f1d350bc82145878","original_redacted":"M******e","context":"submission process. Try again.ARX-f1d350bc82145878 TeamMeetYannik SchradeCo-foun"},{"position":1123,"type":"person_name","token":"ARX-a8e1b878b8eabe22","original_redacted":"P***************n","context":"ly in the realm of MPC (Multi-ARX-a8e1b878b8eabe22). Having also studied law, Ya"},{"position":1340,"type":"person_name","token":"ARX-0a2d15c2b94e656a","original_redacted":"N********e","context":"ionize confidential computing.ARX-0a2d15c2b94e656a BelSenior Cryptography Engine"},{"position":1456,"type":"person_name","token":"ARX-c1a27e526fb59037","original_redacted":"L****l","context":"itterInstagramLinkedInNicolas ARX-c1a27e526fb59037 holds a Master’s degree in ph"},{"position":2218,"type":"person_name","token":"ARX-e92aa427747d5983","original_redacted":"F***************c","context":"king on compilation tools for ARX-e92aa427747d5983 Encryption (FHE) and applied "},{"position":2706,"type":"person_name","token":"ARX-c5c4f246e705eaf8","original_redacted":"T******************y","context":" and economics studies at the ARX-c5c4f246e705eaf8 of Munich. After discovering "},{"position":3082,"type":"person_name","token":"ARX-1befae6fa3074d09","original_redacted":"A******f","context":"olarship from UnternehmerTUM. ARX-1befae6fa3074d09 Strategy Officer, Julian is i"},{"position":3091,"type":"person_name","token":"ARX-645610e51672062d","original_redacted":"S**************r","context":"from UnternehmerTUM. As Chief ARX-645610e51672062d, Julian is instrumental in sh"},{"position":3695,"type":"person_name","token":"ARX-f76cb18c0cfdb069","original_redacted":"A*******m","context":" privacy tooling with Elusiv. ARX-f76cb18c0cfdb069, Nico leads all technical asp"},{"position":3826,"type":"person_name","token":"ARX-9316cd4d881e21d7","original_redacted":"M**************g","context":"ation.Dr. Marius VuilleSenior ARX-9316cd4d881e21d7 EngineerDr. Marius VuilleSeni"}],"arcium_computation_id":"comp_75410a4c695eea1e","processing_time_ms":746,"demo_note":"This demo uses simulated Arcium MPC. In production, PII would be processed by the Arcium network using Multi-Party Computation, ensuring no single party ever sees the plai

"""


schema_prompt = f"""
You are an SEO and AI Search Optimization specialist. Your task is to analyze a PII-anonymized webpage output and generate comprehensive, valid JSON-LD structured data to improve visibility in search engines and AI-powered search platforms (like Google SGE, Bing Chat, Perplexity, ChatGPT search).

INPUT REQUIREMENTS:
The user will provide a PII-anonymized output of a webpage containing:
- Page content (HTML, markdown, or plain text)
- Business information with ARX-anonymized personal details
- An `anonymization_map` array showing what was anonymized
- Product/service descriptions
- Any existing structured data or metadata

CRITICAL - UNDERSTANDING ARX ANONYMIZATION:
The input has been processed through Arcium's Multi-Party Computation (MPC) anonymization. You will receive:

1. **Content with ARX tokens**: Text like "ARX-36e8285193ce0db4" replacing sensitive information
2. **Anonymization map**: Shows what each ARX token represents:
   ```json
   "anonymization_map": [
     {{
       "position": 1533,
       "type": "person_name",
       "token": "ARX-36e8285193ce0db4",
       "original_redacted": "W*********m",
       "context": "...preview of surrounding text..."
     }}
   ]
   ```

3. **ARX Token Types**: Common types include:
   - `person_name`: Individual names (founders, executives, employees)
   - `organization_name`: Company or organization names
   - `email_address`: Email contacts
   - `phone_number`: Phone numbers
   - `address`: Physical addresses
   - `location`: Geographic locations
   - `custom`: Other sensitive identifiers

**CRITICAL INSTRUCTION**: YOU MUST USE THE ARX TOKENS (e.g., "ARX-36e8285193ce0db4") IN YOUR JSON-LD OUTPUT WHERE THE ORIGINAL PII WOULD APPEAR. Do NOT attempt to guess, reconstruct, or use the redacted values like "W*********m".

**ABSOLUTE REQUIREMENT - ALL PERSON NAMES MUST USE ARX TOKENS:**
- EVERY person name that appears in the anonymization_map MUST be replaced with its ARX token in the JSON-LD output
- This includes founders, executives, employees, team members - NO EXCEPTIONS
- Even if a person's name appears multiple times in different contexts, ALWAYS use their ARX token
- DO NOT use any actual person names in the JSON-LD output - only use ARX tokens from the anonymization_map
- The ONLY exception is if a name is a well-known public brand name (like company names), not an individual person

**VERIFICATION STEP - Before finalizing your JSON-LD:**
1. Search the anonymization_map for ALL entries with `"type": "person_name"`
2. For EACH person_name token, verify it appears in your JSON-LD where that person is mentioned
3. Double-check that NO real person names (like "John Doe", "Jane Smith", etc.) appear in any "name" field for Person objects
4. Confirm all founder names, employee names, author names use ARX tokens

YOUR ANALYSIS PROCESS:

1. **Parse the Anonymization Map:**
   - Identify all ARX tokens and their types
   - **PRIORITY: List all `person_name` tokens first - these MUST ALL be used**
   - Understand what category of information each token represents
   - Note the context to understand where tokens should be placed

2. **Extract Key Information:**
   - Business name (may be an ARX token or public brand name)
   - Business type and industry
   - Product/service offerings
   - Location references (use ARX tokens for addresses)
   - Contact methods (use ARX tokens for phone/email)
   - Hours of operation, pricing
   - **Team members, founders (MUST use ARX tokens for ALL person names)**
   - FAQs and content
   - Brand differentiators

3. **Map ARX Tokens to Schema Properties:**
   Based on the token type, place ARX tokens in appropriate schema properties:
   - **`person_name` → MUST be used in `founder`, `employee`, `author`, `name` (in Person schema) - NO REAL NAMES ALLOWED**
   - `organization_name` → `name`, `legalName`, `alternateName`
   - `email_address` → `email` property
   - `phone_number` → `telephone` property
   - `address` → `streetAddress` or full address properties
   - `location` → `addressLocality`, `addressRegion`

4. **Determine Schema Types:**
   - Select the most specific Schema.org @type
   - Identify additional schema opportunities (FAQPage, Product, Service, etc.)
   - Consider nested schemas for comprehensive coverage

SCHEMA GENERATION GUIDELINES:
- Use the most specific @type possible (e.g., "TechnologyCompany" > "Organization")
- **MANDATORY: ALL person names MUST use ARX tokens** - e.g., `"name": "ARX-36e8285193ce0db4"`
- **NEVER use real person names like "John Doe" or "Jane Smith" in the JSON-LD**
- **Check the anonymization_map and use the corresponding ARX token for EVERY person mentioned**
- Include all applicable properties for the chosen schema type
- Add "description" fields optimized for AI snippets (150-160 characters, keyword-rich)
- Structure data hierarchically when appropriate
- Include "sameAs" for social profiles if identifiable (but still use ARX token for the person's name)
- Add "potentialAction" for interactive features
- Include "aggregateRating" structure if reviews are mentioned
- Add "openingHoursSpecification" if hours are present
- Include "offers" or "makesOffer" for products/services
- **If a PII field is completely missing from the input, omit the property entirely**

ARX TOKEN USAGE EXAMPLES:

**Example 1 - Person Name:**
```json
{{
  "@type": "Person",
  "name": "ARX-36e8285193ce0db4",
  "jobTitle": "CEO"
}}
```

**Example 2 - Organization with Contact:**
```json
{{
  "@type": "LocalBusiness",
  "name": "ARX-af9087d16e5013a9",
  "telephone": "ARX-e31879b89678387e",
  "email": "ARX-12345678abcdef12"
}}
```

**Example 3 - Address:**
```json
{{
  "@type": "PostalAddress",
  "streetAddress": "ARX-98765432fedcba98",
  "addressLocality": "ARX-11111111aaaaaaaa",
  "addressRegion": "California",
  "postalCode": "94102"
}}
```

**Example 4 - Multiple Founders:**
```json
{{
  "founder": [
    {{
      "@type": "Person",
      "name": "ARX-token-founder-1"
    }},
    {{
      "@type": "Person",
      "name": "ARX-token-founder-2"
    }}
  ]
}}
```

MULTIPLE SCHEMA SUPPORT:
Generate multiple schemas using @graph when appropriate:
- Main Organization/Business schema
- FAQPage schema (if FAQs exist)
- Product/SoftwareApplication schemas
- BreadcrumbList (for navigation)
- Article/BlogPosting (if content page)

OUTPUT FORMAT:
Generate valid JSON-LD schema as a single string that can be stored as a `.jsonld` file.

The JSON-LD must be:
- Valid, well-formed JSON
- Use "@context": "https://schema.org"
- Include appropriate "@type" or "@graph" for multiple schemas
- **Contain ARX tokens exactly as provided in the anonymization_map**
- Omit properties where no data exists (don't create placeholders)
- Optimized for both traditional SEO and AI search visibility

COMPLETE EXAMPLE OUTPUT:

Given this anonymization map:
```json
"anonymization_map": [
  {{
    "type": "person_name",
    "token": "ARX-founder-abc123",
    "original_redacted": "J*** S****"
  }},
  {{
    "type": "email_address",
    "token": "ARX-email-xyz789",
    "original_redacted": "c******@company.com"
  }}
]
```

Your output should include:
```json
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "Organization",
      "name": "Company Name",
      "email": "ARX-email-xyz789",
      "founder": {{
        "@type": "Person",
        "name": "ARX-founder-abc123"
      }}
    }}
  ]
}}
```

AFTER GENERATING THE SCHEMA, PROVIDE:

1. **Schema Summary:** List all schema types used and justification

2. **Key Optimizations:** Explain specific choices made for AI search visibility

3. **ARX Token Mapping:** Create a table showing:
   | ARX Token | Type | Schema Property | Schema Location |
   |-----------|------|-----------------|-----------------|
   | ARX-36e8285193ce0db4 | person_name | name | founder[0].name |
   | ARX-e31879b89678387e | phone_number | telephone | Organization.telephone |

4. **Content Recommendations:** Suggest any missing information that would enhance the schema

5. **Implementation Notes:** 
   - How to validate the schema
   - Where to place it in the HTML
   - Any special considerations

6. **ARX Privacy Note:** Remind that:
   - ARX tokens can be published safely - they reveal no actual PII
   - The business can replace ARX tokens with real values before deployment if desired
   - The schema is fully functional with ARX tokens for demo/testing purposes
   - Original data is never exposed due to Arcium's Multi-Party Computation

PRIVACY AND ACCURACY:
- ARX tokens are cryptographically secure and safe to publish
- Never attempt to reverse-engineer or guess the original values
- Use tokens exactly as provided - don't modify or shorten them
- The schema functions correctly with ARX tokens in place
- Businesses may choose to replace tokens with real data for production, but it's not required for the schema to be valid and useful

IMPORTANT REMINDERS:
- ✅ DO use ARX tokens like "ARX-36e8285193ce0db4" for ALL person names in the schema
- ❌ DON'T use ANY real person names (e.g., "Yannik Schrade", "Julian Deschler", "John Smith")
- ❌ DON'T use redacted values like "W*********m"
- ❌ DON'T create placeholders like "[NAME]" or "[PHONE]"
- ✅ DO consult the anonymization_map to find the ARX token for EVERY person mentioned
- ✅ DO place tokens in semantically appropriate schema properties
- ✅ DO verify that EVERY entry in anonymization_map with type="person_name" is used in your JSON-LD
- ❌ NEVER output a real person's name in the JSON-LD - this is a privacy violation

**FINAL VERIFICATION CHECKLIST:**
Before submitting your JSON-LD, confirm:
[ ] All person names in the JSON-LD are ARX tokens (format: ARX-xxxxxxxxxxxxx)
[ ] No real person names appear anywhere in the JSON-LD
[ ] Every person_name from the anonymization_map is represented
[ ] Job titles and descriptions can be real, but names must be ARX tokens

{all_text}
"""


schema_response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=3000,
    temperature=0.5,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": schema_prompt
                }
            ]
        }
    ]
)

# Extract the schema content
schema_content = schema_response.content[0].text.strip()

# Save to JSON schema file
output_file = "arcium_team_schema.jsonld"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(schema_content)

print(f"Schema saved to {output_file}")
print("\nSchema preview:")
print(schema_content[:500] + "..." if len(schema_content) > 500 else schema_content)

