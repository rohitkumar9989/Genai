from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
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
                        </Visualization_used>
                    </serial_no>
                    """
        sample_prompt=create_primary_prompt(dictionary)
        print (sample_prompt)
        prompt = ChatPromptTemplate.from_messages(
        [
            ("system","You are a data analyst tasked with identifying appropriate visualization techniques based on the relationships between columns in the provided data. No other explanation is needed to provide."),
            ("user", """Now generate a xml file which has the following elements 
            <serial_no id="[S.No]"
                <Visualization_used>
                    <xaxis>X-axis Column name</xaxis>
                    <yaxis>"Column name wrt other axis to whom this visulization has to be done" </yaxis>
                    <Type of Visualization> </Type of Visualization>
                </Visualization_used>
            </serial_no>
            """),
            ("assistant", "Ok ill be generating an xml file based on the layout you provided, ill be considering on using the following charts: Scatter Plot, Bar Chart, Bubble Chart, Heatmap, Histogram"),
            ("user", "The data is: {context}\n understand the multi relation between the columns analyze them throughout and generate,an xml file. Donot provide anything else other than the XML file!!"),
            ("assistant", f"""```<?xml version="1.0" encoding="UTF-8"?>\n <root>{sample_prompt}"""),

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
                
                viz_type_match = re.search(viz_type_pattern, row)
                xaxis_match = re.search(xaxis_pattern, row)
                yaxis_match = re.search(yaxis_pattern, row)
                
                if viz_type_match and xaxis_match and yaxis_match:
                    viz_type = viz_type_match.group(1).strip()
                    xaxis = xaxis_match.group(1).strip()
                    yaxis = yaxis_match.group(1).strip()
                    
                    # Add to dictionary
                    viz_dict[serial_no] = {"Type": viz_type, "X-Axis": xaxis, "Y-Axis": yaxis}
        except Exception as e:
            print(f"Error processing visualizations: {e}")
        return viz_dict



            

    
