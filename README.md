# ScrapeEase

ScrapeEase is a Python-based web scraping tool with a graphical user interface (GUI) that allows users to easily scrape text content and links from webpages. The tool provides options to export the scraped data in multiple formats, including PDF, CSV, and TXT.

## Features

- **Web Scraping**: Retrieve text content and links from webpages by entering the URL and optional CSS selector.
- **Export Options**: Export scraped data in various formats, including PDF, CSV, and TXT.
- **GUI Interface**: User-friendly graphical interface for easy interaction and data retrieval.
- **Instructions**: Access instructions on how to use the tool directly from the GUI.

## Usage

1. **Enter URL**: Input the URL of the webpage you want to scrape in the designated text field.
2. **Optional Selector**: Enter an optional CSS selector to target specific elements on the webpage (e.g., `p`, `h1`, `.my-class`).
3. **Select Data**: Check the options for the type of data you want to scrape (Text, Links).
4. **Scrape**: Click the "Scrape" button to retrieve content from the webpage.
5. **Export Results**: Choose the desired export format(s) (PDF, CSV, TXT) and click the "Export Results" button to save the scraped content.
6. **Instructions**: Click the "Instructions" button to access detailed instructions on how to use the tool.

## Dependencies

- `requests`: For sending HTTP requests to retrieve webpage content.
- `beautifulsoup4`: For parsing HTML content and extracting data.
- `reportlab`: For generating PDF files.
- `tkinter`: For building the graphical user interface.

## Installation

1. Clone the repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Run the `scraper.py` file to launch the ScrapeEase GUI.



## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
