from typing import List
from JobDescription import JobDescription

from jobspy_indeed import indeed_get_jobs
from ai_manager import get_extra_information

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

def get_jobs(raw_search_term, freelance_term) -> List[JobDescription]:
    search_term = f'"' + raw_search_term + '" ' + freelance_term
    return indeed_get_jobs(search_term, job_type="")

def localize_if_naive(dt, timezone):
    if dt.tzinfo is None:
        return timezone.localize(dt)
    return dt   

def get_all_jobs():
    search_terms = ["Content writer", "Digital Marketing", "Communication", "SEO"]
    freelance_terms = ["freelance", "auto-entrepreneur", "indépendant"]

    #Search all
    all_jobs : List[JobDescription] = []
    for search_term in search_terms:
        for freelance_term in freelance_terms:
            jobs : List[JobDescription] = get_jobs(search_term, freelance_term)
            selected_jobs = filterout_jobs(jobs)
            all_jobs = all_jobs + selected_jobs
    
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

    # remove the ones that are more than 1 week old
    now = localize_if_naive(datetime.now(), utc)
    # Calculate the time one week ago
    one_week_ago = now - timedelta(weeks=1)

    # Filter the jobs
    filtered_jobs = [job for job in unique_jobs if job.published_at >= one_week_ago]

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
        send_mail("Job offers - Freelance", " ".join(result))