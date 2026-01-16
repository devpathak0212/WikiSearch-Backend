from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# Initialize FastAPI
app = FastAPI()

# Enable CORS for React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Wikipedia tool ONCE (important for performance)
api_wrapper = WikipediaAPIWrapper(top_k_results=1, load_max_doc=1)
tool_for_wikipedia = WikipediaQueryRun(api_wrapper=api_wrapper)

# Request model
class WikiRequest(BaseModel):
    query: str

# Response model
class WikiResponse(BaseModel):
    result: str

# API endpoint
@app.post("/wiki", response_model=WikiResponse)
def get_wikipedia_info(data: WikiRequest):
    try:
        raw_result = tool_for_wikipedia.run(data.query)
        cleaned_result = raw_result
        if "Summary:" in raw_result:
            cleaned_result = raw_result.split("Summary:", 1)[1].strip()

        return {"result": cleaned_result}
    except Exception as e:
        return {"result": f"Error: {str(e)}"}
