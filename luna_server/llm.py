import os
import json
import csv
import yaml
from bs4 import BeautifulSoup
from xml.etree import ElementTree
from docx import Document
from PyPDF2 import PdfReader
from markdown import markdown
from xml.etree import ElementTree as ET
from luna_server.llm_chain import LLMChain

class LLM:
    """
    A class to load and generate response from a model
    """
    def __init__(self, model_path, prompt, chat_format, system_prompt = "", task = None, scan_documents=False, document_path=None, links=None):
        """
        Initialize the LLM.

        Args:
            model_path (str): The path to the model.
            prompt (str): The prompt to use for the model.
            system_prompt (str): The system prompt to use for the model.
            chat_format (str): The chat format to use for the model.
            task (str): The task to use for the model.
            scan_documents (bool): Whether to scan documents.
            document_path(str): The path to the document
            links(list): The list of links of the articles
        """
        self.model_path = model_path
        self.prompt = prompt
        self.system_prompt = system_prompt
        self.chat_format = chat_format
        self.task = task
        self.scan_documents = scan_documents
        self.document_path = document_path
        self.document_content = ""
        self.links = links
        self.tasks = ["chat", "summarization", "translation", "code_generation", "text_generation", "image_to_text"]

        # check if scan_documents is true then documant_format isn't none and also path is given else raise an error
        if self.scan_documents:
            if self.document_path is None:
                raise ValueError("Document format and path must be provided if scan_documents is True")
        
        # check if task is not None
        if self.task is None:
            raise ValueError("Task must be provided")
        
        # if system_prompt is empty then set it as according to the task
        if self.system_prompt == "":
            if self.task == "chat":
                self.system_prompt = "You are an intelligent and friendly assistant designed to engage in informative, helpful, and natural conversations. Your goal is to respond to the user's queries with clarity and precision, ensuring an engaging and seamless chat experience. Please prioritize understanding the context and providing thoughtful, relevant answers."
            elif self.task == "summarization":
                self.system_prompt = "You are a powerful summarization tool capable of condensing long pieces of text into concise, clear, and accurate summaries. Your goal is to extract key points while maintaining the essence of the original content. Provide summaries that are easy to understand and preserve the most important information."
            elif self.task == "translation":
                self.system_prompt = "You are an advanced translation system, proficient in converting text between different languages while maintaining accuracy and context. Your goal is to ensure that the translated text is grammatically correct, natural-sounding, and culturally appropriate, while staying true to the original message."
            elif self.task == "code_generation":
                self.system_prompt = "You are a smart code generation assistant, capable of understanding programming requirements and generating clean, functional code in various languages. When the user provides specifications, offer clear and efficient solutions that are easy to integrate and well-structured."
            elif self.task == "text_generation":
                self.system_prompt = "You are a highly creative text generation model. Your task is to generate relevant, high-quality text based on user inputs, whether it's for creative writing, articles, or any other form of written content. Ensure that the generated text is coherent, contextually accurate, and engaging."
            elif self.task == "image_to_text":
                self.system_prompt = "You are an advanced image-to-text converter. Your job is to analyze images and generate accurate, descriptive text based on the visual content. Ensure that the generated text captures key elements of the image, such as objects, scenes, and actions, while remaining clear and contextually appropriate."

    def read_document(self) -> str:
        """
        Function to read the documents.

        Supported File Formats: .txt, .csv, .tsv, .docx, .rtf, .pdf, .html, .xml, .md, .json, .yaml

        Returns:
            str: full document content
        """
        _, ext = os.path.splitext(self.document_path)
        ext = ext.lower()

        if ext == ".txt":
            with open(self.document_path, "r", encoding="utf-8") as file:
                return file.read()
    
        elif ext == ".csv":
            with open(self.document_path, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                return "\n".join(["\t".join(row) for row in reader])
        
        elif ext == ".tsv":
            with open(self.document_path, "r", encoding="utf-8") as file:
                reader = csv.reader(file, delimiter="\t")
                return "\n".join(["\t".join(row) for row in reader])
        
        elif ext == ".docx":
            doc = Document(self.document_path)
            return "\n".join([para.text for para in doc.paragraphs])
        
        elif ext == ".rtf":
            from striprtf.striprtf import rtf_to_text
            with open(self.document_path, "r", encoding="utf-8") as file:
                return rtf_to_text(file.read())
        
        elif ext == ".pdf":
            reader = PdfReader(self.document_path)
            return "\n".join([page.extract_text() for page in reader.pages])
        
        elif ext == ".html":
            with open(self.document_path, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")
                return soup.get_text()
        
        elif ext == ".xml":
            tree = ElementTree.parse(self.document_path)
            return ElementTree.tostring(tree.getroot(), encoding="unicode", method="text")
        
        elif ext == ".md":
            with open(self.document_path, "r", encoding="utf-8") as file:
                html = markdown(file.read())
                soup = BeautifulSoup(html, "html.parser")
                return soup.get_text()
        
        elif ext == ".json":
            with open(self.document_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                return json.dumps(data, indent=4)
        
        elif ext == ".yaml":
            with open(self.document_path, "r", encoding="utf-8") as file:
                data = yaml.safe_load(file)
                return yaml.dump(data, default_flow_style=False)
        
        else:
            return "Unsupported file format."
            
    
    def read_articles(self):
        pass
        
    def create_chat_completion(self):
        """
        Create chat completion with streaming enabled.

        Returns:
            dict: The completion.
        """

        # if scan_documents is true then read the document
        if self.scan_documents:
            self.document_content = self.read_document()

        if self.document_content:
            self.prompt = f"""\
                Document: 
                {self.document_content}

                User Request: 
                {self.prompt}
            """

        # Create chat completion with streaming enabled
        llm = LLMChain(
            model_path=self.model_path,
            chat_format=self.chat_format,
        )

        output = llm._call(prompt=self.prompt, system_prompt=self.system_prompt, streaming=True)
        
        return output