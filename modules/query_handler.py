from models.llama_model import LlamaModel

# def generate_response(query, context_chunks):
#     # Concatenate context into a single prompt
#     context = "\n".join(context_chunks)
#     prompt = (
#         f"Here are some relevant research findings:\n{context}\n"
#         f"Based on this information, answer the following question:\n{query}"
#     )
    
#     llama = LlamaModel()
#     response = llama.generate(prompt)
#     return response

def generate_response(query, context_chunks):
    # Concatenate context into a single prompt
    context = "\n".join(context_chunks)
    prompt = (
        f"Here are some relevant research findings:\n{context}\n"
        f"Based on this information, answer the following question:\n{query}"
    )
    
    llama = LlamaModel(model_name="llama3.2:latest")
    print(prompt)
    response = llama.generate(prompt)
    #response = "Trial response"
    return response