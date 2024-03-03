from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from langchain.chains import LLMChain
from langchain_community.llms import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from bs4 import BeautifulSoup
import requests
import os

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set the HUGGINGFACEHUB_API_TOKEN environment variable
os.environ["HUGGINGFACEHUB_API_TOKEN"] = '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'
# Replace 'your_api_token' with your actual API token

# Load the model using HuggingFaceEndpoint
repo_id = "mistralai/Mistral-7B-Instruct-v0.2"

# Access the API token from the environment variable
huggingfacehub_api_token = os.environ.get("HUGGINGFACEHUB_API_TOKEN")

# Check if the API token is available
if not huggingfacehub_api_token:
    raise ValueError("HUGGINGFACEHUB_API_TOKEN is not set in the environment variables")

llm = HuggingFaceEndpoint(
    repo_id=repo_id,
    model_kwargs={"max_length": 128},  # Adjust this according to your needs
    temperature=0.5,
    token=huggingfacehub_api_token,
)

# Define the request body
class Request(BaseModel):
    url: str

@app.post("/summarize_url")
async def summarize_url(request: Request):
    # Fetch HTML content from the given URL
    try:
        response = requests.get(request.url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        html_content = response.text
    except requests.RequestException as e:
        return {"error": f"Failed to fetch content from the URL: {str(e)}"}

    # Use BeautifulSoup to extract text from HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    extracted_text = soup.get_text()

    # Use the extracted text as input for summarization
    template = '''
    You're an expert in summarizing the articles or blogs or anything that looks messy.
    You can summarize it so well that it could entirely be explained in short.
    Do with: {extracted_text}
    '''

    prompt = PromptTemplate(template=template, input_variables=["extracted_text"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    result = llm_chain.run({"extracted_text": extracted_text})

    return {"result": result}
