# personal assistant

## what will this agent do?
* Browsing YC's website
* Finding W24 batch companies
* Extracting basic information
* Analyzer Agent: Responsible for:
* Visiting each company's website
* Analyzing their product/service
* Gathering founder information
* Creating detailed summaries
* The output will be saved in a JSON file with this structure:
```
{
    "companies": [
        {
            "name": "Company Name",
            "website": "https://company-url.com",
            "product_summary": "Description of what they do...",
            "problem_statement": "Problem they're solving...",
            "founders": ["Founder 1", "Founder 2"]
        }
    ]
}
``

## How to run it?
pip install -r requirements.txt
python run.py

