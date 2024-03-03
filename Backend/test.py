from langchain_community.llms import HuggingFaceEndpoint
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
# %pip install --upgrade --quiet huggingface_hub
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms.openai import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import UnstructuredURLLoader

urls = ["https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/"]

loader = UnstructuredURLLoader(urls=urls)

data = loader.load()

chunk_size = 3000
chunk_overlap = 200

text_splitter = CharacterTextSplitter(
    # separator = "\n\n"
  chunk_size=chunk_size, # Maximum size of a chunk
  chunk_overlap=chunk_overlap, # Maintain continuity, have some overlap of chunks
  length_function=len, # Count number of characters to measure chunk size
)
texts = text_splitter.split_text( data[0].page_content)

# Create Document objects for each text chunk
docs = [Document(page_content=t) for t in texts[:]]

docs

from getpass import getpass

HUGGINGFACEHUB_API_TOKEN = getpass()

import os

os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN

template = """Summarize this in 2 paragraphs. {docs}"""

prompt = PromptTemplate.from_template(template)

repo_id = "mistralai/Mistral-7B-Instruct-v0.2"

llm = HuggingFaceEndpoint(
    repo_id=repo_id, max_length=1024, temperature=0.5, token=HUGGINGFACEHUB_API_TOKEN
)
llm_chain = LLMChain(prompt=prompt, llm=llm)
print(llm_chain.run(docs))























