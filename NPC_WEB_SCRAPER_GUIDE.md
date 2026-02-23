# NPC Plant Status Web Scraper Guide

## Overview

This script connects to the National Power Corporation (NPC) website and extracts real-time plant status data for Agus-Pulangi hydropower plants.

## Features

✅ Automatic HTTP requests to NPC website
✅ HTML parsing with BeautifulSoup
✅ Multiple parsing strategies (tables, sections, elements)
✅ Extracts: plant name, water level, generation status, capacity, current generation
✅ JSON output format
✅ Comprehensive error handling
✅ Retry logic with alternative URLs
✅ Saves results to file

## Requirements

```bash
pip install requests beautifulsoup4
```

Or add to requirements.txt:
```
requests>=2.28.0
beautifulsoup4>=4.11.0
```

## Installation

1. Install dependencies:
```bash
cd npc-reporting-system
pip install requests beautifulsoup4
```

2. Run the scraper:
```bash
python scrape_npc_plant_status.py
```

## Usage

### Basic Usage

```bash
python scrape_npc_plant_status.py
```

### From Python Code

```python
from scrape_npc_plant_status import NPCPlantStatusScraper

# Create scraper
scraper = NPCPlantStatusScraper(timeout=30)

# Scrape data
result = scraper.scrape()

# Access results
if result['success']:
    for plant in result['plants']:
        print(f"Plant: {plant['plant_name']}")
        print(f"Water Level: {plant['water_level']}")
        print(f"Status: {plant['generation_status']}")
        print(f"Generation: {plant['current_generation_mw']} MW")
        print()
else:
    print(f"Error: {result['error']}")
```

## Output Format

### Success Response

```json
{
  "success": true,
  "timestamp": "2026-02-23T10:30:00",
  "source_url": "https://www.napocor.gov.ph/plant-status",
  "plants": [
    {
      "plant_name": "AGUS 1",
      "water_level": "701.50 m.a.s.l",
      "generation_status": "OPERATIONAL",
      "capacity_mw": 100.0,
      "current_generation_mw": 85.5,
      "remarks": "Normal operation",
      "timestamp": "2026-02-23T10:30:00"
    },
    {
      "plant_name": "AGUS 2",
      "water_level": "701.50 m.a.s.l",
      "generation_status": "OPERATIONAL",
      "capacity_mw": 180.0,
      "current_generation_mw": 165.0,
      "remarks": "Normal operation",
      "timestamp": "2026-02-23T10:30:00"
    }
  ],
  "error": null
}
```

### Error Response

```json
{
  "success": false,
  "timestamp": "2026-02-23T10:30:00",
  "source_url": null,
  "plants": [],
  "error": "Failed to connect to NPC website. Please check your internet connection.",
  "suggested_urls": []
}
```

## Configuration

### Update URLs

If the NPC website structure changes, update these URLs in the script:

```python
BASE_URL = "https://www.napocor.gov.ph"
PLANT_STATUS_URL = "https://www.napocor.gov.ph/plant-status"

ALTERNATIVE_URLS = [
    "https://www.napocor.gov.ph/generation",
    "https://www.napocor.gov.ph/operations",
    "https://www.napocor.gov.ph/mindanao-generation",
]
```

### Adjust Timeout

```python
scraper = NPCPlantStatusScraper(timeout=60)  # 60 seconds
```

## Parsing Strategies

The scraper uses multiple strategies to find plant data:

1. **Table Parsing**: Looks for HTML tables with plant data
2. **Section Parsing**: Searches divs, sections, and articles
3. **Element Parsing**: Finds elements with specific class names
4. **Text Extraction**: Uses regex to extract data from free text

## Data Extraction

### Plant Name
Searches for: AGUS 1, AGUS 2, AGUS 4, AGUS 5, AGUS 6, AGUS 7, PULANGI 4

### Water Level
Patterns: `701.50 m.a.s.l`, `290.00 masl`, `701.50 meters`

