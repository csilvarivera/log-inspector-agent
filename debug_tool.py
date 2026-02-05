
from google.adk.tools import google_search

try:
    if hasattr(google_search, 'args_schema'):
        print(f"Args Schema: {google_search.args_schema}")
    else:
        print("No args_schema attribute")
        
    if hasattr(google_search, 'description'):
        print(f"Description: {google_search.description}")
        
except Exception as e:
    print(f"Error: {e}")
