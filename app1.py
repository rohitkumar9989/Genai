import streamlit as st
from PIL import Image
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
# import main

# Set page configuration at the very top
st.set_page_config(page_title="InsightLens", layout="wide")



def main():
    # Custom CSS
    st.markdown(
        """
        <style>
        
        
        .custom-section {
           
            border-radius: 10px;  /* Rounded corners */
            color: white;  /* Text color */
            margin-bottom: 20px;  /* Space below the section */
        }
        .big-font1 { font-size:30px !important; font-weight: bold; }
        .blue-text { color: #1a73e8; font-weight: bold; }
        .btn-primary { background-color: #1a73e8; color: white; padding: 10px 20px; border-radius: 8px; border: none; font-weight: bold; }
        .btn-secondary { background-color: white; color: black; padding: 10px 20px; border-radius: 8px; border: 1px solid #ccc; }
        .feature-list { font-size: 18px; }
        .main-container {
            text-align: center;
            margin-top: 20px;
            
        }
        .main-title {
            font-size: 48px;
            font-weight: 700;
        }
        .sub-title {
            font-size: 24px;
            color: #6c757d;
        }
        .button-container {
            margin-top: 30px;
            text-align: center;
           
        }
        .styled-button {
            background-color: #007bff;
            color: white;
            font-size: 18px;
            padding: 10px 20px;
            border: none;
            border-radius: 25px;
            cursor: pointer;
        }
        .styled-button:hover {
            background-color: #0056b3;
        }
        .chart-container {
            margin: 20px;
        }
       
        .big-font {
            font-size:36px !important;
            font-weight: bold;
            text-align: center;
        }
        .subtext {
            font-size:18px;
            text-align: center;
        }
        .centered-btn {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 20px;
        }
        .custom-footer {
            text-align: center;
            padding: 10px;
            background-color: #f8f9fa;
            font-size: 14px;
            margin-top: 50px;
        }
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 20px;
            background: white;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
        }
        .nav-links a {
            margin-right: 15px;
            text-decoration: none;
            font-weight: bold;
            color: #333;
        }
        
       .custom-container {
    #  background-color: #93d2e2;
    background-color: #87CEEB;
    # background-color: #6da4dd;
    padding: 40px;
    border-radius: 10px;
    width: 100%;
    text-align: center;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

.title {
    font-size: 36px;
    font-weight: bold;
}

.subtitle {
    font-size: 18px;
    color: #555;
}

.card-container {
    display: flex;
    justify-content: space-around;
    margin-top: 20px;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    text-align: center;
    flex: 1;
    margin: 0 10px;
}
    .button-container {
            display: flex;
            justify-content: center;
            align-items: center;
           
        }
        
        .light-blue-button {
            background-color: #01c3f4;
            color: black;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            border-radius: 5px;
        }

        
        
        .light-blue-button1 {
            background-color:none;
            color: black;
            border:none;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            border-radius: 5px;
        }
        .light-blue-button1:hover{
            border:#01c3f4;
        }
        .navbar1 {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: white;
            color: black;
            padding: 10px;
            border-radius: 0px 0px 10px 10px;
            # box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        }
        
        .left-side {
            margin-left: 20px;
        }
        
        .middle-links {
            display: flex;
            gap: 20px;
            align-items: center;
        }
        
        .middle-links a {
            color: black;
            text-decoration: none;
        }
        
        .middle-links a:hover {
            color: lightblue;
        }
        
        .right-side {
            margin-right: 20px;
            font-size: 14px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Navigation Bar
    st.markdown("""
    <div class="navbar">
        <h3 style="margin: 0;">🔍 DataQueryAI</h3>
        <div class="nav-links">
            <a href="#">Platform</a>
            <a href="#">Features</a>
            <a href="#">Solutions</a>
            <a href="#">Resources</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='custom-section'>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])

    with col1:
        # Main Content
        st.markdown("<div class='main-container'>", unsafe_allow_html=True)
        st.markdown("<h1 class='main-title'>Go From Data To Insights In Minutes</h1>", unsafe_allow_html=True)
        # st.markdown("<h1 class='main-title'>A faster way to build and share data apps</h1>", unsafe_allow_html=True)
        st.markdown("<p class='sub-title'>Upload your CSV files and let our intelligent tool generate insightful charts and visualizations in seconds.</p>", unsafe_allow_html=True)

        # Button
    #     st.markdown('''
    # <div class="button-container1">
    #     <button class="light-blue-button1">Let's Start →</button>
    # </div>
    # ''', unsafe_allow_html=True)
#     st.markdown('''
#     <a href="/main" target="_self" class="button-container1">
#         <button class="light-blue-button1">Let's Start →</button>
#     </a>
# ''', unsafe_allow_html=True)
    # Function to navigate
   
        if "page" not in st.session_state:
            st.session_state.page = "app1"  # Default page

# Button to navigate
        if st.button("Let's Start →"):
            st.session_state.page = "main"
            st.rerun()  # Rerun the app to switch pages

# Load the appropriate page based on session state
        if st.session_state.page == "main":
            import main  # Import only when needed
            main.main()  # Call the function in main.py
            st.stop() 

    with col2:
        # Static Visualization - Bar Chart with margin
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)

        # Creating Sample Data
        data = pd.DataFrame({
            'Category': ['A', 'B', 'C', 'D', 'E'],
            'Values': [10, 25, 18, 30, 22]
        })
        
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.bar(data['Category'], data['Values'], color=['#C9E4CA', '#F7D2C4', '#87CEEB', '#C5CAE9', '#FFC5C5'])
        # ax.set_ylabel("Values")
        # ax.set_title("Static Bar Chart")
        plt.subplots_adjust(left=0.2, right=0.8, top=0.9, bottom=0.2)  # Adjust margins
        
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


    
    st.markdown('''
    <div class="custom-container">
        <p class="title">Comprehensive Visualization Tools</p>
        <p class="subtitle">Our platform offers a complete set of visualization tools to help you understand your data from every angle.</p>
        <div class="card-container">
            <div class="card">
                <h4>📊 Charts & Graphs</h4>
                <p>Create beautiful and interactive visualizations with our intuitive chart builder.</p>
            </div>
            <div class="card">
                <h4>🤖 AI-Powered Insights</h4>
                <p>Let our AI analyze your data and discover hidden patterns and insights automatically.</p>
            </div>
            <div class="card">
                <h4>🔍 Natural Language Queries</h4>
                <p>Simply ask questions about your data and get instant visual answers and explanations.</p>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    

    st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)

    # Call to Action
    st.markdown("<p class='big-font'>Ready to transform your data into actionable insights?</p>", unsafe_allow_html=True)
    st.markdown("<p class='subtext'>Join thousands of organizations that use InsightLens to make data-driven decisions faster.</p>", unsafe_allow_html=True)
   
    # st.button("Start Free Trial", key="trial")
    

    # Create the button
    st.markdown('''
    <div class="button-container">
        <button class="light-blue-button">Click Here →</button>
    </div>
    ''', unsafe_allow_html=True)

       
    st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)

    # Footer
    # Create the navigation bar
    st.markdown('''
    <div class="navbar1">
        <div class="left-side">
            <h3 style="margin: 0;">🔍 DataQueryAI</h3>
        </div>
        <div class="middle-links">
            <a href="#">Terms</a>
            <a href="#">Privacy</a>
            <a href="#">Contact</a>
        </div>
        <div class="right-side">
            <p>© 2025 InsightLens. All rights reserved.</p>
        </div>
    </div>
''', unsafe_allow_html=True)
    
    

if __name__ == "__main__":
    main()