### Generation Status
Keywords: OPERATIONAL, RUNNING, OFFLINE, MAINTENANCE, NORMAL OPERATION, STANDBY

### MW Values
Pattern: `85.5 MW`, `100.0 MW`

## Error Handling

The scraper handles:
- ✅ Connection timeouts
- ✅ HTTP errors (404, 500, etc.)
- ✅ SSL certificate issues
- ✅ Network errors
- ✅ Parsing errors
- ✅ Missing data fields

## Integration with Django

### Add to Django Management Command

Create: `backend/reports/management/commands/scrape_npc_status.py`

```python
from django.core.management.base import BaseCommand
from scrape_npc_plant_status import NPCPlantStatusScraper
import json

class Command(BaseCommand):
    help = 'Scrape NPC plant status from website'

    def handle(self, *args, **options):
        scraper = NPCPlantStatusScraper()
        result = scraper.scrape()
        
        if result['success']:
            self.stdout.write(self.style.SUCCESS(
                f"Successfully scraped {len(result['plants'])} plants"
            ))
            self.stdout.write(json.dumps(result, indent=2))
        else:
            self.stdout.write(self.style.ERROR(
                f"Scraping failed: {result['error']}"
            ))
```

Run with:
```bash
python manage.py scrape_npc_status
```

### Add to Scheduled Task

In `backend/reports/services/automated_reports.py`:

```python
from scrape_npc_plant_status import NPCPlantStatusScraper

def update_plant_status_from_web():
    """Update plant status from NPC website"""
    scraper = NPCPlantStatusScraper()
    result = scraper.scrape()
    
    if result['success']:
        for plant_data in result['plants']:
            # Update database with scraped data
            plant_name = plant_data['plant_name']
            # ... update logic
    
    return result
```

## Troubleshooting

### Issue: "Failed to connect to NPC website"

**Solutions:**
1. Check internet connection
2. Verify NPC website is accessible: https://www.napocor.gov.ph
3. Check if firewall is blocking requests
4. Try increasing timeout value

### Issue: "No plant data found"

**Solutions:**
1. NPC website structure may have changed
2. Check the website manually to find new URLs
3. Update `PLANT_STATUS_URL` and `ALTERNATIVE_URLS`
4. Check `suggested_urls` in error response

### Issue: "SSL Certificate Error"

**Solution:**
```python
# Disable SSL verification (not recommended for production)
scraper.session.verify = False
```

### Issue: "Timeout Error"

**Solution:**
```python
# Increase timeout
scraper = NPCPlantStatusScraper(timeout=60)
```

## Limitations

⚠️ **Important Notes:**

1. **Website Availability**: Scraping depends on NPC website being online and accessible
2. **Structure Changes**: If NPC updates their website, the scraper may need updates
3. **Rate Limiting**: Avoid making too many requests in short time
4. **Legal**: Ensure compliance with NPC's terms of service
5. **Data Accuracy**: Scraped data may not be real-time or may be outdated

## Best Practices

1. **Cache Results**: Don't scrape too frequently (recommended: every 15-30 minutes)
2. **Error Logging**: Log all errors for debugging
3. **Fallback Data**: Have backup data source if scraping fails
4. **User Agent**: Use appropriate User-Agent header
5. **Respect robots.txt**: Check NPC's robots.txt file

## Alternative Approaches

If web scraping doesn't work:

1. **API**: Check if NPC provides an official API
2. **RSS/XML Feeds**: Look for data feeds
3. **Email Reports**: Parse automated email reports
4. **Manual Entry**: Use the existing Excel upload feature
5. **Contact NPC**: Request official data access

## Testing

Test the scraper:

```bash
# Run scraper
python scrape_npc_plant_status.py

# Check output file
cat npc_plant_status.json

# Verify JSON format
python -m json.tool npc_plant_status.json
```

## Support

For issues or questions:
1. Check the error message in JSON output
2. Review the troubleshooting section
3. Check NPC website manually
4. Update URLs if website structure changed

---

**Last Updated:** February 23, 2026
**Status:** Ready for testing
