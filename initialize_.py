from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_experimental.agents import create_csv_agent
from transformers import TapasTokenizer, TapasForQuestionAnswering
import torch
import re
import pandas as pd
from dotenv import load_dotenv
import os
import math
load_dotenv()
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]="FIRST_GENAI_APPLICATION"

output_parser=StrOutputParser()
class llm_create():
    def __init__(self):
        self.groq_key=os.getenv("GROQ_API_KEY")
    def subroutine_main(self, *args):
        llm=ChatGroq(model="llama-3.3-70b-versatile", api_key=self.groq_key)
        return llm

    def questionare_lightweight_model(self):
        model=ChatGroq(model="gemma2-9b-it", api_key=self.groq_key)
        return model
    
class Create_prompt_template():
    def call (self, dictionary):
        def create_primary_prompt(dictionary):
            key=list(dictionary.keys())
            return f"""
                    <serial_no id=1>
                        <Visualization_used>
                            <xaxis>{key[0]}</xaxis>
                            <yaxis>{key[1]}</yaxis>
                            <Type of Visualization> Bar Chart</Type of Visualization>
                            <description> </description>
                        </Visualization_used>
                    </serial_no>
                    """
        sample_prompt=create_primary_prompt(dictionary)
        prompt = ChatPromptTemplate.from_messages(
        [
            ("system","You are a Exploratory Data Analyst tasked with identifying appropriate visualization techniques based on the relationships between columns in the provided data. No other explanation is needed to provide."),
            ("user", """Now generate a xml file which has the following elements 
            <serial_no id=[S.No]>
                <Visualization_used>
                    <xaxis>X-axis Column name</xaxis>
                    <yaxis>"Column name wrt other axis to whom this visulization has to be done" </yaxis>
                    <Type of Visualization> </Type of Visualization>
                </Visualization_used>
            </serial_no>
             If having a categorical data then put it in the X-axis
            """),
            ("assistant", "Ok ill be generating an xml file based on the layout you provided, ill be considering on using the following charts: ***Bar Chart, Bubble Chart, Pie chart, Line Chart***"),
            ("user", "The data is: <columns>{context}</columns>\n.*****I need the description of that visulization within the <description></description> tag!!!*** \n For your better understanding here is the 50 top data: {values}, understand the relation between values and ****provide Efficient EDA Visualizations****, ****generate around 15 most efficient reports****!"),
            ("assistant", f"""```<?xml version="1.0" encoding="UTF-8"?>\n <root>{sample_prompt}""")
        ]
        
        )
        return prompt
class Process_pandas():
    def __init__ (self, dataframe):
        self.dataframe=dataframe
    def check_nan (self):
        null_values=self.dataframe.isna().any()
        flag=False
        null_values_list=[]
        for k in range(len(null_values)):
            if null_values.iloc[k]!=False:
                flag=True
                null_values_list.append(k)
        return flag, null_values_list
    def get_dictionary (self):
        dict_={}
        columns=self.dataframe.columns
        for col in columns:
            dict_[col]=self.dataframe.dtypes[col]
        return dict_

    def preprocess_data (self, column_index):
        for k in (column_index):
            if self.dataframe.iloc[:, k].dtype in ['int64', 'float64', 'int32', 'float32']:
                self.dataframe.iloc[:, k].fillna(self.dataframe.iloc[:, k].mean(), inplace=True)
        return self.dataframe
        
    def obtain_data(self,xaxis, yaxis):
        xaxis_values=self.dataframe.get(xaxis).values
        yaxis_values=self.dataframe.get(yaxis).values
        return xaxis_values, yaxis_values

    
class Extract_data():
    def __init__ (self, string):
        self.string=string

    def extract_columns (self):
        index=2
        viz_dict = {}
        try:
            pattern = r"<serial_no id=(.*?)>(.*?)</serial_no>"
            matches = re.finditer(pattern, self.string, re.DOTALL) 
            
            for match in matches:
                serial_no = int(match.group(1))  
                row = match.group(2)  

                viz_type_pattern = r"<Type of Visualization>(.*?)</Type of Visualization>"
                xaxis_pattern = r"<xaxis>(.*?)</xaxis>"
                yaxis_pattern = r"<yaxis>(.*?)</yaxis>"
                desc_pattern=r"<description>(.*?)</description>"
                
                viz_type_match = re.search(viz_type_pattern, row)
                xaxis_match = re.search(xaxis_pattern, row)
                yaxis_match = re.search(yaxis_pattern, row)
                desc_match=re.search(desc_pattern, row)
                
                if viz_type_match and xaxis_match and yaxis_match:
                    viz_type = viz_type_match.group(1).strip()
                    xaxis = xaxis_match.group(1).strip()
                    yaxis = yaxis_match.group(1).strip()
                    desc=desc_match.group(1).strip()

                    viz_dict[serial_no] = {"Type": viz_type, "X-Axis": xaxis, "Y-Axis": yaxis, "desc":desc}
        except Exception as e:
            print(f"Error processing visualizations: {e}")
        return viz_dict
        


class Ask_questions:
    def __init__ (self, dataset_name):
        global output_parser
        self.groq_key=os.getenv("GROQ_API_KEY")
        self.dataset_name=dataset_name
        #self.agent_gpt = create_csv_agent(HuggingFaceEndpoint(model="mistralai/Mistral-7B-Instruct-v0.3", self.dataset_name , verbose=True, allow_dangerous_code=True)
        self.agent_gemma=create_csv_agent(ChatGroq(model="gemma2-9b-it", api_key=self.groq_key), self.dataset_name , verbose=True, allow_dangerous_code=True)

        #model_name = "google/tapas-base-finetuned-wtq"
        #self.tokenizer = TapasTokenizer.from_pretrained(model_name)
        #self.model = TapasForQuestionAnswering.from_pretrained(model_name)

    def answer_question(self, question, model_choice):
        #if model_choice=="ChatGPT":
        #    response=self.agent_gpt.run(question)
        if model_choice=="Gemma":
            response=self.agent_gemma.run(question)
        #else:
        #    data=pd.read_csv(self.dataset_name)
        #    inputs = self.tokenizer(table=data, queries=[question], padding="max_length", return_tensors="pt")
        #    with torch.no_grad():
        #        outputs = self.model(**inputs)
#
        #    # Convert output logits to predicted answers
        #    predicted_answers = self.tokenizer.convert_logits_to_answers(inputs, outputs.logits.detach())
        #    return predicted_answers
        return output_parser.invoke(response)
    
class Makeppt():
    def __init__(self, dataset_name):
        global output_parser
        self.groq_key=os.getenv("GROQ_API_KEY")
        self.dataset_name=dataset_name
        self.agent=create_csv_agent(ChatGroq(model="gemma2-9b-it", api_key=self.groq_key), self.dataset_name , verbose=True, allow_dangerous_code=True)
        
    def presentation(self, desc):
        resp=self.agent.run(f"Explain this in detail in about 50 words{desc}")
        return output_parser.invoke(resp)
