from jobspy import scrape_jobs
from typing import List
from datetime import datetime, date, timezone

from JobDescription import JobDescription

def get_job_url(job):
    if job["job_url_direct"] == "":
        return job["job_url"]
    return job["job_url_direct"]

def get_company_url(job):
    if job["company_url_direct"] == "":
        return job["company_url"]
    return job["company_url_direct"]

def get_salary(job):
    if "{}".format(job["min_amount"]) == "nan" or "{}".format(job["min_amount"])== "None":
        return ""
    return "{}-{}{}".format(job["min_amount"], job["max_amount"], job["currency"])

def get_logo(job):
    try:  
        if "{}".format(job["company_logo"]) == "nan":
            return "https://e7.pngegg.com/pngimages/153/807/png-clipart-timer-clock-computer-icons-unknown-planet-digital-clock-time.png"
        return job["company_logo"]
    except:
        return "https://e7.pngegg.com/pngimages/153/807/png-clipart-timer-clock-computer-icons-unknown-planet-digital-clock-time.png"

def get_jobs(search_term, job_type, results_wanted):
    return scrape_jobs(
        site_name=["indeed"],#, "linkedin", "glassdoor"],
        search_term=search_term,
        location="Paris, France",
        job_type=job_type,
        results_wanted=results_wanted,
        #hours_old=240, # (only Linkedin/Indeed is hour specific, others round up to days old)
        country_indeed='France',  # only needed for indeed / glassdoor
        enforce_annual_salary=True,

        linkedin_fetch_description=False, # get more info such as full description, direct job url for linkedin (slower)
    )

def indeed_get_jobs(search_term, job_type="fulltime")-> List[JobDescription]:
    jobs = get_jobs(search_term, job_type, 25)

    result = []
    for index, job in jobs.iterrows():
        job_desc = JobDescription(title=job["title"], company=job["company"], url=get_job_url(job), company_url=get_company_url(job),
                                  job_description=job["description"])
        published : date = job["date_posted"]
        try:
            published_at = datetime(published.year, published.month, published.day, tzinfo=timezone.utc)
        except:
            published_at = datetime.today()
        job_desc.published_at=published_at
        job_desc.organization_logo_url = get_logo(job)
        job_desc.salary_range = get_salary(job)
        result.append(job_desc)
    
    return result

