from AI.HF_api import call_ai
from JobDescription import AIInformation
import json

def get_extra_information(company, offer) -> AIInformation:
    try:
        return _get_extra_information(company, offer)
    except json.decoder.JSONDecodeError as e:
        #try again once
        return _get_extra_information(company, offer)
    except Exception as e:
        # Throw the error if it's not an SDKError
        raise

def _get_extra_information(company, offer) -> AIInformation:
    prompt = """This is a job offer from the company '{}', make a JSON with this information:
- company_description (string): a description of the company in less than 15 words. 
- position_summary (string): a summary of the role in 3 bullet points
- language_requirements (string): the language requirements in French and English
- experience_requirements (string): the experience requirements
- is_an_internship (Boolean): True if it's an internship, False otherwise
- salary_range (string): the salary range in yearly salary if stated, write 'unknown' otherwise
- should_apply (Boolean): True if the offer requires up to 2 years of work experience and does not ask for other languages than English, French, Hindi or Nepali

Be concise in each answer. Answer in English.

Example:
{{
'company_description': 'Galileo Global Education: A leading international network of higher education institutions.',
'position_summary': 'Project Manager Marketing and Communication: Develop brand experience, manage marketing/communication plan, ensure brand image, monitor e-reputation, create content, and collaborate with digital team.',
'language_requirements': 'French Fluent and English Native',
'experience_requirements': 'Previous experience in a similar role, preferably in an agency.',
'is_an_internship': False,
'salary_range': '€38,000-€42,000',
'should_apply': True,
}}

Offer:
{}""".format(company, offer)
    result = call_ai(prompt, True)
    return AIInformation(json_dump=result)
    