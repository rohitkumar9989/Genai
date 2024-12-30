import streamlit as st
import pandas as pd
import numpy
from initialize_ import *
st.title("Effective Data Visualization Tool")
create_template=Create_prompt_template()
llm=llm_create()
file_path=st.file_uploader(label="Enter the csv file which you want to create visualization on: ")
if file_path:
    with st.spinner("Loading the model"):
        llm_model=llm()

    data=pd.read_csv(file_path)
    pandas=Process_pandas(data)

    flag, null_row=pandas.check_nan()
    if flag:
        st.text("Nan Values are present, perform pre-processing.")
        pandas.preprocess_data(null_row)
    else:
        dict_=pandas.get_dictionary()
        promt_template=create_template()
        chain=promt_template|llm_model
        data=", ".join(f"Column Name: {key} Its datatype: {value} \n" for key, value in dict_.items())
        output=chain.invoke({"context": data})
        st.text(output)
        extractor=Extract_data(output)
        viz_dict=extractor.extract_columns()
        st.text(viz_dict)
else:
    st.text("Eror")




