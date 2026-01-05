import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# List of URLs for all legs (FencingTimeLive tournament url for the specific event)
leg_urls = [
    'https://www.fencingtimelive.com/events/results/127C9B14E0A24F2A824030C5AC81675B',  # Leg 1
    'https://www.fencingtimelive.com/events/results/C2E92E78172249638BA67990ABB81EAE',  # Leg 2
    'https://www.fencingtimelive.com/events/results/432B3D7ABF8145B7A13ECD6DB1F66D73',  # Leg 3
    'https://www.fencingtimelive.com/events/results/C277D8A840A745BBB187C113FBE112E0',  # Leg 4
    'https://www.fencingtimelive.com/events/results/68D27D2642314BA48F4443B0D081518B',  # Leg 5
]

path = '/Users/dancanlas/chromedriver-mac-x64/chromedriver'

options = Options()
options.add_experimental_option("detach", True)
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)

all_bouts = []  # Master list for all legs

for leg_index, website in enumerate(leg_urls, start=1):
    driver.get(website)

    # Head over to the Pools tab
    pools_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Pools')]"))
    )
    pools_button.click()

    # Find all Details buttons
    details_buttons = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.btn.btn-primary.btn-sm"))
    )
    print(f"Leg {leg_index}: Found {len(details_buttons)} Details buttons")

    # Loop through each Details button
    for i in range(len(details_buttons)):
        details_buttons = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.btn.btn-primary.btn-sm"))
        )
        link = details_buttons[i].get_attribute("href")

        # Open Details page in new tab
        driver.execute_script("window.open(arguments[0]);", link)
        driver.switch_to.window(driver.window_handles[1])

        # Find Bout Order table
        tables = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table")))
        bout_table = None
        for table in tables:
            header_cells = table.find_elements(By.TAG_NAME, "th")
            headers = [cell.text.strip() for cell in header_cells]
            if "Right Fencer" in headers and "Left Fencer" in headers:
                bout_table = table
                break

        # Extract rows
        if bout_table:
            table_rows = bout_table.find_elements(By.TAG_NAME, "tr")
            for row in table_rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if cells and len(cells) >= 5:
                    right_fencer = cells[1].text.strip()
                    score1 = cells[2].text.strip()
                    score2 = cells[3].text.strip()
                    left_fencer = cells[4].text.strip()
                    pool_number = f"pool{i + 1}"
                    all_bouts.append([leg_index, pool_number, right_fencer, score1, score2, left_fencer])

        # Close tab and return to main page
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(0.5)

# Convert all bouts to a single DataFrame
all_legs_df = pd.DataFrame(
    all_bouts,
    columns=["Leg", "Pool", "Right Fencer", "Score1", "Score2", "Left Fencer"]
)

# Save to CSV if desired
all_legs_df.to_csv("Men's Saber datasets/all_legs_pool_bouts_ms.csv", index=False)

# Close browser
driver.quit()

print("Scraping complete! Combined DataFrame created.")
