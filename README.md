# Wikipedia Scraper

## Description
The Wikipedia Scraper is a Python script that collects information about political leaders of various countries from an external API and generates structured data in either JSON or CSV format. The project consists of two branches:

- **Feature Branch:**
  - Implements a scraper that builds a JSON file with information about the political leaders of each country obtained from the API.
  - Extracts the first paragraph of the leaders' Wikipedia pages for inclusion in the JSON file.

- **Main Branch:**
  - Includes all features from the feature branch.
  - Utilizes the `Session()` class instead of `requests.get()` for making HTTP requests.
  - Provides an option to switch between storing the output as JSON or CSV.

## Installation

1. Clone the repository to your local machine:
   
   ```
   git clone https://github.com/your-username/wikipedia-scraper.git
   ```

2. Navigate to the project directory:

```
cd wikipedia-scraper
```

3. Create a virtual environment:
   
```
python3 -m venv [name_of_the_virtual_environment]
```

4(a). Activate the virtual environment (on Windows):

```
.\[name_of_the_virtual_environment]\Scripts\activate
```

4(b). Activate the virtual environment (on Unix or MacOS):

```
source [name_of_the_virtual_environment]/bin/activate
```

5.Install dependencies:

```
pip install -r requirements.txt
```

## Usage
Run the main script to collect data and store it in either JSON or CSV format, if you are on the main branch or only json if you are on the feature branch:

```
python main.py
```

Follow the on-screen instructions to choose the output format. The script will process countries, retrieve leaders' data, and update first paragraphs, based on the selected branch.


![giphy (1)](https://github.com/Lucky-sketch/wikipedia-scraper/assets/53155116/c708a111-d37e-4dc5-957b-cbff1bda2a62)


