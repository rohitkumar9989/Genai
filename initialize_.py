from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
import re
from dotenv import load_dotenv
import os
load_dotenv()
#os.environ["HF_TOKEN"]=os.getenv("HF_TOKEN")
#os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
#os.environ["LANGCHAIN_TRACING_V2"]="true"
#os.environ["LANGCHAIN_PROJECT"]="FIRST_GENAI_APPLICATION"
class llm_create():
    def __call__(self, *args, **kwds):
        llm=HuggingFaceEndpoint(model="meta-llama/Llama-3.2-3B-Instruct")
        return llm
    
class Create_prompt_template():
    def __call__ (self):
        prompt = ChatPromptTemplate.from_messages(
        [
            ("system","You are a data analyst tasked with identifying appropriate visualization techniques based on the relationships between columns in the provided data. No other explanation is needed to provide."),
            ("user", "Now generate a table having columns: S.No	,Name of Visualization,X-Axis Columns, Y-Axis Columns,S.No"),
            ("assistant", "S.No	| Name of Visualization | X-Axis Columns | Y-Axis Columns | S.No \n ------|------------------------|-------------|------------|-----"),
            ("user", "The data is: {context}\n understand the relation between the columns and generate,an table having columns: S.No	Name of Visualization	X-Axis Columns	Y-Axis Columns	S.No strictly follow the table!!"),
            ("assistant", "S.No	| Name of Visualization | X-Axis Columns | Y-Axis Columns | Same S.No \n 1  |Bar Chart|fixed acidity, residual sugar|quality|  1")

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

    
class Extract_data():
    def __init__ (self, string):
        self.string=string

    def extract_columns (self):
        viz_=[]
        for index in range (2, 5):
            pattern=rf"{str(index)}(.*?){str(index)}"
            match_=re.search(pattern, self.string)
            viz_.append(match_.group())
        return viz_


            

    
