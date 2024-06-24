# GitHub Trends Analyzer

## Overview

GitHub Trends Analyzer is a Python-based automation project that scrapes, analyzes, and reports on trending repositories from GitHub. This tool provides insights into popular programming languages, repository statistics, and generates a comprehensive PDF report with visualizations.

## Features

- Web scraping of GitHub's trending repositories
- Data analysis of scraped repository information
- Visualization of programming language popularity
- Bar chart of top trending repositories
- PDF report generation with insights and visualizations
- Automated daily execution option

## Requirements

- Python 3.7+
- pip (Python package installer)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/KartikDevSharma/Python_automation/new/main/github_trends_analyzer.git
   cd github_trends_analyzer
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the GitHub Trends Analyzer:

1. For a one-time analysis:
   ```
   python github_trends_analyzer.py
   ```

2. To set up daily scheduled runs:
   ```
   python github_trends_analyzer.py --schedule
   ```
   This will perform an initial analysis and then schedule daily runs at 9:00 AM. To stop the scheduled runs, press Ctrl+C.

## Output

The script generates three main outputs in the same directory:

1. `language_distribution.png`: A pie chart showing the distribution of programming languages.
2. `top_repos.png`: A bar chart of the top trending repositories.
3. `github_trends_report.pdf`: A comprehensive PDF report including:
   - Summary statistics
   - Top programming languages
   - Language distribution chart
   - Top trending repositories chart
   - Detailed table of top repositories

## Customization

You can modify the `github_trends_analyzer.py` script to customize various aspects of the analysis:

- Change the scheduling time by modifying the `schedule.every().day.at("09:00")` line in the `main()` function.
- Adjust the number of top repositories or languages shown by modifying the relevant parameters in the `analyze_data()` function.
- Customize the report layout and content by editing the `generate_report()` function.

## Troubleshooting

If you encounter any issues:

1. Ensure all dependencies are correctly installed.
2. Check your internet connection, as the script requires web access to scrape GitHub.
3. Verify that you have write permissions in the script's directory for generating output files.
4. If you encounter persistent scraping issues, you may need to implement more advanced techniques like using Selenium for browser automation or consider using GitHub's API.

## Contributing

Contributions to improve GitHub Trends Analyzer are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Disclaimer

This tool is for educational and analytical purposes only. Ensure you comply with GitHub's terms of service and robots.txt when using this tool. Be mindful of potential rate limiting when making frequent requests to GitHub.
