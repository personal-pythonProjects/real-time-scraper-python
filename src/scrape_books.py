import requests
from bs4 import BeautifulSoup

def scrape_books(url):
    """Scrapes book data from Books to Scrape."""
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; '
                                                            'Win64; x64; rv:132.0) Gecko/20100101 '
                                                            'Firefox/132.0'}, timeout=10)
        response.raise_for_status()
        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.text, 'html.parser')

        book_items = soup.find_all('article', class_='product_pod')

        for book in book_items:
            title = book.h3.a['title']
            price = book.find('p', class_='price_color').text
            availability = book.find('p', class_='availability').text.strip()

            yield f"Title: {title}, \nPrice: {price}, \nAvailability: {availability} \n"

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while making a request: {e}")

def export_to_txt(data):
    """Exports book data to a text file."""
    try:
        file_name = 'book_list'
        with open(f'{file_name}.txt', 'w') as f:
            f.write('\n'.join(data))

        print(f'Data successfully exported to {file_name}.txt.')
    except FileNotFoundError:
        print('Error: The specified file path was not found.')
    except ValueError:
        print('Error: Invalid data format.')
    except Exception as e:
        print(f'Unexpected error: {e}')

if __name__ == "__main__":
    # Scrape books from the website
    book_list = scrape_books('https://books.toscrape.com/')

    # Print scraped book data
    for book in book_list:
        print(book)

    # Export book data to a text file
    export_to_txt(book_list)



