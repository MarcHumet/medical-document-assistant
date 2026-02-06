docker exec medical-assistant-api python -c "
import os
os.environ['LLM_PROVIDER'] = 'ollama'
os.environ['LLM_ENDPOINT'] = 'http://ollama:11434/v1'
from src.llm.chat import ChatLLM

print('🤖 Testing Ollama LLM with correct endpoint...')
print(f'Provider: {os.getenv(\"LLM_PROVIDER\")}')
print(f'Endpoint: {os.getenv(\"LLM_ENDPOINT\")}')

chat_llm = ChatLLM()
question = 'What is 2 + 2?'
print(f'Question: {question}')
response = chat_llm.invoke(question)
print(f'✅ Response: {response}')
"