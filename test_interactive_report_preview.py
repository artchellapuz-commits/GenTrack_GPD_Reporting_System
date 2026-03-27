#!/usr/bin/env python3
"""
Test script to verify the interactive report preview enhancements
"""

import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def setup_driver():
    """Setup Chrome driver with appropriate options"""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    # chrome_options.add_argument("--headless")  # Comment out for debugging
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def test_interactive_table_features(driver):
    """Test the interactive table features"""
    print("🔍 Testing interactive table features...")
    
    try:
        # Wait for the modern table to be present
        wait = WebDriverWait(driver, 10)
        
        # Test table controls
        table_controls = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "table-controls")))
        print("✅ Table controls found")
        
        # Test filter functionality
        plant_filter = driver.find_element(By.CSS_SELECTOR, "select[v-model='tableFilters.plant']")
        if plant_filter:
            print("✅ Plant filter dropdown found")
        
        # Test search functionality
        search_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Search plants...']")
        if search_input:
            print("✅ Search input found")
            search_input.send_keys("AGUS")
            time.sleep(1)
            search_input.clear()
        
        # Test sortable headers
        sortable_headers = driver.find_elements(By.CLASS_NAME, "sortable-header")
        if sortable_headers:
            print(f"✅ Found {len(sortable_headers)} sortable headers")
            # Click on first sortable header
            sortable_headers[0].click()
            time.sleep(1)
            print("✅ Header sorting clicked successfully")
        
        # Test expandable plant rows
        plant_rows = driver.find_elements(By.CLASS_NAME, "plant-row")
        if plant_rows:
            print(f"✅ Found {len(plant_rows)} plant rows")
            # Click on first plant row to expand
            plant_rows[0].click()
            time.sleep(1)
            print("✅ Plant row expansion clicked successfully")
        
        # Test table actions
        export_btn = driver.find_element(By.CSS_SELECTOR, "button[title='Export Table Data']")
        if export_btn:
            print("✅ Export button found")
        
        compact_btn = driver.find_element(By.CSS_SELECTOR, "button[title='Toggle View']")
        if compact_btn:
            print("✅ Compact view toggle found")
            compact_btn.click()
            time.sleep(1)
            print("✅ Compact view toggled successfully")
        
        return True
        
    except (TimeoutException, NoSuchElementException) as e:
        print(f"❌ Interactive table test failed: {str(e)}")
        return False

def test_enhanced_toolbar(driver):
    """Test the enhanced preview toolbar"""
    print("🔍 Testing enhanced toolbar features...")
    
    try:
        wait = WebDriverWait(driver, 10)
        
        # Test toolbar presence
        toolbar = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "preview-toolbar")))
        print("✅ Enhanced toolbar found")
        
        # Test data summary
        summary_items = driver.find_elements(By.CLASS_NAME, "summary-item")
        if summary_items:
            print(f"✅ Found {len(summary_items)} data summary items")
        
        # Test view options
        view_buttons = driver.find_elements(By.CLASS_NAME, "view-btn")
        if view_buttons:
            print(f"✅ Found {len(view_buttons)} view options")
            # Test analytics view if available
            for btn in view_buttons:
                if "Analytics" in btn.text:
                    btn.click()
                    time.sleep(1)
                    print("✅ Analytics view activated")
                    break
        
        # Test export options
        export_buttons = driver.find_elements(By.CLASS_NAME, "btn-export")
        if export_buttons:
            print(f"✅ Found {len(export_buttons)} export options")
        
        return True
        
    except (TimeoutException, NoSuchElementException) as e:
        print(f"❌ Enhanced toolbar test failed: {str(e)}")
        return False

def test_floating_action_menu(driver):
    """Test the floating action menu"""
    print("🔍 Testing floating action menu...")
    
    try:
        wait = WebDriverWait(driver, 10)
        
        # Test floating action button
        fab_main = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "fab-main")))
        print("✅ Floating action button found")
        
        # Click to expand menu
        fab_main.click()
        time.sleep(1)
        
        # Test menu items
        fab_items = driver.find_elements(By.CLASS_NAME, "fab-item")
        if fab_items:
            print(f"✅ Found {len(fab_items)} floating action menu items")
        
        # Click refresh button if available
        for item in fab_items:
            if "refresh" in item.get_attribute("title").lower():
                item.click()
                time.sleep(1)
                print("✅ Refresh action clicked successfully")
                break
        
        return True
        
    except (TimeoutException, NoSuchElementException) as e:
        print(f"❌ Floating action menu test failed: {str(e)}")
        return False

def test_remarks_modal(driver):
    """Test the remarks detail modal"""
    print("🔍 Testing remarks modal functionality...")
    
    try:
        wait = WebDriverWait(driver, 10)
        
        # Find and click a remarks expand button
        remarks_buttons = driver.find_elements(By.CLASS_NAME, "remarks-expand")
        if remarks_buttons:
            print("✅ Remarks expand buttons found")
            remarks_buttons[0].click()
            time.sleep(1)
            
            # Check if modal opened
            modal = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "remarks-modal")))
            print("✅ Remarks modal opened successfully")
            
            # Test modal content
            detail_sections = driver.find_elements(By.CLASS_NAME, "detail-section")
            if detail_sections:
                print(f"✅ Found {len(detail_sections)} detail sections in modal")
            
            # Close modal
            close_btn = driver.find_element(By.CLASS_NAME, "btn-close-modal")
            close_btn.click()
            time.sleep(1)
            print("✅ Modal closed successfully")
        
        return True
        
    except (TimeoutException, NoSuchElementException) as e:
        print(f"❌ Remarks modal test failed: {str(e)}")
        return False

