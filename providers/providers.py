import os
from strands.models import BedrockModel
from strands.models.openai import OpenAIModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def model_provider(provider: str):
    provider = provider.lower().strip()
    
    if provider == "bedrock":
        return BedrockModel(
            model_id=os.getenv("MODEL_ID2"),
            region_name=os.getenv("REGION_NAME"),
        )
    elif provider == "openai":
        return OpenAIModel(
            client_args={"api_key": os.getenv("OPENAI_API_KEY")},
            model_id="gpt-4o-mini",
        )
    else:
        raise ValueError(f"Unsupported provider: {provider}. Choose 'bedrock' or 'openai'.") 