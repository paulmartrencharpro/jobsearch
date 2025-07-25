import requests
import json
from datetime import datetime
import warnings
from bs4 import BeautifulSoup
from markdownify import markdownify
from typing import List
from JobDescription import JobDescription

warnings.filterwarnings("ignore")

def get_offer(url):
    response = requests.get(url, verify=False)

    if response.status_code == 200:
        # Extract the text from the response
        soup = BeautifulSoup(response.text, 'html.parser')
        match = soup.find('div', {'id': 'the-position-section'})
        text = match.text.rstrip().lstrip()

        return markdownify(text)

    else:
        return ""

def get_logo(job):
    if "{}".format(job["logo_photo_url"]) == "nan":
        return "https://e7.pngegg.com/pngimages/153/807/png-clipart-timer-clock-computer-icons-unknown-planet-digital-clock-time.png"
    return job["logo_photo_url"]

def get_jobs(search_term):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Origin": "https://www.welcometothejungle.com",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "cross-site",
    "content-type": "application/x-www-form-urlencoded",
    "Referer": "https://www.welcometothejungle.com/",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "x-algolia-agent": "Algolia for JavaScript (4.14.3); Browser (lite); JS Helper (3.11.2); react (17.0.2); react-instantsearch (6.38.3)",
    "x-algolia-api-key": "4bd8f6215d0cc52b26430765769e65a0",
    "x-algolia-application-id": "CSEKHVMS53"
    }

    data = """{
        "requests":[{
            "indexName":"wttj_jobs_production_en",
            "params":"attributesToHighlight=%5B%22name%22%5D&attributesToRetrieve=%5B%22*%22%5D&clickAnalytics=true&hitsPerPage=50&maxValuesPerFacet=999&analytics=true&enableABTest=true&userToken=d9c8afab-18d1-41dc-b3ab-da2f75bf30e6&analyticsTags=%5B%22page%3Ajobs_index%22%2C%22language%3Aen%22%5D&facets=%5B%22benefits%22%2C%22organization.commitments%22%2C%22contract_type%22%2C%22contract_duration_minimum%22%2C%22contract_duration_maximum%22%2C%22has_contract_duration%22%2C%22education_level%22%2C%22has_education_level%22%2C%22experience_level_minimum%22%2C%22has_experience_level_minimum%22%2C%22organization.nb_employees%22%2C%22organization.labels%22%2C%22salary_yearly_minimum%22%2C%22has_salary_yearly_minimum%22%2C%22salary_currency%22%2C%22followedCompanies%22%2C%22language%22%2C%22new_profession.category_reference%22%2C%22new_profession.sub_category_reference%22%2C%22remote%22%2C%22sectors.parent_reference%22%2C%22sectors.reference%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)%20AND%20(%22contract_type%22%3A%22full_time%22%20OR%20%22contract_type%22%3A%22temporary%22)%20AND%20(experience_level_minimum%3A0%20TO%201%20OR%20experience_level_minimum%3A1%20TO%203%20OR%20has_experience_level_minimum%3D0)&page=0&query=#####&aroundLatLng=48.85717%2C2.3414&aroundRadius=20000&aroundPrecision=20000"},{"indexName":"wttj_jobs_production_en_promoted","params":"attributesToHighlight=%5B%22name%22%5D&attributesToRetrieve=%5B%22*%22%5D&clickAnalytics=true&hitsPerPage=200&maxValuesPerFacet=999&analytics=true&enableABTest=true&userToken=d9c8afab-18d1-41dc-b3ab-da2f75bf30e6&analyticsTags=%5B%22page%3Ajobs_index%22%2C%22language%3Aen%22%5D&facets=%5B%5D&filters=(%22offices.country_code%22%3A%22FR%22)%20AND%20(%22contract_type%22%3A%22full_time%22%20OR%20%22contract_type%22%3A%22temporary%22)%20AND%20(experience_level_minimum%3A0%20TO%201%20OR%20experience_level_minimum%3A1%20TO%203%20OR%20has_experience_level_minimum%3D0)%20AND%20is_boosted%3Atrue%20AND%20NOT%20reference%3A7e884b19-1ce2-4386-bc6a-643890daf461%20AND%20NOT%20reference%3A1b0237ca-1971-4651-a062-6db5f4c9a6e1%20AND%20NOT%20reference%3Ac27ab821-6822-4156-b4ff-19a9a2940d9d&page=0&query=#####&aroundLatLng=48.85717%2C2.3414&aroundRadius=20000&aroundPrecision=20000"},{"indexName":"wttj_jobs_production_en","params":"analytics=false&facets=%5B%22benefits%22%2C%22organization.commitments%22%2C%22contract_type%22%2C%22contract_duration_minimum%22%2C%22contract_duration_maximum%22%2C%22has_contract_duration%22%2C%22education_level%22%2C%22has_education_level%22%2C%22experience_level_minimum%22%2C%22has_experience_level_minimum%22%2C%22organization.nb_employees%22%2C%22organization.labels%22%2C%22salary_yearly_minimum%22%2C%22has_salary_yearly_minimum%22%2C%22salary_currency%22%2C%22followedCompanies%22%2C%22language%22%2C%22new_profession.category_reference%22%2C%22new_profession.sub_category_reference%22%2C%22remote%22%2C%22sectors.parent_reference%22%2C%22sectors.reference%22%5D&filters=&hitsPerPage=0"},{"indexName":"wttj_jobs_production_en","params":"analytics=false&facets=%5B%22benefits%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)%20AND%20(%22contract_type%22%3A%22full_time%22%20OR%20%22contract_type%22%3A%22temporary%22)%20AND%20(experience_level_minimum%3A0%20TO%201%20OR%20experience_level_minimum%3A1%20TO%203%20OR%20has_experience_level_minimum%3D0)&hitsPerPage=0&query=#####"},{"indexName":"wttj_jobs_production_en","params":"analytics=false&facets=%5B%22organization.commitments%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)%20AND%20(%22contract_type%22%3A%22full_time%22%20OR%20%22contract_type%22%3A%22temporary%22)%20AND%20(experience_level_minimum%3A0%20TO%201%20OR%20experience_level_minimum%3A1%20TO%203%20OR%20has_experience_level_minimum%3D0)&hitsPerPage=0&query=#####"},{"indexName":"wttj_jobs_production_en","params":"analytics=false&facets=%5B%22contract_type%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)%20AND%20(experience_level_minimum%3A0%20TO%201%20OR%20experience_level_minimum%3A1%20TO%203%20OR%20has_experience_level_minimum%3D0)&hitsPerPage=0&query=#####"},{"indexName":"wttj_jobs_production_en","params":"analytics=false&facets=%5B%22contract_duration_minimum%22%5D&filters=contract_duration_minimum%3A1%20TO%203%20OR%20contract_duration_maximum%3A1%20TO%203%20AND%20(%22offices.country_code%22%3A%22FR%22)%20AND%20(%22contract_type%22%3A%22full_time%22%20OR%20%22contract_type%22%3A%22temporary%22)%20AND%20(experience_level_minimum%3A0%20TO%201%20OR%20experience_level_minimum%3A1%20TO%203%20OR%20has_experience_level_minimum%3D0)&hitsPerPage=0&query=#####"},{"indexName":"wttj_jobs_production_en","params":"analytics=false&facets=%5B%22contract_duration_minimum%22%5D&filters=contract_duration_minimum%3A4%20TO%206%20OR%20contract_duration_maximum%3A4%20TO%206%20AND%20(%22offices.country_code%22%3A%22FR%22)%20AND%20(%22contract_type%22%3A%22full_time%22%20OR%20%22contract_type%22%3A%22temporary%22)%20AND%20(experience_level_minimum%3A0%20TO%201%20OR%20experience_level_minimum%3A1%20TO%203%20OR%20has_experience_level_minimum%3D0)&hitsPerPage=0&query=#####"},{"indexName":"wttj_jobs_production_en","params":"analytics=false&facets=%5B%22contract_duration_minimum%22%5D&filters=contract_duration_minimum%3A7%20TO%2012%20OR%20contract_duration_maximum%3A7%20TO%2012%20AND%20(%22offices.country_code%22%3A%22FR%22)%20AND%20(%22contract_type%22%3A%22full_time%22%20OR%20%22contract_type%22%3A%22temporary%22)%20AND%20(experience_level_minimum%3A0%20TO%201%20OR%20experience_level_minimum%3A1%20TO%203%20OR%20has_experience_level_minimum%3D0)&hitsPerPage=0&query=#####"},{"indexName":"wttj_jobs_production_en","params":"analytics=false&facets=%5B%22contract_duration_minimum%22%5D&filters=contract_duration_minimum%3A13%20TO%2024%20OR%20contract_duration_maximum%3A13%20TO%2024%20AND%20(%22offices.country_code%22%3A%22FR%22)%20AND%20(%22contract_type%22%3A%22full_time%22%20OR%20%22contract_type%22%3A%22temporary%22)%20AND%20(experience_level_minimum%3A0%20TO%201%20OR%20experience_level_minimum%3A1%20TO%203%20OR%20has_experience_level_minimum%3D0)&hitsPerPage=0&query=#####"},{"indexName":"wttj_jobs_production_en","params":"analytics=false&facets=%5B%22contract_duration_minimum%22%5D&filters=contract_duration_minimum%3A25%20TO%2036%20OR%20contract_duration_maximum%3A25%20TO%2036%20AND%20(%22offices.country_code%22%3A%22FR%22)%20AND%20(%22contract_type%22%3A%22full_time%22%20OR%20%22contract_type%22%3A%22temporary%22)%20AND%20(experience_level_minimum%3A0%20TO%201%20OR%20experience_level_minimum%3A1%20TO%203%20OR%20has_experience_level_minimum%3D0)&hitsPerPage=0&query=#####"},{"indexName":"wttj_jobs_production_en","params":"analytics=false&facets=%5B%22contract_duration_maximum%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)%20AND%20(%22contract_type%22%3A%22full_time%22%20OR%20%22contract_type%22%3A%22temporary%22)%20AND%20(experience_level_minimum%3A0%20TO%201%20OR%20experience_level_minimum%3A1%20TO%203%20OR%20has_experience_level_minimum%3D0)&hitsPerPage=0&query=#####"},{"indexName":"wttj_jobs_production_en","params":"analytics=false&facets=%5B%22has_contract_duration%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)%20AND%20(%22contract_type%22%3A%22full_time%22%20OR%20%22contract_type%22%3A%22temporary%22)%20AND%20(experience_level_minimum%3A0%20TO%201%20OR%20experience_level_minimum%3A1%20TO%203%20OR%20has_experience_level_minimum%3D0)&hitsPerPage=0&query=#####"},{"indexName":"wttj_jobs_production_en","params":"analytics=false&facets=%5B%22education_level%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)%20AND%20(%22contract_type%22%3A%22full_time%22%20OR%20%22contract_type%22%3A%22temporary%22)%20AND%20(experience_level_minimum%3A0%20TO%201%20OR%20experience_level_minimum%3A1%20TO%203%20OR%20has_experience_level_minimum%3D0)&hitsPerPage=0&query=#####"},{"indexName":"wttj_jobs_production_en","params":"analytics=false&facets=%5B%22has_education_level%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)%20AND%20(%22contract_type%22%3A%22full_time%22%20OR%20%22contract_type%22%3A%22temporary%22)%20AND%20(experience_level_minimum%3A0%20TO%201%20OR%20experience_level_minimum%3A1%20TO%203%20OR%20has_experience_level_minimum%3D0)&hitsPerPage=0&query=#####"},{"indexName":"wttj_jobs_production_en","params":"analytics=false&facets=%5B%22experience_level_minimum%22%5D&filters=experience_level_minimum%3A0%20TO%201%20AND%20(%22offices.country_code%22%3A%22FR%22)%20AND%20(%22contract_type%22%3A%22full_time%22%20OR%20%22contract_type%22%3A%22temporary%22)&hitsPerPage=0&query=#####"},{"indexName":"wttj_jobs_production_en","params":"analytics=false&facets=%5B%22experience_level_minimum%22%5D&filters=experience_level_minimum%3A1%20TO%203%20AND%20(%22offices.country_code%22%3A%22FR%22)%20AND%20(%22contract_type%22%3A%22full_time%22%20OR%20%22contract_type%22%3A%22temporary%22)&hitsPerPage=0&query=#####"},{"indexName":"wttj_jobs_production_en","params":"analytics=false&facets=%5B%22experience_level_minimum%22%5D&filters=experience_level_minimum%3A3%20TO%205%20AND%20(%22offices.country_code%22%3A%22FR%22)%20AND%20(%22contract_type%22%3A%22full_time%22%20OR%20%22contract_type%22%3A%22temporary%22)&hitsPerPage=0&query=#####"},{"indexName":"wttj_jobs_production_en","params":"analytics=false&facets=%5B%22experience_level_minimum%22%5D&filters=experience_level_minimum%3A5%20TO%2010%20AND%20(%22offices.country_code%22%3A%22FR%22)%20AND%20(%22contract_type%22%3A%22full_time%22%20OR%20%22contract_type%22%3A%22temporary%22)&hitsPerPage=0&query=#####"},{"indexName":"wttj_jobs_production_en","params":"analytics=false&facets=%5B%22experience_level_minimum%22%5D&filters=experience_level_minimum%20%3E%3D%2010%20AND%20(%22offices.country_code%22%3A%22FR%22)%20AND%20(%22contract_type%22%3A%22full_time%22%20OR%20%22contract_type%22%3A%22temporary%22)&hitsPerPage=0&query=#####"},{"indexName":"wttj_jobs_production_en","params":"analytics=false&facets=%5B%22has_experience_level_minimum%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)%20AND%20(%22contract_type%22%3A%22full_time%22%20OR%20%22contract_type%22%3A%22temporary%22)&hitsPerPage=0&query=#####"},{"indexName":"wttj_jobs_production_en","params":"analytics=false&facets=%5B%22organization.nb_employees%22%5D&filters=organization.nb_employees%3A0%20TO%2015%20AND%20(%22offices.country_code%22%3A%22FR%22)%20AND%20(%22contract_type%22%3A%22full_time%22%20OR%20%22contract_type%22%3A%22temporary%22)%20AND%20(experience_level_minimum%3A0%20TO%201%20OR%20experience_level_minimum%3A1%20TO%203%20OR%20has_experience_level_minimum%3D0)&hitsPerPage=0&query=#####"},{"indexName":"wttj_jobs_production_en","params":"analytics=false&facets=%5B%22organization.nb_employees%22%5D&filters=organization.nb_employees%3A15%20TO%2050%20AND%20(%22offices.country_code%22%3A%22FR%22)%20AND%20(%22contract_type%22%3A%22full_time%22%20OR%20%22contract_type%22%3A%22temporary%22)%20AND%20(experience_level_minimum%3A0%20TO%201%20OR%20experience_level_minimum%3A1%20TO%203%20OR%20has_experience_level_minimum%3D0)&hitsPerPage=0&query=#####"},{"indexName":"wttj_jobs_production_en","params":"analytics=false&facets=%5B%22organization.nb_employees%22%5D&filters=organization.nb_employees%3A50%20TO%20250%20AND%20(%22offices.country_code%22%3A%22FR%22)%20AND%20(%22contract_type%22%3A%22full_time%22%20OR%20%22contract_type%22%3A%22temporary%22)%20AND%20(experience_level_minimum%3A0%20TO%201%20OR%20experience_level_minimum%3A1%20TO%203%20OR%20has_experience_level_minimum%3D0)&hitsPerPage=0&query=#####"},{"indexName":"wttj_jobs_production_en","params":"analytics=false&facets=%5B%22organization.nb_employees%22%5D&filters=organization.nb_employees%3A250%20TO%202000%20AND%20(%22offices.country_code%22%3A%22FR%22)%20AND%20(%22contract_type%22%3A%22full_time%22%20OR%20%22contract_type%22%3A%22temporary%22)%20AND%20(experience_level_minimum%3A0%20TO%201%20OR%20experience_level_minimum%3A1%20TO%203%20OR%20has_experience_level_minimum%3D0)&hitsPerPage=0&query=#####"},{"indexName":"wttj_jobs_production_en","params":"analytics=false&facets=%5B%22organization.nb_employees%22%5D&filters=organization.nb_employees%20%3E%3D%202000%20AND%20(%22offices.country_code%22%3A%22FR%22)%20AND%20(%22contract_type%22%3A%22full_time%22%20OR%20%22contract_type%22%3A%22temporary%22)%20AND%20(experience_level_minimum%3A0%20TO%201%20OR%20experience_level_minimum%3A1%20TO%203%20OR%20has_experience_level_minimum%3D0)&hitsPerPage=0&query=#####"},{"indexName":"wttj_jobs_production_en","params":"analytics=false&facets=%5B%22organization.labels%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)%20AND%20(%22contract_type%22%3A%22full_time%22%20OR%20%22contract_type%22%3A%22temporary%22)%20AND%20(experience_level_minimum%3A0%20TO%201%20OR%20experience_level_minimum%3A1%20TO%203%20OR%20has_experience_level_minimum%3D0)&hitsPerPage=0&query=#####"},{"indexName":"wttj_jobs_production_en","params":"analytics=false&facets=%5B%22salary_yearly_minimum%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)%20AND%20(%22contract_type%22%3A%22full_time%22%20OR%20%22contract_type%22%3A%22temporary%22)%20AND%20(experience_level_minimum%3A0%20TO%201%20OR%20experience_level_minimum%3A1%20TO%203%20OR%20has_experience_level_minimum%3D0)&hitsPerPage=0&query=#####"},{"indexName":"wttj_jobs_production_en","params":"analytics=false&facets=%5B%22has_salary_yearly_minimum%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)%20AND%20(%22contract_type%22%3A%22full_time%22%20OR%20%22contract_type%22%3A%22temporary%22)%20AND%20(experience_level_minimum%3A0%20TO%201%20OR%20experience_level_minimum%3A1%20TO%203%20OR%20has_experience_level_minimum%3D0)&hitsPerPage=0&query=#####"},{"indexName":"wttj_jobs_production_en","params":"analytics=false&facets=%5B%22salary_currency%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)%20AND%20(%22contract_type%22%3A%22full_time%22%20OR%20%22contract_type%22%3A%22temporary%22)%20AND%20(experience_level_minimum%3A0%20TO%201%20OR%20experience_level_minimum%3A1%20TO%203%20OR%20has_experience_level_minimum%3D0)&hitsPerPage=0&query=#####"},{"indexName":"wttj_jobs_production_en","params":"analytics=false&facets=%5B%22followedCompanies%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)%20AND%20(%22contract_type%22%3A%22full_time%22%20OR%20%22contract_type%22%3A%22temporary%22)%20AND%20(experience_level_minimum%3A0%20TO%201%20OR%20experience_level_minimum%3A1%20TO%203%20OR%20has_experience_level_minimum%3D0)&hitsPerPage=0&query=#####"},{"indexName":"wttj_jobs_production_en","params":"analytics=false&facets=%5B%22language%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)%20AND%20(%22contract_type%22%3A%22full_time%22%20OR%20%22contract_type%22%3A%22temporary%22)%20AND%20(experience_level_minimum%3A0%20TO%201%20OR%20experience_level_minimum%3A1%20TO%203%20OR%20has_experience_level_minimum%3D0)&hitsPerPage=0&query=#####"},{"indexName":"wttj_jobs_production_en","params":"analytics=false&facets=%5B%22new_profession.category_reference%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)%20AND%20(%22contract_type%22%3A%22full_time%22%20OR%20%22contract_type%22%3A%22temporary%22)%20AND%20(experience_level_minimum%3A0%20TO%201%20OR%20experience_level_minimum%3A1%20TO%203%20OR%20has_experience_level_minimum%3D0)&hitsPerPage=0&query=#####"},{"indexName":"wttj_jobs_production_en","params":"analytics=false&facets=%5B%22new_profession.sub_category_reference%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)%20AND%20(%22contract_type%22%3A%22full_time%22%20OR%20%22contract_type%22%3A%22temporary%22)%20AND%20(experience_level_minimum%3A0%20TO%201%20OR%20experience_level_minimum%3A1%20TO%203%20OR%20has_experience_level_minimum%3D0)&hitsPerPage=0&query=#####"},{"indexName":"wttj_jobs_production_en","params":"analytics=false&facets=%5B%22remote%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)%20AND%20(%22contract_type%22%3A%22full_time%22%20OR%20%22contract_type%22%3A%22temporary%22)%20AND%20(experience_level_minimum%3A0%20TO%201%20OR%20experience_level_minimum%3A1%20TO%203%20OR%20has_experience_level_minimum%3D0)&hitsPerPage=0&query=#####"},{"indexName":"wttj_jobs_production_en","params":"analytics=false&facets=%5B%22sectors.parent_reference%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)%20AND%20(%22contract_type%22%3A%22full_time%22%20OR%20%22contract_type%22%3A%22temporary%22)%20AND%20(experience_level_minimum%3A0%20TO%201%20OR%20experience_level_minimum%3A1%20TO%203%20OR%20has_experience_level_minimum%3D0)&hitsPerPage=0&query=#####"},{"indexName":"wttj_jobs_production_en","params":"analytics=false&facets=%5B%22sectors.reference%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)%20AND%20(%22contract_type%22%3A%22full_time%22%20OR%20%22contract_type%22%3A%22temporary%22)%20AND%20(experience_level_minimum%3A0%20TO%201%20OR%20experience_level_minimum%3A1%20TO%203%20OR%20has_experience_level_minimum%3D0)&hitsPerPage=0&query=#####"}
            ]}
        """.replace("#####", search_term.lower().replace(" ", "%20").replace('"', "%22"))

    url = "https://csekhvms53-2.algolianet.com/1/indexes/*/queries?x-algolia-agent=Algolia^%^20for^%^20JavaScript^%^20(4.20.0)^%^3B^%^20Browser^%^20(lite)^%^3B^%^20JS^%^20Helper^%^20(3.11.2)^%^3B^%^20react^%^20(17.0.2)^%^3B^%^20react-instantsearch^%^20(6.38.3)&x-algolia-api-key=4bd8f6215d0cc52b26430765769e65a0&x-algolia-application-id=CSEKHVMS53&search_origin=jobs_search_client"

    response = requests.post(url, headers=headers, data=data, verify=False)

    #parse result
    jsonResponse = json.loads(response.text)
    results = jsonResponse["results"]
    hits = results[0]["hits"]
    jobs = []
    for hit in hits:
        #get the info
        job = {}
        job["name"] = hit["name"]
        if hit["published_at"] != None:
            try:
                # Try parsing with fractional seconds
                published_at = datetime.strptime(hit["published_at"], '%Y-%m-%dT%H:%M:%S.%f%z')
            except ValueError:
                # If it fails, try parsing without fractional seconds
                published_at = datetime.strptime(hit["published_at"], '%Y-%m-%dT%H:%M:%S%z')
            job["published_at"] = published_at
        else:
            job["published_at"] = None
        job["organization_name"] = hit["organization"]["name"]
        if hit["organization"].get("size", None) is not None:
            job["organization_size"] = hit["organization"]["size"]["en"]
        else:
            job["organization_size"] = ""
        job["organization_logo_url"] = hit["organization"]["logo"]["url"]
        job["URL"] = "https://www.welcometothejungle.com/en/companies/{}/jobs/{}?o={}".format(hit["organization"]["slug"], hit["slug"], hit["objectID"])
        job["company_url"] = "https://www.welcometothejungle.com/en/companies/{}/".format(hit["organization"]["slug"])
        jobs.append(job)
    
    return jobs

def wtoj_get_jobs(search_term)-> List[JobDescription]:
    unique_objects = get_jobs(search_term)

    jobs = sorted(unique_objects, key=lambda x: x["published_at"], reverse=True)

    result = []
    for job in jobs:
        job_desc = JobDescription(title=job["name"], company=job["organization_name"], url=job["URL"], company_url=job["company_url"],
                                  job_description=get_offer(job["URL"]))
        job_desc.published_at=job["published_at"]
        job_desc.organization_logo_url = job["organization_logo_url"]
        job_desc.salary_range = ""
        result.append(job_desc)
    
    return result
