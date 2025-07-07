import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
from htmlmin import minify

logcookies = [
    {"name": "_gcl_au", "value": "1.1.1277857290.1715324936"},
    {"name": "_fbp", "value": "fb.2.1715324936558.590721107"},
    {"name": "_ga", "value": "GA1.1.422577978.1681101094"},
    {"name": "_ga_CKKBHDZQLJ", "value": "GS1.1.1716970836.4.1.1716971308.0.0.0"},
    {"name": "_ga_K0KBNZDRCL", "value": "GS1.1.1716970836.4.1.1716971308.0.0.0"},
    {"name": "_ga_E2TK7E0ESJ", "value": "GS1.1.1717048291.11.1.1717048299.52.0.0"},
    {"name": "_ga_YRV4PH7T16", "value": "GS1.1.1717048291.11.1.1717048299.52.0.0"},
    {"name": "_ga_ZM07YZZRDX", "value": "GS1.1.1717048297.4.1.1717048300.57.0.0"},
    {"name": "_ga_5VG6G31KPD", "value": "GS1.1.1717048297.4.1.1717048300.57.0.0"},
]

# Initialize the Selenium WebDriver
driver = webdriver.Safari()


# Function to set cookies and navigate to the desired page
def set_cookies_and_navigate(url):
    driver.get(url)

    for cookie in logcookies:
        driver.add_cookie(cookie)

    driver.refresh()

    # Wait for the page to load after setting cookies
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )


# Function to scrape data from a page using Beautiful Soup
def scrape_page(url):
    driver.get(url)

    # Wait for the page to load
    time.sleep(1)

    # Get the page source and parse it with Beautiful Soup
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    # Extract the desired data
    titles = [title.text for title in soup.find_all("h1")]  # Update as needed

    # strip \n, \t, and extra spaces from the titles
    titles = [title.strip() for title in titles]
    titles = [title.replace("\n", "") for title in titles]
    titles = [title.replace("\t", "") for title in titles]
    titles = [title.replace("  ", " ") for title in titles]
    titles = list(filter(None, titles))
    titles = list(set(titles))

    # get the html of the page a div with class name "section-tree", or sometimes if "main-content" is not available, a div with class name "article-body"
    main_content_html = soup.find("div", class_="section-tree")
    if main_content_html is None:
        main_content_html = soup.find("div", class_="article-body")
    if main_content_html is None:
        main_content_html = soup.find("div", class_="content")
    if main_content_html is None:
        main_content_html = soup.find("main", class_="l-main")
    if main_content_html is None:
        main_content_html = soup.find("section", class_="p-body")
    if main_content_html is None:
        main_content_html = soup.find("div", class_="main-content")
    if main_content_html is None:
        main_content_html = soup.find("div", class_="main-contents")

    if main_content_html is not None:
        main_content_html = str(main_content_html)
        main_content_html = minify(main_content_html, remove_empty_space=True)
    else:
        main_content_html = "N/A"
        # print URL
        print(f"🔥 {url} does not have main content")

    os.makedirs("data", exist_ok=True)
    timestamp = int(time.time())
    # Save the HTML content to a text file
    file_name = f"data/scraped_data_{timestamp}.txt"
    with open(file_name, "w") as file:
        file.write(main_content_html)

    # Append to the csv file
    with open("scraped_data.csv", "a") as file:
        file.write(f"{url},{titles},{file_name}\n")

    print(f"👉 {titles}, 🚧 Content: {main_content_html != 'N/A'} - {timestamp}")

    return {
        "url": url,
        "titles": titles,
        "file_path": file_name,
    }


# Read the Excel file containing the URLs
url_csv_file = "ritsumeikan_urls
 .csv"
df = pd.read_csv(url_csv_file)
urls = df["URL"].tolist()  # Assuming the column with URLs is named 'Links'

# Scrape data from each URL
all_data = []
for url in urls:
    data = scrape_page(url)
    all_data.append(data)
    # break

# Close the WebDriver
driver.quit()

# Save the scraped data to a new CSV file
# output_df = pd.DataFrame(
#     all_data, columns=["URL", "Titles", "Folder Name", "File Path"]
# )
# output_df.to_csv("scraped_data.csv", index=False)

print("Data scraped and saved to scraped_data.csv")
