from datetime import datetime
import json

class JobDescription:
    def __init__(self, title, company, url, company_url, job_description):
        self.title = title
        self.company = company
        self.url = url
        self.company_url = company_url
        self.published_at : datetime = datetime(1900, 1, 1)  # Initialize to None or a default value
        self.job_description = job_description
        self.organization_logo_url = ""
        self.ai_result : AIInformation = None
        self.salary_range = ""
    
    def to_dict(self):
        return {
            "title": self.title,
            "company": self.company,
            "url": self.url,
            "company_url": self.company_url,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "job_description": self.job_description,
            "organization_logo_url": self.organization_logo_url,
            "ai_result": self.ai_result.to_dict() if self.ai_result else None,
            "salary_range": self.salary_range
        }

    @staticmethod
    def from_dict(data):
        ai_result = AIInformation.from_dict(data["ai_result"]) if data["ai_result"] else None
        job_desc = JobDescription(
            title=data["title"],
            company=data["company"],
            url=data["url"],
            company_url=data["company_url"],
            job_description=data["job_description"]
        )
        job_desc.published_at = datetime.fromisoformat(data["published_at"]) if data["published_at"] else None
        job_desc.organization_logo_url = data["organization_logo_url"]
        job_desc.ai_result = ai_result
        job_desc.salary_range = data["salary_range"]
        return job_desc
    
    def format_should_apply(self, should_apply : bool):
        if should_apply:
            return "&#x2B50; "
        return ""
    
    def get_salary(self):
        if self.ai_result.salary_range.lower() not in ["", "unknown"]:
            return self.ai_result.salary_range
        return self.salary_range
    
    def format_str_or_list(self, input):
        if isinstance(input, str):
            return input.replace("\n", "<br />")
        if isinstance(input, list):
            return "<ul>" + "".join(f"<li>{item}</li>" for item in input) + "</ul>"
        return input
    
    def format_posted_date(self, date):
        if "{}".format(date) == "nan":
            return "?"
        if isinstance(date, str):
            return datetime.datetime.fromtimestamp(int(date)).strftime("%d/%m/%Y")
        return date.strftime("%d/%m/%Y")

    def to_html(self):
        #open box
        result = ["<div class='job'>"]
        #logo
        result.append("<div class='logobox'><img src='{}' alt='No logo' class='logo'></div>".format(self.organization_logo_url))
        #text part
        result.append("<div style='flex: 5; padding: 10px;'>")
        result.append("<h3><a href='{}' target='_blank'>{}{}</a></h3>".format(self.url, self.format_should_apply(self.ai_result.should_apply), self.title))
        result.append("<p><a href='{}' target='_blank'>{}</a> ({}) - published at {}</p>".format(self.company_url, self.company, self.ai_result.company_description, self.format_posted_date(self.published_at)))
        result.append("<p><h4>Position: {}</h4>{}</p>".format(self.get_salary(), self.format_str_or_list(self.ai_result.position_summary)))
        result.append("<p><h4>Language:</h4>{}</p>".format(self.format_str_or_list(self.ai_result.language_requirements)))
        result.append("<p><h4>Experience:</h4>{}</p>".format(self.format_str_or_list(self.ai_result.experience_requirements)))
        #close text part
        result.append("</div>")
        #close box
        result.append("</div>")
        return " ".join(result)
    
class AIInformation:
    def __init__(self, json_dump):
        obj = json.loads(json_dump)
        print(obj)
        #Check result
        if not "company_description" in obj:
            obj["company_description"] = ""
        if not "position_summary" in obj:
            obj["position_summary"] = ""
        if not "language_requirements" in obj:
            obj["language_requirements"] = ""
        if not "experience_requirements" in obj:
            obj["experience_requirements"] = ""
        if not "is_an_internship" in obj:
            obj["is_an_internship"] = False
        if not "salary_range" in obj:
            obj["salary_range"] = ""
        if not "should_apply" in obj:
            obj["should_apply"] = True

        self.company_description = obj["company_description"]
        self.position_summary = obj["position_summary"]
        self.language_requirements = obj["language_requirements"]
        self.experience_requirements = obj["experience_requirements"]
        self.is_an_internship = obj["is_an_internship"]
        self.salary_range = obj["salary_range"]
        self.should_apply : bool = obj["should_apply"]
    
    def to_dict(self):
        return {
            "company_description": self.company_description,
            "position_summary": self.position_summary,
            "language_requirements": self.language_requirements,
            "experience_requirements": self.experience_requirements,
            "is_an_internship": self.is_an_internship,
            "salary_range": self.salary_range,
            "should_apply": self.should_apply
        }

    @staticmethod
    def from_dict(data):
        json_dump = json.dumps(data)
        return AIInformation(json_dump)
