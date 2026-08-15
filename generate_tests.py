# Generate pytest test cases using OpenAI API for a Flask app
# Must:
# - read app.py
# - call OpenAI
# - generate test_app.py
# - ensure valid python
# - fallback if invalid
from openai import OpenAI
import os
import ast
# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# Read your Flask app code
with open("app.py", "r") as f:
code = f.read()
# Strong prompt to control AI output
prompt = f"""
Generate ONLY valid pytest test code for this Flask app.
STRICT RULES:
- Output ONLY Python code
- NO explanations
- NO markdown (no ``` blocks)
- MUST use this exact import:
from app import app
- Use Flask test client
- Include at least one test function
- Code must run with pytest without modification
Flask App Code:
{code}
"""
try:
response = client.chat.completions.create(
model="gpt-4o-mini",
messages=[
{"role": "user", "content": prompt}
]
)
tests = response.choices[0].message.content.strip()

except Exception as e:
print("AI request failed:", e)
tests = ""
# Step 1: Remove markdown if AI adds it
if "```" in tests:
tests = tests.replace("```python", "").replace("```", "").strip()
# Step 2: Fix common wrong imports
tests = tests.replace("from your_flask_app import app", "from app import app")
tests = tests.replace("from main import app", "from app import app")
tests = tests.replace("flask_app", "app")
# Step 3: Ensure correct import exists
if "from app import app" not in tests:
print("Fixing missing import...")
tests = "from app import app\n\n" + tests
# Step 4: Validate Python syntax
try:
ast.parse(tests)
print("AI generated valid Python tests")
except SyntaxError:
print("Invalid AI output. Using fallback test.")
tests = """
from app import app
def test_home():
client = app.test_client()
response = client.get("/")
assert response.status_code == 200
"""
# Step 5: Final safety check (must contain test function)
if "def test_" not in tests:
print("No test function found. Using fallback.")
tests = """
from app import app
def test_home():
client = app.test_client()
response = client.get("/")
assert response.status_code == 200
"""
# Save the test file
with open("test_app.py", "w") as f:
f.write(tests)
print("test_app.py created successfully")
