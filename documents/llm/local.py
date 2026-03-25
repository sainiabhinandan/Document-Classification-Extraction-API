import requests, os, json
import requests, os, json
from .base import LLMBackend
from .remote import PROMPT_TEMPLATE
import re


PROMPT_TEMPLATE = """You are a document classifier for an EU worker posting company.
Classify the document text below into exactly one category:
identity_document | employment_contract | payslip | invoice | tax_form | other

Then extract the relevant key fields as JSON.

Fields to extract per category:
- identity_document: full_name, date_of_birth, document_number, expiry_date, nationality
- employment_contract: employee_name, employer, start_date, job_title, salary
- payslip: employee_name, employer, period, gross_salary, net_salary
- invoice: issuer, recipient, total_amount, date, invoice_number
- tax_form: taxpayer_name, fiscal_code, tax_year, total_income, tax_withheld
- other: (return empty dict)

Respond ONLY with valid JSON.
Do NOT include explanations, comments, or extra text.
The response must start with '{{' and end with '}}'.
{{"category": "...", "extracted_fields": {{...}}}}

Document text:
{text}"""


class LocalLLM(LLMBackend):
    def classify(self, text: str) -> dict:
        url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434") + "/api/generate"
        payload = {
            "model": os.getenv("OLLAMA_MODEL", "llama3.2"),
            "prompt": PROMPT_TEMPLATE.format(text=text[:4000]),
            "stream": False
        }
        r = requests.post(url, json=payload, timeout=30)
        r.raise_for_status()

        # Robust JSON extraction from LLM response
        raw_output = r.json()["response"]

        # Extract ONLY JSON part
        match = re.search(r'\{.*\}', raw_output, re.DOTALL)
        if not match:
            raise ValueError("LLM did not return valid JSON")

        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON from LLM: {raw_output}")
        
    