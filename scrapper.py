import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def scrape_wikipedia_data(url, scrape_headlines, selected_headlines_tags, scrape_links, scrape_media, scrape_tags, scrape_p_tags):
    driver = get_driver()
    try:
        driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        tables = scrape_tables(soup)
        headlines = scrape_headlines_func(soup, scrape_headlines, selected_headlines_tags)
        links = scrape_links_func(soup, scrape_links)
        media = scrape_media_func(soup, scrape_media)
        tags_data = scrape_tags_func(soup, scrape_tags)
        p_tags_data = scrape_p_tags_func(soup, scrape_p_tags)

        return tables, headlines, links, media, tags_data, p_tags_data, None
    except Exception as e:
        return None, None, None, None, None, None, f"Error occurred: {str(e)}"

def scrape_tables(soup):
    tables = soup.find_all("table", {"class": "wikitable"})
    all_table_data = []
    for i, table in enumerate(tables, 1):
        st.write(f"Scraping Table {i}...")
        rows = table.find_all("tr")
        headers = [th.text.strip() for th in rows[0].find_all("th")]
        data = [[col.text.strip() for col in row.find_all(["th", "td"])] for row in rows[1:]]
        df = pd.DataFrame(data, columns=headers)
        all_table_data.append(df)
    if not tables:
        st.warning("No tables found on this page.")
    return all_table_data

def scrape_headlines_func(soup, scrape_headlines, selected_headlines_tags):
    if not scrape_headlines:
        return []
    headlines = []
    for tag in selected_headlines_tags:
        headline_tags = soup.find_all(tag)
        headlines += [tag.text.strip() for tag in headline_tags]
    return headlines

def scrape_links_func(soup, scrape_links):
    if not scrape_links:
        return []
    anchor_tags = soup.find_all("a", href=True)
    return [a['href'] for a in anchor_tags if a['href'].startswith("http")]

def scrape_media_func(soup, scrape_media):
    if not scrape_media:
        return {"images": [], "videos": [], "audios": []}
    media = {
        "images": [img['src'] for img in soup.find_all("img", src=True)],
        "videos": [video['src'] for video in soup.find_all("video", src=True)],
        "audios": [audio['src'] for audio in soup.find_all("audio", src=True)]
    }
    return media

def scrape_tags_func(soup, scrape_tags):
    if not scrape_tags:
        return {}
    tags_data = {}
    for tag in scrape_tags:
        tags = soup.find_all(tag)
        tags_data[tag] = [t.text.strip() for t in tags]
    return tags_data

def scrape_p_tags_func(soup, scrape_p_tags):
    if not scrape_p_tags:
        return []
    p_tags = soup.find_all("p")
    return [p.text.strip() for p in p_tags]

def start_scraping(url, scrape_headlines, selected_headlines_tags, scrape_links, scrape_media, scrape_tags, scrape_p_tags):
    with st.spinner("Scraping in progress..."):
        table_data, headlines, links, media, tags_data, p_tags_data, error = scrape_wikipedia_data(url, scrape_headlines, selected_headlines_tags, scrape_links, scrape_media, scrape_tags, scrape_p_tags)
        if error:
            st.error(error)
        else:
            st.success("Data scraped successfully!")
            display_results(table_data, headlines, links, media, tags_data, p_tags_data)

def display_results(table_data, headlines, links, media, tags_data, p_tags_data):
    combined_data = {
        "Tables": table_data,
        "Headlines": headlines,
        "Links": links,
        "Images": media["images"],
        "Videos": media["videos"],
        "Audios": media["audios"],
        "Tags": tags_data,
        "P_Tags": p_tags_data
    }

    for i, df in enumerate(table_data, 1):
        st.write(f"Table {i}:")
        st.write(df)

    if headlines:
        st.write("Headlines Found:")
        for headline in headlines:
            st.write(f"- {headline}")

    if links:
        st.write("Links Found:")
        for link in links:
            st.write(f"- {link}")

    if media["images"]:
        st.write("Images Found:")
        for img in media["images"]:
            st.write(f"- {img}")

    if media["videos"]:
        st.write("Videos Found:")
        for video in media["videos"]:
            st.write(f"- {video}")

    if media["audios"]:
        st.write("Audios Found:")
        for audio in media["audios"]:
            st.write(f"- {audio}")

    if tags_data:
        st.write("Tags Found:")
        for tag, texts in tags_data.items():
            st.write(f"{tag}:")
            for text in texts:
                st.write(f"- {text}")

    if p_tags_data:
        st.write("P Tags Found:")
        for p_text in p_tags_data:
            st.write(f"- {p_text}")

    combined_df = pd.DataFrame.from_dict(combined_data, orient='index').transpose()
    csv_combined = combined_df.to_csv(index=False)
    st.download_button(label="Download Combined Data CSV", data=csv_combined, file_name="scraped_data.csv", mime="text/csv")
    

st.title("Web Scrapper - Tools")
st.write("Table, Headline, Link, Media, and Tag Scraper")


with st.sidebar:
    st.title("Web Scrapper - Tools")
    url = st.text_input("Enter the URL:")
    scrape_headlines = st.checkbox("Scrape Headlines")
    headline_tags = ["h1", "h2", "h3", "h4", "h5", "h6"]
    selected_headlines_tags = st.multiselect("Select headlines to scrape:", headline_tags)
    scrape_links = st.checkbox("Scrape Links")
    scrape_media = st.checkbox("Scrape Media (Images, Videos, Audios)")
    scrape_tags = st.multiselect("Select tags to scrape:", ["p", "span", "div", "li", "ul", "ol", "a"])
    scrape_p_tags = st.checkbox("Scrape paragraph")

