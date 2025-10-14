from utils.logger import logger
from strands import tool

valid_companies = [
    "Google",
    "Apple",
    "Microsoft",
    "Amazon",
    "Facebook",
    "Twitter",
    "DXC Technology",
    "IBM",
    "Accenture",
    "TCS",
    "Infosys",
    "Wipro",
    "HCL",
]

@tool
def check_valid_company(company_name: str) -> bool:
    """
    Check if the company name is valid
    """
    logger.info(f"Checking if {company_name} is a valid company")
    
    if company_name in valid_companies:
        logger.info(f"{company_name} is a valid company")
        return True
    else:
        logger.info(f"{company_name} is not a valid company")
        return False