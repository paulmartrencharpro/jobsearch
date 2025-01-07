from typing import List
from JobDescription import JobDescription
from datetime import datetime, date

from jobspy import scrape_jobs

def get_job_url(job):
    if "{}".format(job["job_url_direct"]) in ["null", "nan", "None"]:
        return job["job_url"]
    return job["job_url_direct"]

def get_company_url(job):
    if "{}".format(job["company_url_direct"]) in ["null", "nan", "None"]:
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

def get_jobs(search_term, results_wanted):
    return scrape_jobs(
        site_name=["linkedin"],#, "linkedin", "glassdoor"],
        search_term=search_term,
        location="Paris, France",
        job_type="fulltime",
        results_wanted=results_wanted,
        #hours_old=240, # (only Linkedin/Indeed is hour specific, others round up to days old)
        linkedin_fetch_description=True,
        enforce_annual_salary=True,
    )

def linkedin_get_jobs(search_term)-> List[JobDescription]:
    jobs = get_jobs(search_term, 25)

    result = []
    for index, job in jobs.iterrows():
        job_desc = JobDescription(title=job["title"], company=job["company"], url=get_job_url(job), company_url=get_company_url(job),
                                  job_description=job["description"])
        published : date = job["date_posted"]
        job_desc.published_at=datetime.datetime(published.year, published.month, published.day)
        job_desc.organization_logo_url = get_logo(job)
        job_desc.salary_range = get_salary(job)
        result.append(job_desc)
    
    return result


