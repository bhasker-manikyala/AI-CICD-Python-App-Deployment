# Python script to analyze CI/CD logs using OpenAI
# input: sys.argv log string
# output: root cause + fix
# use OpenAI client, env key, gpt-4o-mini
# handle errors and truncate logs
import sys
from openai import OpenAI
import os
import sys
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
log_data = sys.argv[1]
prompt = f"Explain this CI/CD failure and suggest fix:\n{log_data}"
response = client.chat.completions.create(
 model="gpt-4o-mini",
 messages=[
 {"role": "user", "content": prompt}
 ]
)
print(response.choices[0].message.content)