if st.button("Start Scraping"):
    start_scraping(url, scrape_headlines, selected_headlines_tags, scrape_links, scrape_media, scrape_tags, scrape_p_tags)


def about_page():
    st.markdown("---")
    st.header("About ")
    st.info("This project is a web scraping tool developed using Streamlit, Selenium, and BeautifulSoup. It allows users to extract structured and unstructured data from web pages, including tables, headlines, links, media files, specific HTML tags, and paragraphs. The project is designed to provide an intuitive user interface and robust scraping capabilities, making it accessible to both developers and non-technical users.")
    st.write("""
             
        ###### Key Features
         
        1. Streamlit Interface:
             - User-Friendly Input Options:
                - URL input field for specifying the target web page.
                - Checkboxes and dropdown menus for selecting the type of data to scrape.
             
             - Interactive Display:
                - Scraped data is displayed in a categorized and readable format.
                - Option to download combined scraped data as a CSV file
        
        2. Data Extraction Capabilities:
            - **Tables:** Extracts and formats data from HTML tables with the class wikitable.
            - **Headlines:** Scrapes headlines based on user-selected tags (e.g., h1, h2, h3).
            - **Links**: Extracts hyperlinks from anchor (a) tags.
            - **Media Files:** Identifies and lists sources of images, videos, and audio files.
            - **Specific Tags:** Allows users to target specific HTML tags (e.g., div, span, li) for scraping.
            - **Paragraphs:** Extracts text from all paragraph (p) tags.
             
        3. Headless Browsing:
            - Utilizes Selenium’s headless mode to perform scraping without opening a browser window, improving performance and user convenience.

        4. Error Handling:
            - Provides meaningful error messages in case of invalid URLs, network issues, or inaccessible pages.
             

        ##### Technical Details
             
        1. Core Libraries Used:
             - **Streamlit:** For creating an interactive web interface.
             - **Selenium:** For automating web browsing and scraping dynamic content.
             - **BeautifulSoup:** For parsing and extracting data from HTML.
             - **Pandas:** For organizing scraped data into structured formats.
             
        2. Functions:
             - get_driver()
                - Initializes a Selenium WebDriver with options for headless browsing, GPU acceleration, and sandboxing.
             
             - scrape_tables(soup)
                - Extracts data from HTML tables with the class wikitable and formats it as Pandas DataFrames.
             
             - scrape_headlines_func(soup, scrape_headlines, selected_headlines_tags)
                - Scrapes headlines based on selected tags (e.g., h1, h2).

             - scrape_links_func(soup, scrape_links)
                - Extracts all hyperlinks from anchor (a) tags.

             - scrape_media_func(soup, scrape_media)
                - Retrieves sources of images, videos, and audio files.

             - scrape_tags_func(soup, scrape_tags)
                - Extracts text content from user-selected HTML tags.

             - scrape_p_tags_func(soup, scrape_p_tags)
                - Extracts and returns text content from paragraph tags.

             - start_scraping()
                - Orchestrates the scraping process based on user input and invokes other functions.

             - display_results()
                - Displays the scraped data and provides a CSV download option.

             - about_page()
                - Shows a brief description of the project in the Streamlit app.
             
        ##### User Workflow

        1. Input the URL:
            - Enter the web page URL into the input field.

        2. Select Data to Scrape:
            - Choose from options such as headlines, links, media files, specific tags, and paragraphs.
            - For headlines or tags, select specific HTML tags to target.

        3. Start Scraping:
            - Click the "Start Scraping" button to begin the process.

        4. View and Download Results:
            - Review the scraped data displayed in the app.
            - Download the combined data as a CSV file if needed.
             

        ##### Challenges and Solutions

        1. Dynamic Content:
            - **Challenge:** Extracting data from JavaScript-rendered pages.
            - **Solution:** Utilized Selenium’s WebDriver to render dynamic content before scraping.

        2. Performance:
            - **Challenge:** Delays due to large pages or extensive scraping operations.
            - **Solution:** Enabled headless browsing and optimized the scraping functions for speed.

        3. Error Handling:
            - **Challenge:** Handling invalid URLs or network errors.
            - **Solution:** Implemented try-except blocks to capture and display descriptive error messages.

             
        ##### Future Enhancements

        1. Improved Filtering:
            - Add options to filter scraped data, such as selecting specific rows or columns from tables.

        2. Browser Selection:
            - Allow users to choose between browsers (e.g., Chrome, Firefox).

        3. Pagination Support:
            - Enable scraping of multi-page content by navigating through paginated results.

        4. Data Visualization:
            - Integrate charts or graphs to visualize scraped data within the app.

        5. API Integration:
            - Provide scraped data as an API for developers to integrate into other applications.
             
            
        ##### Conclusion
        
        The Web Scraper Tool is a powerful and versatile application designed for extracting valuable data from web pages. Its combination of an intuitive interface and comprehensive scraping capabilities makes it suitable for a wide range of use cases, from research to business intelligence. By leveraging technologies like Selenium, BeautifulSoup, and Streamlit, this project demonstrates the potential of combining automation with user-friendly design.
    """)
about_page()
