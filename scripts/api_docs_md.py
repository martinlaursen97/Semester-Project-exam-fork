import requests
import pandas as pd

api_url = "http://localhost:7070/api/openapi.json"

response = requests.get(api_url)
api_spec = response.json()

# create lists to hold the data
endpoints, methods, summaries, descriptions = [], [], [], []

# Parsing the JSON data
for path, methods_dict in api_spec["paths"].items():
    for method, details in methods_dict.items():
        endpoints.append(path)
        methods.append(method.upper())
        summaries.append(details.get("summary", "No summary"))
        descriptions.append(details.get("description", "No description"))

# Creating a DataFrame
api_df = pd.DataFrame(
    {
        "Endpoint": endpoints,
        "Method": methods,
        "Summary": summaries,
        "Description": descriptions,
    }
)

markdown_table = api_df.to_markdown(index=False)

# Writing to a markdown file
with open("./docs/API_DOCUMENTATION.md", "w") as file:
    file.write(markdown_table)
