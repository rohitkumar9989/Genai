# DataQueryAI: Auto-Generated Insights with Natural Language Queries

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Streamlit](https://img.shields.io/badge/UI-Framework-FF4B4B?logo=streamlit)

An AI-powered data visualization tool that transforms raw CSV data into actionable insights through **auto-generated charts** and a **natural language Q&A interface**. Built for non-technical users and analysts alike!

---

## 🚀 Features

- **Select CSV file and Upload**: Instantly process datasets with automated NaN handling.
- **Auto-Visualization**: Generates scatter plots, bar charts, line charts, histograms, and pie charts.
- **AI-Powered Q&A**: Ask questions like *"Show sales trends"* or *"Explain outliers"* and get instant answers.
- **One-Click Downloads**: Export visualizations as PNG files.
- **Responsive UI**: Works seamlessly on desktop and mobile (optimization in progress).

---

## ⚙️ Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/DataQueryAI.git
   cd DataQueryAI

Install Dependencies

pip install -r requirements.txt
Add API Keys
Create a .env file in the root directory and add your Groq API key:

GROQ_API_KEY=your_api_key_here
🖥️ Usage
Run the Streamlit App

streamlit run app.py

Upload a CSV File
Use the file uploader to add your dataset.

Explore Visualizations
The app auto-generates charts based on column relationships.

Ask Questions
Type natural language queries in the chat-style panel (e.g., "Which product has the highest revenue?").

Demo ![image](https://github.com/user-attachments/assets/80651320-40ad-4955-b820-0b811228459d)


🛠️ Technologies
Frontend: Streamlit

Data Processing: Pandas, NumPy

Visualization: Matplotlib, Seaborn

AI/NLP: LangChain, Groq API (Llama-3-70B, Gemma-9B)

Utilities: Python-DotEnv, FAISS

📋 Testing Status
Test Case	Status
CSV Upload & NaN Handling	✅ Passed
Natural Language Queries	✅ Passed
100k Rows Rendering	⚡ Optimized
Mobile Responsiveness	❌ In Progress


👥 Team

K. Rohit Kumar (Backend)

K. Hemanth Kumar (Visualization)

J. Jayanth (Testing)

Y. Kishore (UI/UX)

D. Pramodh (AI Integration)

📜 License
This project is licensed under the MIT License. See LICENSE for details.

🙏 Acknowledgements

NASSCOM for the hackathon platform.
Groq for providing AI model access.
Streamlit for the intuitive UI framework.

