import requests
from datetime import datetime
import warnings
from markdownify import markdownify
from typing import List
from JobDescription import JobDescription
from time import sleep

warnings.filterwarnings("ignore")

def _get_offer_and_logo(offer_number):
    url = f"https://www.apec.fr/cms/webservices/offre/public?numeroOffre={offer_number}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": f"https://www.apec.fr/candidat/recherche-emploi.html/emploi/detail-offre/{offer_number}",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    }
    response = requests.get(url, headers=headers, verify=False)
    logo = "https://e7.pngegg.com/pngimages/153/807/png-clipart-timer-clock-computer-icons-unknown-planet-digital-clock-time.png"

    if response.status_code == 200:
        data = response.json()
        if data["affichageLogo"] == True:
            logo = "https://www.apec.fr/files/live/mounts/images/" + data["logoEtablissement"]
        
        #Languages
        Language_requirements = "<h1>Langues:</h1> "
        for competence in data["competences"]:
            if competence["type"] == "LANGUE":
                level = "Unknown"
                if competence["idNomNiveau"] == 102461:
                    level = "C1/C2"
                elif competence["idNomNiveau"] == 102460:
                    level = "B2"
                elif competence["idNomNiveau"] == 102459:
                    level = "A2/B1"
                elif competence["idNomNiveau"] == 102458:
                    level = "A1"

                Language_requirements += f"\r\n{competence['libelle']}: {level}"


        offer = f"""<h1>Descriptif du poste</h1>
        {data["texteHtml"]}

        <h1>Profil recherché</h1>
        {data["texteHtmlProfil"]}

        <h1>L'entreprise</h1>
        {data["texteHtmlEntreprise"]}

        {Language_requirements}
        """
        return markdownify(offer), logo
    else:
        return "", logo

def get_offer_and_logo(offer_number):
    try:
        return _get_offer_and_logo(offer_number)
    except:
        sleep(5)
        return _get_offer_and_logo(offer_number)


def _get_jobs(search_term):
    jobs = []

    url = "https://www.apec.fr/cms/webservices/rechercheOffre"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": f"https://www.apec.fr/candidat/recherche-emploi.html/emploi?motsCles={search_term}&lieux=75&typesConvention=143684&typesConvention=143685&typesConvention=143686&typesConvention=143687&niveauxExperience=101881&anciennetePublication=101851&typesContrat=101888",
        "Content-Type": "application/json",
        "Origin": "https://www.apec.fr",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    }

    payload = {
        "lieux": ["596201"],#Courbevoie
        "fonctions": [],
        "statutPoste": [],
        "typesContrat": ["101888"],
        "typesConvention": ["143684", "143685", "143686", "143687"],
        "niveauxExperience": ["101881"],
        "idsEtablissement": [],
        "secteursActivite": [],
        "typesTeletravail": [],
        "idNomZonesDeplacement": [],
        "positionNumbersExcluded": [],
        "typeClient": "CADRE",
        "sorts": [
            {
                "type": "SCORE",
                "direction": "DESCENDING"
            }
        ],
        "pagination": {
            "range": 60,
            "startIndex": 0
        },
        "activeFiltre": True,
        "pointGeolocDeReference": {
            "distance": "15",
            "latitude": 48.8984226,
            "longitude": 2.2556897
        },        
        "motsCles": search_term,
        "anciennetePublication": "101851"
    }

    response = requests.post(url, headers=headers, json=payload)

    # Check response
    if response.status_code == 200:
        data = response.json()
        for hit in data["resultats"]:
            #{'id': 176950639, 'numeroOffre': '176950639W', 'intitule': 'Responsable E-Commerce F/H', 'intituleSurbrillance': 'Responsable E-Commerce F/H', 'nomCommercial': 'MICHAEL PAGE INTERNATIONAL FRANCE', 'lieuTexte': 'Paris 08 - 75', 'salaireTexte': '100 - 120 k€ brut annuel', 'texteOffre': "Rattaché au Directeur du Développement Commercial, le Responsable E-Commerce est en charge de : Définir et déployer la stratégie e-commerce : Élaborer un plan d'action ambitieux pour booster l'activité e-commerce, en ligne avec les objectifs globaux de l'entreprise,.  Optimiser l...", 'urlLogo': '/media_entreprise/164586/logo_MICHAEL_PAGE_INTERNATIONAL_FRANCE_164586_791231.jpg', 'dateValidation': '2025-07-28T03:58:15.000+0000', 'datePublication': '2025-07-28T03:58:15.000+0000', 'indicateurOqa': True, 'localisable': False, 'score': 14.139965, 'offreConfidentielle': False, 'secteurActivite': 101704, 'secteurActiviteParent': 101776, 'clientReel': True, 'contractDuration': 0, 'typeContrat': 101888, 'origineCode': 101866, 'indicateurFaibleCandidature': False}
            #get the info
            job = {}
            job["name"] = hit["intitule"]
            job["published_at"] = datetime.strptime(hit["datePublication"], '%Y-%m-%dT%H:%M:%S.%f%z')
            job["organization_name"] = hit["nomCommercial"]
            job["URL"] = f"https://www.apec.fr/candidat/recherche-emploi.html/emploi/detail-offre/{hit['numeroOffre']}"
            job["salary_range"] = hit["salaireTexte"]
            job["offer_number"] = hit["numeroOffre"]
            jobs.append(job)
    else:
        print(f"Request failed with status code {response.status_code}")
    return jobs

def get_jobs(search_term):
    try:
        return _get_jobs(search_term)
    except:
        sleep(5)
        return _get_jobs(search_term)


def apec_get_jobs(search_term)-> List[JobDescription]:
    unique_objects = get_jobs(search_term)

    jobs = sorted(unique_objects, key=lambda x: x["published_at"], reverse=True)

    result = []
    for job in jobs:
        offer, logo = get_offer_and_logo(job["offer_number"])
        job_desc = JobDescription(title=job["name"], company=job["organization_name"], url=job["URL"], company_url=job["URL"],
                                  job_description=offer, from_platform="APEC")
        job_desc.published_at=job["published_at"]
        job_desc.organization_logo_url = logo
        job_desc.salary_range = job["salary_range"]
        result.append(job_desc)

    return result
