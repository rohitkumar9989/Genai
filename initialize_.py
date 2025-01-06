from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re
from dotenv import load_dotenv
import os
load_dotenv()
os.environ["HF_TOKEN"]=os.getenv("HF_TOKEN")
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]="FIRST_GENAI_APPLICATION"
class llm_create():
    def __call__(self, *args, **kwds):
        llm=HuggingFaceEndpoint(model="meta-llama/Meta-Llama-3-8B-Instruct")
        return llm
    
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
            <serial_no id="[S.No]"
                <Visualization_used>
                    <xaxis>X-axis Column name</xaxis>
                    <yaxis>"Column name wrt other axis to whom this visulization has to be done" </yaxis>
                    <Type of Visualization> </Type of Visualization>
                </Visualization_used>
            </serial_no>
             If having a categorical data then put it in the X-axis
            """),
            ("assistant", "Ok ill be generating an xml file based on the layout you provided, ill be considering on using the following charts: ***Scatter Plot, Bar Chart, Bubble Chart, Pie chart, Line Chart, Histogram***"),
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
            pattern = r"<serial_no id=(\d+)>(.*?)</serial_no>"
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
    
class Ask_questions():
    def __init__ (self, dataframe, llm_model):
        self.dataframe=dataframe
        self.llm_model=llm_model

    def create_question (self, query):
        prompt=ChatPromptTemplate.from_messages([
            ("system", "You are a Question Answering Assistant who answers the questions based on the given dataset"),
            ("user", """Here is the question for you <question>{question}</question>, \nHere is the dataset for you to use to answer the question <dataset>{dataset}</dataset>\n 
             ***Enclose the answer wihtin the <answer></answer> tag!!!!***,
             **After answering end the converstaion. I just need the answer for what i asked, thats it!!!!!**
             **Explain in detail, your answers have to be in the perspective of a Data Analyst**
             
             """),
            ("system", "<answer>")

        ])
        chain=prompt | self.llm_model
        return chain.invoke({"question": query, "dataset": self.dataframe})



        






            

    
