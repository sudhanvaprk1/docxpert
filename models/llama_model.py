from transformers import AutoModelForCausalLM, AutoTokenizer
from app.config import Config

config = Config()

# class LlamaModel:
#     def __init__(self):
#         self.tokenizer = AutoTokenizer.from_pretrained(config.LLAMA_MODEL_PATH, 
#                                                         use_auth_token=config.LLAMA_API_KEY)
#         self.model = AutoModelForCausalLM.from_pretrained(config.LLAMA_MODEL_PATH, 
#                                                       use_auth_token=config.LLAMA_API_KEY)

#     def generate(self, prompt, max_length=500):
#         inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True)
#         outputs = self.model.generate(inputs["input_ids"], max_new_tokens=max_length)
#         response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
#         return response


import ollama

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


