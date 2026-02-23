"""
Test script for NPC Plant Status Scraper
Demonstrates usage and validates functionality
"""

import json
from scrape_npc_plant_status import NPCPlantStatusScraper


def test_basic_scraping():
    """Test basic scraping functionality"""
    print("=" * 70)
    print("TEST 1: Basic Scraping")
    print("=" * 70)
    
    scraper = NPCPlantStatusScraper(timeout=30)
    result = scraper.scrape()
    
    print(f"Success: {result['success']}")
    print(f"Timestamp: {result['timestamp']}")
    print(f"Source URL: {result['source_url']}")
    print(f"Plants Found: {len(result['plants'])}")
    
    if result['success']:
        print("\n✓ Scraping successful!")
        for i, plant in enumerate(result['plants'], 1):
            print(f"\nPlant {i}:")
            print(f"  Name: {plant['plant_name']}")
            print(f"  Water Level: {plant['water_level']}")
            print(f"  Status: {plant['generation_status']}")
            print(f"  Capacity: {plant['capacity_mw']} MW")
            print(f"  Current Gen: {plant['current_generation_mw']} MW")
    else:
        print(f"\n✗ Scraping failed: {result['error']}")
        if 'suggested_urls' in result:
            print("\nSuggested URLs to try:")
            for url in result['suggested_urls']:
                print(f"  - {url}")
    
    return result


def test_json_output():
    """Test JSON output format"""
    print("\n" + "=" * 70)
    print("TEST 2: JSON Output Format")
    print("=" * 70)
    
    scraper = NPCPlantStatusScraper()
    result = scraper.scrape()
    
    try:
        json_str = json.dumps(result, indent=2, ensure_ascii=False)
        print("\n✓ Valid JSON format")
        print("\nJSON Output:")
        print(json_str[:500] + "..." if len(json_str) > 500 else json_str)
        return True
    except Exception as e:
        print(f"\n✗ Invalid JSON: {str(e)}")
        return False


def test_error_handling():
    """Test error handling with invalid URL"""
    print("\n" + "=" * 70)
    print("TEST 3: Error Handling")
    print("=" * 70)
    
    scraper = NPCPlantStatusScraper(timeout=5)
    scraper.PLANT_STATUS_URL = "https://invalid-url-that-does-not-exist.com"
    scraper.ALTERNATIVE_URLS = []
    
    result = scraper.scrape()
    
    if not result['success'] and result['error']:
        print("✓ Error handling works correctly")
        print(f"Error message: {result['error']}")
        return True
    else:
        print("✗ Error handling failed")
        return False


def test_data_extraction():
    """Test data extraction from sample HTML"""
    print("\n" + "=" * 70)
    print("TEST 4: Data Extraction")
    print("=" * 70)
    
    # Sample HTML with plant data
    sample_html = """
    <html>
    <body>
        <table>
            <thead>
                <tr>
                    <th>Plant Name</th>
                    <th>Water Level</th>
                    <th>Status</th>
                    <th>Generation (MW)</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>AGUS 1</td>
                    <td>701.50 m.a.s.l</td>
                    <td>OPERATIONAL</td>
                    <td>85.5 MW</td>
                </tr>
                <tr>
                    <td>AGUS 2</td>
                    <td>701.50 m.a.s.l</td>
                    <td>OPERATIONAL</td>
                    <td>165.0 MW</td>
                </tr>
            </tbody>
        </table>
    </body>
    </html>
    """
    
    scraper = NPCPlantStatusScraper()
    plants = scraper.parse_plant_data(sample_html)
    
    if plants and len(plants) >= 2:
        print(f"✓ Successfully extracted {len(plants)} plants from sample HTML")
        for plant in plants:
            print(f"\n  Plant: {plant['plant_name']}")
            print(f"  Water Level: {plant['water_level']}")
            print(f"  Status: {plant['generation_status']}")
        return True
    else:
        print("✗ Failed to extract data from sample HTML")
        return False


def test_file_output():
    """Test saving results to file"""
    print("\n" + "=" * 70)
    print("TEST 5: File Output")
    print("=" * 70)
    
    scraper = NPCPlantStatusScraper()
    result = scraper.scrape()
    
    output_file = 'test_npc_output.json'
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        # Verify file was created and is valid JSON
        with open(output_file, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        
        print(f"✓ Successfully saved and loaded from {output_file}")
        print(f"  File size: {len(json.dumps(loaded_data))} bytes")
        return True
    except Exception as e:
        print(f"✗ File operation failed: {str(e)}")
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("NPC PLANT STATUS SCRAPER - TEST SUITE")
    print("=" * 70)
    print()
    
    tests = [
        ("Basic Scraping", test_basic_scraping),
        ("JSON Output", test_json_output),
        ("Error Handling", test_error_handling),
        ("Data Extraction", test_data_extraction),
        ("File Output", test_file_output)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ Test '{test_name}' crashed: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print()
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
    
    return passed == total


if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1)
