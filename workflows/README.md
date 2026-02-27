# n8n Workflows

## Weekly Regulatory Brief

**File:** `regulatory_brief.json`

Automated regulatory intelligence system that runs every Monday at 8am.

### What it does

1. **Collects** news from 22 regulatory agencies across US, Canada, and EU via SerpAPI
2. **Deduplicates** articles by URL and fuzzy title matching (70% word overlap threshold)
3. **Filters** against a history of previously sent articles (stored in n8n Data Table)
4. **Analyzes** new articles using an OpenAI O3 agent with access to master reference sheets
5. **Delivers** a styled HTML executive brief via Gmail
6. **Archives** sent article URLs to prevent re-processing

### Agencies monitored

| Region | Agencies |
|--------|----------|
| US (10) | FDA, FTC, CPSC, EPA, USDA, TTB, Supplements, Cosmetics, FCC |
| Canada (6) | Health Canada, CFIA, Competition Bureau, PMRA, NHP |
| EU (6) | Commission, RAPEX, ECHA, EFSA, EMA, CE Marking |

### Required credentials

- SerpAPI key
- Google Sheets OAuth2 (for master reference sheets)
- OpenAI API key
- Gmail OAuth2
- Slack API (for no-articles notifications)

### Import

Import `regulatory_brief.json` directly into your n8n instance via **Settings > Import Workflow**.