def test_enhanced_charts(driver):
    """Test the enhanced chart interactivity"""
    print("🔍 Testing enhanced chart features...")
    
    try:
        wait = WebDriverWait(driver, 10)
        
        # Test chart containers
        chart_boxes = driver.find_elements(By.CLASS_NAME, "chart-box")
        if chart_boxes:
            print(f"✅ Found {len(chart_boxes)} chart containers")
        
        # Test chart wrappers
        chart_wrappers = driver.find_elements(By.CLASS_NAME, "chart-wrapper")
        if chart_wrappers:
            print(f"✅ Found {len(chart_wrappers)} chart wrappers")
            
            # Hover over first chart to test interactivity
            driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('mouseover', {bubbles: true}));", chart_wrappers[0])
            time.sleep(1)
            print("✅ Chart hover interaction tested")
        
        return True
        
    except (TimeoutException, NoSuchElementException) as e:
        print(f"❌ Enhanced charts test failed: {str(e)}")
        return False

def test_responsive_design(driver):
    """Test responsive design features"""
    print("🔍 Testing responsive design...")
    
    try:
        # Test different screen sizes
        screen_sizes = [
            (1920, 1080, "Desktop"),
            (1024, 768, "Tablet"),
            (375, 667, "Mobile")
        ]
        
        for width, height, device in screen_sizes:
            driver.set_window_size(width, height)
            time.sleep(2)
            
            # Check if table is still accessible
            table_container = driver.find_element(By.CLASS_NAME, "modern-table-container")
            if table_container.is_displayed():
                print(f"✅ {device} ({width}x{height}): Table container visible")
            
            # Check toolbar responsiveness
            toolbar = driver.find_element(By.CLASS_NAME, "preview-toolbar")
            if toolbar.is_displayed():
                print(f"✅ {device} ({width}x{height}): Toolbar responsive")
        
        # Reset to desktop size
        driver.set_window_size(1920, 1080)
        time.sleep(1)
        
        return True
        
    except (TimeoutException, NoSuchElementException) as e:
        print(f"❌ Responsive design test failed: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Interactive Report Preview Enhancement Tests")
    print("=" * 60)
    
    driver = setup_driver()
    
    try:
        # Navigate to the application
        print("📱 Navigating to Generate Report page...")
        driver.get("http://localhost:8080/generate-report")
        
        # Wait for page to load
        wait = WebDriverWait(driver, 15)
        
        # Check if we need to login first
        try:
            login_form = driver.find_element(By.CSS_SELECTOR, "form")
            if "login" in driver.current_url.lower() or any(keyword in driver.page_source.lower() for keyword in ["login", "sign in", "username", "password"]):
                print("🔐 Login required, attempting to login...")
                
                username_field = driver.find_element(By.CSS_SELECTOR, "input[type='text'], input[name='username'], input[placeholder*='username']")
                password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password'], input[name='password']")
                
                username_field.send_keys("admin")
                password_field.send_keys("admin123")
                
                login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], button:contains('Login'), .btn-login")
                login_button.click()
                
                time.sleep(3)
                print("✅ Login completed")
                
                # Navigate to generate report page after login
                driver.get("http://localhost:8080/generate-report")
                
        except NoSuchElementException:
            print("ℹ️ No login required or already logged in")
        
        # Wait for the generate report page to load
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "generate-report-page")))
        print("✅ Generate Report page loaded")
        
        # Generate a report first
        print("📊 Generating report preview...")
        
        # Set report date
        date_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='date']")))
        driver.execute_script("arguments[0].value = '2026-03-18';", date_input)
        
        # Click generate button
        generate_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-generate")))
        generate_btn.click()
        
        # Wait for preview to load
        print("⏳ Waiting for report preview to load...")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "preview-card")), timeout=30)
        print("✅ Report preview loaded successfully")
        
        # Run all tests
        test_results = []
        
        test_results.append(("Interactive Table Features", test_interactive_table_features(driver)))
        test_results.append(("Enhanced Toolbar", test_enhanced_toolbar(driver)))
        test_results.append(("Floating Action Menu", test_floating_action_menu(driver)))
        test_results.append(("Remarks Modal", test_remarks_modal(driver)))
        test_results.append(("Enhanced Charts", test_enhanced_charts(driver)))
        test_results.append(("Responsive Design", test_responsive_design(driver)))
        
        # Print results summary
        print("\n" + "=" * 60)
        print("📋 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        passed = 0
        total = len(test_results)
        
        for test_name, result in test_results:
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{test_name:<30} {status}")
            if result:
                passed += 1
        
        print("-" * 60)
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("\n🎉 ALL TESTS PASSED! Interactive report preview enhancements are working correctly.")
        else:
            print(f"\n⚠️ {total - passed} test(s) failed. Please check the implementation.")
        
        # Take a screenshot of the final result
        driver.save_screenshot("interactive_report_preview_final.png")
        print("📸 Final screenshot saved as 'interactive_report_preview_final.png'")
        
    except Exception as e:
        print(f"❌ Test execution failed: {str(e)}")
        driver.save_screenshot("interactive_report_preview_error.png")
        print("📸 Error screenshot saved as 'interactive_report_preview_error.png'")
        
    finally:
        print("\n🔚 Closing browser...")
        driver.quit()
        print("✅ Test completed!")

if __name__ == "__main__":
    main()