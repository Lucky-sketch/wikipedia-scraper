from requests import Session
from src.scraper import WikipediaScraper

def process_countries(scraper):
    """
    Process countries, retrieve leaders' data, and update first paragraphs.
    """
    countries = scraper.get_countries()

    print("Processing... ")
    for country in countries:
        try:
            if not scraper.cookie_fresh():
                scraper.refresh_cookie()
            else:
                scraper.get_leaders(country)
                for leader in scraper.leaders_data[country]:
                    wikipedia_url = leader.get("wikipedia_url")
                    id = leader.get('id')
                    first_paragraph = scraper.clean_paragraph(scraper.get_first_paragraph(wikipedia_url))
                    scraper.update_leaders_data(country, first_paragraph, id)

        except Exception as e:
            print(f"Error processing {country}: {e}")

def main():
    """
    Main entry point for the program.
    """
    try:
        scraper = WikipediaScraper(Session())
        scraper.refresh_cookie()

        # Process countries and update leaders' data
        process_countries(scraper)

        # Switch to store data in different formats
        choice1 = input("Do you want to store the data as json(1) or csv(2): ")
        if choice1 == "1":
            scraper.to_json_file("output.json")
        elif choice1 == "2":
            scraper.to_csv_file("output.csv")

    except Exception as main_error:
        print(f"Main Error: {main_error}")

if __name__ == '__main__':
    main()
