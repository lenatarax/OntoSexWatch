import requests
import xml.etree.ElementTree as ET
import csv
import os
from datetime import datetime

# Fonction pour récupérer les données de PubMed
def fetch_pubmed_data():
    # Exécuter la requête PubMed pour obtenir les résultats
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": "developmental biology sex ontogenesis",  # Mots-clés
        "retmax": "10",  # Limiter à 10 résultats pour le test
        "retmode": "xml",  # Demander une réponse au format XML
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        root = ET.fromstring(response.text)
        ids = root.findall(".//Id")
        
        # Liste pour stocker les résultats
        results = []
        
        for article_id in ids:
            article_id = article_id.text
            
            # Obtenir les détails de l'article avec un autre appel API
            url_details = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
            params_details = {
                "db": "pubmed",
                "id": article_id,
                "retmode": "xml",
            }
            
            response_details = requests.get(url_details, params=params_details)
            
            if response_details.status_code == 200:
                root_details = ET.fromstring(response_details.text)
                docsum = root_details.find(".//DocSum")
                
                title = docsum.find("Item[@Name='Title']").text
                authors = docsum.find("Item[@Name='AuthorList']")
                if authors is not None:
                    authors = ", ".join([author.text for author in authors.findall("Item")])
                else:
                    authors = "No authors available"
                
                # Lien vers l'article PubMed
                link = f"https://pubmed.ncbi.nlm.nih.gov/{article_id}/"
                
                # Ajouter les résultats dans la liste
                results.append([title, authors, link])
        
        # Enregistrer les résultats dans un fichier CSV
        save_to_csv(results)
    else:
        print("Erreur de requête à PubMed.")

# Fonction pour enregistrer les données dans un fichier CSV
def save_to_csv(results):
    # Créer un nom de fichier avec la date actuelle
    today_date = datetime.today().strftime('%Y-%m-%d')
    file_name = f"pubmed_results_{today_date}.csv"
    
    # Vérifier si le dossier 'archives' existe, sinon le créer
    if not os.path.exists('archives'):
        os.makedirs('archives')
    
    file_path = os.path.join('archives', file_name)
    
    # Enregistrer les résultats dans le fichier CSV
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Authors', 'Link'])  # En-tête
        writer.writerows(results)  # Écrire les données
        
    print(f"Le fichier CSV a été créé avec succès : {file_path}")

# Appeler la fonction pour récupérer les données et les enregistrer
fetch_pubmed_data()
