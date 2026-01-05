from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from datetime import datetime

class GoogleDorksSearcher:
    def __init__(self, browser="firefox", output_dir="output"):
        self.browser = browser
        self.driver = None
        self.output_dir = output_dir
        self.results = []
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Dossier '{output_dir}' cree")
        
    def start_browser(self):
        if self.browser == "firefox":
            self.driver = webdriver.Firefox()
        elif self.browser == "chrome":
            self.driver = webdriver.Chrome()
        elif self.browser == "edge":
            self.driver = webdriver.Edge()
        else:
            raise ValueError("Unsupported browser, please use firefox, chrome or edge")
        
        self.driver.maximize_window()
        
    def detect_captcha(self):
        captcha_indicators = [
            "//iframe[contains(@src, 'recaptcha')]",
            "//*[contains(text(), 'unusual traffic')]",
            "//*[contains(text(), 'not a robot')]",
            "//form[@id='captcha-form']",
            "//*[@id='recaptcha']",
            "//*[contains(@class, 'g-recaptcha')]",
        ]
        
        for indicator in captcha_indicators:
            try:
                elements = self.driver.find_elements(By.XPATH, indicator)
                if elements:
                    return True
            except:
                continue
        
        return False
    
    def wait_for_captcha_resolution(self):
        print("\n" + "=" * 60)
        print("CAPTCHA DETECTED!")
        print("=" * 60)
        print("Script is on stand-by")
        print("Please solve the captcha in the browser window")
        print("The script will resume automatically once the CAPTCHA is solved")
        print("=" * 60 + "\n")
        
        while self.detect_captcha():
            time.sleep(2)
        
        print("CAPTCHA Solved! resuming script...\n")
        time.sleep(2)
    
    def extract_search_results(self):
        results = []
        try:
            time.sleep(2)
            search_results = self.driver.find_elements(By.CSS_SELECTOR, "div.g")
            for i, result in enumerate(search_results[:10], 1):
                try:
                    title_element = result.find_element(By.CSS_SELECTOR, "h3")
                    title = title_element.text
                    link_element = result.find_element(By.CSS_SELECTOR, "a")
                    url = link_element.get_attribute("href")
                    try:
                        desc_element = result.find_element(By.CSS_SELECTOR, "div[data-sncf='1'], div.VwiC3b")
                        description = desc_element.text
                    except:
                        description = "No description available"
                    if title and url:
                        results.append({
                            "position": i,
                            "title": title,
                            "url": url,
                            "description": description
                        })
                except Exception as e:
                    continue
        except Exception as e:
            print(f"Error while extracting results: {str(e)}")
        return results
    
    def save_results_to_file(self, target_site, target_name, filename=None):
        if filename is None:
            safe_target = target_site.replace("://", "_").replace("/", "_").replace(".", "_")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dorks_results_{safe_target}_{timestamp}.txt"
        
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write(f"GOOGLE DORKS SEARCH RESULTS:\n")
                f.write(f"Target Site: {target_site}\n")
                f.write(f"Target Name: {target_name}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Dork queries: {len(self.results)}\n")
                f.write("=" * 80 + "\n\n")
                
                for dork_result in self.results:
                    f.write("\n" + "=" * 80 + "\n")
                    f.write(f"DORK: {dork_result['dork']}\n")
                    f.write(f"Amount of results: {len(dork_result['results'])}\n")
                    f.write("=" * 80 + "\n\n")
                    
                    if dork_result['results']:
                        for res in dork_result['results']:
                            f.write(f"[{res['position']}] {res['title']}\n")
                            f.write(f"    URL: {res['url']}\n")
                            f.write(f"    Description: {res['description']}\n")
                            f.write("\n")
                    else:
                        f.write("    No result found.\n\n")
                
                f.write("\n" + "=" * 80 + "\n")
                f.write("END OF REPORT\n")
                f.write("=" * 80 + "\n")
            
            print(f"\nFile saved in: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"Error while saving: {str(e)}")
            return None
    
    def search_dork(self, dork_query, delay=3):
        try:
            self.driver.get("https://www.google.com")
            time.sleep(2)
            
            if self.detect_captcha():
                self.wait_for_captcha_resolution()
            
            try:
                reject_button = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Tout refuser') or contains(., 'Reject all') or contains(., 'Je refuse')]"))
                )
                reject_button.click()
                print("Cookies rejected")
                time.sleep(1)
            except:
                try:
                    more_options = self.driver.find_element(By.XPATH, "//button[contains(., 'Plus d') or contains(., 'More options')]")
                    more_options.click()
                    time.sleep(1)
                    
                    reject_button = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Tout refuser') or contains(., 'Reject all') or contains(., 'Je refuse')]"))
                    )
                    reject_button.click()
                    print("Cookies rejected")
                    time.sleep(1)
                except:
                    pass
            
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            
            search_box.clear()
            search_box.send_keys(dork_query)
            search_box.send_keys(Keys.RETURN)
            
            time.sleep(2)
            
            if self.detect_captcha():
                self.wait_for_captcha_resolution()
            
            search_results = self.extract_search_results()
            
            self.results.append({
                "dork": dork_query,
                "results": search_results
            })
            
            print(f"Ongoing query: {dork_query} ({len(search_results)} results)")
            time.sleep(delay)
            
        except Exception as e:
            print(f"Error while searching '{dork_query}': {str(e)}")
    
    def search_multiple_dorks(self, target_site, target_name, dorks_list, delay=3):
        print(f"\nTarget Site: {target_site}")
        print(f"Target Name: {target_name}")
        print(f"Amount of dorks to query: {len(dorks_list)}\n")
        
        for i, dork in enumerate(dorks_list, 1):
            full_query = dork.format(
                target=target_site,
                target_site=target_site,
                target_name=target_name
            )
            print(f"[{i}/{len(dorks_list)}] ", end="")
            self.search_dork(full_query, delay)
    
    def close(self):
        if self.driver:
            print("\nThe browser has been closed..")
            self.driver.quit()


def load_dorks_from_file(filename="all_dorks.txt"):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            dorks = []
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    line = line.strip('\'"')
                    dorks.append(line)
            return dorks
    except FileNotFoundError:
        print(f"Error: file '{filename}' not found")
        print(f"Please create a file '{filename}'")
        return []
    except Exception as e:
        print(f"Error while reading file: {str(e)}")
        return []


def main():
    TARGET_SITE = "amutis.fr"
    TARGET_NAME = "Amutis"
    BROWSER = "firefox"
    DELAY = 3
    DORKS_FILE = "all_dorks.txt"
    
    DORKS = load_dorks_from_file(DORKS_FILE)
    
    if not DORKS:
        print("No dork queries found, please specify one in the field 'DORKS_FILE'")
        return
    
    print(f"Loaded {len(DORKS)} dork queries from '{DORKS_FILE}'")
    
    searcher = GoogleDorksSearcher(browser=BROWSER)
    
    try:
        print("\nLaunching the script")
        print("=" * 50)
        
        searcher.start_browser()
        
        searcher.search_multiple_dorks(TARGET_SITE, TARGET_NAME, DORKS, delay=DELAY)
        
        searcher.save_results_to_file(TARGET_SITE, TARGET_NAME)
        
        print("\n" + "=" * 50)
        print("All searches are completed")
        print("The browser remains open")
        print("Press enter to close...")
        input()
        
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"\nError: {str(e)}")
    finally:
        searcher.close()


if __name__ == "__main__":
    main()