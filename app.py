from typing import List
from JobDescription import JobDescription

from jobspy_indeed import indeed_get_jobs
from WelcomeToTheJungle import wtoj_get_jobs
from jobspy_linkedin import linkedin_get_jobs
from apec import apec_get_jobs
from ai_manager import get_extra_information

from concurrent.futures import ThreadPoolExecutor, as_completed
from send_email import send_mail
from datetime import datetime, timedelta
import pytz
import re

def match_whole_words(words, text):
    return any(re.search(rf'\b{re.escape(word)}\b', text) for word in words)

def filterout_jobs(jobs : List[JobDescription]) -> List[JobDescription]:
    job_filter = ["marketing", "communication", "community", "content", "digital", "Responsable contenu", "business development", "experience", "social media", "Digital Acquisition", "brand", "ppc", "seo", "sea", "ads", "user acquisition", "adops", "consultant"]
    job_filter_negative = ["stage", "stagiaire", "alternant", "alternance", "intern", "internship", "apprenti"]
    selected_jobs : List[JobDescription] = []
    for job in jobs:
        title = job.title.lower()
        if not match_whole_words(job_filter_negative, title) and match_whole_words(job_filter, title):
            selected_jobs.append(job)
    
    return selected_jobs

def get_jobs(raw_search_term, platform) -> List[JobDescription]:
    search_term = '"' + raw_search_term + '"'

    if platform == "Indeed":
        return indeed_get_jobs(search_term)
    elif platform == "Welcome to the jungle":
        return wtoj_get_jobs(search_term)
    elif platform == "LinkedIn":
        return linkedin_get_jobs(search_term)
    elif platform == "APEC":
        return apec_get_jobs(search_term)

def localize_if_naive(dt, timezone):
    if dt.tzinfo is None:
        return timezone.localize(dt)
    return dt

def process_search_on_platform(platform, search_terms) -> List[JobDescription]:
    platform_jobs = []
    for search_term in search_terms:
        jobs: List[JobDescription] = get_jobs(search_term, platform)
        selected_jobs = filterout_jobs(jobs)
        platform_jobs.extend(selected_jobs)
    return platform_jobs

from datetime import datetime

def log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{timestamp} - {message}")

def get_all_jobs():
    search_terms = ["Content writer", "Digital Marketing", "Communication", "Business development", "SEO"]
    platforms = ["Welcome to the jungle", "Indeed", "LinkedIn", "APEC"]

    log("Start searching for jobs")
    #Search all
    all_jobs : List[JobDescription] = []
    #Runs the search for each platform in //
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_search_on_platform, platform, search_terms) for platform in platforms]

    for future in as_completed(futures):
        all_jobs.extend(future.result())
    
    #merge
    seen_urls = set()
    unique_jobs : List[JobDescription] = []

    for obj in all_jobs:
        if obj.url not in seen_urls:
            seen_urls.add(obj.url)
            unique_jobs.append(obj)
    
    #to make the published_at sortable
    utc = pytz.UTC
    for job in unique_jobs:
        job.published_at = localize_if_naive(job.published_at, utc)

    # remove the ones that are more than 4.5 days old
    now = localize_if_naive(datetime.now(), utc)
    # Calculate the time 4.5 days ago
    one_week_ago = now - timedelta(days=4.5)

    # Filter the jobs
    filtered_jobs = [job for job in unique_jobs if job.published_at >= one_week_ago]
    log("Done searching for jobs")

    return sorted(filtered_jobs, key=lambda x: x.published_at, reverse=True)
            
if __name__ == "__main__":
    jobs = get_all_jobs()

    if len(jobs) > 0:
        result = ["<html><head><style>.job{display: flex;width:70%;margin: 5px auto;border: 1px solid;border-radius: 5px;}.logobox{flex: 1;display: flex;align-items: center;justify-content: center;}.logo{width:100px;height:100px}h4{margin: 2px;}</style></head><body>"]
        for job in jobs:
            job.ai_result = get_extra_information(job.company, job.job_description)
            if job.ai_result.is_an_internship == False and job.ai_result.high_experience == False:
                result.append(job.to_html())
        result.append("</body></html>")
        send_mail("Job offers", " ".join(result))

        #Stats
        from collections import Counter
        # Count occurrences of each from_platform
        filtered_jobs = [
            job for job in jobs
            if not job.ai_result.is_an_internship and not job.ai_result.high_experience
        ]
        platform_counts = Counter(job.from_platform for job in filtered_jobs)

        # Sort by from_platform alphabetically
        sorted_counts = dict(sorted(platform_counts.items()))
        print("Stats:")
        for platform, count in sorted_counts.items():
            print(f"{platform}: {count}")
