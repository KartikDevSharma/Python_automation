import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
import schedule
import time
import os
import argparse
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_github_trending():
    url = "https://github.com/trending"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch data: {e}")
        return pd.DataFrame()

    soup = BeautifulSoup(response.content, 'html.parser')
    
    repos = []
    for repo in soup.select('article.Box-row'):
        try:
            name_element = repo.select_one('h2.h3.lh-condensed')
            name = name_element.text.strip()
            full_name = name_element.select_one('a')['href'].strip('/')
            
            description_element = repo.select_one('p.col-9')
            description = description_element.text.strip() if description_element else "No description"
            
            language_element = repo.select_one('span[itemprop="programmingLanguage"]')
            language = language_element.text.strip() if language_element else "Unknown"
            
            stars_element = repo.select_one('a.muted-link[href$="stargazers"]')
            stars = int(stars_element.text.strip().replace(',', '')) if stars_element else 0
            
            today_stars_element = repo.select_one('span.d-inline-block.float-sm-right')
            today_stars = int(today_stars_element.text.strip().split()[0].replace(',', '')) if today_stars_element else 0
            
            repos.append({
                'name': name,
                'full_name': full_name,
                'description': description,
                'language': language,
                'stars': stars,
                'today_stars': today_stars
            })
        except Exception as e:
            logging.warning(f"Error parsing repository: {e}")
    
    if not repos:
        logging.warning("No repositories found. The page structure might have changed.")
    
    return pd.DataFrame(repos)

def analyze_data(df):
    language_counts = df['language'].value_counts()
    avg_stars = df['stars'].mean()
    total_stars = df['stars'].sum()  # Add this line
    total_today_stars = df['today_stars'].sum()
    top_languages = language_counts.head(10)
    top_repos = df.sort_values('today_stars', ascending=False).head(10)
    
    return language_counts, avg_stars, total_stars, total_today_stars, top_languages, top_repos

def create_visualizations(language_counts, top_repos):
    plt.figure(figsize=(10, 10))
    plt.pie(language_counts.values, labels=language_counts.index, autopct='%1.1f%%', startangle=90)
    plt.title('Distribution of Programming Languages')
    plt.axis('equal')
    plt.tight_layout(pad=3.0)
    plt.savefig('language_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()

    plt.figure(figsize=(12, 8))
    chart = sns.barplot(x='today_stars', y='name', data=top_repos)
    plt.title('Top 10 Trending Repositories by Stars Gained Today')
    plt.xlabel('Stars Gained Today')
    plt.ylabel('Repository')
    
    # Fix for the UserWarning
    ticks = chart.get_xticks()
    chart.set_xticks(ticks)
    chart.set_xticklabels(chart.get_xticklabels(), rotation=45, ha='right')
    
    plt.tight_layout(pad=3.0)
    plt.savefig('top_repos.png', dpi=300, bbox_inches='tight')
    plt.close()

def generate_report(df, language_counts, avg_stars, total_stars, total_today_stars, top_languages, top_repos):
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, 'GitHub Trending Repositories Report', 0, 1, 'C')
        
        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    pdf = PDF()
    pdf.add_page()
    
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 10, f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Summary", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 5, f"Number of repositories analyzed: {len(df)}")
    pdf.multi_cell(0, 5, f"Average number of stars: {avg_stars:.2f}")
    pdf.multi_cell(0, 5, f"Total stars gained today: {total_today_stars}")
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Top Programming Languages", ln=True)
    pdf.set_font("Arial", "", 10)
    for lang, count in top_languages.items():
        pdf.cell(0, 5, f"{lang}: {count}", ln=True)
    pdf.ln(5)
    
    pdf.image("language_distribution.png", x=10, y=pdf.get_y(), w=190)
    pdf.ln(140)  # Adjust this value to ensure proper placement
    
    pdf.add_page()
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Top Trending Repositories", ln=True)
    pdf.image("top_repos.png", x=10, y=pdf.get_y(), w=190)
    pdf.ln(140)  # Adjust this value to ensure proper placement
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Summary", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 5, f"Number of repositories analyzed: {len(df)}")
    pdf.multi_cell(0, 5, f"Total number of stars: {total_stars:,}")  # Add this line
    pdf.multi_cell(0, 5, f"Average number of stars: {avg_stars:.2f}")
    pdf.multi_cell(0, 5, f"Total stars gained today: {total_today_stars}")
    pdf.ln(5)
    pdf.set_font("Arial", "", 8)
    for _, row in top_repos.iterrows():
        pdf.cell(80, 6, row['name'][:30], border=1)
        pdf.cell(30, 6, row['language'], border=1)
        pdf.cell(30, 6, str(row['stars']), border=1)
        pdf.cell(50, 6, str(row['today_stars']), border=1)
        pdf.ln()
    
    pdf.output("github_trends_report.pdf")

def run_analysis():
    logging.info("Running GitHub Trends analysis...")
    df = scrape_github_trending()
    if df.empty:
        logging.error("Unable to scrape data. Exiting analysis.")
        return
    language_counts, avg_stars, total_stars, total_today_stars, top_languages, top_repos = analyze_data(df)
    create_visualizations(language_counts, top_repos)
    generate_report(df, language_counts, avg_stars, total_stars, total_today_stars, top_languages, top_repos)
    logging.info("Analysis complete. Report generated: github_trends_report.pdf")
def main():
    parser = argparse.ArgumentParser(description="GitHub Trends Analyzer")
    parser.add_argument("--schedule", action="store_true", help="Run the script daily at 9:00 AM")
    args = parser.parse_args()

    run_analysis()

    if args.schedule:
        logging.info("Scheduling daily runs at 9:00 AM. Press Ctrl+C to exit.")
        schedule.every().day.at("09:00").do(run_analysis)
        while True:
            schedule.run_pending()
            time.sleep(60)

if __name__ == "__main__":
    main()