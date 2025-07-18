from AI.mistral import call_ai
from JobDescription import AIInformation
import json

def get_extra_information(company, offer) -> AIInformation:
    return get_extra_information_loopable(company, offer, 0)

def get_extra_information_loopable(company, offer, try_number) -> AIInformation:
    try:
        return _get_extra_information(company, offer)
    except json.decoder.JSONDecodeError as e:
        if try_number > 5:
            return AIInformation(json_dump="{}")
        return get_extra_information_loopable(company, offer + " ", try_number + 1)
    except Exception as e:
        # Throw the error if it's not an SDKError
        raise

def _get_extra_information(company, offer) -> AIInformation:
    prompt = """Extract the following information from this job offer and format it as a JSON object:

- company_description: A brief description of the company in fewer than 15 words.
- position_summary: A summary of the role in 3 bullet points.
- language_requirements: The language requirements, noting if the offer is written in French or English.
- experience_requirements: The required experience for the position.
- is_an_internship: Boolean indicating if the position is an internship.
- salary_range: The yearly salary range if stated, otherwise 'unknown'.
- should_apply: Boolean indicating if the offer requires no more than 2 years of work experience and only requires languages among English, French, Hindi, or Nepali.

Be concise in each answer and respond in English.

Example:
{{
  "company_description": "Leading international network of higher education institutions.",
  "position_summary": [
    "Develop brand experience.",
    "Manage marketing/communication plan.",
    "Ensure brand image and monitor e-reputation."
  ],
  "language_requirements": "Fluent French, Native. Offer is in English",
  "experience_requirements": "2 years in a similar role",
  "is_an_internship": false,
  "salary_range": "€38,000-€42,000",
  "should_apply": true
}}

Company: 
{}

Offer: 
{}
""".format(company, offer)

    result = call_ai(prompt, True)
    print(result)
    return AIInformation(json_dump=result)
    