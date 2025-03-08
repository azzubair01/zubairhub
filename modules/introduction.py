import streamlit as st

@st.fragment
def intro():
    # Title Section
    st.markdown(
        "<h1 style='text-align: center; color: black;'>🕵️ Welcome Readers!</h1>",
        unsafe_allow_html=True
    )
    st.write("---")

    # About Me Section
    st.write("## 👨‍💻 About Me")
    st.markdown(
        """
        <div style="font-family:sans-serif; font-size: 18px; color: Black;">
            <ul>
                <li> Experienced <span style="font-weight:bold; color:MediumBlue;">Data Scientist</span> with over 4 years of expertise in data analytics, machine learning, and process automation.</li>
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

    # Asia Digital Engineering Experience
    st.markdown(
        """
        <div style="font-family:sans-serif; font-size: 18px; color: Black;">
            <b>🔹 Data Scientist II</b> (Sept 2021 - Present)  
            <em>Asia Digital Engineering Sdn Bhd</em>  
            <ul>
                <li>🚀 Spearhead digital innovation initiatives to enhance operational efficiency across AirAsia departments.</li>
                <li>🔗 Design, develop, and optimize scalable data pipelines for <b>seamless extraction, transformation, and loading (ETL)</b>.</li>
                <li>📊 Conduct advanced data analysis to generate actionable insights that drive data-informed decision-making in <b>aviation engineering operations</b>.</li>
                <li>🤖 Integrate <b>AI-driven automation</b> to streamline processes and advance aviation digitalization efforts.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    # DataMicron Experience
    st.markdown(
        """
        <div style="font-family:sans-serif; font-size: 18px; color: Black;">
            <b>🔹 Junior Data Scientist</b> (July 2020 - Sept 2021)  
            <em>DataMicron Systems Sdn Bhd</em>  
            <ul>
                <li>📈 Provided <b>Big Data consulting</b> through proof-of-concept (POC) projects to drive business intelligence solutions.</li>
                <li>🛠️ Engineered <b>data transformation workflows</b> using <b>EzData</b> and <b>Python</b> for efficient processing and analysis.</li>
                <li>📉 Developed and deployed <b>predictive analytics models</b> for demand forecasting and trend analysis using <b>DataMicron Foresight</b>.</li>
                <li>🌐 Designed and implemented <b>AI-powered solutions</b> for <b>DataMicron EagleEye</b> to enhance decision-making capabilities.</li>
                <li>📊 Built interactive <b>Business Intelligence dashboards</b> with <b>DataMicron InstaBI</b> for real-time data visualization.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()
