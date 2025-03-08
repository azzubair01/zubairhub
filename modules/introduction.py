import streamlit as st

@st.fragment
def intro():
    # Title Section
    st.markdown(
        "<h1 style='text-align: center; color: var(--text-color);'>🕵️ Welcome Readers!</h1>",
        unsafe_allow_html=True
    )
    st.write("---")

    # About Me Section
    st.write("## 👨‍💻 About Me")
    st.markdown(
        """
        <style>
            .custom-text {
                font-family: sans-serif;
                font-size: 18px;
                color: var(--text-color);
            }
        </style>
        <div class="custom-text">
            <ul>
                <li> Experienced <span style="font-weight:bold; color:DodgerBlue;">Data Scientist</span> with over 4 years of expertise in data analytics, machine learning, and process automation.</li>
                <li> Passionate about leveraging data-driven solutions to drive efficiency, scalability, and operational improvements.</li>
                <li> Strong advocate for continuous learning and a firm believer in an experiment-driven approach to solving complex problems.</li>
                <li> Specialized in building end-to-end data pipelines, integrating AI-driven automation, and delivering actionable insights to optimize decision-making.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.write("---")

    # Experience Section
    st.write("## 💼 My Experience")

    with st.expander("Sept 2022 - Present", expanded=True):
        st.markdown(
            """
            <div class="custom-text">
                <b>🔹 Data Scientist II</b> <em>Asia Digital Engineering Sdn Bhd</em>  
                <ul>
                    <li>🚀 Enable digital innovation initiatives to enhance operational efficiency across AirAsia departments.</li>
                    <li>🔗 Develop and optimize scalable data pipelines for <b>seamless extraction, transformation, and loading (ETL)</b>.</li>
                    <li>📊 Conduct advanced data analysis to generate actionable insights for <b>aviation engineering operations</b>.</li>
                    <li>🤖 Integrate <b>AI-driven automation</b> to streamline processes and advance aviation digitalization efforts.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    with st.expander("July 2020 - Sept 2022", expanded=True):
        st.markdown(
            """
            <div class="custom-text">
                <b>🔹 Junior Data Scientist</b> <em>DataMicron Systems Sdn Bhd</em>  
                <ul>
                    <li>📈 Provided <b>Big Data consulting</b> through proof-of-concept (POC) projects to drive business intelligence solutions.</li>
                    <li>🛠️ Engineered <b>data transformation workflows</b> using <b>EzData</b> and <b>Python</b> for efficient processing and analysis.</li>
                    <li>📉 Developed and deployed <b>predictive analytics models</b> for demand forecasting and trend analysis.</li>
                    <li>🌐 Designed and implemented <b>AI-powered solutions</b> for decision-making improvements.</li>
                    <li>📊 Built interactive <b>Business Intelligence dashboards</b> for real-time data visualization.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    # Skills Section
    st.write("## 🛠️ Technical Skills")
    skills = {
        "Python & SQL": 75,
        "Machine Learning & AI (Google Vertex AI)": 30,
        "Data Visualization (Google Looker Studio)": 80,
        "Data Orchestration (Apache Airflow)": 50,
        "Big Data (MongoDB, Google BigQuery)": 40
    }

    for skill, level in skills.items():
        st.write(f"**{skill}**")
        st.progress(level / 100)

    st.divider()

    # Contact Section
    st.write("📧 Feel free to reach out via email or connect with me on LinkedIn!")

    # Footer
    st.markdown(
        """
        <style>
            .footer {
                text-align: center;
                font-size: 14px;
                padding: 10px;
                color: var(--text-color);
            }
        </style>
        <div class="footer">
            © 2024 Muhammad Azzubair Azeman | Built with ❤️ using Streamlit
        </div>
        """,
        unsafe_allow_html=True
    )
