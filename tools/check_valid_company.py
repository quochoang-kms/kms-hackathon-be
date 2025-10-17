from utils.logger import logger
from strands import tool

valid_companies = [
    "Google",
    "Apple",
    "Microsoft",
    "Amazon",
    "Facebook",
    "Twitter",
    "DXC Technology", # Happy Case
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
    Check if the company name is valid against a predefined list of companies.
    
    This function validates whether a given company name exists in the list of
    valid companies maintained by the system.
    
    Args:
        company_name (str): The name of the company to validate.
                           Case-sensitive matching is performed.
    
    Returns:
        bool: True if the company name is found in the valid companies list,
              False otherwise.

    """
    logger.info(f"Checking if {company_name} is a valid company")
    
    if company_name in valid_companies:
        logger.info(f"{company_name} is a valid company")
        return True
    else:
        logger.info(f"{company_name} is not a valid company")
        return False