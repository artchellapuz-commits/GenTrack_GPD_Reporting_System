"""
NPC Plant Status Web Scraper
Connects to the National Power Corporation (NPC) website and extracts
current plant status for Agus-Pulangi hydropower plants.

Requirements:
- requests
- beautifulsoup4

Install: pip install requests beautifulsoup4
"""

import requests
from bs4 import BeautifulSoup
import json
import sys
from datetime import datetime
from typing import Dict, List, Optional


class NPCPlantStatusScraper:
    """Scraper for NPC Agus-Pulangi plant status"""
    
    # NPC website URLs (verified actual URLs)
    BASE_URL = "https://www.napocor.gov.ph"
    PLANT_STATUS_URL = "https://www.napocor.gov.ph/mindanao-generation-plants/"
    
    # Alternative URLs to try
    ALTERNATIVE_URLS = [
        "https://www.napocor.gov.ph/dams-management-mandate/",
        "https://www.napocor.gov.ph/generation",
        "https://www.napocor.gov.ph/operations",
    ]
    
    # Agus-Pulangi plant names to search for
    PLANT_NAMES = [
        'AGUS 1', 'AGUS 2', 'AGUS 4', 'AGUS 5', 'AGUS 6', 'AGUS 7',
        'PULANGI 4', 'PULANGI IV', 'PULANGUI 4', 'PULANGUI IV'
    ]
    
    def __init__(self, timeout: int = 30):
        """
        Initialize the scraper
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
    
    def fetch_page(self, url: str) -> Optional[str]:
        """
        Fetch HTML content from URL
        
        Args:
            url: URL to fetch
            
        Returns:
            HTML content as string, or None if failed
        """
        try:
            print(f"Fetching: {url}")
            response = self.session.get(url, timeout=self.timeout, verify=True)
            response.raise_for_status()
            return response.text
        except requests.exceptions.Timeout:
            print(f"ERROR: Request timeout for {url}")
            return None
        except requests.exceptions.ConnectionError:
            print(f"ERROR: Connection error for {url}")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"ERROR: HTTP error {e.response.status_code} for {url}")
            return None
        except Exception as e:
            print(f"ERROR: Unexpected error fetching {url}: {str(e)}")
            return None
    
    def parse_plant_data(self, html: str) -> List[Dict]:
        """
        Parse HTML content to extract plant status data
        
        Args:
            html: HTML content as string
            
        Returns:
            List of plant data dictionaries
        """
        soup = BeautifulSoup(html, 'html.parser')
        plants_data = []
        
        # Strategy 1: Look for tables with plant data
        tables = soup.find_all('table')
        for table in tables:
            plant_data = self._parse_table(table)
            if plant_data:
                plants_data.extend(plant_data)
        
        # Strategy 2: Look for divs/sections with plant information
        if not plants_data:
            sections = soup.find_all(['div', 'section', 'article'])
            for section in sections:
                plant_data = self._parse_section(section)
                if plant_data:
                    plants_data.append(plant_data)
        
        # Strategy 3: Look for specific class names or IDs
        if not plants_data:
            plant_elements = soup.find_all(class_=['plant', 'plant-status', 'generation', 'hydropower'])
            for element in plant_elements:
                plant_data = self._parse_element(element)
                if plant_data:
                    plants_data.append(plant_data)
        
        return plants_data
    
    def _parse_table(self, table) -> List[Dict]:
        """Parse table element for plant data"""
        plants = []
        
        try:
            # Get headers
            headers = []
            header_row = table.find('thead')
            if header_row:
                headers = [th.get_text(strip=True).lower() for th in header_row.find_all(['th', 'td'])]
            else:
                # Try first row as header
                first_row = table.find('tr')
                if first_row:
                    headers = [th.get_text(strip=True).lower() for th in first_row.find_all(['th', 'td'])]
            
            # Get data rows
            rows = table.find_all('tr')[1:] if headers else table.find_all('tr')
            
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if not cells:
                    continue
                
                row_data = [cell.get_text(strip=True) for cell in cells]
                
                # Check if this row contains Agus-Pulangi plant data
                row_text = ' '.join(row_data).upper()
                if any(plant.upper() in row_text for plant in self.PLANT_NAMES):
                    plant_info = self._extract_plant_info(row_data, headers)
                    if plant_info:
                        plants.append(plant_info)
        
        except Exception as e:
            print(f"Error parsing table: {str(e)}")
        
        return plants
    
    def _parse_section(self, section) -> Optional[Dict]:
        """Parse section element for plant data"""
        try:
            text = section.get_text(strip=True).upper()
            
            # Check if section contains Agus-Pulangi plant
            for plant_name in self.PLANT_NAMES:
                if plant_name.upper() in text:
                    return self._extract_plant_info_from_text(section.get_text())
        
        except Exception as e:
            print(f"Error parsing section: {str(e)}")
        
        return None
    
    def _parse_element(self, element) -> Optional[Dict]:
        """Parse generic element for plant data"""
        try:
            text = element.get_text(strip=True).upper()
            
            # Check if element contains Agus-Pulangi plant
            for plant_name in self.PLANT_NAMES:
                if plant_name.upper() in text:
                    return self._extract_plant_info_from_text(element.get_text())
        
        except Exception as e:
            print(f"Error parsing element: {str(e)}")
        
        return None
    
    def _extract_plant_info(self, row_data: List[str], headers: List[str]) -> Optional[Dict]:
        """Extract plant information from table row"""
        plant_info = {
            'plant_name': None,
            'water_level': None,
            'generation_status': None,
            'capacity_mw': None,
            'current_generation_mw': None,
            'remarks': None,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            # Map headers to data
            for i, header in enumerate(headers):
                if i >= len(row_data):
                    break
                
                value = row_data[i]
                
                # Plant name
                if 'plant' in header or 'name' in header:
                    plant_info['plant_name'] = value
                
                # Water level
                elif 'water' in header or 'level' in header or 'elevation' in header:
                    plant_info['water_level'] = value
                
                # Generation status
                elif 'status' in header or 'operation' in header:
                    plant_info['generation_status'] = value
                
                # Capacity
                elif 'capacity' in header or 'rated' in header:
                    plant_info['capacity_mw'] = self._extract_number(value)
                
                # Current generation
                elif 'generation' in header or 'output' in header or 'load' in header:
                    plant_info['current_generation_mw'] = self._extract_number(value)
                
                # Remarks
                elif 'remark' in header or 'note' in header or 'comment' in header:
                    plant_info['remarks'] = value
            
            # If no headers, try to extract from row data directly
            if not headers:
                for value in row_data:
                    if any(plant.upper() in value.upper() for plant in self.PLANT_NAMES):
                        plant_info['plant_name'] = value
                    elif 'm.a.s.l' in value.lower() or 'masl' in value.lower():
                        plant_info['water_level'] = value
                    elif any(status in value.upper() for status in ['OPERATIONAL', 'RUNNING', 'OFFLINE', 'MAINTENANCE']):
                        plant_info['generation_status'] = value
            
            # Return only if we found at least plant name
            if plant_info['plant_name']:
                return plant_info
        
        except Exception as e:
            print(f"Error extracting plant info: {str(e)}")
        
        return None
    
    def _extract_plant_info_from_text(self, text: str) -> Optional[Dict]:
        """Extract plant information from free text"""
        plant_info = {
            'plant_name': None,
            'water_level': None,
            'generation_status': None,
            'capacity_mw': None,
            'current_generation_mw': None,
            'remarks': text[:200],  # First 200 chars as remarks
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            text_upper = text.upper()
            
            # Extract plant name
            for plant_name in self.PLANT_NAMES:
                if plant_name.upper() in text_upper:
                    plant_info['plant_name'] = plant_name
                    break
            
            # Extract water level (e.g., "701.50 m.a.s.l" or "290.00 masl")
            import re
            water_level_match = re.search(r'(\d+\.?\d*)\s*(m\.a\.s\.l|masl|meters)', text, re.IGNORECASE)
            if water_level_match:
                plant_info['water_level'] = f"{water_level_match.group(1)} m.a.s.l"
            
            # Extract generation status
            status_keywords = ['OPERATIONAL', 'RUNNING', 'OFFLINE', 'MAINTENANCE', 'NORMAL OPERATION', 'STANDBY']
            for keyword in status_keywords:
                if keyword in text_upper:
                    plant_info['generation_status'] = keyword
                    break
            
            # Extract MW values
            mw_matches = re.findall(r'(\d+\.?\d*)\s*MW', text, re.IGNORECASE)
            if mw_matches:
                plant_info['current_generation_mw'] = float(mw_matches[0])
            
            if plant_info['plant_name']:
                return plant_info
        
        except Exception as e:
            print(f"Error extracting from text: {str(e)}")
        
        return None
    
    def _extract_number(self, text: str) -> Optional[float]:
        """Extract numeric value from text"""
        try:
            import re
            match = re.search(r'(\d+\.?\d*)', text)
            if match:
                return float(match.group(1))
        except:
            pass
        return None
    
    def scrape(self) -> Dict:
        """
        Main scraping method
        
        Returns:
            Dictionary with scraping results
        """
        result = {
            'success': False,
            'timestamp': datetime.now().isoformat(),
            'source_url': None,
            'plants': [],
            'error': None
        }
        
        # Try main URL first
        urls_to_try = [self.PLANT_STATUS_URL] + self.ALTERNATIVE_URLS
        
        for url in urls_to_try:
            html = self.fetch_page(url)
            
            if html:
                plants_data = self.parse_plant_data(html)
                
                if plants_data:
                    result['success'] = True
                    result['source_url'] = url
                    result['plants'] = plants_data
                    print(f"✓ Successfully extracted {len(plants_data)} plant(s) from {url}")
                    return result
        
        # If no data found, try to get any page content for debugging
        html = self.fetch_page(self.BASE_URL)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            # Look for links that might contain plant status
            links = soup.find_all('a', href=True)
            relevant_links = [
                link['href'] for link in links 
                if any(keyword in link.get_text().lower() for keyword in ['plant', 'generation', 'status', 'operation', 'mindanao'])
            ]
            
            if relevant_links:
                result['error'] = f"No plant data found. Found {len(relevant_links)} potentially relevant links. Try these URLs manually."
                result['suggested_urls'] = relevant_links[:5]
            else:
                result['error'] = "No plant data found on NPC website. The website structure may have changed."
        else:
            result['error'] = "Failed to connect to NPC website. Please check your internet connection."
        
        return result


def main():
    """Main execution function"""
    print("=" * 70)
    print("NPC Agus-Pulangi Plant Status Scraper")
    print("=" * 70)
    print()
    
    # Create scraper instance
    scraper = NPCPlantStatusScraper(timeout=30)
    
    # Scrape data
    print("Starting web scraping...")
    print()
    result = scraper.scrape()
    
    # Output results as JSON
    print()
    print("=" * 70)
    print("RESULTS (JSON)")
    print("=" * 70)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Save to file
    output_file = 'npc_plant_status.json'
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print()
        print(f"✓ Results saved to: {output_file}")
    except Exception as e:
        print(f"✗ Failed to save results: {str(e)}")
    
    # Exit with appropriate code
    sys.exit(0 if result['success'] else 1)


if __name__ == '__main__':
    main()
