from langchain.llms.llamacpp import LlamaCpp
from llama_index.core import VectorStoreIndex, Document
from llama_index.llms.langchain import LangChainLLM
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.langchain import LangchainEmbedding

# Initialize Llama-Cpp LLM
llm = LlamaCpp(model_path="/home/alokmishra/Luna/qwen2-0_5b-instruct-q2_k.gguf", n_ctx=2048)  # Adjust `model_path` and `n_ctx` as needed
embedding_model = OpenAIEmbedding()
llm_embd = LangchainEmbedding(embedding_model)

# Wrap LlamaCpp with LangChain's LLM wrapper
langchain_llm = LangChainLLM(llm=llm)

# Load the .txt file as a document
def load_txt_as_documents(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    return [Document(text=text)]

# Load your text file
documents = load_txt_as_documents("test.txt")  # Replace with your .txt file path

# Build an index with the LLaMA model
index = VectorStoreIndex.from_documents(documents, llm=langchain_llm, embed_model=llm_embd)

# Chat with the AI
def chat_with_ai(index, query):
    response = index.query(query)
    return response

# Example interaction
query = "What is this document about?"
response = chat_with_ai(index, query)
print(f"AI Response: {response}")