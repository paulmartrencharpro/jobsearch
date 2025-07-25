# JobSearch
## Goal

This is a tool to search for jobs for a friend. It looks for marketing jobs in Paris, France, then send an email to them.

## How it works

There are 3 github actions that runs the app.py (most complete one), the app_freelance.py (for freelance jobs) and app_teaching.py (for teaching jobs) daily.
In app.py, the flow is:

    - For each job platform (LinkedIn, Indeed & Welcome to the jungle)
        - For each search term
            - look for jobs in the area
    - Then we merge the results by URL of the job offer
    - Then we filter by date (old offers are removed)
    - Then we filter the results with positive keyworks (the ones we expect) and negative keyworks (mostly to remove the internships)

    - Then, we use the Mistral AI API to extract the information we want:
        - Job description
        - Company description
        - Language requirements
        - Experience requirements
        - If it's an internship
        - If they should apply based on requirements
    
    - Then we take all the remaining jobs and format an HTML email with the information for each job. If the AI think we should apply, I put a gold star in front of the job title