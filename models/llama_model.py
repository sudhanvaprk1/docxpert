from app.config import Config
import ollama

config = Config()

class LlamaModel:
    def __init__(self, model_name="llama3"):
        self.model = model_name  # Ollama uses "llama3" for LLaMA 3.2

    def generate(self, prompt, max_tokens=500):
        response = ollama.chat(
            model=self.model, 
            messages=[{"role": "user", "content": prompt}],
            options={"num_predict": max_tokens}  # Equivalent to max_length
        )
        return response["message"]["content"]


