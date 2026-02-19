from fastapi import FastAPI, HTTPException
import requests
from bs4 import BeautifulSoup

app = FastAPI()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_target_price(url):
    """Fetch the target price from the consensus page."""

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    td_elements = soup.find_all("td", class_="c-table__cell c-table__cell--dotted c-table__cell--bold")

    if len(td_elements) > 4:
        price_spans = td_elements[4].find_all("span", class_="c-table__content")
        if price_spans:
            return price_spans[0].get_text(strip=True).split()[0]  # Extract price
    return None

def extract_financial_data(response_url, soup):
    """Extract financial data from a Boursorama course page."""
    output = {}
    output['Main url'] = response_url
    
    # Extract table row data for "1 an", "3 ans", "5 ans"
    for row in soup.find_all("tr", class_="c-table__row"):
        first_col = row.find("th")
        if first_col and first_col.get_text(strip=True) in ["1 an", "3 ans", "5 ans"]:
            data = [cell.get_text(strip=True).replace("\u202f", "") for cell in row.find_all(["th", "td"])]
            output[data[0]] = data[1]

    # Extract numerical values
    values = [
        cell.get_text(strip=True).split()[0] 
        for cell in soup.find_all("td", class_="c-table__cell c-table__cell--dotted c-table__cell--inherit-height c-table__cell--align-top / u-text-left u-text-right u-ellipsis")
    ]

    # Extract years
    years = [
        h3.get_text(strip=True)[-4:]
        for h3 in soup.find_all("h3", class_="c-table__title u-text-uppercase u-text-size-xxxs u-text-normal-whitespace")
        if h3.get_text(strip=True)[-4:].isdigit()
    ]

    # Map values to corresponding years
    for index, year in enumerate(years):
        if index < len(values) and (index + 9) < len(values):  # Avoid IndexError
            output[f'Dividende par action {year}'] = values[index]
            output[f'PER {year}'] = values[index + 9]

    consensus_url = response_url.replace("cours/", "cours/consensus/", 1)
    output['Objectif de cours'] = fetch_target_price(consensus_url) or "Price data unavailable"
    output['Consensus url'] = consensus_url
    return output

def query_company(company_name, recursive_call=True):
    """Search for a company and extract financial data from Boursorama."""
    
    # Étape 1: Essayer d'abord l'URL directe avec le ticker (actions internationales)
    if len(company_name) <= 5 and company_name.isupper():
        direct_url = f"https://www.boursorama.com/cours/{company_name}/"
        response = requests.get(direct_url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            return extract_financial_data(response.url, soup)
    
    # Étape 2: Utiliser la recherche pour découvrir l'URL correcte
    search_url = f"https://www.boursorama.com/recherche/?query={company_name}"
    response = requests.get(search_url, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Failed to fetch data. Status Code: {response.status_code}")

    # Étape 3: Analyser la réponse de recherche
    response_url = response.url
    soup = BeautifulSoup(response.text, "html.parser")

    # Si la recherche redirige directement vers une page de cours
    if response_url.startswith("https://www.boursorama.com/cours/"):
        return extract_financial_data(response_url, soup)

    # Étape 4: Chercher le premier lien vers une page de cours dans les résultats
    # Chercher tous les liens qui mènent vers /cours/
    course_links = soup.find_all("a", href=True)
    for link in course_links:
        href = link.get('href')
        if href and '/cours/' in href:
            # Construire l'URL complète si nécessaire
            if href.startswith('/'):
                full_url = f"https://www.boursorama.com{href}"
            else:
                full_url = href
            
            # Essayer ce lien
            try:
                course_response = requests.get(full_url, headers=headers)
                if course_response.status_code == 200:
                    course_soup = BeautifulSoup(course_response.text, "html.parser")
                    return extract_financial_data(course_response.url, course_soup)
            except:
                continue

    # Étape 5: Fallback - chercher un lien texte (ancien comportement)
    if recursive_call:
        link_tag = soup.find("a", class_="c-link c-link--animated / o-ellipsis")
        if link_tag:
            return query_company(link_tag.text.strip(), recursive_call=False)

    return {}

@app.get("/query")
def get_stock_info(company_name: str):
    """API endpoint to get stock information."""
    return query_company(company_name)
