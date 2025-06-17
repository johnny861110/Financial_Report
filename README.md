# Financial Agent Project

## Overview
This project is designed to scrape financial data from the Taiwan Stock Exchange (TWSE) and generate reports. It includes a Python script for data scraping and a batch file for running the scraper.

## File Structure
- **twse_scraper.py**: The main Python script for scraping TWSE data.
- **run_scraper.bat**: A batch file to execute the scraper script.
- **reports/**: A directory containing generated reports, such as `202501_2337_AI1.pdf`.

## Requirements
- Python 3.8 or higher
- Virtual environment (`venv`) for dependency management

## Setup
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd financial_agent
   ```
3. Set up the virtual environment:
   ```
   python -m venv venv
   ```
4. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```
5. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Run the scraper using the batch file:
   ```
   run_scraper.bat
   ```
2. Check the `reports/` directory for generated reports.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Author
Johnn
