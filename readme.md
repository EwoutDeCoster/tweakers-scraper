# Tweakers Price Scraper README

## Overview
The Tweakers Price Scraper is a sophisticated Python application designed to harvest pricing and specification data for products listed on the popular Dutch tech site, Tweakers.net. By employing this tool, users can effortlessly compare prices and specs from various retailers, making it an indispensable resource for savvy shoppers and professionals alike. The application features a user-friendly web interface powered by Flask, enabling searches directly through a browser.

## Key Features
- **Effortless Product Searches**: Input a product name to fetch relevant listings.
- **Comprehensive Price Listings**: View a curated list of retailer prices for your searched product, neatly organized from lowest to highest.
- **Detailed Product Specifications**: Access a complete rundown of product specs to make informed decisions.
- **Price Analytics**: Get insights with calculated average and median prices across retailers.
- **EAN Code Revelation**: Quickly identify products with European Article Numbers for easy reference.

## Getting Started

### Prerequisites
- Python 3.8+
- Flask
- BeautifulSoup4
- requests
- unidecode
- Selenium WebDriver for Chrome

### Installation Guide

1. **Clone the Project**:
   ```
   git clone https://github.com/your-username/tweakers-price-scraper.git
   cd tweakers-price-scraper
   ```

2. **Set Up the Environment**:
   - Create and activate a virtual environment:
     ```
     python -m venv venv
     source venv/bin/activate  # Use `venv\Scripts\activate` on Windows
     ```
   - Install dependencies:
     ```
     pip install -r requirements.txt
     ```

3. **Chrome WebDriver**:
   - Ensure you have the Chrome WebDriver downloaded and set in your system's PATH. The WebDriver is crucial for the application's scraping functionality.

4. **Launch the Application**:
   - Run the Flask server:
     ```
     python gui.py
     ```
   - The web interface will be accessible at `http://localhost:80/`.

## How to Use

- Open your browser and head to `http://localhost:80/`.
- Type the name of the product you're interested in into the provided field.
- Hit "Search" to display a comprehensive list of prices, specs, and other relevant data for your queried product.

## Expanded Utility

This scraper's utility extends beyond simple price comparisons, offering potential for integration into larger systems and projects:

- **Price Alert Systems**: Tailor the scraper to monitor and alert you to price drops, ensuring you never miss a deal.
- **ERP System Integration for Retailers**: Integrate this tool into your retail ERP system for real-time competitor price monitoring, enabling dynamic pricing strategies.
- **Market Research**: Utilize the scraper for detailed market analysis and trend tracking over time.

## Considerations

- The application uses a headless Chrome session to navigate and scrape data, necessitating a compatible Chrome WebDriver in your PATH.
- To maintain respectful use, avoid excessive request rates that could lead to being rate-limited by the target site.
- Intended for personal and educational use, users should adhere to Tweakers.net's terms of service.

## Disclaimer
This tool is intended for personal and educational use only. Users should adhere to Tweakers.net's terms of service when using this scraper. The developer of the Tweakers Price Scraper is not responsible for any misuse of the tool or any potential consequences that arise from its use. Users should ensure that their actions comply with the legal and ethical standards applicable in their jurisdiction.

## License
This project is released under the MIT License. For more details, see the LICENSE file.