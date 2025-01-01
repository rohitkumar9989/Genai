import streamlit as st
import pandas as pd
import numpy
from initialize_ import *
import matplotlib.pyplot as plt
import seaborn as sns
import re
import numpy as np


st.title("Effective Data Visualization Tool")
create_template=Create_prompt_template()
llm=llm_create()
file_path=st.file_uploader(label="Enter the csv file which you want to create visualization on: ")
if file_path:
    with st.spinner("Loading the model"):
        llm_model=llm()

    data=pd.read_csv(file_path)
    pandas=Process_pandas(data)
    flag, null=pandas.check_nan()
    if flag:
        st.text("PreProcessing needs to be done.")
        data=pandas.preprocess_data(null)

    class Visualize_data():
        def run(self, data):
            for key in data:
                try:
                    sub_dictionary = data[key]
                    xaxis = sub_dictionary.get("X-Axis")
                    yaxis = sub_dictionary.get("Y-Axis")
                    xaxis_values, yaxis_values = pandas.obtain_data(xaxis, yaxis)
                    viz_type = sub_dictionary.get("Type")

                    if viz_type == "Scatter Plot":
                        data_df = pd.DataFrame({xaxis: xaxis_values, yaxis: yaxis_values})
                        aggregated_data = data_df.groupby(xaxis).sum().reset_index()
                        xaxis_values = aggregated_data[xaxis]
                        yaxis_values = aggregated_data[yaxis]
                        if re.search("(.*?)-(.*?)", str(xaxis_values)) or re.search("(.*?)/(.*?)", str(xaxis_values)):
                            xaxis_values = xaxis_values[:20]
                            yaxis_values = yaxis_values[:20]
                        fig, ax = plt.subplots(figsize=(26, 13))
                        sns.scatterplot(x=xaxis_values, y=yaxis_values, color='blue', alpha=0.6, edgecolor='black', ax=ax)
                        ax.set_title("Scatter Plot")
                        ax.set_xlabel(xaxis)
                        ax.set_ylabel(yaxis)
                        plt.xticks(rotation=90)
                        st.pyplot(fig)

                    elif viz_type == "Bar Chart":
                        data_df = pd.DataFrame({xaxis: xaxis_values, yaxis: yaxis_values})
                        aggregated_data = data_df.groupby(xaxis).sum().reset_index()
                        xaxis_values = aggregated_data[xaxis]
                        yaxis_values = aggregated_data[yaxis]
                        if re.search("(.*?)-(.*?)", str(xaxis_values)) or re.search("(.*?)/(.*?)", str(xaxis_values)):
                            xaxis_values = xaxis_values[:20]
                            yaxis_values = yaxis_values[:20]
                        fig, ax = plt.subplots(figsize=(26, 13))
                        sns.barplot(x=xaxis_values, y=yaxis_values, color='blue', ax=ax)
                        ax.set_xlabel(xaxis)
                        ax.set_ylabel(yaxis)
                        ax.set_title("Bar Chart Example")
                        plt.xticks(rotation=90)
                        st.pyplot(fig)

                    elif viz_type == "Bubble Chart":
                        data_df = pd.DataFrame({xaxis: xaxis_values, yaxis: yaxis_values})
                        aggregated_data = data_df.groupby(xaxis).sum().reset_index()
                        xaxis_values = aggregated_data[xaxis]
                        yaxis_values = aggregated_data[yaxis]
                        sub_data = pd.DataFrame({
                            xaxis: xaxis_values,
                            yaxis: yaxis_values,
                            'size': yaxis_values
                        })
                        fig, ax = plt.subplots(figsize=(26, 13))
                        sns.scatterplot(
                            data=sub_data, x=xaxis, y=yaxis, size='size', hue=xaxis, alpha=0.6,
                            edgecolor='black', palette="viridis", ax=ax
                        )
                        ax.set_title("Bubble Chart")
                        ax.set_xlabel(xaxis)
                        ax.set_ylabel(yaxis)
                        st.pyplot(fig)

                    elif viz_type == "Heatmap":
                        xaxis_values = xaxis_values[:30]
                        yaxis_values = yaxis_values[:30]
                        heatmap_data = pd.DataFrame({xaxis: xaxis_values, yaxis: yaxis_values})
                        fig, ax = plt.subplots()
                        try:
                            sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="YlGnBu", ax=ax)
                        except Exception:
                            heatmap_data = pd.DataFrame({xaxis: yaxis_values, yaxis: xaxis_values})
                            sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="YlGnBu", ax=ax)
                        ax.set_title(f"Heatmap: {xaxis} vs {yaxis}")
                        st.pyplot(fig)

                    elif viz_type == "Histogram":
                        fig, ax = plt.subplots()
                        sns.histplot(x=xaxis_values, y=yaxis_values, kde=False, color='blue', ax=ax)
                        ax.set_title(f"Histogram of {xaxis}")
                        ax.set_xlabel(xaxis)
                        ax.set_ylabel(yaxis)
                        plt.xticks(rotation=90)
                        st.pyplot(fig)

                    elif viz_type == "Pie Chart":
                        data_df = pd.DataFrame({xaxis: xaxis_values, yaxis: yaxis_values})
                        aggregated_data = data_df.groupby(xaxis).sum().reset_index()
                        pie_data = aggregated_data[:10]
                        labels = pie_data[xaxis]
                        sizes = pie_data[yaxis]
                        fig, ax = plt.subplots(figsize=(10, 10))
                        wedges, texts, autotexts = ax.pie(
                            sizes,
                            labels=labels,
                            autopct='%1.1f%%',
                            startangle=90,
                            colors=sns.color_palette("pastel"),
                            textprops=dict(color="black"),
                        )
                        ax.legend(
                            wedges,
                            labels,
                            title=xaxis,
                            loc="center left",
                            bbox_to_anchor=(1, 0.5),
                        )
                        ax.set_title(f"Pie Chart of {xaxis} vs {yaxis}")
                        st.pyplot(fig)

                    elif viz_type == "Line Chart":
                        data_df = pd.DataFrame({xaxis: xaxis_values, yaxis: yaxis_values})
                        aggregated_data = data_df.groupby(xaxis).sum().reset_index()
                        xaxis_values = aggregated_data[xaxis]
                        yaxis_values = aggregated_data[yaxis]
                        fig, ax = plt.subplots(figsize=(15, 8))
                        sns.lineplot(x=xaxis_values, y=yaxis_values, marker="o", ax=ax)
                        ax.set_title("Line Chart")
                        ax.set_xlabel(xaxis)
                        ax.set_ylabel(yaxis)
                        plt.xticks(rotation=90)
                        st.pyplot(fig)

                except Exception:
                    continue
    visualizer=Visualize_data()
    dict_=pandas.get_dictionary()
    promt_template=create_template.call(dict_)
    chain=promt_template|llm_model
    data=", ".join(f"Column Name: {key} Its datatype: {value} \n" for key, value in dict_.items())
    output=chain.invoke({"context": data})
    extractor=Extract_data(output)
    #st.text(output)
    viz_dict=extractor.extract_columns()
    st.text(viz_dict)
    visualizer.run(viz_dict)
else:
    pass




