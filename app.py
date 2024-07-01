import pandas as pd
import plotly
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import time
import json
import PIL 
from PIL import Image
import html
import base64

agg_trans_data = pd.read_csv("https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/dataset/agg_trans_data.csv")
agg_trans_data['State'] = agg_trans_data['State'].replace('Andaman & Nicobar Islands', 'Andaman & Nicobar')
map_trans_data = pd.read_csv("https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/dataset/map_trans_data.csv")
map_trans_data['State'] = map_trans_data['State'].replace('Andaman And Nicobar Islands', 'Andaman & Nicobar')
map_trans_data['State'] = map_trans_data['State'].replace('Jammu And Kashmir', 'Jammu & Kashmir')
map_user_data = pd.read_csv("https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/dataset/map_user_data.csv")
map_user_data['State'] = map_user_data['State'].replace('Andaman And Nicobar Islands', 'Andaman & Nicobar')
map_user_data['State'] = map_user_data['State'].replace('Jammu And Kashmir', 'Jammu & Kashmir')
agg_ins_data = pd.read_csv("https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/dataset/agg_ins_data.csv")
agg_ins_data['State'] = agg_ins_data['State'].replace('Andaman & Nicobar Islands', 'Andaman & Nicobar')
agg_ins_data['State'] = agg_ins_data['State'].replace('Jammu & Kashmir', 'Jammu & Kashmir')
map_ins_data = pd.read_csv("https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/dataset/map_ins_data.csv")
map_ins_data['State'] = map_ins_data['State'].replace('Andaman And Nicobar Islands', 'Andaman & Nicobar')
map_ins_data['State'] = map_ins_data['State'].replace('Jammu And Kashmir', 'Jammu & Kashmir')


class Convert:
    @staticmethod
    def millions(transaction):
        c = transaction / 1_000_000
        d = '{:.2f}'.format(c)
        return f'{d}M'

    @staticmethod
    def billions(transaction):
        c = transaction / 1_000_000_000
        d = '{:.2f}'.format(c)
        return f'{d}B'

    @staticmethod
    def trillions(transaction):
        c = transaction / 1_000_000_000_000
        d = '{:.2f}'.format(c)
        return f'{d}T'

    @staticmethod
    def crores(transaction):
        c = transaction / 10_000_000
        d = '{:.2f}'.format(c)
        return f'{d}Cr'

    @staticmethod
    def thousands(transaction):
        c = transaction / 1_000
        d = '{:.2f}'.format(c)
        return f'{d}K'

    @staticmethod
    def rupees(transaction):
        if transaction <= 1_000:
            return str(transaction)
        elif transaction <= 1_000_000:
            return Convert.thousands(transaction)
        elif transaction <= 1_000_000_000:
            return Convert.millions(transaction)
        elif transaction <= 1_000_000_000_000:
            return Convert.billions(transaction)
        else:
            return Convert.trillions(transaction)

def state_geojson_link():
    state_geojson_links = { "Andaman & Nicobar":"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/ANDAMAN%20%26%20NICOBAR_DISTRICTS.geojson",
                            'Andhra Pradesh':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/ANDHRA%20PRADESH_DISTRICTS.geojson",
                            'Arunachal Pradesh':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/ARUNACHAL%20PRADESH_DISTRICTS.geojson",
                            'Assam':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/ASSAM_DISTRICTS.geojson", 
                            'Bihar':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/BIHAR_DISTRICTS.geojson", 
                            'Chandigarh':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/CHANDIGARH_DISTRICTS.geojson", 
                            'Chhattisgarh':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/CHHATTISGARH_DISTRICTS.geojson",
                            'Dadra and Nagar Haveli and Daman and Diu':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/Dadra%20And%20Nagar%20Haveli%20And%20Daman%20And%20Diu%20DISTRICTS.geojson", 
                            'Delhi' :"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/DELHI_DISTRICTS.geojson", 
                            'Goa':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/GOA_DISTRICTS.geojson",
                            'Gujarat':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/GUJARAT_DISTRICTS.geojson", 
                            'Haryana':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/HARYANA_DISTRICTS.geojson", 
                            'Himachal Pradesh':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/HIMACHAL%20PRADESH_DISTRICTS.geojson", 
                            'Jammu & Kashmir': "https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/JAMMU%20%26%20KASHMIR_DISTRICTS.geojson",
                            'Jharkhand':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/JHARKHAND_DISTRICTS.geojson", 
                            'Karnataka':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/KARNATAKA_DISTRICTS.geojson", 
                            'Kerala':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/KERALA_DISTRICTS.geojson", 
                            'Ladakh':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/LADAKH_DISTRICTS.geojson", 
                            'Lakshadweep':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/LAKSHADWEEP_DISTRICTS.geojson",
                            'Madhya Pradesh':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/MADHYA%20PRADESH_DISTRICTS.geojson", 
                            'Maharashtra':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/MAHARASHTRA_DISTRICTS.geojson", 
                            'Manipur':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/MANIPUR_DISTRICTS.geojson", 
                            'Meghalaya':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/MEGHALAYA_DISTRICTS.geojson", 
                            'Mizoram':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/MIZORAM_DISTRICTS.geojson",
                            'Nagaland':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/NAGALAND_DISTRICTS.geojson", 
                            'Odisha':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/ODISHA_DISTRICTS.geojson", 
                            'Puducherry':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/PUDUCHERRY_DISTRICTS.geojson", 
                            'Punjab':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/PUNJAB_DISTRICTS.geojson", 
                            'Rajasthan':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/RAJASTHAN_DISTRICTS.geojson",
                            'Sikkim':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/SIKKIM_DISTRICTS.geojson", 
                            'Tamil Nadu':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/TAMIL%20NADU_DISTRICTS.geojson", 
                            'Telangana':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/TELANGANA_DISTRICTS.geojson", 
                            'Tripura': "https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/TRIPURA_DISTRICTS.geojson", 
                            'Uttar Pradesh':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/UTTAR%20PRADESH_DISTRICTS.geojson",
                            'Uttarakhand':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/UTTARAKHAND_DISTRICTS.geojson", 
                            'West Bengal':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/WEST%20BENGAL_DISTRICTS.geojson"
                        }
    return state_geojson_links

def state_zoom():
    zoom = { "Andaman & Nicobar": 5,
                            'Andhra Pradesh':5.5,
                            'Arunachal Pradesh':5.5,
                            'Assam':5.5, 
                            'Bihar':5.5, 
                            'Chandigarh':9, 
                            'Chhattisgarh':5.5,
                            'Dadra and Nagar Haveli and Daman and Diu':8, 
                            'Delhi' :8, 
                            'Goa':7,
                            'Gujarat':5.5, 
                            'Haryana':6, 
                            'Himachal Pradesh':6, 
                            'Jammu & Kashmir': 5.5,
                            'Jharkhand':5.5, 
                            'Karnataka':5.5, 
                            'Kerala':6, 
                            'Ladakh':5, 
                            'Lakshadweep':6,
                            'Madhya Pradesh':5.5, 
                            'Maharashtra':5.5, 
                            'Manipur':7, 
                            'Meghalaya':7, 
                            'Mizoram':7,
                            'Nagaland':7, 
                            'Odisha':5.5, 
                            'Puducherry':7, 
                            'Punjab':6, 
                            'Rajasthan':5.5,
                            'Sikkim':5, 
                            'Tamil Nadu':5.5, 
                            'Telangana':5.5, 
                            'Tripura': 7, 
                            'Uttar Pradesh':5.5,
                            'Uttarakhand':6, 
                            'West Bengal':5
                        }
    return zoom


# Define a dictionary mapping states to their latitude and longitude
def state_coordinate():
    state_coordinates = {
        "Andaman & Nicobar": {"lat": 10.7449, "lon": 92.5000},
        "Andhra Pradesh": {"lat": 15.9129, "lon": 79.7400},
        "Arunachal Pradesh": {"lat": 28.2180, "lon": 94.7278},
        "Assam": {"lat": 26.2006, "lon": 92.9376},
        "Bihar": {"lat": 25.0961, "lon": 85.3131},
        "Chandigarh": {"lat": 30.7333, "lon": 76.7794},
        "Chhattisgarh": {"lat": 21.2787, "lon": 81.8661},
        "Dadra and Nagar Haveli and Daman and Diu": {"lat": 20.1809, "lon": 73.0169},
        "Delhi": {"lat": 28.7041, "lon": 77.1025},
        "Goa": {"lat": 15.2993, "lon": 74.1240},
        "Gujarat": {"lat": 22.2587, "lon": 71.1924},
        "Haryana": {"lat": 29.0588, "lon": 76.0856},
        "Himachal Pradesh": {"lat": 31.1048, "lon": 77.1734},
        "Jammu & Kashmir": {"lat": 33.7782, "lon": 76.5762},
        "Jharkhand": {"lat": 23.6102, "lon": 85.2799},
        "Karnataka": {"lat": 15.3173, "lon": 75.7139},
        "Kerala": {"lat": 10.8505, "lon": 76.2711},
        "Ladakh": {"lat": 34.1526, "lon": 77.5770},
        "Lakshadweep": {"lat": 10.5667, "lon": 72.6417},
        "Madhya Pradesh": {"lat": 22.9734, "lon": 78.6569},
        "Maharashtra": {"lat": 19.7515, "lon": 75.7139},
        "Manipur": {"lat": 24.6637, "lon": 93.9063},
        "Meghalaya": {"lat": 25.4670, "lon": 91.3662},
        "Mizoram": {"lat": 23.1645, "lon": 92.9376},
        "Nagaland": {"lat": 26.1584, "lon": 94.5624},
        "Odisha": {"lat": 20.9517, "lon": 85.0985},
        "Puducherry": {"lat": 11.9416, "lon": 79.8083},
        "Punjab": {"lat": 31.1471, "lon": 75.3412},
        "Rajasthan": {"lat": 27.0238, "lon": 74.2179},
        "Sikkim": {"lat": 27.5330, "lon": 88.5122},
        "Tamil Nadu": {"lat": 11.1271, "lon": 78.6569},
        "Telangana": {"lat": 18.1124, "lon": 79.0193},
        "Tripura": {"lat": 23.9408, "lon": 91.9882},
        "Uttar Pradesh": {"lat": 26.8467, "lon": 80.9462},
        "Uttarakhand": {"lat": 30.0668, "lon": 79.0193},
        "West Bengal": {"lat": 22.9868, "lon": 87.8550}
    }
    return state_coordinates


# Set page title and favicon
st.set_page_config(page_title="Navin's Pulse Vision-A Phonepe Data App",layout="wide", page_icon="https://i.postimg.cc/4xzCQFWX/rock-chart-2.png")
violet_color = "#6F36AD"

st.markdown("<div style='text-align:center'><a href='https://postimg.cc/VrCzqwSm'><img src='https://i.postimg.cc/ydcYJMNc/new-logo-navins-pulse-vision.png' alt='pulse-2.webp'/></a></div>", unsafe_allow_html=True)


selected = option_menu("Navigation",
                       options=["ABOUT", "HOME", "TOP INSIGHTS", "FILTERED INSIGHTS"],
                       icons=["info-circle", "house", "bar-chart", "toggles"],
                       default_index=1,
                       orientation="horizontal",
                       styles={"container": {"width": "100%","border": "2px ridge #000000","background-color": "#391C59"},  # Adjust width to make it smaller
                               "icon": {"color": "#F8CD47", "font-size": "20px"},  # Adjust icon size and color
                               "nav-link": {"font-family": "**Helvetica**", "font-size": "20px", "text-align": "center", "color": "#FFFFFF"},  # Adjust font size and alignment
                               "nav-link-selected": {"background-color": "#FFFFFF", "color": "#391C59"}}) 

if selected == "ABOUT":

    def about_page():
        st.title(":violet[Welcome to Navin's Pulse Vision]")
        st.markdown("""
        Navin's Pulse Vision is your window into the heartbeat of financial transactions, user engagement, and insurance trends across states and districts in India. Dive into comprehensive insights derived from transaction data, user data, and insurance data meticulously curated and visualized for your understanding.
        """)

        st.header(":violet[Data Source]")
        st.write("The data used in this analysis is derived from PhonePe Pulse.")
        st.link_button("Go to PhonePe Pulse","https://www.phonepe.com/pulse/")

        st.header(":violet[Understanding the Pulse]")

        st.markdown("""
        At Navin's Pulse Vision, we believe in empowering decision-makers with actionable insights. Our platform provides a holistic view of the financial landscape, highlighting key trends and patterns that shape the way we understand economic activities.
        """)

        st.header(":violet[Unraveling Transaction Dynamics]")

        st.markdown("""
        Delve into the intricacies of financial transactions with our in-depth analysis:

        - Discover the Top 10 States with the Highest and Lowest Transaction Amounts.
        - Explore the Average Transaction Value for the Top 10 States, guiding you through the economic pulse of different regions.
        - Navigate through the Top 10 Districts with the Highest Transaction Amounts, uncovering localized spending patterns.
        - Track Quarter-wise Transaction Amount Distribution for specific states, offering a granular view of transaction trends over time.
        """)

        st.header(":violet[Mapping User Engagement]")

        st.markdown("""
        Understand the user landscape with our user data analysis:

        - Identify the Top 10 States with the Highest and Lowest User Counts, shedding light on regions with high engagement.
        - Explore the Quarter-wise User Distribution for specific states, providing insights into user behavior fluctuations over time.
        """)

        st.header(":violet[Insights into Insurance Trends]")

        st.markdown("""
        Navigate through the insurance landscape with our comprehensive analysis:

        - Uncover the Top 10 States with the Highest and Lowest Insurance Amounts, aiding in understanding insurance penetration across regions.
        - Explore the Top 10 Districts with the Highest Insurance Amounts, highlighting areas with significant insurance coverage.
        - Track Quarter-wise Insurance Amount Distribution for specific states, offering insights into insurance trends and preferences.
        """)

        st.header(":violet[Streamlined Visualization with Streamlit]")

        st.markdown("""
        Navin's Pulse Vision leverages Streamlit to present complex data in a user-friendly interface. Our interactive visualizations enable seamless exploration of trends, empowering users to derive meaningful insights effortlessly.
        """)

        st.header(":violet[Empowering Decision-Making]")

        st.markdown("""
        Whether you're a policymaker, business strategist, or simply curious about the financial landscape, Navin's Pulse Vision equips you with the tools to make informed decisions. Unlock the power of data-driven insights and navigate the pulse of India's financial ecosystem with confidence.
        """)
                # Disclaimer
        st.header(":red[Disclaimer]")
        st.write("The data and analysis presented in this dashboard are for informational purposes only and do not constitute financial advice.")
        st.write(":red[Please note that the data presented in this dashboard is limited to the period until 2023.]")

        st.header(":violet[Technology Used]")
        st.markdown("""
            - **Implemented backend logic with Python.**
            - **Pandas for Data Manupulation.**
            - **Plotly is a versatile graphing library used for creating interactive and visually appealing plots and charts.**
            - **Utilized Streamlit for web application development.**
        """)
        st.header(":violet[Join Us on the Journey]")

        st.markdown("""
        Embark on a journey of discovery with Navin's Pulse Vision. Explore, analyze, and uncover the pulse of India's financial dynamics like never before. Welcome aboard!

        *Navin's Pulse Vision - Illuminating Insights, Empowering Decisions.*
        """)       
        # About section
        st.header(":violet[About Me]")
        st.markdown("""
            Hi, I'm Navin, deeply passionate about the sea of data science and AI. 
            My goal is to become a skilled data scientist.

            Beyond the lines of code, my aim is to innovate and be a part of transformative technological evolution. 
            The world needs solutions that not only solve problems but redefine them. 
            I'm here to create change.
        """)
        def follow_button():
            st.markdown("""
            <style>
                .libutton {
                display: flex;
                flex-direction: column;
                justify-content: center;
                padding: 7px;
                text-align: center;
                outline: none;
                text-decoration: none !important;
                color: #ffffff !important;
                width: 200px;
                height: 32px;
                border-radius: 16px;
                background-color: #0A66C2;
                font-family: "SF Pro Text", Helvetica, sans-serif;
                }
            </style>
            <a class="libutton" href="https://www.linkedin.com/comm/mynetwork/discovery-see-all?usecase=PEOPLE_FOLLOWS&followMember=navinkumarsofficial" target="_blank">Click to Follow me 👆</a>
            """, unsafe_allow_html=True)

        # LinkedIn link with logo
        st.header(":violet[Connect with Me]")
        col1, col2 = st.columns([1,20])
           
        with col1:  
            
            linkedin_logo = "https://img.icons8.com/fluent/48/000000/linkedin.png"  
            linkedin_url = "https://www.linkedin.com/in/navinkumarsofficial/"  
            st.markdown(f"[![LinkedIn]({linkedin_logo})]({linkedin_url})")
        with col2:
            follow_button()
            



        
       

        # Email with logo
        email_logo = "https://img.icons8.com/fluent/48/000000/email.png"  
        your_email = "https://mail.google.com/mail/?view=cm&source=mailto&to=navinofficial1@gmail.com"
        st.markdown(f"[![Email]({email_logo})]({your_email})")

    
    about_page()



if selected == "HOME":

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("![Alt Text](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZWFrODU1bmo4YWdmN3V4Nmd3bjJzMDlwd2hqOXFuMTVuNjh2M2QxMCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/BXhnYI8ik0BvLYqx7J/giphy.gif)")

    with col2:
        st.markdown("[![13620-Crore.png](https://i.postimg.cc/FHdbnc9k/13620-Crore.png)](https://postimg.cc/yDKSDD37)")
    
    def home_page():
        st.title(":violet[Welcome to Navin's Pulse Vision]")
        st.markdown("""
        Navin's Pulse Vision is your gateway to comprehensive insights into India's financial landscape. Explore transaction data, user engagement, and insurance trends across states and districts with ease.
        """)

             # Introduction to PhonePe
        st.header(":violet[What is PhonePe?]")
        st.write("PhonePe is a leading Indian digital payments platform, empowering millions of users to seamlessly perform transactions, recharge phones, pay bills, and access various financial services.")

        st.header(":violet[What is PhonePe Pulse Data?]")
        st.write("PhonePe Pulse is an insightful data provided by PhonePe that offers users and businesses access to valuable data. It provides data on transaction, user, and insurance across different states and districts in India.")
        
        st.title(":violet[Unveiling India's Digital Landscape: Insights from PhonePe Pulse]")
        
        st.title(":violet[Project Summary ]")
        st.markdown("""
                    - Presents valuable insights from PhonePe Pulse data in an easy-to-understand format.
                    - Utilized Plotly to create interactive visuals for detailed analysis of transaction amounts, user distribution, and insurance metrics.
                    - Integrated Geo Maps for intuitive visualization of transaction, user, and insurance data across states and districts of India.
                    - Analyzed factors that influence transaction amounts and counts in different regions, as well as fluctuations in transaction volumes across quarters.
                    - Enabled detailed data exploration through filter options, supporting informed decision-making in financial services and digital transactions.
                    """)
        
        st.header(":violet[Discover Insights]")
        st.markdown("""
        - **Transaction Dynamics**: Explore transaction trends across states and districts, uncovering patterns in spending behavior.
        - **User Engagement**: Understand user behavior and engagement levels across different regions in India.
        - **Insurance Trends**: Gain insights into insurance penetration and preferences across states and districts.
        """)
        st.markdown("<div style='text-align:center'><a href='https://postimg.cc/VrCzqwSm'><img src='https://i.postimg.cc/gJMrPkmX/pulse-2.webp' alt='pulse-2.webp'/></a></div>", unsafe_allow_html=True)

        st.header(":violet[Get Started]")
        st.markdown("""
        Dive into the data-driven world of Navin's Pulse Vision and unlock the power of insights. Begin your journey now!
        """)
        st.write(":red[Please note that the data presented in this dashboard is limited to the period until 2023.]")

            # Data Source
        st.header(":violet[Data Source]")
        st.write("The data used in this analysis is derived from PhonePe Pulse.")
        st.link_button("Go to PhonePe Pulse","https://www.phonepe.com/pulse/")

        # Useful Information
        st.header(":violet[Useful Information]")
        st.write("- **Stay Informed:** Keep yourself updated with the latest trends in India's digital payments ecosystem.")
        st.write("- **Make Informed Decisions:** Use the insights from PhonePe Pulse to make informed decisions about digital transactions and financial strategies.")
        st.write("- **Explore Opportunities:** Identify potential business opportunities or areas for improvement based on the analysis of digital payment data.")   
       
        st.header(":violet[To Know More]")
        col5, col6 = st.columns(2)
        with col5:
            st.video('https://youtu.be/c_1H6vivsiA?si=lVPODg0axykJgeAZ') 

        with col6:
            st.video('https://youtu.be/Yy03rjSUIB8?si=eJRqbCm-K_RDtv0Y') 
    home_page()               


if selected == "TOP INSIGHTS" :
    st.subheader("Insights")
    filter_container1 =  st.container(border = True) 
    insights_type = st.radio('Category Selection',["**Transactions**","**Users**","**Insurance**"], index = None)
    st.write("You selected:", f"<span style='color:#F8CD47'>{insights_type}</span>", unsafe_allow_html=True)
    if insights_type == "**Transactions**":

        insights_container =  st.container(border = True)
        insights_container.subheader("Insights Types")
        insights_filter_type = insights_container.radio("Select Type", ["Geo Visualization","Top Insights"],key = 'trans_insights', horizontal=True,index= 0)
        
        if insights_filter_type == "Geo Visualization":

            def geo():
                # @st.cache_data
                def india_geojson():
                    india = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                    return india  
                              
                trans_geo_queries = ["Total Data","District Wise Total Data"]
                st.title(":violet[Transaction Data Distribution Across States]")      
                selected_query = st.selectbox("Select a Query", trans_geo_queries,key ="trans_geo_query",index= 0)  
            
                if selected_query == trans_geo_queries[0]:
                    trans_geo_year_wise = st.toggle('Year-Wise')
                    if not trans_geo_year_wise:
                        def total_agg_trans_geo():
                            show_total_trans_count = st.checkbox("Change Colors On The Map Based On Total Transaction Count")

                            if not show_total_trans_count:
                                df = agg_trans_data.groupby(["State"], as_index=False).agg({"Amount":["sum","mean"],"Trans_Count":["sum","mean"]})
                                df['State'] = df['State'].replace('Andaman And Nicobar Islands', 'Andaman & Nicobar')
                                df.columns = ['State', 'Total_Transaction_Amount', 'Average_Transaction_Amount', 'Total_Transaction_Count', 'Average_Transaction_Count']
                                formated_Total_Transaction_Amount = [Convert.rupees(amount) for amount in df['Total_Transaction_Amount']]
                                formated_Average_Transaction_Amount = [Convert.rupees(amount) for amount in df['Average_Transaction_Amount']]
                                formated_Total_Transaction_Count =  [Convert.rupees(amount) for amount in df['Total_Transaction_Count']]
                                formated_Average_Transaction_Count =  [Convert.rupees(amount) for amount in df['Average_Transaction_Count']]
                                hover_template = (
                                                    "<b>%{location}</b><br>"
                                                    "Total Transaction Value: %{customdata[0]}<br>"
                                                    "Average Transaction Value: %{customdata[1]}<br>"
                                                    "Total Transaction: %{customdata[2]}<br>"
                                                    "Average Transaction: %{customdata[3]}"
                                                )
                                
                                customdata = list(zip(formated_Total_Transaction_Amount, formated_Average_Transaction_Amount, formated_Total_Transaction_Count, formated_Average_Transaction_Count))

                                fig = px.choropleth_mapbox(
                                    df,
                                    geojson= india_geojson(),
                                    locations='State',
                                    mapbox_style="carto-positron",
                                    zoom=3.5,
                                    center={"lat": 21.7679, "lon": 78.8718}, 
                                    # opacity=0.5,
                                    featureidkey='properties.ST_NM', 
                                    color='Total_Transaction_Amount', 
                                    color_continuous_scale=px.colors.sequential.dense_r,
                                    )
                                fig.update_geos(fitbounds="locations", visible=False)
                                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                                fig.update_layout(geo_bgcolor="#210D38")
                                fig.update_traces(hovertemplate=hover_template, customdata=customdata)
                                fig.update_coloraxes(colorbar_title_text='Total Transaction Value')
                                fig.update_layout(height=600)
                                st.subheader("Showing Total Transaction Value: Sum of All Years")
                                st.plotly_chart(fig,use_container_width = True)

                            elif show_total_trans_count:
                                df = agg_trans_data.groupby(["State"], as_index=False).agg({"Amount":["sum","mean"],"Trans_Count":["sum","mean"]})
                                df['State'] = df['State'].replace('Andaman And Nicobar Islands', 'Andaman & Nicobar')
                                df.columns = ['State', 'Total_Transaction_Amount', 'Average_Transaction_Amount', 'Total_Transaction_Count', 'Average_Transaction_Count']
                                formated_Total_Transaction_Amount = [Convert.rupees(amount) for amount in df['Total_Transaction_Amount']]
                                formated_Average_Transaction_Amount = [Convert.rupees(amount) for amount in df['Average_Transaction_Amount']]
                                formated_Total_Transaction_Count =  [Convert.rupees(amount) for amount in df['Total_Transaction_Count']]
                                formated_Average_Transaction_Count =  [Convert.rupees(amount) for amount in df['Average_Transaction_Count']]
                                hover_template = (
                                                    "<b>%{location}</b><br>"
                                                    "Total Transaction: %{customdata[2]}<br>"
                                                    "Average Transaction: %{customdata[3]}<br>"
                                                    "Total Transaction Value: %{customdata[0]}<br>"
                                                    "Average Transaction Value: %{customdata[1]}<br>"
                                                )
                                
                                customdata = list(zip(formated_Total_Transaction_Amount, formated_Average_Transaction_Amount, formated_Total_Transaction_Count, formated_Average_Transaction_Count))

                                fig = px.choropleth_mapbox(
                                    df,
                                    geojson= india_geojson(),
                                    locations='State',
                                    mapbox_style="carto-positron",
                                    zoom=3.5,
                                    center={"lat": 21.7679, "lon": 78.8718}, 
                                    # opacity=0.5,
                                    featureidkey='properties.ST_NM', 
                                    color='Total_Transaction_Count', 
                                    color_continuous_scale= px.colors.sequential.dense_r,
                                    )
                                fig.update_geos(fitbounds="locations", visible=False)
                                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                                fig.update_layout(geo_bgcolor="#210D38")
                                fig.update_traces(hovertemplate=hover_template, customdata=customdata)
                                fig.update_layout(height=600)
                                fig.update_coloraxes(colorbar_title_text='Total Transaction Count')
                                st.subheader("Showing Total Transaction Count: Sum of All Years")
                                st.plotly_chart(fig,use_container_width = True)                            
                        total_agg_trans_geo()
                    
                    if trans_geo_year_wise:

                        def year_wise_agg_trans_geo():
                            
                            selected_year = st.select_slider("Select Year", sorted(agg_trans_data['Year'].unique()))
                            show_total_trans_count = st.checkbox("Change Colors On The Map Based On Total Transaction Count")

                            if not show_total_trans_count:
                                df = agg_trans_data.loc[agg_trans_data.Year == selected_year].groupby(["State"], as_index=False).agg({"Amount":["sum","mean"],"Trans_Count":["sum","mean"]})
                                df['State'] = df['State'].replace('Andaman And Nicobar Islands', 'Andaman & Nicobar')
                                df.columns = ['State', 'Total_Transaction_Amount', 'Average_Transaction_Amount', 'Total_Transaction_Count', 'Average_Transaction_Count']
                                formated_Total_Transaction_Amount = [Convert.rupees(amount) for amount in df['Total_Transaction_Amount']]
                                formated_Average_Transaction_Amount = [Convert.rupees(amount) for amount in df['Average_Transaction_Amount']]
                                formated_Total_Transaction_Count =  [Convert.rupees(amount) for amount in df['Total_Transaction_Count']]
                                formated_Average_Transaction_Count =  [Convert.rupees(amount) for amount in df['Average_Transaction_Count']]
                                hover_template = (
                                                    "<b>%{location}</b><br>"
                                                    "Total Transaction Value: %{customdata[0]}<br>"
                                                    "Average Transaction Value: %{customdata[1]}<br>"
                                                    "Total Transaction: %{customdata[2]}<br>"
                                                    "Average Transaction: %{customdata[3]}"
                                                )
                                
                                customdata = list(zip(formated_Total_Transaction_Amount, formated_Average_Transaction_Amount, formated_Total_Transaction_Count, formated_Average_Transaction_Count))

                                fig = px.choropleth_mapbox(
                                    df,
                                    geojson=india_geojson(),
                                    locations='State',
                                    mapbox_style="carto-positron",
                                    zoom=3.5,
                                    center={"lat": 21.7679, "lon": 78.8718}, 
                                    # opacity=0.5,
                                    featureidkey='properties.ST_NM', 
                                    color='Total_Transaction_Amount', 
                                    color_continuous_scale= px.colors.sequential.dense_r)
                                fig.update_geos(fitbounds="locations", visible=False)
                                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                                fig.update_layout(geo_bgcolor="#210D38")
                                fig.update_layout(height=600)
                                fig.update_traces(hovertemplate=hover_template, customdata=customdata)
                                fig.update_coloraxes(colorbar_title_text='Total Transaction Value')
                                st.subheader(f"Showing Transaction Value of Year: {selected_year}")
                                st.plotly_chart(fig,use_container_width = True)          

                            elif show_total_trans_count:
                                df = agg_trans_data.loc[agg_trans_data.Year == selected_year].groupby(["State"], as_index=False).agg({"Amount":["sum","mean"],"Trans_Count":["sum","mean"]})
                                df['State'] = df['State'].replace('Andaman And Nicobar Islands', 'Andaman & Nicobar')
                                df.columns = ['State', 'Total_Transaction_Amount', 'Average_Transaction_Amount', 'Total_Transaction_Count', 'Average_Transaction_Count']
                                formated_Total_Transaction_Amount = [Convert.rupees(amount) for amount in df['Total_Transaction_Amount']]
                                formated_Average_Transaction_Amount = [Convert.rupees(amount) for amount in df['Average_Transaction_Amount']]
                                formated_Total_Transaction_Count =  [Convert.rupees(amount) for amount in df['Total_Transaction_Count']]
                                formated_Average_Transaction_Count =  [Convert.rupees(amount) for amount in df['Average_Transaction_Count']]
                                hover_template = (
                                                    "<b>%{location}</b><br>"
                                                    "Total Transaction: %{customdata[2]}<br>"
                                                    "Average Transaction: %{customdata[3]}<br>"
                                                    "Total Transaction Value: %{customdata[0]}<br>"
                                                    "Average Transaction Value: %{customdata[1]}<br>"
                                                )
                                
                                customdata = list(zip(formated_Total_Transaction_Amount, formated_Average_Transaction_Amount, formated_Total_Transaction_Count, formated_Average_Transaction_Count))

                                fig = px.choropleth_mapbox(
                                    df,
                                    geojson=india_geojson(),
                                    locations='State',
                                    mapbox_style="carto-positron",
                                    zoom=3.5,
                                    center={"lat": 21.7679, "lon": 78.8718}, 
                                    # opacity=0.5,
                                    featureidkey='properties.ST_NM', 
                                    color='Total_Transaction_Count', 
                                    color_continuous_scale= px.colors.sequential.dense_r)
                                fig.update_geos(fitbounds="locations", visible=False)
                                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                                fig.update_layout(geo_bgcolor="#210D38")
                                fig.update_layout(height=600)
                                fig.update_traces(hovertemplate=hover_template, customdata=customdata)
                                fig.update_coloraxes(colorbar_title_text='Total Transaction Count')
                                st.subheader(f"Showing Transaction Count of Year: {selected_year}")
                                st.plotly_chart(fig,use_container_width = True)       
                        year_wise_agg_trans_geo()
      
                  
                    
                if selected_query == trans_geo_queries[1]: 
                    trans_geo_dist_year_wise = st.toggle('Year-Wise')   

                    if not trans_geo_dist_year_wise:
                        def district_wise_trans_total():
                            show_total_trans_count = st.checkbox("Change Colors On The Map Based On Total Transaction Count")
                            map_trans_data['State'] = map_trans_data['State'].replace('Andaman And Nicobar Islands', 'Andaman & Nicobar')
                            selected_state = st.selectbox("Select State", sorted([state for state in map_trans_data['State'].unique() if state != "Dadra And Nagar Haveli And Daman And Diu"]),index = 29)
                            state_coordinates = state_coordinate()
                            zoom = state_zoom()
                            state_geojson_links = state_geojson_link()
                            if selected_state in state_geojson_links:
                                geojson_link = state_geojson_links[selected_state]

                                if not show_total_trans_count:
                                    df = map_trans_data.loc[map_trans_data['State'] == selected_state].groupby("District", as_index = False).agg({"Amount":["sum","mean"],"Trans_Count":["sum","mean"]})
                                    df.columns = ["District",'Total_Transaction_Amount', 'Average_Transaction_Amount', 'Total_Transaction_Count', 'Average_Transaction_Count']
                                    formated_Total_Transaction_Amount = [Convert.rupees(amount) for amount in df['Total_Transaction_Amount']]
                                    formated_Average_Transaction_Amount = [Convert.rupees(amount) for amount in df['Average_Transaction_Amount']]
                                    formated_Total_Transaction_Count =  [Convert.rupees(amount) for amount in df['Total_Transaction_Count']]
                                    formated_Average_Transaction_Count =  [Convert.rupees(amount) for amount in df['Average_Transaction_Count']]
                                    hover_template = (
                                                        "<b>%{location}</b><br>"
                                                        "Total Transaction Value: %{customdata[0]}<br>"
                                                        "Average Transaction Value: %{customdata[1]}<br>"
                                                        "Total Transaction: %{customdata[2]}<br>"
                                                        "Average Transaction: %{customdata[3]}"
                                                    )
                                    
                                    customdata = list(zip(formated_Total_Transaction_Amount, formated_Average_Transaction_Amount, formated_Total_Transaction_Count, formated_Average_Transaction_Count))
                                    
                                    center_coordinates = state_coordinates[selected_state]
                                    depth = zoom[selected_state]
                                    fig = px.choropleth_mapbox(
                                        df,
                                        geojson=geojson_link,
                                        locations='District',
                                        mapbox_style="carto-positron",
                                        zoom=depth,
                                        center=center_coordinates, 
                                        
                                        featureidkey='properties.dtname', 
                                        color='Total_Transaction_Amount', 
                                        color_continuous_scale= px.colors.sequential.Viridis)
                                    fig.update_geos(fitbounds="locations", visible=False)
                                    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                                    fig.update_layout(geo_bgcolor="#210D38")
                                    fig.update_coloraxes(colorbar_title_text='Total Transaction Value')
                                    fig.update_traces(hovertemplate=hover_template, customdata=customdata)
                                    st.subheader(f"Showing Transaction Value for the Districts of {selected_state}")
                                    st.plotly_chart(fig,use_container_width = True)  

                                elif show_total_trans_count: 
                                    df = map_trans_data.loc[map_trans_data['State'] == selected_state].groupby("District", as_index = False).agg({"Amount":["sum","mean"],"Trans_Count":["sum","mean"]})
                                    df.columns = ["District",'Total_Transaction_Amount', 'Average_Transaction_Amount', 'Total_Transaction_Count', 'Average_Transaction_Count']
                                    formated_Total_Transaction_Amount = [Convert.rupees(amount) for amount in df['Total_Transaction_Amount']]
                                    formated_Average_Transaction_Amount = [Convert.rupees(amount) for amount in df['Average_Transaction_Amount']]
                                    formated_Total_Transaction_Count =  [Convert.rupees(amount) for amount in df['Total_Transaction_Count']]
                                    formated_Average_Transaction_Count =  [Convert.rupees(amount) for amount in df['Average_Transaction_Count']]
                                    hover_template = (
                                                        "<b>%{location}</b><br>"
                                                        "Total Transaction: %{customdata[2]}<br>"
                                                        "Average Transaction: %{customdata[3]}<br>"
                                                        "Total Transaction Value: %{customdata[0]}<br>"
                                                        "Average Transaction Value: %{customdata[1]}<br>"
                                                    )
                                    
                                    customdata = list(zip(formated_Total_Transaction_Amount, formated_Average_Transaction_Amount, formated_Total_Transaction_Count, formated_Average_Transaction_Count))
                                    
                                    center_coordinates = state_coordinates[selected_state]
                                    depth = zoom[selected_state]
                                    fig = px.choropleth_mapbox(
                                        df,
                                        geojson=geojson_link,
                                        locations='District',
                                        mapbox_style="carto-positron",
                                        zoom=depth,
                                        center=center_coordinates, 
                                        
                                        featureidkey='properties.dtname', 
                                        color='Total_Transaction_Count', 
                                        color_continuous_scale=px.colors.sequential.Viridis)
                                    fig.update_geos(fitbounds="locations", visible=False)
                                    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                                    fig.update_layout(geo_bgcolor="#210D38")
                                    fig.update_coloraxes(colorbar_title_text='Total Transaction Count')
                                    fig.update_traces(hovertemplate=hover_template, customdata=customdata)
                                    st.subheader(f"Showing Transaction Count for the Districts of {selected_state}")
                                    st.plotly_chart(fig,use_container_width = True)                                         
                        district_wise_trans_total()

                    if trans_geo_dist_year_wise:
                        def yearly_district_wise_trans_total():
                            show_total_trans_count = st.checkbox("Change Colors On The Map Based On Total Transaction Count")
                            map_trans_data['State'] = map_trans_data['State'].replace('Andaman And Nicobar Islands', 'Andaman & Nicobar')
                            selected_state = st.selectbox("Select State", sorted([state for state in map_trans_data['State'].unique() if state != "Dadra And Nagar Haveli And Daman And Diu"]),index = 29)
                            selected_year = st.select_slider("Select Year", sorted(map_trans_data['Year'].unique()))
                            state_geojson_links = state_geojson_link()
                            zoom = state_zoom()
                            state_coordinates = state_coordinate()

                            if selected_state in state_geojson_links:
                                geojson_link = state_geojson_links[selected_state]

                                if not show_total_trans_count:
                                    df = map_trans_data.loc[(map_trans_data['State'] == selected_state) & (map_trans_data['Year'] == selected_year)].groupby("District", as_index = False).agg({"Amount":["sum","mean"],"Trans_Count":["sum","mean"]})
                                    df.columns = ["District",'Total_Transaction_Amount', 'Average_Transaction_Amount', 'Total_Transaction_Count', 'Average_Transaction_Count']
                                    formated_Total_Transaction_Amount = [Convert.rupees(amount) for amount in df['Total_Transaction_Amount']]
                                    formated_Average_Transaction_Amount = [Convert.rupees(amount) for amount in df['Average_Transaction_Amount']]
                                    formated_Total_Transaction_Count =  [Convert.rupees(amount) for amount in df['Total_Transaction_Count']]
                                    formated_Average_Transaction_Count =  [Convert.rupees(amount) for amount in df['Average_Transaction_Count']]
                                    hover_template = (
                                                        "<b>%{location}</b><br>"
                                                        "Total Transaction Value: %{customdata[0]}<br>"
                                                        "Average Transaction Value: %{customdata[1]}<br>"
                                                        "Total Transaction: %{customdata[2]}<br>"
                                                        "Average Transaction: %{customdata[3]}"
                                                    )
                                    
                                    customdata = list(zip(formated_Total_Transaction_Amount, formated_Average_Transaction_Amount, formated_Total_Transaction_Count, formated_Average_Transaction_Count))
                                    
                                    center_coordinates = state_coordinates[selected_state]
                                    depth = zoom[selected_state]
                                    fig = px.choropleth_mapbox(
                                        df,
                                        geojson=geojson_link,
                                        locations='District',
                                        mapbox_style="carto-positron",
                                        zoom=depth,
                                        center=center_coordinates, 
                                        
                                        featureidkey='properties.dtname', 
                                        color='Total_Transaction_Amount', 
                                        color_continuous_scale=px.colors.sequential.Viridis)
                                    fig.update_geos(fitbounds="locations", visible=False)
                                    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                                    fig.update_layout(geo_bgcolor="#210D38")
                                    fig.update_coloraxes(colorbar_title_text='Total Transaction Value')
                                    fig.update_traces(hovertemplate=hover_template, customdata=customdata)
                                    st.subheader(f"Showing Transaction Value for the Districts of {selected_state} on the Year {selected_year}")
                                    st.plotly_chart(fig,use_container_width = True)       

                                elif show_total_trans_count:   
                                        df = map_trans_data.loc[(map_trans_data['State'] == selected_state) & (map_trans_data['Year'] == selected_year)].groupby("District", as_index = False).agg({"Amount":["sum","mean"],"Trans_Count":["sum","mean"]})
                                        df.columns = ["District",'Total_Transaction_Amount', 'Average_Transaction_Amount', 'Total_Transaction_Count', 'Average_Transaction_Count']
                                        formated_Total_Transaction_Amount = [Convert.rupees(amount) for amount in df['Total_Transaction_Amount']]
                                        formated_Average_Transaction_Amount = [Convert.rupees(amount) for amount in df['Average_Transaction_Amount']]
                                        formated_Total_Transaction_Count =  [Convert.rupees(amount) for amount in df['Total_Transaction_Count']]
                                        formated_Average_Transaction_Count =  [Convert.rupees(amount) for amount in df['Average_Transaction_Count']]
                                        hover_template = (
                                                            "<b>%{location}</b><br>"
                                                            "Total Transaction: %{customdata[2]}<br>"
                                                            "Average Transaction: %{customdata[3]}<br>"
                                                            "Total Transaction Value: %{customdata[0]}<br>"
                                                            "Average Transaction Value: %{customdata[1]}<br>"
                                                        )
                                        
                                        customdata = list(zip(formated_Total_Transaction_Amount, formated_Average_Transaction_Amount, formated_Total_Transaction_Count, formated_Average_Transaction_Count))
                                        
                                        center_coordinates = state_coordinates[selected_state]
                                        depth = zoom[selected_state]
                                        fig = px.choropleth_mapbox(
                                            df,
                                            geojson=geojson_link,
                                            locations='District',
                                            mapbox_style="carto-positron",
                                            zoom=depth,
                                            center=center_coordinates, 
                                            
                                            featureidkey='properties.dtname', 
                                            color='Total_Transaction_Count', 
                                            color_continuous_scale=px.colors.sequential.Viridis)
                                        fig.update_geos(fitbounds="locations", visible=False)
                                        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                                        fig.update_layout(geo_bgcolor="#210D38")
                                        fig.update_coloraxes(colorbar_title_text='Total Transaction Count')
                                        fig.update_traces(hovertemplate=hover_template, customdata=customdata)
                                        st.subheader(f"Showing Transaction Count for the Districts of {selected_state} on the Year {selected_year}")
                                        st.plotly_chart(fig,use_container_width = True)                                 
                        yearly_district_wise_trans_total()

            geo()



        if insights_filter_type == "Top Insights":                

            def trans_top_insights():           
                top_queries = ["Top 10 States with Highest Transactions",
                                "Top 10 States with Lowest Transactions",
                                "Average Transactions for Top 10 States",
                                "Top 10 District With Highest Transactions",
                                "Quarter-wise transaction distribution for specific state"]
                        
                selected_query = st.selectbox("Select a Query", top_queries,index= None)  


                
                if selected_query:
                    if selected_query == top_queries[0]:
                        year_wise_high_perf_amount_over_time = st.toggle('Year-Wise') 
                        if not year_wise_high_perf_amount_over_time:
                            def top_10_states():
                                reason = """
                                🟡 According to PhonePe, 44% of **Telangana**'s population uses digital payments, which is the highest in India.
                                The Telangana government has actively promoted digital payments through various initiatives like **"Telangana Digital Transactions Mission"** and **"Har Ghar Digital Payment"** campaign. This, along with subsidies and incentives, has encouraged citizens to adopt PhonePe and other digital wallets.
                                Telangana boasts a young and tech-savvy population, particularly in Hyderabad, the IT hub of India. 
                                """
                                reason2 = """🟡 **Karnataka** has a strong tech-savvy population and a well-developed digital infrastructure. This makes it more receptive to digital payments.
                                            Karnataka has a high concentration of urban areas with a growing middle class. This segment is more likely to use digital payment platforms for various transactions."""
                                reason3 = """🟡 **Maharashtra** boasts the largest population in India, and a significant portion is tech-savvy and open to adopting digital payments. Particularly in Mumbai and Pune, where digital 
                                        payments are more prevalent due to faster internet connectivity and a higher standard of living."""
                                
                                reason4 = """🟡 **Rajasthan, Andhra Pradesh, Tamil Nadu, Madhya Pradesh, Uttar Pradesh, Bihar, and West Bengal** have some of the largest populations in India, which means that there are more people engaging in economic activity and making transactions. 
                                                These states have diversified economies with a mix of agriculture, industry, and services. 
                                                These states have relatively well-developed infrastructure, including roads, railways, and airports. This makes it easier for goods and services to be transported and for people to travel, which can lead to more economic activity and transactions.
                                                These states have a growing middle class, which means that there are more people with disposable income who are able to make purchases and engage in economic activity."""
                                def stream_data():
                                    for word in reason.split():
                                        yield word + " "
                                        time.sleep(0.03)

                                def stream_data1():
                                    for word in reason3.split():
                                        yield word + " "
                                        time.sleep(0.03)

                                def stream_data2():
                                    for word in reason2.split():
                                        yield word + " "
                                        time.sleep(0.03)        

                                def stream_data3():
                                    for word in reason4.split():
                                        yield word + " "
                                        time.sleep(0.03)          

                                                            
                                def top_10_statess(agg_trans_data):
                                    top_10_states = agg_trans_data.groupby(["State"], as_index=False).Amount.sum().sort_values(by="Amount", ascending=False).head(10)
                                    return top_10_states
                                col1, col2 = st.columns(2)
                                with col1:
                                    top_10_states = top_10_statess(agg_trans_data)
                                    formated_amount_10 = [Convert.rupees(amount) for amount in top_10_states['Amount']]
                                    
                                    
                                    fig = px.bar(top_10_states, 
                                                x="State", 
                                                y="Amount",
                                                color = "State", 
                                                color_discrete_sequence=px.colors.qualitative.Alphabet,
                                                text=formated_amount_10,title = "Transaction Amount")
                                    fig.update_layout(xaxis=dict(title='State'), yaxis=dict(title="Total Amount"))
                                    fig.update_traces(hovertemplate="Amount: %{text}",textposition='outside')
                                    st.plotly_chart(fig, use_container_width=True)
                                    st.dataframe(top_10_states,width=500, height=400, hide_index= True)
                                            
                                with col2:
                                    a = top_10_statess(agg_trans_data)
                                    filter1 = list(a.State.unique())
                                    top_10_states = agg_trans_data.loc[agg_trans_data.State.isin(filter1)].groupby(["State"], as_index=False).Trans_Count.sum().sort_values(by="Trans_Count", ascending=False).head(10)
                                    formated_amount_10 = [Convert.rupees(amount) for amount in top_10_states['Trans_Count']]
                                    
                                    
                                    fig = px.bar(top_10_states, 
                                                x="State", 
                                                y="Trans_Count",
                                                color = "State", 
                                                color_discrete_sequence=px.colors.qualitative.Alphabet,
                                                text=formated_amount_10,title = "Transaction Count")
                                    
                                    fig.update_layout(xaxis=dict(title='State'), yaxis=dict(title="Transaction Count"))
                                    fig.update_traces(hovertemplate="Transaction Count: %{text}",textposition='outside')
                                    st.plotly_chart(fig, use_container_width=True)
                                    st.dataframe(top_10_states,width=500, height=400, hide_index= True)
                                
                                st.write_stream(stream_data)
                                st.write_stream(stream_data1)
                                st.write_stream(stream_data2)
                                st.write_stream(stream_data3)
                                

                            top_10_states()   
                            
                        if year_wise_high_perf_amount_over_time:      
                            def top_10_states_on_year():
                                
                                selected_year = st.select_slider("Select Year", sorted(agg_trans_data['Year'].unique()))

                                col3, col4 = st.columns(2)
                                top_10_states = agg_trans_data.loc[agg_trans_data.Year == selected_year].groupby(["State"], as_index=False).Amount.sum().sort_values(by="Amount", ascending=False).head(10)
                                with col3:
                                    if selected_year:
                                        top_10_states = agg_trans_data.loc[agg_trans_data.Year == selected_year].groupby(["State"], as_index=False).Amount.sum().sort_values(by="Amount", ascending=False).head(10)
                                        formated_amount_10 = [Convert.rupees(amount) for amount in top_10_states['Amount']]
                    
                                        fig = px.bar(top_10_states, 
                                                    x="State", 
                                                    y="Amount",
                                                    color = "State", 
                                                    color_discrete_sequence=px.colors.qualitative.Alphabet,
                                                    text=formated_amount_10,title = "Transaction Amount")
                                        fig.update_layout(xaxis=dict(title='State'), yaxis=dict(title="Total Amount"))
                                        fig.update_traces(hovertemplate="Amount: %{text}",textposition='outside')
                                        st.plotly_chart(fig, use_container_width=True)
                                        st.dataframe(top_10_states,width=500, height=400, hide_index= True)
                                
                                with col4:
                                    if selected_year:
                                        a = agg_trans_data.loc[agg_trans_data.Year == selected_year].groupby(["State"], as_index=False).Amount.sum().sort_values(by="Amount", ascending=False).head(10)
                                        filter = list(a.State.unique())
                                        top_10_states1 = agg_trans_data.loc[(agg_trans_data.Year == selected_year)&(agg_trans_data.State.isin(filter))].groupby(["State"], as_index=False).Trans_Count.sum().sort_values(by="Trans_Count", ascending=False)
                                        formated_amount_10 = [Convert.rupees(amount) for amount in top_10_states1['Trans_Count']]

                                        fig = px.bar(top_10_states1, 
                                                    x="State", 
                                                    y="Trans_Count",
                                                    color = "State", 
                                                    color_discrete_sequence=px.colors.qualitative.Alphabet,
                                                    text=formated_amount_10,title = "Transaction Count")
                                        fig.update_layout(xaxis=dict(title='State'), yaxis=dict(title="Total Transaction Count"))
                                        fig.update_traces(hovertemplate="Transaction Count: %{text}",textposition='outside')
                                        st.plotly_chart(fig, use_container_width=True)

                                        st.dataframe(top_10_states1,width=500, height=400, hide_index= True)
                                expander = st.expander("See explanation")
                            top_10_states_on_year()                


                if selected_query:
                    if selected_query == top_queries[1]:
                        year_wise__low_perf_state_amount_over_time= st.toggle('Year-Wise')
                        if not year_wise__low_perf_state_amount_over_time:
                            def low_10_states():
                                reason = """
                                🟡 **Lakshadweep** has the smallest population among all Indian states and UTs, with around 66,000 inhabitants.
                                The economy of Lakshadweep is primarily based on fishing and tourism, with limited industrial activity or large-scale businesses.  
                                """
                                reason2 = """🟡 **Mizoram**'s economy relies heavily on agriculture, with a large number of small and marginal farmers. This sector typically involves smaller transactions compared to industries like manufacturing or services."""
                                reason3 = """🟡 **Andaman and Nicobar** has the second-smallest population among Indian states and UTs, With a population of around 4.64 Lakhs. 
                                            The economy heavily relies on tourism and fisheries, with limited industrial activity or large-scale businesses. This restricts the generation and circulation of wealth within the islands."""
                                
                                reason4 = """🟡 **Ladakh, Sikkim, Nagaland, Meghalaya, and Daman & Diu** all face geographical challenges that can hinder economic activity and trade.
                                                Their economies are primarily based on agriculture, tourism, and small-scale industries. 
                                                Internet penetration and digital infrastructure in these regions might be less developed compared to national averages.
                                                In some states like Nagaland and Meghalaya, informal trade and barter systems might still play a significant role in local economies, further contributing to lower recorded transaction volumes."""
                                reason5 =  """🟡 **Tripura** is the third smallest state in India by population, with around 3.67 million inhabitants. This translates to a smaller consumer base and fewer overall financial transactions compared to larger states. 
                                                The economy primarily relies on agriculture, bamboo and rubber plantations, with limited industrial activity and large-scale businesses.
                                                Cash remains the preferred mode of payment for many in Tripura, especially in rural areas. """
                                
                                def stream_data():
                                    for word in reason.split():
                                        yield word + " "
                                        time.sleep(0.02)

                                def stream_data1():
                                    for word in reason2.split():
                                        yield word + " "
                                        time.sleep(0.02)

                                def stream_data2():
                                    for word in reason3.split():
                                        yield word + " "
                                        time.sleep(0.02)                               

                                def stream_data3():
                                    for word in reason4.split():
                                        yield word + " "
                                        time.sleep(0.02)  

                                def stream_data4():
                                    for word in reason5.split():
                                        yield word + " "
                                        time.sleep(0.02)  
                                    
                                col1, col2 = st.columns(2)
                                top_10_states = agg_trans_data.groupby(["State"], as_index=False).Amount.sum().sort_values(by="Amount").head(10)
                                formated_amount_10 = [Convert.rupees(amount) for amount in top_10_states['Amount']]
                                top_10_states.State = top_10_states.State.replace("Andaman & Nicobar Islands","Andaman & Nicobar")
                                top_10_states.State = top_10_states.State.replace("Dadra & Nagar Haveli & Daman & Diu","DNHDD")
                                
                                with col1:
                                    fig = px.bar(top_10_states, 
                                                x="State", 
                                                y="Amount", 
                                                color = "State",
                                                color_continuous_scale=px.colors.qualitative.Alphabet,
                                                text = formated_amount_10,title = "Transaction Amount")
                                    fig.update_layout(xaxis=dict(title='State'), yaxis=dict(title="Amount"))
                                    fig.update_traces(hovertemplate="State: %{x}<br>Amount: %{text}",textposition='outside')
                                    st.plotly_chart(fig,use_container_width=True)
                                    st.dataframe(top_10_states,width=500, height=400, hide_index= True)
                                
                                with col2:
                                    a = agg_trans_data.groupby(["State"], as_index=False).Amount.sum().sort_values(by="Amount").head(10)
                                    filter = list(a.State.unique())
                                    top_10_states = agg_trans_data.loc[agg_trans_data.State.isin(filter)].groupby(["State"], as_index=False).Trans_Count.sum().sort_values(by="Trans_Count").head(10)
                                    top_10_states.State = top_10_states.State.replace("Andaman & Nicobar Islands","Andaman & Nicobar")
                                    top_10_states.State = top_10_states.State.replace("Dadra & Nagar Haveli & Daman & Diu","DNHDD")
                                    formated_amount_2 = [Convert.rupees(amount) for amount in top_10_states['Trans_Count']]
                                    fig = px.bar(top_10_states, 
                                                x="State", 
                                                y="Trans_Count", 
                                                color = "State",
                                                color_continuous_scale=px.colors.qualitative.Alphabet,
                                                text = formated_amount_2,title = "Transaction Count")
                                    fig.update_layout(xaxis=dict(title='State'), yaxis=dict(title="Transaction Count"))
                                    fig.update_traces(hovertemplate="State: %{x}<br>Transaction Count: %{text}",textposition='outside')
                                    st.plotly_chart(fig,use_container_width=True)
                                    st.dataframe(top_10_states,width=500, height=400, hide_index= True)
                                st.write_stream(stream_data)
                                st.write_stream(stream_data1)
                                st.write_stream(stream_data2)
                                st.write_stream(stream_data3)
                                st.write_stream(stream_data4)

                            low_10_states() 

                        if year_wise__low_perf_state_amount_over_time:
                            def low_10_states_on_year():
                                selected_year = st.select_slider("Select Year", sorted(agg_trans_data['Year'].unique()))
                                col3, col4 = st.columns(2,gap="medium")                               
                                top_10_states = agg_trans_data.loc[agg_trans_data.Year == selected_year].groupby(["State"], as_index=False).Amount.sum().sort_values(by="Amount").head(10)
                                
                                with col3: 
                                    top_10_states = agg_trans_data.loc[agg_trans_data.Year == selected_year].groupby(["State"], as_index=False).Amount.sum().sort_values(by="Amount").head(10)
                                    formated_amount_10 = [Convert.rupees(amount) for amount in top_10_states['Amount']]
                                    top_10_states.State = top_10_states.State.replace("Andaman & Nicobar Islands","Andaman & Nicobar")
                                    top_10_states.State = top_10_states.State.replace("Dadra & Nagar Haveli & Daman & Diu","DNHDD")
                                    if selected_year:
                                        fig = px.bar(top_10_states, 
                                                    x="State", 
                                                    y="Amount", 
                                                    color = "State",
                                                    color_continuous_scale=px.colors.cyclical.Twilight,
                                                    text = formated_amount_10,title = "Transaction Amount")
                                        fig.update_layout(xaxis=dict(title='State'), yaxis=dict(title="Amount"))
                                        fig.update_traces(hovertemplate="State: %{x}<br>Amount: %{text}")
                                        fig.update_traces(textposition='outside')
                                        st.plotly_chart(fig,use_container_width=True)
                                        st.dataframe(top_10_states,width=500, height=400, hide_index= True)

                                with col4:
                                    if selected_year:
                                        a = agg_trans_data.loc[agg_trans_data.Year == selected_year].groupby(["State"], as_index=False).Amount.sum().sort_values(by="Amount").head(10)
                                        filter = list(a.State.unique())
                                        top_10_states = agg_trans_data.loc[(agg_trans_data.Year == selected_year)&(agg_trans_data.State.isin(filter))].groupby(["State"], as_index=False).Trans_Count.sum().sort_values(by="Trans_Count").head(10)
                                        top_10_states.State = top_10_states.State.replace("Andaman & Nicobar Islands","Andaman & Nicobar")
                                        top_10_states.State = top_10_states.State.replace("Dadra & Nagar Haveli & Daman & Diu","DNHDD")
                                        formated_amount_10 = [Convert.rupees(amount) for amount in top_10_states['Trans_Count']]
                                        fig = px.bar(top_10_states, 
                                                    x="State", 
                                                    y="Trans_Count", 
                                                    color = "State",
                                                    color_continuous_scale=px.colors.qualitative.Alphabet,
                                                    text = formated_amount_10,title = "Transaction Count")
                                        fig.update_layout(xaxis=dict(title='State'), yaxis=dict(title="Transaction Count"))
                                        fig.update_traces(hovertemplate="State: %{x}<br>Transaction Count: %{text}")
                                        fig.update_traces(textposition='outside')
                                        st.plotly_chart(fig,use_container_width=True)
                                        st.dataframe(top_10_states, width=500, height=400,hide_index= True)
                                
                            low_10_states_on_year()              

                 
                if selected_query:
                    if selected_query == top_queries[2]:
                        year_wise_high_perf_amount_avg_over_time= st.toggle('Year-Wise')
                        if not year_wise_high_perf_amount_avg_over_time:
                            def mean_trans_value_10_states():
                                col1, col2 = st.columns(2,gap="medium")  
                                with col1:     
                                    avg_trans_value_top_10_states = agg_trans_data.groupby(["State"],as_index= False).Amount.mean().sort_values(by= "Amount", ascending = False).iloc[0:11]
                                    formated_amount_10 = [Convert.rupees(amount) for amount in avg_trans_value_top_10_states['Amount']]
                                    
                                    fig = px.bar(avg_trans_value_top_10_states, 
                                                x="State", 
                                                y="Amount", 
                                                color = "State",
                                                color_continuous_scale=px.colors.qualitative.Alphabet,
                                                text = formated_amount_10,title = "Average Transaction Amount")
                                    fig.update_layout(xaxis=dict(title='State'), yaxis=dict(title="Average  Amount"))
                                    fig.update_traces(hovertemplate="State: %{x}<br>Average Amount: %{text}")
                                    fig.update_traces(textposition='outside')
                                    st.plotly_chart(fig, use_container_width=True)
                                    st.dataframe(avg_trans_value_top_10_states,width=500, height=400, hide_index= True)

                                with col2:  
                                    a = agg_trans_data.groupby(["State"],as_index= False).Amount.mean().sort_values(by= "Amount", ascending = False).iloc[0:11]
                                    filter = list(a.State.unique())                                       
                                    avg_trans_value_top_10_states = agg_trans_data.loc[agg_trans_data.State.isin(filter)].groupby(["State"],as_index= False).Trans_Count.mean().sort_values(by= "Trans_Count", ascending = False).iloc[0:11]
                                    formated_amount_10 = [Convert.rupees(amount) for amount in avg_trans_value_top_10_states['Trans_Count']]
                                    
                                    fig = px.bar(avg_trans_value_top_10_states, 
                                                x="State", 
                                                y="Trans_Count", 
                                                color = "State",
                                                color_continuous_scale=px.colors.qualitative.Alphabet,
                                                text = formated_amount_10,title = "Average Transaction Count")
                                    fig.update_layout(xaxis=dict(title='State'), yaxis=dict(title="Average Transaction Count"))
                                    fig.update_traces(hovertemplate="State: %{x}<br>Average Transaction Count: %{text}")
                                    fig.update_traces(textposition='outside')
                                    st.plotly_chart(fig, use_container_width=True)
                                    st.dataframe(avg_trans_value_top_10_states, width=500, height=400,hide_index= True)                                    


                            mean_trans_value_10_states()    
                        
                        if year_wise_high_perf_amount_avg_over_time:                             
                            def mean_trans_value_10_states():
                                selected_year = st.select_slider("Select Year", sorted(agg_trans_data['Year'].unique()))       
                                avg_trans_value_top_10_states = agg_trans_data.loc[agg_trans_data.Year == selected_year].groupby(["State"],as_index= False).Amount.mean().sort_values(by= "Amount", ascending = False).head(10)
                                formated_amount_10 = [Convert.rupees(amount) for amount in avg_trans_value_top_10_states['Amount']]
                                
                                col1, col2 = st.columns(2,gap="medium")  
                                if selected_year:
                                    with col1:
                                        fig = px.bar(avg_trans_value_top_10_states, 
                                                    x="State", 
                                                    y="Amount", 
                                                    color = "State",
                                                    color_continuous_scale=px.colors.qualitative.Alphabet,
                                                    text = formated_amount_10,title = "Average Transaction Amount")
                                        fig.update_layout(xaxis=dict(title='State'), yaxis=dict(title="Average  Amount"))
                                        fig.update_traces(hovertemplate="State: %{x}<br>Average Amount: %{text}")
                                        fig.update_traces(textposition='outside')
                                        st.plotly_chart(fig, use_container_width=True)
                                        st.dataframe(avg_trans_value_top_10_states,width=500, height=400, hide_index= True)

                                if selected_year:
                                    with col2:
                                        a = agg_trans_data.loc[agg_trans_data.Year == selected_year].groupby(["State"],as_index= False).Amount.mean().sort_values(by= "Amount", ascending = False).head(10)
                                        filter = list(a.State.unique())
                                        avg_trans_count_top_10_states = agg_trans_data.loc[(agg_trans_data.Year == selected_year)&(agg_trans_data.State.isin(filter))].groupby(["State"],as_index= False).Trans_Count.mean().sort_values(by= "Trans_Count", ascending = False).head(10)
                                        formated_amount_c = [Convert.rupees(amount) for amount in avg_trans_count_top_10_states['Trans_Count']]
                                        fig = px.bar(avg_trans_count_top_10_states, 
                                                    x="State", 
                                                    y="Trans_Count", 
                                                    color = "State",
                                                    color_continuous_scale=px.colors.qualitative.Alphabet,
                                                    text = formated_amount_c,title = "Average Transaction Count")
                                        fig.update_layout(xaxis=dict(title='State'), yaxis=dict(title="Average Transaction Count"))
                                        fig.update_traces(hovertemplate="State: %{x}<br>Transaction Count: %{text}")
                                        fig.update_traces(textposition='outside')
                                        st.plotly_chart(fig, use_container_width=True)
                                        st.dataframe(avg_trans_count_top_10_states,width=500, height=400, hide_index= True)
                            mean_trans_value_10_states()    


                if selected_query:
                    if selected_query == top_queries[3]:
                        year_wise_dist_high_perf_amount_over_time = st.toggle('Year-Wise') 
                        if year_wise_dist_high_perf_amount_over_time:
                            def yearly_top_10_dist_on_year():                                                                         
                                selected_year = st.select_slider("Select Year", sorted(map_trans_data['Year'].unique()))
                                top_10_dis_df = map_trans_data.loc[map_trans_data.Year == selected_year].groupby("District",as_index= False).Amount.sum().sort_values(by="Amount",ascending = False).head(10)                            
                                top_10_dis_df["District"] = top_10_dis_df["District"].replace("Central","Delhi Central")
                                formated_amount_10_dis = [Convert.rupees(amount) for amount in top_10_dis_df['Amount']]
                                col1, col2 = st.columns(2,gap="medium")  
                                with col1:
                                    
                                    fig = px.bar(top_10_dis_df, 
                                                x="District", 
                                                y="Amount", 
                                                color = "District",
                                                color_continuous_scale=px.colors.diverging.Spectral_r,
                                                text = formated_amount_10_dis,title = "Transaction Amount")
                                    fig.update_layout(xaxis=dict(title='Districts'), yaxis=dict(title="Total Amount"))
                                    fig.update_traces(hovertemplate="Districts: %{x}<br>Amount: %{text}")
                                    fig.update_traces(textposition='outside')
                                    st.plotly_chart(fig, use_container_width=True)                                                                                                                                                        
                                    st.dataframe(top_10_dis_df,width=500, height=400, hide_index= True)

                                with col2:
                                    a = map_trans_data.loc[map_trans_data.Year == selected_year].groupby("District",as_index= False).Amount.sum().sort_values(by="Amount",ascending = False).head(10) 
                                    filter = list(a.District.unique())  
                                       
            
                                    top_10_dis_df = map_trans_data.loc[(map_trans_data.Year == selected_year)&(map_trans_data.District.isin(filter))].groupby("District",as_index= False).Trans_Count.sum().sort_values(by="Trans_Count",ascending = False).head(10)                            
                                    top_10_dis_df["District"] = top_10_dis_df["District"].replace("Central","Delhi Central")
                                    formated_amount_10_dis = [Convert.rupees(amount) for amount in top_10_dis_df['Trans_Count']]                                    
                                    fig = px.bar(top_10_dis_df, 
                                                x="District", 
                                                y="Trans_Count", 
                                                color = "District",
                                                color_continuous_scale=px.colors.cyclical.Twilight,
                                                text = formated_amount_10_dis,title = "Transaction Count")
                                    fig.update_layout(xaxis=dict(title='Districts'), yaxis=dict(title="Transaction Count"))
                                    fig.update_traces(hovertemplate="Districts: %{x}<br>Transaction Count: %{text}")
                                    fig.update_traces(textposition='outside')
                                    st.plotly_chart(fig, use_container_width=True)                                                                                                                                                        
                                    st.dataframe(top_10_dis_df,width=500, height=400, hide_index= True)                                    
                            yearly_top_10_dist_on_year()                 


                        else:     
                            def top_10_dist_on_year():
                                reason1 = """🟡 **Bengaluru** is known as the Silicon Valley of India. It houses numerous tech companies and startups with a large young, tech-savvy population. This demographic often has higher disposable income and is more likely to adopt digital payment methods like PhonePe."""
                                reason2 = """
                                🟡**Hyderabad and Rangareddy** together form a bustling metropolitan area, naturally driving up transaction volumes. Telangana's government initiatives, like the "Telangana Digital Transactions Mission" and "Har Ghar Digital Payment," have encouraged PhonePe adoption. Moreover, the region's young and tech-savvy population, especially in Hyderabad, contributes to its high digital transaction rates. **Medchal Malkajgiri**, within this area, leads in PhonePe transactions due to its urbanization, strong IT and business presence, and proactive government support for digital payments. 
                                """
                                reason3 = """🟡 **Pune** is a major IT hub with a large young population and a growing middle class. It has a large student population, and students are typically early adopters of digital payments for everyday needs."""  
                                reason4 = """🟡 **Jaipur** is a renowned center for gemstones and jewelry. The city is renowned worldwide for its gemstone cutting, polishing, and trading activities. These transactions often involve larger sums of money.
                                        Jaipur is a major tourist destination in India. Tourists often rely on digital wallets for convenience and security. This high tourist volume can significantly contribute to transaction volume and potentially translate to higher overall transaction value on PhonePe."""
                                reason5 = """🟡 **Visakhapatnam** (Vizag) serves as a major port city and industrial hub, facilitating extensive trade and commerce activities. The presence of industries, shipping companies, and commercial enterprises results in a large volume of financial transactions, contributing to the overall transaction amount.  """
                                reason6 = """🟡 **Patna** is one of the largest and most populous cities in India, with a dense urban population. The high population density naturally leads to a higher volume of transactions, including digital transactions."""
                                reason7 = """🟡 **Krishna** is known for agriculture. If there's a trend towards digital transactions within the agricultural sector, it could contribute to a high transaction volume on PhonePe."""
                                reason8 = """🟡 Delhi Central, a bustling commercial hub, teems with corporate offices, markets, and shopping centers, fostering extensive economic activity and driving a surge in transactions, including digital payments.
                                                Delhi Central is one of the busiest railway stations in India. This translates to a large number of people constantly on the move and potentially using PhonePe for various small transactions."""
                                def dis_stream_data():
                                    for word in reason1.split():
                                        yield word + " "
                                        time.sleep(0.03)

                                def dis_stream_data1():
                                    for word in reason2.split():
                                        yield word + " "
                                        time.sleep(0.03)

                                def dis_stream_data2():
                                    for word in reason3.split():
                                        yield word + " "
                                        time.sleep(0.03)        

                                def dis_stream_data3():
                                    for word in reason4.split():
                                        yield word + " "
                                        time.sleep(0.03)          

                                def dis_stream_data4():
                                    for word in reason5.split():
                                        yield word + " "
                                        time.sleep(0.03)     

                                def dis_stream_data5():
                                    for word in reason6.split():
                                        yield word + " "
                                        time.sleep(0.03)  

                                def dis_stream_data6():
                                    for word in reason7.split():
                                        yield word + " "
                                        time.sleep(0.03)   

                                def dis_stream_data7():
                                    for word in reason8.split():
                                        yield word + " "
                                        time.sleep(0.03)                                                

                                
                                
                                top_10_dis_df = map_trans_data.groupby("District",as_index= False).Amount.sum().sort_values(by="Amount",ascending = False).head(10)                            
                                top_10_dis_df["District"] = top_10_dis_df["District"].replace("Central","Delhi Central")
                                formated_amount_10_dis = [Convert.rupees(amount) for amount in top_10_dis_df['Amount']]
                                col1, col2 = st.columns(2,gap="medium")  
                                with col1:
                                    fig = px.bar(top_10_dis_df, 
                                                x="District", 
                                                y="Amount", 
                                                color = "District",
                                                color_continuous_scale=px.colors.cyclical.Twilight,
                                                text = formated_amount_10_dis,title = "Transaction Amount")
                                    fig.update_layout(xaxis=dict(title='Districts'), yaxis=dict(title="Total Amount"))
                                    fig.update_traces(hovertemplate="Districts: %{x}<br>Amount: %{text}")
                                    fig.update_traces(textposition='outside')
                                    st.plotly_chart(fig, use_container_width=True)                                                                                                                                                       
                                    st.dataframe(top_10_dis_df,width=500, height=400, hide_index= True)

                                with col2:
                                    a = map_trans_data.groupby("District",as_index= False).Amount.sum().sort_values(by="Amount",ascending = False).head(10)                            
                                    filter = list(a.District.unique())
                        
                                    top_10_dis_df = map_trans_data.loc[map_trans_data.District.isin(filter)].groupby("District",as_index= False).Trans_Count.sum().sort_values(by="Trans_Count",ascending = False).head(10)                            
                                    top_10_dis_df["District"] = top_10_dis_df["District"].replace("Central","Delhi Central")      
                                    formated_amount_10_dis = [Convert.rupees(amount) for amount in top_10_dis_df['Trans_Count']]                             
                                    fig = px.bar(top_10_dis_df, 
                                                x="District", 
                                                y="Trans_Count", 
                                                color = "District",
                                                color_continuous_scale=px.colors.cyclical.Twilight,
                                                text = formated_amount_10_dis,title = "Transaction Count")
                                    fig.update_layout(xaxis=dict(title='Districts'), yaxis=dict(title="Total Amount"))
                                    fig.update_traces(hovertemplate="Districts: %{x}<br>Amount: %{text}")
                                    fig.update_traces(textposition='outside')
                                    st.plotly_chart(fig, use_container_width=True)                                                                                                                                                       
                                    st.dataframe(top_10_dis_df,width=500, height=400, hide_index= True)    
                                st.write_stream(dis_stream_data)
                                st.write_stream(dis_stream_data1)
                                st.write_stream(dis_stream_data2)
                                st.write_stream(dis_stream_data3)
                                st.write_stream(dis_stream_data4)
                                st.write_stream(dis_stream_data5)    
                                st.write_stream(dis_stream_data6)
                                st.write_stream(dis_stream_data7)     

                            top_10_dist_on_year()                 



                if selected_query:
                    if selected_query == top_queries[4]:                         
                        def Quar_wise_trans_dis():
                            st.info("You selected: Quarter-wise transaction distribution for specific state")
                              
                            selected_state = st.selectbox("Select State", sorted(agg_trans_data['State'].unique()),index= None)
                            selected_year = st.selectbox("Select Year", sorted(agg_trans_data['Year'].unique()),index= None)
                            if selected_state and selected_year:
                                st.success(f"Showing insights for Year: {selected_year} and State: {selected_state}")
                            col1, col2 = st.columns(2,gap="medium")
                            
                            with col1:
                                
                                Q_wise_trans_dis = agg_trans_data.loc[(agg_trans_data.State == selected_state )&(agg_trans_data.Year == selected_year)].groupby(["Quarter"],as_index = False).Amount.sum()
                
                                if selected_state and selected_year:
                                    
                                    fig_Q_wise_trans_dis = px.bar(Q_wise_trans_dis, x = "Quarter", 
                                                                y = "Amount",
                                                                title=f'Distribution Transactions Value in {selected_state} ({selected_year})', 
                                                                text = [Convert.rupees(amount) for amount in Q_wise_trans_dis['Amount']],
                                                                color='Amount',
                                                                color_continuous_scale = px.colors.diverging.Spectral_r,
                                                                barmode="group")
                                    fig_Q_wise_trans_dis.update_traces(hovertemplate="Quarter: %{x}<br>Amount: %{text}")
                                    fig_Q_wise_trans_dis.update_layout(legend_title_text='Transaction Amount')
                                    fig_Q_wise_trans_dis.update_layout(xaxis=dict(title='Quarter'), yaxis=dict(title="Total Amount"))
                                    fig_Q_wise_trans_dis.update_traces(textposition='outside')
                                    fig_Q_wise_trans_dis.update_yaxes(type='log', dtick=1)
                                    fig_Q_wise_trans_dis.update_xaxes(title_text='Quarter', tickvals=[1, 2, 3, 4], ticktext=['Q1 (Jan,Feb,Mar)', 'Q2(Apr,May,Jun)', 'Q3(Jul,Aug,Sep)', 'Q4(Oct,Nov,Dec)'])
                                    st.plotly_chart(fig_Q_wise_trans_dis, use_container_width=True)


                                else:
                                    st.warning("Please select all the above options")

                            with col2:
                                Q_wise_trans_dis = agg_trans_data.loc[(agg_trans_data.State == selected_state )&(agg_trans_data.Year == selected_year)].groupby(["Quarter"],as_index = False).Trans_Count.sum()
                
                                if selected_state and selected_year:
                                    fig_Q_wise_trans_dis = px.bar(Q_wise_trans_dis, x = "Quarter", 
                                                                y = "Trans_Count",
                                                                title=f'Distribution Transactions Count in {selected_state} ({selected_year})', 
                                                                text = [Convert.rupees(amount) for amount in Q_wise_trans_dis['Trans_Count']],
                                                                color='Trans_Count',
                                                                color_continuous_scale = px.colors.diverging.Spectral_r,
                                                                barmode="group")
                                    fig_Q_wise_trans_dis.update_layout(legend_title_text='Transaction Count')
                                    fig_Q_wise_trans_dis.update_traces(hovertemplate="Quarter: %{x}<br>Transaction Count: %{text}")
                                    fig_Q_wise_trans_dis.update_layout(xaxis=dict(title='Quarter'), yaxis=dict(title="Total Transaction Count"))
                                    fig_Q_wise_trans_dis.update_traces(textposition='outside')
                                    fig_Q_wise_trans_dis.update_yaxes(type='log', dtick=1)
                                    fig_Q_wise_trans_dis.update_xaxes(title_text='Quarter', tickvals=[1, 2, 3, 4], ticktext=['Q1 (Jan,Feb,Mar)', 'Q2(Apr,May,Jun)', 'Q3(Jul,Aug,Sep)', 'Q4(Oct,Nov,Dec)'])
                                    st.plotly_chart(fig_Q_wise_trans_dis, use_container_width=True)
    
                               
                            if selected_state and selected_year:
                                if selected_state != "Andaman & Nicobar Islands" and selected_state != "Lakshadweep" and selected_state != "Goa" and selected_year != 2020 and selected_year != 2021:
                                    st.write('🟡 The increase in transactions in October, November, and December is due to people spending more money on festivals like Diwali, Dussehra, Eid, and Christmas, as well as on weddings and towards the end of the year.')
                                    st.write('🟡 July to December corresponds to the harvest season in many parts of India. Increased agricultural income during this time may boost rural spending, leading to higher transactions.')
                                    st.write('🟡 Many Indian companies follow a fiscal year that ends in March, which means the period leading up to December often sees increased corporate spending as businesses aim to utilize their budgets before the year-end.')
                                
                                if selected_year == 2020 or selected_year == 2021:
                                    st.write('🟡 The COVID-19 pandemic and associated lockdown periods in 2020 and 2021, economic activity slowed down considerably due to restrictions on movement, closure of businesses, and disruptions in supply chains.')

                                elif selected_state == "Andaman & Nicobar Islands" :
                                    st.write("""🟡 **Q4 (Oct-Dec):**
                                                    - Peak tourist season which typically falls between November and May contributes to higher transaction volumes.
                                                    - Diwali festivities could also increase spending.""")
                                    
                                    st.write("""🟡  **Q1 (Jan-Mar):**  - Might experience a decrease in spending following the holiday season in December, contributing to lower transaction amounts.""")

                                elif selected_state == "Goa" and selected_year == 2022 or selected_year == 2023 :      
                                    st.write("""🟡 **Lower transaction amounts in Q3 (Jul-Sep):**
                                                - Likely due to monsoon season (June to September), reducing tourism activity.""")
                                    st.write("""🟡 **Higher transaction amounts generally in Q4 and Q2:**
                                                    - Q4 (Oct-Dec): Increased tourism during this period, possibly due to festivals like Diwali.
                                                    - Q2 (Apr-Jun): Peak tourist activity season.""")
                                    
                                elif selected_state == "Goa" and selected_year == 2018 or selected_year == 2019 :      
                                    st.write("""🟡 **Higher transaction amounts generally in Q4(Oct-Dec):**
                                                    - Increased tourism during this period, possibly due to festivals like Diwali.""")                                


                        Quar_wise_trans_dis()                         

            trans_top_insights()


    if insights_type == "**Users**":

        users_insights_container =  st.container(border = True)
        users_insights_container.subheader("Insights Types")
        users_insights_filter_type = users_insights_container.radio("Select Type", ["Geo Visualization","Top Insights"],key="user_insights", horizontal=True)
        
        if users_insights_filter_type == "Geo Visualization":


            def users_geo():
       
                def india_users_geojson():
                    india = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                    return india  
                              
                user_geo_queries = ["Total Users",
                                   "District Wise Total Users"]
                st.title(":violet[User Count Distribution Across States]")      
                user_geo_selected_query = st.selectbox("Select a Query", user_geo_queries,index= 0)  
            
                if user_geo_selected_query ==  user_geo_queries[0]:
                    user_count_on_years = st.toggle('Year-Wise')
                    if not user_count_on_years:
                        def total_map_trans_geo():
                            df = map_user_data.groupby(["State"],as_index= False).agg({"Registered_Users":["sum","mean"]})
                            df['State'] = df['State'].replace('Andaman And Nicobar Islands', 'Andaman & Nicobar')
                            df.columns = ['State', 'Total_User_Count', 'Average_User_Count']
                            formated_Total_user_count = [Convert.rupees(amount) for amount in df['Total_User_Count']]
                            formated_Average_user_count =  [Convert.rupees(amount) for amount in df['Average_User_Count']]
                            hover_template = (
                                                "<b>%{location}</b><br>"
                                                "Total Users: %{customdata[0]}<br>"
                                                "Average Yearly Users: %{customdata[1]}<br>"
                                            )
                            
                            customdata = list(zip(formated_Total_user_count, formated_Average_user_count))

                            fig = px.choropleth_mapbox(
                                df,
                                geojson= india_users_geojson(),
                                locations='State',
                                mapbox_style="carto-positron",
                                zoom=3.5,
                                center={"lat": 21.7679, "lon": 78.8718}, 
                                # opacity=0.5,
                                featureidkey='properties.ST_NM', 
                                color='Total_User_Count', 
                                color_continuous_scale= px.colors.sequential.dense_r
                                )
                            fig.update_geos(fitbounds="locations", visible=False)
                            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                            fig.update_layout(geo_bgcolor="#210D38")
                            fig.update_traces(hovertemplate=hover_template, customdata=customdata)
                            fig.update_layout(height=600)
                            fig.update_coloraxes(colorbar_title_text='Total User Count')
                            st.subheader("Showing Total User Count: Sum of All Years")
                            st.plotly_chart(fig,use_container_width = True)
                        total_map_trans_geo()
                    
                    if user_count_on_years:
                        def year_wise_map_users_geo():
                            
                            selected_year = st.select_slider("Select Year", sorted(map_user_data['Year'].unique()))
                            df = map_user_data.loc[map_user_data.Year == selected_year].groupby(["State"],as_index= False).agg({"Registered_Users":["sum","mean"]})
                            df['State'] = df['State'].replace('Andaman And Nicobar Islands', 'Andaman & Nicobar')
                            df.columns = ['State', 'Total_User_Count', 'Average_User_Count']
                            formated_Total_user_count = [Convert.rupees(amount) for amount in df['Total_User_Count']]
                            formated_Average_user_count =  [Convert.rupees(amount) for amount in df['Average_User_Count']]
                            hover_template = (
                                                "<b>%{location}</b><br>"
                                                "Total Users: %{customdata[0]}<br>"
                                                "Average Yearly Users: %{customdata[1]}<br>"
                                            )
                            
                            customdata = list(zip(formated_Total_user_count, formated_Average_user_count))
                            custom_color_scale = [
                                [0.0, '#440f60'],  # Dark Purple
                                [0.2, '#5e257a'],  # Deep Purple
                                [0.4, '#7b3a95'],  # Rich Purple
                                [0.6, '#9360a7'],  # Lavender
                                [0.8, '#af82b9'],  # Soft Purple
                                [1.0, '#c7b8db']   # Pale Purple
                            ]


                            fig = px.choropleth_mapbox(
                                df,
                                geojson= india_users_geojson(),
                                locations='State',
                                mapbox_style="carto-positron",
                                zoom=3.5,
                                center={"lat": 21.7679, "lon": 78.8718}, 
                                # opacity=0.5,
                                featureidkey='properties.ST_NM', 
                                color='Total_User_Count', 
                                color_continuous_scale= px.colors.sequential.dense_r
                                )
                            fig.update_geos(fitbounds="locations", visible=False)
                            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                            fig.update_layout(geo_bgcolor="#210D38")
                            fig.update_traces(hovertemplate=hover_template, customdata=customdata)
                            fig.update_coloraxes(colorbar_title_text='Total User Count')
                            fig.update_layout(height=600)
                            st.subheader(f"Showing User Count for the Year: {selected_year}")
                            st.plotly_chart(fig,use_container_width = True)          
                        year_wise_map_users_geo()
                

                if user_geo_selected_query == user_geo_queries[1]:  
                    dist_user_count_on_years = st.toggle('Year-Wise')
                    if not dist_user_count_on_years:
                        def district_wise_user_total():
                            map_user_data['State'] = map_user_data['State'].replace('Andaman And Nicobar Islands', 'Andaman & Nicobar')
                            selected_state = st.selectbox("Select State", sorted([state for state in map_user_data['State'].unique() if state != "Dadra And Nagar Haveli And Daman And Diu"]),index = 29)
                            state_coordinates = state_coordinate()
                            zoom = state_zoom()
                            state_geojson_links = state_geojson_link()
                            if selected_state in state_geojson_links:
                                geojson_link = state_geojson_links[selected_state]
                                df = map_user_data.loc[map_user_data['State'] == selected_state].groupby("District", as_index = False).agg({"Registered_Users":["sum","mean"]})
                                df.columns = ['District', 'Total_User_Count', 'Average_User_Count']
                                formated_Total_user_count = [Convert.rupees(amount) for amount in df['Total_User_Count']]
                                formated_Average_user_count =  [Convert.rupees(amount) for amount in df['Average_User_Count']]
                                hover_template = (
                                                    "<b>%{location}</b><br>"
                                                    "Total Users: %{customdata[0]}<br>"
                                                    "Average Yearly Users: %{customdata[1]}<br>"
                                                )
                                customdata = list(zip(formated_Total_user_count, formated_Average_user_count))
                            
                                
                                center_coordinates = state_coordinates[selected_state]
                                depth = zoom[selected_state]
                                fig = px.choropleth_mapbox(
                                    df,
                                    geojson=geojson_link,
                                    locations='District',
                                    mapbox_style="carto-positron",
                                    zoom=depth,
                                    center=center_coordinates, 
                                    
                                    featureidkey='properties.dtname', 
                                    color='Total_User_Count', 
                                    color_continuous_scale=px.colors.sequential.Viridis)
                                fig.update_geos(fitbounds="locations", visible=False)
                                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                                fig.update_layout(geo_bgcolor="#210D38")
                                fig.update_traces(hovertemplate=hover_template, customdata=customdata)
                                fig.update_coloraxes(colorbar_title_text='Total User Count')
                                st.subheader(f"Showing Users Count for the Districts of {selected_state}")
                                st.plotly_chart(fig,use_container_width = True)          
                        district_wise_user_total()

                    if dist_user_count_on_years:
                        def yearly_district_wise_user_total():
                            map_user_data['State'] = map_user_data['State'].replace('Andaman And Nicobar Islands', 'Andaman & Nicobar')
                            selected_year = st.select_slider("Select Year", sorted(map_user_data['Year'].unique()))
                            selected_state = st.selectbox("Select State", sorted([state for state in map_user_data['State'].unique() if state != "Dadra And Nagar Haveli And Daman And Diu"]),index = 29)
                            state_coordinates = state_coordinate()
                            zoom = state_zoom()
                            state_geojson_links = state_geojson_link()
                            if selected_state in state_geojson_links:
                                geojson_link = state_geojson_links[selected_state]
                                df = map_user_data.loc[(map_user_data['State'] == selected_state)&(map_user_data['Year'] == selected_year)].groupby("District", as_index = False).agg({"Registered_Users":["sum","mean"]})
                                df.columns = ['District', 'Total_User_Count', 'Average_User_Count']
                                formated_Total_user_count = [Convert.rupees(amount) for amount in df['Total_User_Count']]
                                formated_Average_user_count =  [Convert.rupees(amount) for amount in df['Average_User_Count']]
                                hover_template = (
                                                    "<b>%{location}</b><br>"
                                                    "Total Users: %{customdata[0]}<br>"
                                                    "Average Yearly Users: %{customdata[1]}<br>"
                                                )
                                customdata = list(zip(formated_Total_user_count, formated_Average_user_count))
                            
                                
                                center_coordinates = state_coordinates[selected_state]
                                depth = zoom[selected_state]
                                fig = px.choropleth_mapbox(
                                    df,
                                    geojson=geojson_link,
                                    locations='District',
                                    mapbox_style="carto-positron",
                                    zoom=depth,
                                    center=center_coordinates, 
                                    
                                    featureidkey='properties.dtname', 
                                    color='Total_User_Count', 
                                    color_continuous_scale=px.colors.sequential.Viridis)
                                fig.update_geos(fitbounds="locations", visible=False)
                                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                                fig.update_coloraxes(colorbar_title_text='Total User Count')
                                fig.update_layout(geo_bgcolor="#210D38")
                                fig.update_traces(hovertemplate=hover_template, customdata=customdata)
                                st.subheader(f"Showing Users Count for the Districts of {selected_state}")
                                st.plotly_chart(fig,use_container_width = True)   
                        yearly_district_wise_user_total()

            users_geo()

        if users_insights_filter_type == "Top Insights":                

            def user_top_insights():           
                top_queries = ["Top 10 States with Highest Users",
                                "Top 10 States with Lowest Users",
                                "Top 10 District With Highest Users",
                                "Quarter-wise User distribution for specific state"]
                        
                selected_query = st.selectbox("Select a Query", top_queries,index= None)  


                
                if selected_query:
                    if selected_query == top_queries[0]:
                        top_10_user_states_on_year = st.toggle('Year-Wise') 
                        if not top_10_user_states_on_year:
                            def top_10_user_states():
                                reason3 = """
                                🟡 According to PhonePe, 44% of **Telangana**'s population uses digital payments, which is the highest in India.
                                The Telangana government has actively promoted digital payments through various initiatives like **"Telangana Digital Transactions Mission"** and **"Har Ghar Digital Payment"** campaign. This, along with subsidies and incentives, has encouraged citizens to adopt PhonePe and other digital wallets.
                                Telangana boasts a young and tech-savvy population, particularly in Hyderabad, the IT hub of India. 
                                """
                                reason2 = """🟡 **Karnataka** has a strong tech-savvy population and a well-developed digital infrastructure. This makes it more receptive to digital payments.
                                            Karnataka has a high concentration of urban areas with a growing middle class. This segment is more likely to use digital payment platforms for various transactions."""
                                reason = """🟡 **Maharashtra** boasts the largest population in India, and a significant portion is tech-savvy and open to adopting digital payments. Particularly in Mumbai and Pune, where digital 
                                        payments are more prevalent due to faster internet connectivity and a higher standard of living."""
                                
                                reason4 = """🟡 **Rajasthan, Andhra Pradesh, Tamil Nadu, Madhya Pradesh, Uttar Pradesh, Gujarat, and West Bengal** have some of the largest populations in India, which means that there are more people engaging in economic activity and making transactions. 
                                                These states have diversified economies with a mix of agriculture, industry, and services. 
                                                These states have relatively well-developed infrastructure, including roads, railways, and airports. This makes it easier for goods and services to be transported and for people to travel, which can lead to more economic activity and transactions.
                                                These states have a growing middle class, which means that there are more people with disposable income who are able to make purchases and engage in economic activity."""
                                def stream_data():
                                    for word in reason.split():
                                        yield word + " "
                                        time.sleep(0.03)

                                def stream_data1():
                                    for word in reason3.split():
                                        yield word + " "
                                        time.sleep(0.03)

                                def stream_data2():
                                    for word in reason2.split():
                                        yield word + " "
                                        time.sleep(0.03)        

                                def stream_data3():
                                    for word in reason4.split():
                                        yield word + " "
                                        time.sleep(0.03)          

                                                            
                                def top_10_states_user(map_user_data):
                                    top_10_states = map_user_data.groupby(["State"], as_index=False).Registered_Users.sum().sort_values(by="Registered_Users", ascending=False).head(10)
                                    return top_10_states
                                
                                top_10_user_states = top_10_states_user(map_user_data)
                                formated_user_count = [Convert.rupees(amount) for amount in top_10_user_states['Registered_Users']]
                                
                                
                                fig = px.bar(top_10_user_states, 
                                            x="State", 
                                            y="Registered_Users",
                                            color = "State", 
                                            color_discrete_sequence=px.colors.qualitative.Bold,
                                            text =formated_user_count)
                                
                                fig.update_traces(hovertemplate="Users: %{text}",textposition='outside')  
                                fig.update_layout(xaxis=dict(title='State'), yaxis=dict(title="User Count")) 
                                st.plotly_chart(fig, use_container_width=True)
                                st.write_stream(stream_data)
                                st.write_stream(stream_data1)
                                st.write_stream(stream_data2)
                                st.write_stream(stream_data3)
                                st.dataframe(top_10_user_states, hide_index= True)
                            top_10_user_states()                

                        if top_10_user_states_on_year:      
                            def top_10_user_states_on_year():                                                           
                                def top_10_states_user(map_user_data):
                                    selected_year = st.select_slider("Select Year", sorted(map_user_data['Year'].unique()))
                                    top_10_states = map_user_data.loc[map_user_data.Year == selected_year].groupby(["State"], as_index=False).Registered_Users.sum().sort_values(by="Registered_Users", ascending=False).head(10)
                                    return top_10_states
                                
                                top_10_user_states = top_10_states_user(map_user_data)
                                formated_user_count = [Convert.rupees(amount) for amount in top_10_user_states['Registered_Users']]
                                
                                
                                fig = px.bar(top_10_user_states, 
                                            x="State", 
                                            y="Registered_Users",
                                            color = "State", 
                                            color_discrete_sequence=px.colors.qualitative.Bold,
                                            text =formated_user_count)
                                
                                fig.update_traces(hovertemplate="Users: %{text}",textposition='outside')  
                                fig.update_layout(xaxis=dict(title='State'), yaxis=dict(title="User Count")) 
                                st.plotly_chart(fig, use_container_width=True)
                                st.dataframe(top_10_user_states, hide_index= True)  
                            top_10_user_states_on_year()                


                if selected_query:
                    if selected_query == top_queries[1]:
                        low_10_user_states_yearly= st.toggle('Year-Wise')
                        if not low_10_user_states_yearly:
                            def low_10_user_states():
                                reason = """
                                🟡 **Lakshadweep** has the smallest population among all Indian states and UTs, with around 66,000 inhabitants.
                                The economy of Lakshadweep is primarily based on fishing and tourism, with limited industrial activity or large-scale businesses.  
                                """
                                reason2 = """🟡 **Mizoram**'s economy relies heavily on agriculture, with a large number of small and marginal farmers. This sector typically involves smaller transactions compared to industries like manufacturing or services."""
                                reason3 = """🟡 **Andaman and Nicobar** has the second-smallest population among Indian states and UTs, With a population of around 4.64 Lakhs. 
                                            The economy heavily relies on tourism and fisheries, with limited industrial activity or large-scale businesses. This restricts the generation and circulation of wealth within the islands."""
                                
                                reason4 = """🟡 **Ladakh, Sikkim, Nagaland, Meghalaya, and Daman & Diu** all face geographical challenges that can hinder economic activity and trade.
                                                Their economies are primarily based on agriculture, tourism, and small-scale industries. 
                                                Internet penetration and digital infrastructure in these regions might be less developed compared to national averages.
                                                In some states like Nagaland and Meghalaya, informal trade and barter systems might still play a significant role in local economies, further contributing to lower recorded transaction volumes."""
                                reason5 =  """🟡 **Tripura** is the third smallest state in India by population, with around 3.67 million inhabitants. This translates to a smaller consumer base and fewer overall financial transactions compared to larger states. 
                                                The economy primarily relies on agriculture, bamboo and rubber plantations, with limited industrial activity and large-scale businesses.
                                                Cash remains the preferred mode of payment for many in Tripura, especially in rural areas. """
                                
                                def stream_data():
                                    for word in reason.split():
                                        yield word + " "
                                        time.sleep(0.02)

                                def stream_data1():
                                    for word in reason2.split():
                                        yield word + " "
                                        time.sleep(0.02)

                                def stream_data2():
                                    for word in reason3.split():
                                        yield word + " "
                                        time.sleep(0.02)                               

                                def stream_data3():
                                    for word in reason4.split():
                                        yield word + " "
                                        time.sleep(0.02)  

                                def stream_data4():
                                    for word in reason5.split():
                                        yield word + " "
                                        time.sleep(0.02)  
                                    

                                def low_10_states_user(map_user_data):
                                    low_10_states = map_user_data.groupby(["State"], as_index=False).Registered_Users.sum().sort_values(by="Registered_Users", ascending= True).head(10)
                                    return low_10_states
                                
                                low_10_user_states = low_10_states_user(map_user_data)
                                formated_user_count = [Convert.rupees(amount) for amount in low_10_user_states['Registered_Users']]
                                
                                
                                fig = px.bar(low_10_user_states, 
                                            x="State", 
                                            y="Registered_Users",
                                            color = "State", 
                                            color_discrete_sequence=px.colors.qualitative.Bold,
                                            text=formated_user_count)

                                fig.update_layout(xaxis=dict(title='State'), yaxis=dict(title="User Count"))
                                fig.update_traces(hovertemplate="Users: %{text}",textposition='outside')                               
                                st.plotly_chart(fig, use_container_width=True)
                                st.write_stream(stream_data)
                                st.write_stream(stream_data1)
                                st.write_stream(stream_data2)
                                st.write_stream(stream_data3)
                                st.write_stream(stream_data4)
                                st.dataframe(low_10_user_states, hide_index= True)
                            low_10_user_states() 

                        if low_10_user_states_yearly:
                            def low_10_states_on_year():     
                                selected_year = st.select_slider("Select Year", sorted(map_user_data['Year'].unique()))
                                yearly_low_10_user_states =  map_user_data.loc[map_user_data.Year == selected_year].groupby(["State"], as_index=False).Registered_Users.sum().sort_values(by="Registered_Users", ascending= True).head(10)
                                formated_user_count = [Convert.rupees(amount) for amount in yearly_low_10_user_states['Registered_Users']]
                                                               
                                fig = px.bar(yearly_low_10_user_states, 
                                            x="State", 
                                            y="Registered_Users",
                                            color = "State", 
                                            color_discrete_sequence=px.colors.qualitative.Bold,
                                            text=formated_user_count)

                                fig.update_layout(xaxis=dict(title='State'), yaxis=dict(title="User Count"))
                                fig.update_traces(hovertemplate="Users: %{text}",textposition='outside')                               
                                st.plotly_chart(fig, use_container_width=True)
                                st.dataframe(yearly_low_10_user_states, hide_index= True)
                            low_10_states_on_year()              

                 
                if selected_query:
                    if selected_query == top_queries[2]:
                        year_wise_dist_high_perf_amount_over_time = st.toggle('Year-Wise') 
                        if year_wise_dist_high_perf_amount_over_time:
                            def yearly_top_10_dist_user():                                                                         
                                selected_year = st.select_slider("Select Year", sorted(map_user_data['Year'].unique()))
                                top_10_dis_df = map_user_data.loc[map_user_data.Year == selected_year].groupby(["District"], as_index=False).Registered_Users.sum().sort_values(by="Registered_Users", ascending=False).head(10)
                                top_10_dis_df["District"] = top_10_dis_df["District"].replace("Central","Delhi Central")
                                formated_amount_10_dis = [Convert.rupees(amount) for amount in top_10_dis_df['Registered_Users']]
                                
                                
                                fig = px.bar(top_10_dis_df, 
                                            x="District",
                                            y="Registered_Users",
                                            color = "District", 
                                            color_discrete_sequence=px.colors.qualitative.Bold,
                                            text =formated_amount_10_dis)
                                
                                fig.update_traces(hovertemplate="Users: %{text}",textposition='outside')  
                                fig.update_layout(xaxis=dict(title='District'), yaxis=dict(title="User Count")) 
                                st.plotly_chart(fig, use_container_width=True)                                                                                                                                                        
                                st.dataframe(top_10_dis_df, hide_index= True)
                            yearly_top_10_dist_user()                 


                        else:     
                            def top_10_dist_user_on_year():
                                reason1 = """🟡 **Bengaluru** is known as the Silicon Valley of India. It houses numerous tech companies and startups with a large young, tech-savvy population. This demographic often has higher disposable income and is more likely to adopt digital payment methods like PhonePe."""
                                reason5 = """
                                🟡**Hyderabad and Rangareddy** together form a bustling metropolitan area, naturally driving up transaction volumes. Telangana's government initiatives, like the "Telangana Digital Transactions Mission" and "Har Ghar Digital Payment," have encouraged PhonePe adoption. Moreover, the region's young and tech-savvy population, especially in Hyderabad, contributes to its high digital transaction rates. **Medchal Malkajgiri**, within this area, leads in PhonePe transactions due to its urbanization, strong IT and business presence, and proactive government support for digital payments. 
                                """
                                reason2 = """🟡 **Pune** is a major IT hub with a large young population and a growing middle class. It has a large student population, and students are typically early adopters of digital payments for everyday needs."""  
                                reason3 = """🟡 **Jaipur** is a renowned center for gemstones and jewelry. The city is renowned worldwide for its gemstone cutting, polishing, and trading activities. These transactions often involve larger sums of money.
                                        Jaipur is a major tourist destination in India. Tourists often rely on digital wallets for convenience and security. This high tourist volume can significantly contribute to transaction volume and potentially translate to higher overall transaction value on PhonePe."""
                                reason4 = """🟡 Both **Thane and Mumbai Suburban** are densely populated areas. A larger population base naturally translates to a wider potential user base for PhonePe. 
                                                These regions are part of the Mumbai Metropolitan Region (MMR), a major economic hub in India. This translates to a higher disposable income for many residents, making them more likely to adopt digital wallets like PhonePe. """
                                reason6 = """🟡 **Ahmedabad and Surat** both cities have a significant population base, and economic growth leads to more people having money to spend. This translates to a larger potential user group for PhonePe compared to regions with smaller populations or lower economic activity."""
                                reason7 = """🟡 **North 24 Parganas** The district, being part of the Kolkata metropolitan area, is experiencing economic growth. This leads to a rise in disposable income, making residents more likely to explore digital wallets for transactions.
                                                  It is the one of the most populous districts in India. A larger population translates to a wider potential user base for PhonePe."""
                            
                                def users_dis_stream_data():
                                    for word in reason1.split():
                                        yield word + " "
                                        time.sleep(0.03)

                                def users_dis_stream_data1():
                                    for word in reason2.split():
                                        yield word + " "
                                        time.sleep(0.03)

                                def users_dis_stream_data2():
                                    for word in reason3.split():
                                        yield word + " "
                                        time.sleep(0.03)        

                                def users_dis_stream_data3():
                                    for word in reason4.split():
                                        yield word + " "
                                        time.sleep(0.03)          

                                def users_dis_stream_data4():
                                    for word in reason5.split():
                                        yield word + " "
                                        time.sleep(0.03)     

                                def users_dis_stream_data5():
                                    for word in reason6.split():
                                        yield word + " "
                                        time.sleep(0.03)  

                                def users_dis_stream_data6():
                                    for word in reason7.split():
                                        yield word + " "
                                        time.sleep(0.03)   
                                
                                
                                top_10_dis_df = map_user_data.groupby(["District"], as_index=False).Registered_Users.sum().sort_values(by="Registered_Users", ascending=False).head(10)
                                top_10_dis_df["District"] = top_10_dis_df["District"].replace("Central","Delhi Central")
                                formated_amount_10_dis = [Convert.rupees(amount) for amount in top_10_dis_df['Registered_Users']]
                                                            
                                fig = px.bar(top_10_dis_df, 
                                            x="District",
                                            y="Registered_Users",
                                            color = "District", 
                                            color_discrete_sequence=px.colors.qualitative.Bold,
                                            text =formated_amount_10_dis)
                                
                                fig.update_traces(hovertemplate="Users: %{text}",textposition='outside')  
                                fig.update_layout(xaxis=dict(title='District'), yaxis=dict(title="User Count")) 
                                st.plotly_chart(fig, use_container_width=True)                                                                                                                                                        
                                st.write_stream(users_dis_stream_data)
                                st.write_stream(users_dis_stream_data1)
                                st.write_stream(users_dis_stream_data2)
                                st.write_stream(users_dis_stream_data3)
                                st.write_stream(users_dis_stream_data4)
                                st.write_stream(users_dis_stream_data5)    
                                st.write_stream(users_dis_stream_data6)                                                                                                                                                   
                                st.dataframe(top_10_dis_df, hide_index= True)
                            top_10_dist_user_on_year()                 



                if selected_query:
                    if selected_query == top_queries[3]:                         
                        def Quar_wise_user_dis():
                            
                            selected_state = st.selectbox("Select State", sorted(map_user_data['State'].unique()),index= None)
                            selected_year = st.selectbox("Select Year", sorted(map_user_data['Year'].unique()),index= None)

                            Q_wise_user_dis = map_user_data.loc[(map_user_data.State == selected_state )&(map_user_data.Year == selected_year)].groupby(["Quarter"],as_index = False).Registered_Users.sum()
            


                            if selected_state and selected_year:
                                st.success(f"Showing insights for Year: {selected_year} and State: {selected_state}")
                                fig_Q_wise_user_dis = px.bar(Q_wise_user_dis, x = "Quarter", 
                                                            y = "Registered_Users",
                                                            title=f'Distribution Users in {selected_state} ({selected_year})', 
                                                            text = [Convert.rupees(amount) for amount in Q_wise_user_dis['Registered_Users']],
                                                            color='Registered_Users',
                                                            color_continuous_scale = px.colors.diverging.Spectral_r,
                                                            barmode="group")
                                fig_Q_wise_user_dis.update_traces(hovertemplate="Quarter: %{x}<br>Users: %{text}")
                                fig_Q_wise_user_dis.update_traces(textposition='outside')
                                fig_Q_wise_user_dis.update_yaxes(type='log', dtick=1)
                                fig_Q_wise_user_dis.update_xaxes(title_text='Quarter', tickvals=[1, 2, 3, 4], ticktext=['Q1 (Jan,Feb,Mar)', 'Q2(Apr,May,Jun)', 'Q3(Jul,Aug,Sep)', 'Q4(Oct,Nov,Dec)'])
                                st.plotly_chart(fig_Q_wise_user_dis, use_container_width=True)

                            else:
                                st.warning("Please select all the above options")

                        Quar_wise_user_dis()                         
            user_top_insights()


    if insights_type == "**Insurance**":
        ins_insights_container =  st.container(border = True)
        ins_insights_container.subheader("Insights Types")
        ins_insights_filter_type = ins_insights_container.radio("Select Type", ["Geo Visualization","Top Insights"],key="user_insights", horizontal=True)
        
        if ins_insights_filter_type == "Geo Visualization":


            def ins_geo():
       
                def india_ins_geojson():
                    india = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                    return india  
                              
                ins_amt_geo_queries = ["Total Insurance",
                                      "District Wise Total Insurance"]
                st.title(':violet[Insurance Data Distribution Across States]') 
                ins_amt_geo_selected_query = st.selectbox("Select a Query", ins_amt_geo_queries,index= 0)  
            
                if ins_amt_geo_selected_query ==  ins_amt_geo_queries[0]:
                    ins_amt_on_years = st.toggle('Year-Wise')
                    if not ins_amt_on_years:
                        def total_ins_amount_geo():
                            show_total_count = st.checkbox("Change Colors On The Map Based On Total Insurance Count")
                            if not show_total_count:
                                df = agg_ins_data.groupby(["State"],as_index= False).agg({"Amount":["sum","mean"],"Insurance_Count":["sum","mean"]})
                                df['State'] = df['State'].replace('Andaman And Nicobar Islands', 'Andaman & Nicobar')
                                df.columns = ['State', 'Total_Ins_Amount', 'Average_Ins_Amount','Total_Ins_Count','Average_Ins_Count']
                                formated_Total_ins_amount = [Convert.rupees(amount) for amount in df['Total_Ins_Amount']]
                                formated_Average_ins_amount =  [Convert.rupees(amount) for amount in df['Average_Ins_Amount']]
                                formated_Total_Insurance_Count =  [Convert.rupees(amount) for amount in df['Total_Ins_Count']]
                                formated_Average_Insurance_Count =  [Convert.rupees(round(amount)) for amount in df['Average_Ins_Count']]
                                hover_template = (
                                                    "<b>%{location}</b><br>"
                                                    "Total Insurance Value: %{customdata[0]}<br>"
                                                    "Average Yearly Insurance Value: %{customdata[1]}<br>"
                                                    "Total Insurance Count: %{customdata[2]}<br>"
                                                    "Average Yearly Insurance Count: %{customdata[3]}<br>"
                                                )
                                
                                customdata = list(zip(formated_Total_ins_amount, formated_Average_ins_amount,formated_Total_Insurance_Count,formated_Average_Insurance_Count))

                                fig = px.choropleth_mapbox(
                                    df,
                                    geojson= india_ins_geojson(),
                                    locations='State',
                                    mapbox_style="carto-positron",
                                    zoom=3.5,
                                    center={"lat": 21.7679, "lon": 78.8718}, 
                                    # opacity=0.5,
                                    featureidkey='properties.ST_NM', 
                                    color='Total_Ins_Amount', 
                                    color_continuous_scale= px.colors.sequential.dense_r
                                    )
                                fig.update_geos(fitbounds="locations", visible=False)
                            
                                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                                fig.update_layout(geo_bgcolor="#210D38")
                                fig.update_traces(hovertemplate=hover_template, customdata=customdata)
                                fig.update_layout(height=600)
                                fig.update_coloraxes(colorbar_title_text='Total Insurance Amount')
                                st.subheader("Showing Total Insurance Amount: Sum of All Years")
                                st.plotly_chart(fig,use_container_width = True)
                            elif show_total_count : 
                                df = agg_ins_data.groupby(["State"],as_index= False).agg({"Amount":["sum","mean"],"Insurance_Count":["sum","mean"]})
                                df['State'] = df['State'].replace('Andaman And Nicobar Islands', 'Andaman & Nicobar')
                                df.columns = ['State', 'Total_Ins_Amount', 'Average_Ins_Amount','Total_Ins_Count','Average_Ins_Count']
                                formated_Total_ins_amount = [Convert.rupees(amount) for amount in df['Total_Ins_Amount']]
                                formated_Average_ins_amount =  [Convert.rupees(amount) for amount in df['Average_Ins_Amount']]
                                formated_Total_Insurance_Count =  [Convert.rupees(amount) for amount in df['Total_Ins_Count']]
                                formated_Average_Insurance_Count =  [Convert.rupees(round(amount)) for amount in df['Average_Ins_Count']]
                                hover_template = (
                                                "<b>%{location}</b><br>"
                                                "Total Insurance Count: %{customdata[2]}<br>"
                                                "Average Yearly Insurance Count: %{customdata[3]}<br>"
                                                "Total Insurance Value: %{customdata[0]}<br>"
                                                "Average Yearly Insurance Value: %{customdata[1]}<br>"
                                            )
                                customdata = list(zip(formated_Total_ins_amount, formated_Average_ins_amount,formated_Total_Insurance_Count,formated_Average_Insurance_Count))
                                fig1 = px.choropleth_mapbox(
                                    df,
                                    geojson= india_ins_geojson(),
                                    locations='State',
                                    mapbox_style="carto-positron",
                                    zoom=3.5,
                                    center={"lat": 21.7679, "lon": 78.8718}, 
                                    featureidkey='properties.ST_NM', 
                                    color='Total_Ins_Count', 
                                    color_continuous_scale= px.colors.sequential.dense_r
                                )
                                fig1.update_geos(fitbounds="locations", visible=False)
                                fig1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                                fig1.update_layout(geo_bgcolor="#210D38")
                                fig1.update_traces(hovertemplate=hover_template, customdata=customdata)
                                fig1.update_layout(height=600)
                                fig1.update_coloraxes(colorbar_title_text='Total Insurance Count')
                                st.subheader("Showing Total Insurance Amount: Sum of All Years")
                                st.plotly_chart(fig1,use_container_width = True)                                   
                        total_ins_amount_geo()
                    if ins_amt_on_years:   
                        def year_wise_ins_amt_geo():
                            show_total_count = st.checkbox("Change Colors On The Map Based On Total Insurance Count")
                            if not show_total_count:
                                selected_year = st.select_slider("Select Year", sorted(agg_ins_data['Year'].unique()))
                                df = agg_ins_data.loc[agg_ins_data.Year == selected_year].groupby(["State"],as_index= False).agg({"Amount":["sum","mean"],"Insurance_Count":["sum","mean"]})
                                df['State'] = df['State'].replace('Andaman And Nicobar Islands', 'Andaman & Nicobar')
                                df.columns = ['State', 'Total_Ins_Amount', 'Average_Ins_Amount','Total_Ins_Count','Average_Ins_Count']
                                formated_Total_ins_amount = [Convert.rupees(amount) for amount in df['Total_Ins_Amount']]
                                formated_Average_ins_amount =  [Convert.rupees(amount) for amount in df['Average_Ins_Amount']]
                                formated_Total_Insurance_Count =  [Convert.rupees(amount) for amount in df['Total_Ins_Count']]
                                formated_Average_Insurance_Count =  [Convert.rupees(round(amount)) for amount in df['Average_Ins_Count']]
                                hover_template = (
                                                    "<b>%{location}</b><br>"
                                                    "Total Insurance Value: %{customdata[0]}<br>"
                                                    "Average Yearly Insurance Value: %{customdata[1]}<br>"
                                                    "Total Insurance Count: %{customdata[2]}<br>"
                                                    "Average Yearly Insurance Count: %{customdata[3]}<br>"
                                                )
                                
                                customdata = list(zip(formated_Total_ins_amount, formated_Average_ins_amount,formated_Total_Insurance_Count,formated_Average_Insurance_Count))


                                fig = px.choropleth_mapbox(
                                    df,
                                    geojson= india_ins_geojson(),
                                    locations='State',
                                    mapbox_style="carto-positron",
                                    zoom=3.5,
                                    center={"lat": 21.7679, "lon": 78.8718}, 
                                    # opacity=0.5,
                                    featureidkey='properties.ST_NM', 
                                    color='Total_Ins_Amount', 
                                    color_continuous_scale= px.colors.sequential.dense_r,
                                    )
                                fig.update_geos(fitbounds="locations", visible=False)
                                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                                fig.update_layout(geo_bgcolor="#210D38")
                                fig.update_traces(hovertemplate=hover_template, customdata=customdata)
                                fig.update_layout(height=600)
                                fig.update_coloraxes(colorbar_title_text='Total Insurance Value')
                                st.subheader(f"Showing Total Insurance Amount for the Year: {selected_year}")
                                st.plotly_chart(fig,use_container_width = True)       

                            elif show_total_count :                 
                                selected_year = st.select_slider("Select Year", sorted(agg_ins_data['Year'].unique()),value=min(agg_ins_data['Year']))
                                df = agg_ins_data.loc[agg_ins_data.Year == selected_year].groupby(["State"],as_index= False).agg({"Amount":["sum","mean"],"Insurance_Count":["sum","mean"]})
                                df['State'] = df['State'].replace('Andaman And Nicobar Islands', 'Andaman & Nicobar')
                                df.columns = ['State', 'Total_Ins_Amount', 'Average_Ins_Amount','Total_Ins_Count','Average_Ins_Count']
                                formated_Total_ins_amount = [Convert.rupees(amount) for amount in df['Total_Ins_Amount']]
                                formated_Average_ins_amount =  [Convert.rupees(amount) for amount in df['Average_Ins_Amount']]
                                formated_Total_Insurance_Count =  [Convert.rupees(amount) for amount in df['Total_Ins_Count']]
                                formated_Average_Insurance_Count =  [Convert.rupees(round(amount)) for amount in df['Average_Ins_Count']]
                                hover_template = (  
                                                    "<b>%{location}</b><br>"
                                                    "Total Insurance Count: %{customdata[2]}<br>"
                                                    "Average Yearly Insurance Count: %{customdata[3]}<br>"
                                                    "Total Insurance Value: %{customdata[0]}<br>"
                                                    "Average Yearly Insurance Value: %{customdata[1]}<br>"
                                                )
                                
                                customdata = list(zip(formated_Total_ins_amount, formated_Average_ins_amount,formated_Total_Insurance_Count,formated_Average_Insurance_Count))


                                fig = px.choropleth_mapbox(
                                    df,
                                    geojson= india_ins_geojson(),
                                    locations='State',
                                    mapbox_style="carto-positron",
                                    zoom=3.5,
                                    center={"lat": 21.7679, "lon": 78.8718}, 
                                    # opacity=0.5,
                                    featureidkey='properties.ST_NM', 
                                    color='Total_Ins_Count', 
                                    color_continuous_scale= px.colors.sequential.dense_r,
                                    )
                                fig.update_geos(fitbounds="locations", visible=False)
                                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                                fig.update_layout(geo_bgcolor="#210D38")
                                fig.update_traces(hovertemplate=hover_template, customdata=customdata)
                                fig.update_layout(height=600)
                                fig.update_coloraxes(colorbar_title_text='Total Insurance Count')
                                st.subheader(f"Showing Total Insurance Amount for the Year: {selected_year}")
                                st.plotly_chart(fig,use_container_width = True)     
                        year_wise_ins_amt_geo()
                    

                if ins_amt_geo_selected_query == ins_amt_geo_queries[1]:  
                    ins_amt_dist_on_years = st.toggle('Year-Wise')  
                    if not ins_amt_dist_on_years:
                        def district_wise_ins_total():
                            show_total_count = st.checkbox("Change Colors On The Map Based On Total Insurance Count")
                            selected_state = st.selectbox("Select State", sorted([state for state in map_ins_data['State'].unique() if state != "Dadra And Nagar Haveli And Daman And Diu"]),index = 29)
                            state_coordinates = state_coordinate()
                            zoom = state_zoom()
                            state_geojson_links = state_geojson_link()
                            if selected_state in state_geojson_links:
                                geojson_link = state_geojson_links[selected_state]

                                if not show_total_count:
                                    df = map_ins_data.loc[map_ins_data['State'] == selected_state].groupby("District", as_index = False).agg({"Amount":["sum","mean"],"Insurance_Count":["sum","mean"]})
                                    df.columns = ['District', 'Total_Ins_Amount', 'Average_Ins_Amount','Total_Ins_Count','Average_Ins_Count']
                                    formated_Total_ins_amount = [Convert.rupees(amount) for amount in df['Total_Ins_Amount']]
                                    formated_Average_ins_amount =  [Convert.rupees(amount) for amount in df['Average_Ins_Amount']]
                                    formated_Total_Insurance_Count =  [Convert.rupees(amount) for amount in df['Total_Ins_Count']]
                                    formated_Average_Insurance_Count =  [Convert.rupees(round(amount)) for amount in df['Average_Ins_Count']]
                                    hover_template = (
                                                        "<b>%{location}</b><br>"
                                                        "Total Insurance Value: %{customdata[0]}<br>"
                                                        "Average Yearly Insurance Value: %{customdata[1]}<br>"
                                                        "Total Insurance Count: %{customdata[2]}<br>"
                                                        "Average Yearly Insurance Count: %{customdata[3]}<br>"
                                                    )
                                    customdata = list(zip(formated_Total_ins_amount, formated_Average_ins_amount,formated_Total_Insurance_Count,formated_Average_Insurance_Count))
                                    
                                    
                                    center_coordinates = state_coordinates[selected_state]
                                    depth = zoom[selected_state]
                                    fig = px.choropleth_mapbox(
                                        df,
                                        geojson=geojson_link,
                                        locations='District',
                                        mapbox_style="carto-positron",
                                        zoom=depth,
                                        center=center_coordinates, 
                                        
                                        featureidkey='properties.dtname', 
                                        color='Total_Ins_Amount', 
                                        color_continuous_scale= px.colors.sequential.Viridis)
                                    fig.update_geos(fitbounds="locations", visible=False)
                                    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                                    fig.update_layout(geo_bgcolor="#210D38")
                                    fig.update_coloraxes(colorbar_title_text='Total Insurance Value')
                                    fig.update_traces(hovertemplate=hover_template, customdata=customdata)
                                    st.subheader(f"Showing Insurance Value for the Districts of {selected_state}")
                                    st.plotly_chart(fig,use_container_width = True)        

                                elif show_total_count:
                                    df = map_ins_data.loc[map_ins_data['State'] == selected_state].groupby("District", as_index = False).agg({"Amount":["sum","mean"],"Insurance_Count":["sum","mean"]})
                                    df.columns = ['District', 'Total_Ins_Amount', 'Average_Ins_Amount','Total_Ins_Count','Average_Ins_Count']
                                    formated_Total_ins_amount = [Convert.rupees(amount) for amount in df['Total_Ins_Amount']]
                                    formated_Average_ins_amount =  [Convert.rupees(amount) for amount in df['Average_Ins_Amount']]
                                    formated_Total_Insurance_Count =  [Convert.rupees(amount) for amount in df['Total_Ins_Count']]
                                    formated_Average_Insurance_Count =  [Convert.rupees(round(amount)) for amount in df['Average_Ins_Count']]
                                    hover_template = (
                                                        "<b>%{location}</b><br>"
                                                        "Total Insurance Count: %{customdata[2]}<br>"
                                                        "Average Yearly Insurance Count: %{customdata[3]}<br>"
                                                        "Total Insurance Value: %{customdata[0]}<br>"
                                                        "Average Yearly Insurance Value: %{customdata[1]}<br>"
                                                    )
                                    customdata = list(zip(formated_Total_ins_amount, formated_Average_ins_amount,formated_Total_Insurance_Count,formated_Average_Insurance_Count))
                                    
                                    
                                    center_coordinates = state_coordinates[selected_state]
                                    depth = zoom[selected_state]
                                    fig = px.choropleth_mapbox(
                                        df,
                                        geojson=geojson_link,
                                        locations='District',
                                        mapbox_style="carto-positron",
                                        zoom=depth,
                                        center=center_coordinates, 
                                        
                                        featureidkey='properties.dtname', 
                                        color='Total_Ins_Count', 
                                        color_continuous_scale= px.colors.sequential.Viridis)
                                    fig.update_geos(fitbounds="locations", visible=False)
                                    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                                    fig.update_layout(geo_bgcolor="#210D38")
                                    fig.update_coloraxes(colorbar_title_text='Total Insurance Count')
                                    fig.update_traces(hovertemplate=hover_template, customdata=customdata)
                                    st.subheader(f"Showing Insurance Count for the Districts of {selected_state}")
                                    st.plotly_chart(fig,use_container_width = True)                                    

                        district_wise_ins_total()

                    if ins_amt_dist_on_years:
                        def yearly_district_wise_ins_total():
                            show_total_count = st.checkbox("Change Colors On The Map Based On Total Insurance Count")
                            selected_year = st.select_slider("Select Year", sorted(map_ins_data['Year'].unique()))
                            selected_state = st.selectbox("Select State", sorted([state for state in map_ins_data['State'].unique() if state != "Dadra And Nagar Haveli And Daman And Diu"]),index = 29)
                            state_coordinates = state_coordinate()
                            zoom = state_zoom()
                            state_geojson_links = state_geojson_link()
                            if selected_state in state_geojson_links:
                                geojson_link = state_geojson_links[selected_state]

                                if not show_total_count:
                                    df = map_ins_data.loc[(map_ins_data['State'] == selected_state)&(map_ins_data['Year'] == selected_year)].groupby("District", as_index = False).agg({"Amount":["sum","mean"],"Insurance_Count":["sum","mean"]})
                                    df.columns = ['District', 'Total_Ins_Amount', 'Average_Ins_Amount','Total_Ins_Count','Average_Ins_Count']
                                    formated_Total_ins_amount = [Convert.rupees(amount) for amount in df['Total_Ins_Amount']]
                                    formated_Average_ins_amount =  [Convert.rupees(amount) for amount in df['Average_Ins_Amount']]
                                    formated_Total_Insurance_Count =  [Convert.rupees(amount) for amount in df['Total_Ins_Count']]
                                    formated_Average_Insurance_Count =  [Convert.rupees(round(amount)) for amount in df['Average_Ins_Count']]
                                    hover_template = (
                                                        "<b>%{location}</b><br>"
                                                        "Total Insurance Value: %{customdata[0]}<br>"
                                                        "Average Yearly Insurance Value: %{customdata[1]}<br>"
                                                        "Total Insurance Count: %{customdata[2]}<br>"
                                                        "Average Yearly Insurance Count: %{customdata[3]}<br>"
                                                    )
                                    customdata = list(zip(formated_Total_ins_amount, formated_Average_ins_amount,formated_Total_Insurance_Count,formated_Average_Insurance_Count))
                                    
                                    
                                    center_coordinates = state_coordinates[selected_state]
                                    depth = zoom[selected_state]
                                    fig = px.choropleth_mapbox(
                                        df,
                                        geojson=geojson_link,
                                        locations='District',
                                        mapbox_style="carto-positron",
                                        zoom=depth,
                                        center=center_coordinates, 
                                        
                                        featureidkey='properties.dtname', 
                                        color='Total_Ins_Amount', 
                                        color_continuous_scale= px.colors.sequential.Viridis)
                                    fig.update_geos(fitbounds="locations", visible=False)
                                    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                                    fig.update_layout(geo_bgcolor="#210D38")
                                    fig.update_traces(hovertemplate=hover_template, customdata=customdata)
                                    fig.update_coloraxes(colorbar_title_text='Total Insurance Value')
                                    st.subheader(f"Showing Total Insurance Amount for the Districts of {selected_state} on Year {selected_year}")
                                    st.plotly_chart(fig,use_container_width = True)         

                                elif show_total_count:
                                    df = map_ins_data.loc[(map_ins_data['State'] == selected_state)&(map_ins_data['Year'] == selected_year)].groupby("District", as_index = False).agg({"Amount":["sum","mean"],"Insurance_Count":["sum","mean"]})
                                    df.columns = ['District', 'Total_Ins_Amount', 'Average_Ins_Amount','Total_Ins_Count','Average_Ins_Count']
                                    formated_Total_ins_amount = [Convert.rupees(amount) for amount in df['Total_Ins_Amount']]
                                    formated_Average_ins_amount =  [Convert.rupees(amount) for amount in df['Average_Ins_Amount']]
                                    formated_Total_Insurance_Count =  [Convert.rupees(amount) for amount in df['Total_Ins_Count']]
                                    formated_Average_Insurance_Count =  [Convert.rupees(round(amount)) for amount in df['Average_Ins_Count']]
                                    hover_template = (
                                                        "<b>%{location}</b><br>"
                                                        "Total Insurance Count: %{customdata[2]}<br>"
                                                        "Average Yearly Insurance Count: %{customdata[3]}<br>"
                                                        "Total Insurance Value: %{customdata[0]}<br>"
                                                        "Average Yearly Insurance Value: %{customdata[1]}<br>"
                                                    )
                                    customdata = list(zip(formated_Total_ins_amount, formated_Average_ins_amount,formated_Total_Insurance_Count,formated_Average_Insurance_Count))
                                    
                                    
                                    center_coordinates = state_coordinates[selected_state]
                                    depth = zoom[selected_state]
                                    fig = px.choropleth_mapbox(
                                        df,
                                        geojson=geojson_link,
                                        locations='District',
                                        mapbox_style="carto-positron",
                                        zoom=depth,
                                        center=center_coordinates, 
                                        
                                        featureidkey='properties.dtname', 
                                        color='Total_Ins_Count', 
                                        color_continuous_scale=px.colors.sequential.Viridis)
                                    fig.update_geos(fitbounds="locations", visible=False)
                                    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                                    fig.update_layout(geo_bgcolor="#210D38")
                                    fig.update_traces(hovertemplate=hover_template, customdata=customdata)
                                    fig.update_coloraxes(colorbar_title_text='Total Insurance Count')
                                    st.subheader(f"Showing Total Insurance Count for the Districts of {selected_state} on Year {selected_year}")
                                    st.plotly_chart(fig,use_container_width = True)                                         

                        yearly_district_wise_ins_total()

            ins_geo()

        if ins_insights_filter_type == "Top Insights":    

            def ins_top_insights():           
                top_queries = ["Top 10 States with Highest Insurance",
                                "Top 10 States with Lowest Insurance",
                                "Top 10 District With Highest Insurance",
                                "Quarter-wise Insurance distribution for specific state"]
                        
                selected_query = st.selectbox("Select a Query", top_queries,index= None)  


                
                if selected_query:
                    if selected_query == top_queries[0]:
                        yearly_top_10_states_on_ins = st.toggle('Year-Wise') 
                        if not yearly_top_10_states_on_ins:
                            def top_10_states():                                                          
                                def top_10_statess(agg_ins_data):
                                    top_10_states = agg_ins_data.groupby(["State"], as_index=False).Amount.sum().sort_values(by="Amount", ascending=False).head(10)
                                    return top_10_states
                                
                                col1, col2 = st.columns(2)
                                with col1:
                                    top_10_states = top_10_statess(agg_ins_data)
                                    formated_amount_10 = [Convert.rupees(amount) for amount in top_10_states['Amount']]
                                    
                                    
                                    fig = px.bar(top_10_states, 
                                                x="State", 
                                                y="Amount",
                                                color = "State", 
                                                color_discrete_sequence=px.colors.qualitative.Alphabet,
                                                text=formated_amount_10,title = "Insurance Amount")
                                    fig.update_layout(xaxis=dict(title='State'), yaxis=dict(title="Total Insurance Amount"))
                                    fig.update_traces(hovertemplate="Amount: %{text}",textposition='outside')
                                    st.plotly_chart(fig, use_container_width=True)
                                    st.dataframe(top_10_states,width=500, height=400, hide_index= True)

                                with col2:
                                        a = top_10_statess(agg_ins_data)
                                        filter1 = list(a.State.unique())
                                        top_10_states = agg_ins_data.loc[agg_ins_data.State.isin(filter1)].groupby(["State"], as_index=False).Insurance_Count.sum().sort_values(by="Insurance_Count", ascending=False).head(10)
                                        formated_amount_10 = [Convert.rupees(amount) for amount in top_10_states['Insurance_Count']]
                                        
                                        
                                        fig = px.bar(top_10_states, 
                                                    x="State", 
                                                    y="Insurance_Count",
                                                    color = "State", 
                                                    color_discrete_sequence=px.colors.qualitative.Alphabet,
                                                    text=formated_amount_10,title = "Insurance Count")
                                        
                                        fig.update_layout(xaxis=dict(title='State'), yaxis=dict(title="Insurance Count"))
                                        fig.update_traces(hovertemplate="Insurance Count: %{text}",textposition='outside')
                                        st.plotly_chart(fig, use_container_width=True)
                                        st.dataframe(top_10_states,width=500, height=400, hide_index= True)
                                                                    
                            top_10_states()                

                        if yearly_top_10_states_on_ins:      
                            def top_10_states_on_year():     
                                selected_year = st.select_slider("Select Year", sorted(agg_ins_data['Year'].unique()))                          
                                col3, col4 = st.columns(2)
                                with col3:
                                    top_10_states_ins = agg_ins_data.loc[agg_ins_data.Year == selected_year].groupby(["State"], as_index=False).Amount.sum().sort_values(by="Amount", ascending=False).head(10)
                                    formated_amount_10 = [Convert.rupees(amount) for amount in top_10_states_ins['Amount']]
                                    
                                    
                                    fig = px.bar(top_10_states_ins, 
                                                x="State", 
                                                y="Amount",
                                                color = "State", 
                                                color_discrete_sequence=px.colors.qualitative.Alphabet,
                                                text=formated_amount_10,
                                                title = "Insurance Value")
                                    fig.update_layout(xaxis=dict(title='State'), yaxis=dict(title="Total Insurance Amount"))
                                    fig.update_traces(hovertemplate="Amount: %{text}",textposition='outside')
                                    st.plotly_chart(fig, use_container_width=True)
                                    st.dataframe(top_10_states_ins,width=500, height=400,hide_index= True)
                                with col4:
                                    a = agg_ins_data.loc[agg_ins_data.Year == selected_year].groupby(["State"], as_index=False).Insurance_Count.sum().sort_values(by="Insurance_Count", ascending=False).head(10)
                                    filter = list(a.State.unique())
                                    top_10_states1 = agg_ins_data.loc[(agg_ins_data.Year == selected_year)&(agg_ins_data.State.isin(filter))].groupby(["State"], as_index=False).Insurance_Count.sum().sort_values(by="Insurance_Count", ascending=False)
                                    formated_amount_10 = [Convert.rupees(amount) for amount in top_10_states1['Insurance_Count']]

                                    fig = px.bar(top_10_states1, 
                                                x="State", 
                                                y="Insurance_Count",
                                                color = "State", 
                                                color_discrete_sequence=px.colors.qualitative.Alphabet,
                                                text=formated_amount_10,title = "Insurance Count")
                                    fig.update_layout(xaxis=dict(title='State'), yaxis=dict(title="Total Insurance Count"))
                                    fig.update_traces(hovertemplate="Insurance Count: %{text}",textposition='outside')
                                    st.plotly_chart(fig, use_container_width=True)
                                    st.dataframe(top_10_states1,width=500, height=400, hide_index= True)                            
                            top_10_states_on_year()                


                if selected_query:
                    if selected_query == top_queries[1]:
                        year_wise__low_perf_state_amount_over_time= st.toggle('Year-Wise')
                        if not year_wise__low_perf_state_amount_over_time:
                            def low_10_states():
                                col1, col2 = st.columns(2)
                                with col1:
                                    low_10_states = agg_ins_data.groupby(["State"], as_index=False).Amount.sum().sort_values(by="Amount", ascending=True).head(10)
                                    low_10_states.State = low_10_states.State.replace("Dadra & Nagar Haveli & Daman & Diu","DNHDD")
                                    
                                    formated_amount_10 = [Convert.rupees(amount) for amount in low_10_states['Amount']]
                                    
                                    
                                    fig = px.bar(low_10_states, 
                                                x="State", 
                                                y="Amount",
                                                color = "State", 
                                                color_discrete_sequence=px.colors.qualitative.Alphabet,
                                                text=formated_amount_10,title = "Insurance Amount")
                                    fig.update_layout(xaxis=dict(title='State'), yaxis=dict(title="Total Insurance Amount"))
                                    fig.update_traces(hovertemplate="Amount: %{text}",textposition='outside')
                                    st.plotly_chart(fig, use_container_width=True)
                                    st.dataframe(low_10_states,width=500, height=400, hide_index= True)

                                with col2:
                                        a = agg_ins_data.groupby(["State"], as_index=False).Amount.sum().sort_values(by="Amount", ascending=True).head(10)
                                        filter1 = list(a.State.unique())
                                        low_10_states = agg_ins_data.loc[agg_ins_data.State.isin(filter1)].groupby(["State"], as_index=False).Insurance_Count.sum().sort_values(by="Insurance_Count", ascending=True).head(10)
                                        low_10_states.State = low_10_states.State.replace("Dadra & Nagar Haveli & Daman & Diu","DNHDD")
                                        formated_amount_10 = [Convert.rupees(amount) for amount in low_10_states['Insurance_Count']]
                                        
                                        
                                        fig = px.bar(low_10_states, 
                                                    x="State", 
                                                    y="Insurance_Count",
                                                    color = "State", 
                                                    color_discrete_sequence=px.colors.qualitative.Alphabet,
                                                    text=formated_amount_10,title = "Insurance Count")
                                        
                                        fig.update_layout(xaxis=dict(title='State'), yaxis=dict(title="Insurance Count"))
                                        fig.update_traces(hovertemplate="Insurance Count: %{text}",textposition='outside')
                                        st.plotly_chart(fig, use_container_width=True)
                                        st.dataframe(low_10_states,width=500, height=400, hide_index= True)
                            low_10_states() 

                        if year_wise__low_perf_state_amount_over_time:
                            def low_10_states_on_year():
                                selected_year = st.select_slider("Select Year", sorted(agg_ins_data['Year'].unique()))                          
                                col3, col4 = st.columns(2)
                                with col3:
                                    low_10_states_ins = agg_ins_data.loc[agg_ins_data.Year == selected_year].groupby(["State"], as_index=False).Amount.sum().sort_values(by="Amount", ascending=True).head(10)
                                    formated_amount_10 = [Convert.rupees(amount) for amount in low_10_states_ins['Amount']]
                                    low_10_states_ins.State = low_10_states_ins.State.replace("Dadra & Nagar Haveli & Daman & Diu","DNHDD")
                                    
                                    fig = px.bar(low_10_states_ins, 
                                                x="State", 
                                                y="Amount",
                                                color = "State", 
                                                color_discrete_sequence=px.colors.qualitative.Alphabet,
                                                text=formated_amount_10,
                                                title = "Insurance Value")
                                    fig.update_layout(xaxis=dict(title='State'), yaxis=dict(title="Total Insurance Amount"))
                                    fig.update_traces(hovertemplate="Amount: %{text}",textposition='outside')
                                    st.plotly_chart(fig, use_container_width=True)
                                    st.dataframe(low_10_states_ins,width=500, height=400,hide_index= True)
                                with col4:
                                    a = agg_ins_data.loc[agg_ins_data.Year == selected_year].groupby(["State"], as_index=False).Insurance_Count.sum().sort_values(by="Insurance_Count", ascending=True).head(10)
                                    filter = list(a.State.unique())
                                    low_10_states1 = agg_ins_data.loc[(agg_ins_data.Year == selected_year)&(agg_ins_data.State.isin(filter))].groupby(["State"], as_index=False).Insurance_Count.sum().sort_values(by="Insurance_Count", ascending=True)
                                    formated_amount_10 = [Convert.rupees(amount) for amount in low_10_states1['Insurance_Count']]
                                    low_10_states1.State = low_10_states1.State.replace("Andaman & Nicobar Islands","Andaman & Nicobar")
                                    low_10_states1.State = low_10_states1.State.replace("Dadra & Nagar Haveli & Daman & Diu","DNHDD")
                                   
                                    fig = px.bar(low_10_states1, 
                                                x="State", 
                                                y="Insurance_Count",
                                                color = "State", 
                                                color_discrete_sequence=px.colors.qualitative.Alphabet,
                                                text=formated_amount_10,title = "Insurance Count")
                                    fig.update_layout(xaxis=dict(title='State'), yaxis=dict(title="Total Insurance Count"))
                                    fig.update_traces(hovertemplate="Insurance Count: %{text}",textposition='outside')
                                    st.plotly_chart(fig, use_container_width=True)
                                    st.dataframe(low_10_states1,width=500, height=400, hide_index= True)     
                            low_10_states_on_year()              

                 

                if selected_query:
                    if selected_query == top_queries[2]:
                        year_wise_dist_ins_amount_over_time = st.toggle('Year-Wise') 
                        if year_wise_dist_ins_amount_over_time:
                            def yearly_top_10_ins_dist_on_year():                                                                         
                                selected_year = st.select_slider("Select Year", sorted(map_ins_data['Year'].unique()))
                                top_10_dis_df = map_ins_data.loc[map_ins_data.Year == selected_year].groupby("District",as_index= False).Amount.sum().sort_values(by="Amount",ascending = False).head(10)                            
                                top_10_dis_df["District"] = top_10_dis_df["District"].replace("Central","Delhi Central")
                                formated_amount_10_dis = [Convert.rupees(amount) for amount in top_10_dis_df['Amount']]
                                col1, col2 = st.columns(2,gap="medium")
                                with col1:
                                    fig = px.bar(top_10_dis_df, 
                                                x="District", 
                                                y="Amount", 
                                                color = "District",
                                                color_continuous_scale=px.colors.diverging.Spectral_r,
                                                text = formated_amount_10_dis,title = "Insurance Amount")
                                    fig.update_layout(xaxis=dict(title='Districts'), yaxis=dict(title="Total Amount"))
                                    fig.update_traces(hovertemplate="Districts: %{x}<br>Amount: %{text}")
                                    fig.update_traces(textposition='outside')
                                    st.plotly_chart(fig, use_container_width=True)                                                                                                                                                        
                                    st.dataframe(top_10_dis_df,width=500, height=400, hide_index= True)
                                with col2:
                                    a = map_ins_data.loc[map_ins_data.Year == selected_year].groupby("District",as_index= False).Amount.sum().sort_values(by="Amount",ascending = False).head(10)                            
                                    filter = list(a.District.unique())  
                                       
            
                                    top_10_dis_df = map_ins_data.loc[(map_ins_data.Year == selected_year)&(map_ins_data.District.isin(filter))].groupby("District",as_index= False).Insurance_Count.sum().sort_values(by="Insurance_Count",ascending = False).head(10)                            
                                    top_10_dis_df["District"] = top_10_dis_df["District"].replace("Central","Delhi Central")
                                    formated_amount_10_dis = [Convert.rupees(amount) for amount in top_10_dis_df['Insurance_Count']]                                    
                                    fig = px.bar(top_10_dis_df, 
                                                x="District", 
                                                y="Insurance_Count", 
                                                color = "District",
                                                color_continuous_scale=px.colors.cyclical.Twilight,
                                                text = formated_amount_10_dis,title = "Insurance Count")
                                    fig.update_layout(xaxis=dict(title='Districts'), yaxis=dict(title="Insurance Count"))
                                    fig.update_traces(hovertemplate="Districts: %{x}<br>Insurance Count: %{text}")
                                    fig.update_traces(textposition='outside')
                                    st.plotly_chart(fig, use_container_width=True)                                                                                                                                                        
                                    st.dataframe(top_10_dis_df,width=500, height=400, hide_index= True)                                
                            yearly_top_10_ins_dist_on_year()                 


                        else:     
                            def top_10_dist_on_ins():
                                                               
                                top_10_dis_df = map_ins_data.groupby("District",as_index= False).Amount.sum().sort_values(by="Amount",ascending = False).head(10)                            
                                formated_amount_10_dis = [Convert.rupees(amount) for amount in top_10_dis_df['Amount']]
                                col1, col2 = st.columns(2,gap="medium")  
                                with col1:
                                    fig = px.bar(top_10_dis_df, 
                                                x="District", 
                                                y="Amount", 
                                                color = "District",
                                                color_continuous_scale=px.colors.diverging.Spectral_r,
                                                text = formated_amount_10_dis,title = "Insurance Amount")
                                    fig.update_layout(xaxis=dict(title='Districts'), yaxis=dict(title="Total Amount"))
                                    fig.update_traces(hovertemplate="Districts: %{x}<br>Amount: %{text}")
                                    fig.update_traces(textposition='outside')
                                    st.plotly_chart(fig, use_container_width=True)                                                                                                                                                       
                                    st.dataframe(top_10_dis_df,width=500, height=400 ,hide_index= True)

                                with col2:
                                    a = map_ins_data.groupby("District",as_index= False).Amount.sum().sort_values(by="Amount",ascending = False).head(10)                            
                                    filter = list(a.District.unique())
                        
                                    top_10_dis_df = map_ins_data.loc[map_ins_data.District.isin(filter)].groupby("District",as_index= False).Insurance_Count.sum().sort_values(by="Insurance_Count",ascending = False).head(10)                            
                                    top_10_dis_df["District"] = top_10_dis_df["District"].replace("Central","Delhi Central")      
                                    formated_amount_10_dis = [Convert.rupees(amount) for amount in top_10_dis_df['Insurance_Count']]                             
                                    fig = px.bar(top_10_dis_df, 
                                                x="District", 
                                                y="Insurance_Count", 
                                                color = "District",
                                                color_continuous_scale=px.colors.cyclical.Twilight,
                                                text = formated_amount_10_dis,title = "Insurance Count")
                                    fig.update_layout(xaxis=dict(title='Districts'), yaxis=dict(title="Insurance Count"))
                                    fig.update_traces(hovertemplate="Districts: %{x}<br>Insurance Count: %{text}")
                                    fig.update_traces(textposition='outside')
                                    st.plotly_chart(fig, use_container_width=True)                                                                                                                                                       
                                    st.dataframe(top_10_dis_df,width=500, height=400, hide_index= True)                                        
                            top_10_dist_on_ins()                 



                if selected_query:
                    if selected_query == top_queries[3]:                         
                        def Quar_wise_ins_dis():

                            st.info("You selected: Quarter-wise transaction distribution for specific state")
                            
                            selected_state = st.selectbox("Select State", sorted(agg_ins_data['State'].unique()),index= None)
                            selected_year = st.selectbox("Select Year", sorted(agg_ins_data['Year'].unique()),index= None)
                            
                            if selected_state and selected_year:
                                st.success(f"Showing insights for Year: {selected_year} and State: {selected_state}")
                            col1, col2 = st.columns(2,gap="medium")
                            with col1:
                                Q_wise_ins_dis = agg_ins_data.loc[(agg_ins_data.State == selected_state )&(agg_ins_data.Year == selected_year)].groupby(["Quarter"],as_index = False).Amount.sum()
                


                                if selected_state and selected_year:
                                    
                                    fig_Q_wise_ins_dis = px.bar(Q_wise_ins_dis, x = "Quarter", 
                                                                y = "Amount",
                                                                title=f'Distribution of Insurance Amount in {selected_state} ({selected_year})', 
                                                                text = [Convert.rupees(amount) for amount in Q_wise_ins_dis['Amount']],
                                                                color='Amount',
                                                                color_continuous_scale = px.colors.diverging.Spectral_r,
                                                                barmode="group")
                                    fig_Q_wise_ins_dis.update_traces(hovertemplate="Quarter: %{x}<br>Amount: %{text}")
                                    fig_Q_wise_ins_dis.update_traces(textposition='outside')
                                    fig_Q_wise_ins_dis.update_yaxes(type='log', dtick=1)
                                    fig_Q_wise_ins_dis.update_xaxes(title_text='Quarter', tickvals=[1, 2, 3, 4], ticktext=['Q1 (Jan,Feb,Mar)', 'Q2(Apr,May,Jun)', 'Q3(Jul,Aug,Sep)', 'Q4(Oct,Nov,Dec)'])
                                    st.plotly_chart(fig_Q_wise_ins_dis, use_container_width=True)

                                else:
                                    st.warning("Please select all the above options")

                            with col2:
                                Q_wise_ins_dis = agg_ins_data.loc[(agg_ins_data.State == selected_state )&(agg_ins_data.Year == selected_year)].groupby(["Quarter"],as_index = False).Insurance_Count.sum()
                                if selected_state and selected_year:
                                    fig_Q_wise_ins_dis = px.bar(Q_wise_ins_dis, x = "Quarter", 
                                                                y = "Insurance_Count",
                                                                title=f'Distribution Insurance Count in {selected_state} ({selected_year})', 
                                                                text = [Convert.rupees(amount) for amount in Q_wise_ins_dis['Insurance_Count']],
                                                                color='Insurance_Count',
                                                                color_continuous_scale = px.colors.diverging.Spectral_r,
                                                                barmode="group")
                                    fig_Q_wise_ins_dis.update_layout(legend_title_text='Transaction Count')
                                    fig_Q_wise_ins_dis.update_traces(hovertemplate="Quarter: %{x}<br>Transaction Count: %{text}")
                                    fig_Q_wise_ins_dis.update_layout(xaxis=dict(title='Quarter'), yaxis=dict(title="Insurance_Count"))
                                    fig_Q_wise_ins_dis.update_traces(textposition='outside')
                                    fig_Q_wise_ins_dis.update_yaxes(type='log', dtick=1)
                                    fig_Q_wise_ins_dis.update_xaxes(title_text='Quarter', tickvals=[1, 2, 3, 4], ticktext=['Q1 (Jan,Feb,Mar)', 'Q2(Apr,May,Jun)', 'Q3(Jul,Aug,Sep)', 'Q4(Oct,Nov,Dec)'])
                                    st.plotly_chart(fig_Q_wise_ins_dis, use_container_width=True)
    
                                
                                                      

                        Quar_wise_ins_dis()                         

            ins_top_insights()




if selected == "FILTERED INSIGHTS":

    def filters():
            filter_container =  st.container(border = True)
            filter_container.subheader("Filter Options")
            filter_type = filter_container.radio("Category Selection", ["Transactions","Users", "Insurance"], index= None)
            st.write("You selected:", f"<span style='color:#F8CD47'>{filter_type}</span>", unsafe_allow_html=True)


            if filter_type == 'Transactions':
                def filter_trans():
                    trans_filter_container =  st.container(border = True)
                    trans_type = trans_filter_container.radio("Select Type", ["State Wise", "District Wise"], index= None,horizontal=True)
                    
                    # State Wise Transactions
                    if trans_type == "State Wise":
                        
                        def state_wise_trans():
                            statewise_transaction_queries = ["Transaction Amount growth for a specific state & specific Transaction Type ","Quarter-wise transaction amount distribution for specific state",
                                                "Comparing data for the specific transaction type on quarter, and year","Distribution of Transactions Across Different Transaction Types for a specific state",]
                            
                            selected_query = st.selectbox("Select a Query", statewise_transaction_queries,index= None)

                            if selected_query:
                                if selected_query == statewise_transaction_queries[0]:   # Query 1

                                    def trans_amount_by_state_transtype():


                                        st.info("You selected: Transaction growth for a specific state & specific Transaction Type")

                                        selected_state = st.selectbox("Select State", sorted(agg_trans_data['State'].unique()),index= None)
                                        selected_Transaction_Type = st.selectbox("Select Transaction Type", sorted(agg_trans_data['Transaction_Type'].unique()),index= None)
                                        if st.button("Get"):
                                            if selected_state and selected_Transaction_Type:
                                        
                                                st.success(f"Showing insights for State: {selected_state} and Transaction Type: {selected_Transaction_Type}")
                                                col1, col2 = st.columns(2)
                                            
                                                with col1:
                                                    trans_amount_by_state_transtype = agg_trans_data.loc[(agg_trans_data.State == selected_state) & (agg_trans_data.Transaction_Type == selected_Transaction_Type)].groupby(["Year"],as_index= False).agg({"Amount": "sum"})
                                                    formated_trans_amount_by_state_transtype = [Convert.rupees(amount) for amount in trans_amount_by_state_transtype['Amount']]
                                                

                                                    if selected_state and selected_Transaction_Type:
                                                        
                                                        fig_trans_amount_by_state_transtype = px.bar(trans_amount_by_state_transtype, 
                                                                                                    x = "Year", 
                                                                                                    y = "Amount", 
                                                                                                    color = "Amount",
                                                                                                    text= formated_trans_amount_by_state_transtype,
                                                                                                    color_continuous_scale=px.colors.diverging.Spectral_r,
                                                                                                    title=f"{selected_state}'s {selected_Transaction_Type} Amount Growth ")
                                                        
                                                        fig_trans_amount_by_state_transtype.update_layout(xaxis=dict(title='Year'), 
                                                                                                        yaxis=dict(title="Amount"))
                                                        fig_trans_amount_by_state_transtype.update_traces(hovertemplate="Year: %{x}<br>Amount: %{text}")
                                                        fig_trans_amount_by_state_transtype.update_traces(textposition='outside')
                                                        fig_trans_amount_by_state_transtype.update_yaxes(type='log', dtick=1) 

                                                        st.plotly_chart(fig_trans_amount_by_state_transtype, use_container_width=True)
                                                        st.dataframe(trans_amount_by_state_transtype.loc[:,["Year", "Amount"]].style.format({'Year': '{:.0f}'}),hide_index=True)
                                                    

                                                with col2:
                                                    trans_count_by_state_transtype = agg_trans_data.loc[(agg_trans_data.State == selected_state) & (agg_trans_data.Transaction_Type == selected_Transaction_Type)].groupby(["Year"],as_index= False).agg({"Trans_Count": "sum"})
                                                    formated_trans_count_by_state_transtype = [Convert.rupees(amount) for amount in trans_count_by_state_transtype['Trans_Count']]
                                                    

                                                    if selected_state and selected_Transaction_Type:
                                                        fig_trans_count_by_state_transtype = px.bar(trans_count_by_state_transtype, 
                                                                                                    x = "Year", 
                                                                                                    y = "Trans_Count", 
                                                                                                    color = "Trans_Count",
                                                                                                    text= formated_trans_count_by_state_transtype,
                                                                                                    color_continuous_scale=px.colors.diverging.Spectral_r,
                                                                                                    title=f"{selected_state}'s {selected_Transaction_Type} Trasaction Count Growth ")
                                                        
                                                        fig_trans_count_by_state_transtype.update_layout(xaxis=dict(title='Year'), 
                                                                                                        yaxis=dict(title="Amount"))
                                                        fig_trans_count_by_state_transtype.update_traces(hovertemplate="Year: %{x}<br>Amount: %{text}")
                                                        fig_trans_count_by_state_transtype.update_traces(textposition='outside')
                                                        fig_trans_count_by_state_transtype.update_yaxes(type='log', dtick=1) 

                                                        st.plotly_chart(fig_trans_count_by_state_transtype, use_container_width=True)
                                                        st.dataframe(trans_count_by_state_transtype.loc[:,["Year", "Trans_Count"]].style.format({'Year': '{:.0f}'}),hide_index=True)
                                                    
                                            else:
                                                st.warning("Please select all the above options")

                                    
                                    trans_amount_by_state_transtype()

                            if selected_query:
                                if selected_query == statewise_transaction_queries[1]:  # Query 2

                                    def Q_wise_trans_dis():
                                        st.info("You selected: Quarter-wise transaction distribution for specific state")
                                        
                                        selected_year = st.selectbox("Select Year", sorted(agg_trans_data['Year'].unique()),index= None)
                                        selected_state = st.selectbox("Select State", sorted(agg_trans_data['State'].unique()),index= None)

                                        Q_wise_trans_dis = agg_trans_data.loc[(agg_trans_data.State == selected_state )&(agg_trans_data.Year == selected_year)]

                                        if st.button("Get"):

                                            if selected_state and selected_year:
                                                st.success(f"Showing insights for Year: {selected_year} and State: {selected_state}")
                                                fig_Q_wise_trans_dis = px.bar(Q_wise_trans_dis, x = "Quarter", 
                                                                            y = "Amount",
                                                                            title=f'Distribution of Transaction Amount in {selected_state} ({selected_year})', 
                                                                            text = [Convert.rupees(amount) for amount in Q_wise_trans_dis['Amount']],
                                                                            color='Transaction_Type',
                                                                            color_discrete_sequence = px.colors.qualitative.Alphabet,
                                                                            barmode="group")
                                                fig_Q_wise_trans_dis.update_traces(hovertemplate="Quarter: %{x}<br>Amount: %{text}")
                                                
                                                fig_Q_wise_trans_dis.update_layout(xaxis=dict(title='Quarter'), 
                                                                                                        yaxis=dict(title="Amount"))
                                                fig_Q_wise_trans_dis.update_traces(textposition='outside')
                                                fig_Q_wise_trans_dis.update_yaxes(type='log', dtick=1)
                                                st.plotly_chart(fig_Q_wise_trans_dis, use_container_width=True)
                                                


                                                Q_wise_trans_count = agg_trans_data.loc[(agg_trans_data.State == selected_state )&(agg_trans_data.Year == selected_year)]
                                                fig_Q_wise_trans_count = px.bar(Q_wise_trans_count, x = "Quarter", 
                                                                            y = "Trans_Count",
                                                                            title=f'Distribution of Transaction Count in {selected_state} ({selected_year})', 
                                                                            text = [Convert.rupees(amount) for amount in Q_wise_trans_count['Trans_Count']],
                                                                            color='Transaction_Type',
                                                                            color_discrete_sequence = px.colors.qualitative.Alphabet,
                                                                            barmode="group")
                                        
                                                fig_Q_wise_trans_count.update_layout(xaxis=dict(title='Quarter'), 
                                                                                                        yaxis=dict(title="Transaction Count"))                                            
                                                fig_Q_wise_trans_count.update_traces(hovertemplate="Quarter: %{x}<br>Amount: %{text}")
                                                fig_Q_wise_trans_count.update_traces(textposition='outside')
                                                fig_Q_wise_trans_count.update_yaxes(type='log', dtick=1)
                                                st.plotly_chart(fig_Q_wise_trans_count, use_container_width=True)
                                                col1, col2 = st.columns(2)
                                                with col1:
                                                    st.header("Transaction Amount")
                                                    st.dataframe(Q_wise_trans_dis.loc[:,["Year","Quarter","Transaction_Type","Amount"]].style.format({'Year': '{:.0f}'}),hide_index=True)
                                                with col2:
                                                    st.header("Transaction Count")
                                                    st.dataframe(Q_wise_trans_count.loc[:,["Year","Quarter","Transaction_Type","Trans_Count"]].style.format({'Year': '{:.0f}'}),hide_index=True)

                                            else:
                                                st.warning("Please select all the above options")
                                    Q_wise_trans_dis()

                            if selected_query:
                                if selected_query == statewise_transaction_queries[2]:

                                    def comp_transtype_on_q_y():
                                        st.info("You selected: Comparision of  data for the specific transaction type, quarter, and year")

                                        selected_year = st.selectbox("Select Year", sorted(agg_trans_data['Year'].unique()),index= None)
                                        selected_quarter = st.selectbox("Select Quarter", sorted(agg_trans_data['Quarter'].unique()),index= None)
                                        selected_trans_type = st.selectbox("Select Transaction Type", sorted(agg_trans_data['Transaction_Type'].unique()),index= None)

                                        comp_transtype_on_q_y = agg_trans_data.loc[(agg_trans_data.Year == selected_year )&(agg_trans_data.Quarter == selected_quarter)&(agg_trans_data.Transaction_Type == selected_trans_type )]

                                        if st.button("Get"):

                                            if selected_year and selected_quarter:
                                                st.success(f"Showing insights for Year: {selected_year} ,Quarter: {selected_quarter} and Transaction Type: {selected_trans_type}")


                                                fig_comp_transtype_on_q_y = px.scatter(comp_transtype_on_q_y, x="State", y="Amount", color_discrete_sequence=["purple"], title= f"Comparison of Transaction Amounts for Transaction Types in Q{selected_quarter} {selected_year}")
                                                fig_comp_transtype_on_q_y.update_layout(xaxis=dict(title='State'), 
                                                                                                        yaxis=dict(title="Amount"))                                           
                                                fig_comp_transtype_on_q_y.update_yaxes(type='log', dtick=1)
                                                fig_comp_transtype_on_q_y.update_traces(text = [Convert.rupees(amount) for amount in comp_transtype_on_q_y['Amount']],hovertemplate="State: %{x}<br>Amount: %{text}")
                                                fig_comp_transtype_on_q_y.update_layout(title_font_size=20)
                                                st.plotly_chart(fig_comp_transtype_on_q_y, use_container_width=True)

                                                fig_comp_transtype_on_q_y_count = px.scatter(comp_transtype_on_q_y, x="State", y="Trans_Count", color_discrete_sequence=["purple"], title= f"Comparison of Transaction Count for Transaction Types in Q{selected_quarter} {selected_year}")
                                                fig_comp_transtype_on_q_y_count.update_yaxes(type='log', dtick=1)
                                                fig_comp_transtype_on_q_y_count.update_layout(xaxis=dict(title='State'), 
                                                                                                        yaxis=dict(title="Transaction Count"))                                           
                                                fig_comp_transtype_on_q_y_count.update_traces(text = [Convert.rupees(amount) for amount in comp_transtype_on_q_y['Trans_Count']],hovertemplate="State: %{x}<br>Transaction Count: %{text}")
                                                fig_comp_transtype_on_q_y_count.update_layout(title_font_size=20)
                                                st.plotly_chart(fig_comp_transtype_on_q_y_count, use_container_width=True)
                                                st.dataframe(comp_transtype_on_q_y.loc[:,["State","Transaction_Type","Amount","Trans_Count"]], hide_index=True)                                                  

                                            else:
                                                st.warning("Please select all the above options")

                                    comp_transtype_on_q_y()
                            if selected_query:
                                if selected_query == statewise_transaction_queries[3]:
                                    def transaction_type_counts():
                                        see_aggregate = st.toggle('Show Aggregate')
                                        if not see_aggregate:
                                            selected_year = st.select_slider("Select Year", sorted(agg_trans_data['Year'].unique()))
                                            selected_state = st.selectbox("Select State", sorted(agg_trans_data['State'].unique()))
                                            transaction_type_counts = agg_trans_data.loc[(agg_trans_data.State == selected_state)&(agg_trans_data.Year == selected_year)].groupby('Transaction_Type', as_index=  False).Trans_Count.sum()
                                            formated_transcount = [Convert.rupees(amount) for amount in transaction_type_counts['Trans_Count']]

                                            # Plotting the distribution of transactions across different transaction types using a pie chart
                                            fig2 = px.bar(transaction_type_counts, 
                                                        x='Transaction_Type',
                                                        y='Trans_Count',
                                                        title='Distribution of Transactions Across Different Transaction Types', 
                                                        color = "Transaction_Type",
                                                        text = formated_transcount,
                                                        color_discrete_sequence= px.colors.cyclical.Twilight_r)


                                            fig2.update_layout(xaxis=dict(title='Transaction Type'), 
                                                            yaxis=dict(title='Transaction Count'))
                                            fig2.update_traces(hovertemplate="Trans_Count: %{text}")  
                                            fig2.update_yaxes(type='log', dtick= 1)
                                            fig2.update_traces(textposition='outside')
                                            fig2.update_layout(legend_title_text='Transaction Type')

                                            st.plotly_chart(fig2, use_container_width=True)     
                                            st.dataframe(transaction_type_counts.loc[:, ["Transaction_Type", "Trans_Count"]].sort_values("Trans_Count", ascending=False).reset_index(drop=True),hide_index=True)
                                        
                                        if see_aggregate:
                                            transaction_type_counts = agg_trans_data.groupby('Transaction_Type', as_index=  False).Trans_Count.sum()
                                            formated_transcount = [Convert.rupees(amount) for amount in transaction_type_counts['Trans_Count']]

                                            # Plotting the distribution of transactions across different transaction types using a pie chart
                                            fig2 = px.bar(transaction_type_counts, 
                                                        x='Transaction_Type',
                                                        y='Trans_Count',
                                                        title='Distribution of Transactions Across Different Transaction Types', 
                                                        color = "Transaction_Type",
                                                        text = formated_transcount,
                                                        color_discrete_sequence= px.colors.cyclical.Twilight_r)


                                            fig2.update_layout(xaxis=dict(title='Transaction Type'), 
                                                            yaxis=dict(title='Transaction Count'))
                                            fig2.update_traces(hovertemplate="Trans_Count: %{text}")  
                                            fig2.update_yaxes(type='log', dtick= 1)
                                            fig2.update_traces(textposition='outside')
                                            fig2.update_layout(legend_title_text='Transaction Type')

                                            st.plotly_chart(fig2, use_container_width=True)     
                                            st.dataframe(transaction_type_counts.loc[:, ["Transaction_Type", "Trans_Count"]].sort_values("Trans_Count", ascending=False).reset_index(drop=True),hide_index=True)                                    
                                    transaction_type_counts()

                        
                        state_wise_trans()

                    # District Wise Transactions  
                    if trans_type == "District Wise":

                        def district_wise_trans():

                            districtwise_transaction_queries = ["Year-wise Growth of Transaction Data by District",
                                                                "Transaction Amount & Transaction count distribution by district for selected state and year",
                                                                "Total Sum of Amount by State Across All Districts"]
                            
                            selected_query = st.selectbox("Select a Query", districtwise_transaction_queries,index= None)

                            if selected_query:
                                if selected_query == districtwise_transaction_queries[0]:  
                                    
                                    def year_wise_amount_growth_by_dist():
                                        st.info("You selected: Year-wise Growth of Transaction by District")

                                        selected_state = st.selectbox("Select State", sorted(map_trans_data.State.unique()),index= None)
                                        selected_district = st.selectbox("Select State", sorted(map_trans_data[map_trans_data.State == selected_state].District.unique()),index= None)
                                        year_district_wise_amount = map_trans_data.loc[(map_trans_data.State == selected_state ) & (map_trans_data.District == selected_district )].groupby(["Year"],as_index = False).Amount.sum()
                                


                                        if selected_state and selected_district:  
                                            

                                            if st.button("Get"):
                                                st.success(f"Showing insights for State: {selected_state} and District: {selected_district}")
                                            
                                                col1,col2 = st.columns(2)
                                                with col1:
                                                        formated_year_district_wise_amount = [Convert.rupees(amount) for amount in year_district_wise_amount['Amount']]
                                                        year_district_wise_amount_fig = px.bar(year_district_wise_amount, 
                                                                                            x = "Year", 
                                                                                            y = "Amount", 
                                                                                            color = "Amount", 
                                                                                            title = f"Year-wise Amount for state {selected_state} District {selected_district}",
                                                                                            text = formated_year_district_wise_amount,
                                                                                            color_continuous_scale= px.colors.diverging.Spectral_r)
                                                        year_district_wise_amount_fig.update_traces(hovertemplate="Year: %{x}<br>Amount: %{text}")
                                                        year_district_wise_amount_fig.update_traces(textposition='outside')
                                                        st.plotly_chart(year_district_wise_amount_fig, use_container_width=True)

                                                with col2:
                                                        year_district_wise_tc = map_trans_data.loc[(map_trans_data.State == selected_state ) & (map_trans_data.District == selected_district )].groupby(["Year"],as_index = False).Trans_Count.sum()

                                                        formated_year_district_wise_tc = [Convert.rupees(amount) for amount in year_district_wise_tc['Trans_Count']]
                                                        year_district_wise_tc_fig = px.bar(year_district_wise_tc, 
                                                                                            x = "Year", 
                                                                                            y = "Trans_Count", 
                                                                                            color = "Trans_Count", 
                                                                                            title = f"Year-wise Transcation Count for State: {selected_state} District {selected_district}",
                                                                                            text = formated_year_district_wise_tc,
                                                                                            color_continuous_scale= px.colors.diverging.Spectral_r)
                                                        year_district_wise_tc_fig.update_traces(hovertemplate="Year: %{x}<br>Transaction Count: %{text}")
                                                        year_district_wise_tc_fig.update_layout(xaxis=dict(title='Year'), 
                                                            yaxis=dict(title='Transaction Count'))
                                                        year_district_wise_tc_fig.update_traces(textposition='outside')
                                                        st.plotly_chart(year_district_wise_tc_fig, use_container_width=True)
                                                st.dataframe(map_trans_data.loc[(map_trans_data.State == selected_state ) & (map_trans_data.District == selected_district )].groupby(["Year"],as_index = False).agg({"Amount":"sum","Trans_Count":"sum"}).style.format({'Year': '{:.0f}'}),hide_index=True)

                                        else:
                                            st.warning("Please select all the above options")                                               

                                    year_wise_amount_growth_by_dist()



                            if selected_query:
                                if selected_query == districtwise_transaction_queries[1]:   
                                    def tc_by_dist_state_year_wise():
                                        st.info("You selected: Transaction distribution by district for selected state and year")

                                        selected_state = st.selectbox("Select State", sorted(map_trans_data.State.unique()),index= None)
                                        selected_year = st.selectbox("Select Year", sorted(map_trans_data.Year.unique()),index= None)
                                        state_wise_dist_tc = map_trans_data.loc[(map_trans_data.Year== selected_year) & (map_trans_data.State == selected_state)].groupby(["District","Year"],as_index = False).Trans_Count.sum()
                                
                                        if st.button("Get"):

                                            if selected_state and selected_year:
                                                st.success(f"Showing insights for State: {selected_state} and Year: {selected_year}")
                                                state_wise_dist_amount = map_trans_data.loc[(map_trans_data.Year== selected_year) & (map_trans_data.State == selected_state)].groupby(["District","Year"],as_index = False).Amount.sum()
                                                formated_state_wise_dist_amount = [Convert.rupees(amount) for amount in state_wise_dist_amount['Amount']]
                                                state_wise_dist_amount_fig = px.scatter(state_wise_dist_amount, 
                                                                                    x="District", 
                                                                                    y="Amount",color_discrete_sequence=["purple"],
                                                                                    title = f"District-wise Transaction Amount Distribution in {selected_state} - {selected_year}")
                                                state_wise_dist_amount_fig.update_traces(hovertemplate="District: %{x}<br>Transaction Amount: %{customdata}", customdata=formated_state_wise_dist_amount, hoverinfo="x+y+text")
                                                state_wise_dist_amount_fig.update_yaxes(type='log', dtick=1, title = "Transaction Amount")
                                                state_wise_dist_amount_fig.update_layout(xaxis_tickangle=-90)
                                                st.plotly_chart(state_wise_dist_amount_fig, use_container_width=True)
                                            

                                                state_wise_dist_tc = map_trans_data.loc[(map_trans_data.Year== selected_year) & (map_trans_data.State == selected_state)].groupby(["District","Year"],as_index = False).Trans_Count.sum()
                                                formated_state_wise_dist_tc = [Convert.rupees(amount) for amount in state_wise_dist_tc['Trans_Count']]
                                                state_wise_dist_tc_fig = px.scatter(state_wise_dist_tc, 
                                                                                    x="District", 
                                                                                    y="Trans_Count",
                                                                                    title = f"District-wise Transaction count Distribution in {selected_state} - {selected_year}")
                                                state_wise_dist_tc_fig.update_traces(hovertemplate="District: %{x}<br>Transaction Count: %{customdata}", customdata=formated_state_wise_dist_tc, hoverinfo="x+y+text")
                                                state_wise_dist_tc_fig.update_yaxes(type='log', dtick=1, title = "Transaction Count")
                                                state_wise_dist_tc_fig.update_layout(xaxis_tickangle=-90)
                                                st.plotly_chart(state_wise_dist_tc_fig, use_container_width=True)
                                                st.dataframe(map_trans_data.loc[(map_trans_data.Year== selected_year) & (map_trans_data.State == selected_state)].groupby(["District","Year"],as_index = False).agg({"Amount":"sum","Trans_Count": "sum"}).style.format({'Year': '{:.0f}'}),hide_index=True)
                                            else:
                                                st.warning("Please select all the above options")
                                    
                                    tc_by_dist_state_year_wise()

                            if selected_query:
                                if selected_query == districtwise_transaction_queries[2]:   
                                    def dist_wise_total_amnt_sum():
                                        st.info("You selected: Total Sum of Transactions by State Across All Districts")

                                        selected_state = st.selectbox("Select State", sorted(map_trans_data.State.unique()),index= None)
                                        dist_wise_total_amnt_sum = map_trans_data.loc[(map_trans_data.State == selected_state)].groupby("District",as_index = False).Amount.sum()
                                
                                        if st.button("Get"):

                                            if selected_state:
                                                st.success(f"Showing insights for State: {selected_state}")

                                                formated_dist_wise_total_amnt_sum = [Convert.rupees(amount) for amount in dist_wise_total_amnt_sum['Amount']]
                                                dist_wise_total_amnt_sum_fig = px.bar(dist_wise_total_amnt_sum, 
                                                                                    x = "District",
                                                                                    y = "Amount", 
                                                                                    color_discrete_sequence=["purple"],
                                                                                    title = f"Total Sum of Amount in {selected_state} by District",
                                                                                    text = formated_dist_wise_total_amnt_sum)
                                                dist_wise_total_amnt_sum_fig.update_traces(hovertemplate="District: %{x}<br>Amount: %{text}")
                                                dist_wise_total_amnt_sum_fig.update_traces(textposition='outside')
                                                dist_wise_total_amnt_sum_fig.update_yaxes(title = "Total Amount")
                                                dist_wise_total_amnt_sum_fig.update_layout(xaxis_tickangle=-90)
                                                st.plotly_chart(dist_wise_total_amnt_sum_fig, use_container_width=True)


                                                dist_wise_total_tc_sum = map_trans_data.loc[(map_trans_data.State == selected_state)].groupby("District",as_index = False).Trans_Count.sum()
                                                formated_dist_wise_total_tc_sum = [Convert.rupees(amount) for amount in dist_wise_total_tc_sum['Trans_Count']]
                                                dist_wise_total_tc_sum_fig = px.bar(dist_wise_total_tc_sum, 
                                                                                    x = "District",
                                                                                    y = "Trans_Count", 
                                                                                    color_discrete_sequence=["gray"],
                                                                                    title = f"Total Sum of Transaction Count in {selected_state} by District",
                                                                                    text = formated_dist_wise_total_tc_sum)
                                                dist_wise_total_tc_sum_fig.update_traces(hovertemplate="District: %{x}<br>Transaction Count: %{text}")
                                                dist_wise_total_tc_sum_fig.update_traces(textposition='outside')
                                                dist_wise_total_tc_sum_fig.update_yaxes(title = "Transaction Count")
                                                dist_wise_total_tc_sum_fig.update_layout(xaxis_tickangle=-90)
                                                st.plotly_chart(dist_wise_total_tc_sum_fig, use_container_width=True)
                                                st.dataframe(map_trans_data.loc[(map_trans_data.State == selected_state)].groupby("District",as_index = False).agg({"Amount":"sum","Trans_Count": "sum"}),hide_index=True)

                                            else:
                                                st.warning("Please select all the above options")
                                    
                                    dist_wise_total_amnt_sum()
                            
                        #outer function
                        district_wise_trans()
                filter_trans()   

            if filter_type == 'Insurance':
                def filter_ins():
                    trans_filter_container =  st.container(border = True)
                    trans_type = trans_filter_container.radio("Select Type", ["State Wise", "District Wise"], index= None,horizontal=True)
                    
                    # State Wise Insurance
                    if trans_type == "State Wise":
                        
                        def state_wise_ins():
                            statewise_Insurance_queries = ["Quarter-wise Insurance amount & count distribution for specific state"]
                            
                            selected_query = st.selectbox("Select a Query", statewise_Insurance_queries,index= None)


                            if selected_query:
                                if selected_query == statewise_Insurance_queries[0]:  # Query 2

                                    def Q_wise_ins_dis():
                                        st.info("You selected: Quarter-wise Insurance amount & count distribution for specific state")
                                        
                                        selected_year = st.selectbox("Select Year", sorted(agg_ins_data['Year'].unique()),index= None)
                                        selected_state = st.selectbox("Select State", sorted(agg_ins_data['State'].unique()),index= None)

                                        Q_wise_ins_dis = agg_ins_data.loc[(agg_ins_data.State == selected_state )&(agg_ins_data.Year == selected_year)]

                                        if st.button("Get"):

                                            if selected_state and selected_year:
                                                st.success(f"Showing insights for Year: {selected_year} and State: {selected_state}")
                                                fig_Q_wise_ins_dis = px.bar(Q_wise_ins_dis, x = "Quarter", 
                                                                            y = "Amount",
                                                                            title=f'Distribution of Insurance Amount in {selected_state} ({selected_year})', 
                                                                            text = [Convert.rupees(amount) for amount in Q_wise_ins_dis['Amount']],
                                                                            color='Amount',
                                                                            color_continuous_scale = px.colors.sequential.dense,
                                                                            )
                                                fig_Q_wise_ins_dis.update_traces(hovertemplate="Quarter: %{x}<br>Amount: %{text}")
                                                
                                                fig_Q_wise_ins_dis.update_layout(xaxis=dict(title='Quarter'), 
                                                                                                        yaxis=dict(title="Amount"))
                                                fig_Q_wise_ins_dis.update_traces(textposition='outside')
                                                fig_Q_wise_ins_dis.update_xaxes(title_text='Quarter', tickvals=[1, 2, 3, 4], ticktext=['Q1', 'Q2', 'Q3', 'Q4'])
                                                fig_Q_wise_ins_dis.update_yaxes(type='log', dtick=1)
                                                st.plotly_chart(fig_Q_wise_ins_dis, use_container_width=True)
                                                


                                                Q_wise_ins_count = agg_ins_data.loc[(agg_ins_data.State == selected_state )&(agg_ins_data.Year == selected_year)]
                                                fig_Q_wise_ins_count = px.bar(Q_wise_ins_count, x = "Quarter", 
                                                                            y = "Insurance_Count",
                                                                            title=f'Distribution of Insurance Count in {selected_state} ({selected_year})', 
                                                                            text = [Convert.rupees(amount) for amount in Q_wise_ins_count['Insurance_Count']],
                                                                            color='Insurance_Count',
                                                                            color_continuous_scale = px.colors.sequential.dense,
                                                                            barmode="group")
                                        
                                                fig_Q_wise_ins_count.update_layout(xaxis=dict(title='Quarter'), 
                                                                                                        yaxis=dict(title="Insurance Count"))                                            
                                                fig_Q_wise_ins_count.update_traces(hovertemplate="Quarter: %{x}<br>Amount: %{text}")
                                                fig_Q_wise_ins_count.update_xaxes(title_text='Quarter', tickvals=[1, 2, 3, 4], ticktext=['Q1', 'Q2', 'Q3', 'Q4'])
                                                fig_Q_wise_ins_count.update_traces(textposition='outside')
                                                fig_Q_wise_ins_count.update_yaxes(type='log', dtick=1)
                                                st.plotly_chart(fig_Q_wise_ins_count, use_container_width=True)

                                                st.header("Insurance Amount")
                                                st.dataframe(Q_wise_ins_dis.loc[:,["Year","Quarter","Amount","Insurance_Count"]].style.format({'Year': '{:.0f}'}),hide_index=True)
                                 

                                            else:
                                                st.warning("Please select all the above options")
                                    Q_wise_ins_dis()
                        
                        state_wise_ins()

                    # District Wise Insurance  
                    if trans_type == "District Wise":

                        def district_wise_ins():

                            districtwise_Insurance_queries = ["Year-wise Growth of Insurance Data by District",
                                                                "Insurance Amount & Insurance count distribution by district for selected state and year",
                                                                "Total Sum of Insurance by District Across All Districts"]
                            
                            selected_query = st.selectbox("Select a Query", districtwise_Insurance_queries,index= None)

                            if selected_query:
                                if selected_query == districtwise_Insurance_queries[0]:  
                                    
                                    def year_wise_amount_growth_by_dist():
                                        st.info("Year-wise Growth of Insurance Data by District")

                                        selected_state = st.selectbox("Select State", sorted(map_ins_data.State.unique()),index= None)
                                        selected_district = st.selectbox("Select State", sorted(map_ins_data[map_ins_data.State == selected_state].District.unique()),index= None)
                                        year_district_wise_amount = map_ins_data.loc[(map_ins_data.State == selected_state ) & (map_ins_data.District == selected_district )].groupby(["Year"],as_index = False).Amount.sum()
                                
  

                                        if st.button("Get"):
                                            if selected_state and selected_district:  
                                                st.success(f"Showing insights for State: {selected_state} and District: {selected_district}")
                                            
                                                col1,col2 = st.columns(2)
                                                with col1:
                                                        formated_year_district_wise_amount = [Convert.rupees(amount) for amount in year_district_wise_amount['Amount']]
                                                        year_district_wise_amount_fig = px.bar(year_district_wise_amount, 
                                                                                            x = "Year", 
                                                                                            y = "Amount", 
                                                                                            color = "Amount", 
                                                                                            title = f"Year-wise Insurance Amount for state {selected_state} District {selected_district}",
                                                                                            text = formated_year_district_wise_amount,
                                                                                            color_continuous_scale= px.colors.diverging.Spectral_r)
                                                        year_district_wise_amount_fig.update_traces(hovertemplate="Year: %{x}<br>Amount: %{text}")
                                                        year_district_wise_amount_fig.update_traces(textposition='outside')
                                                        st.plotly_chart(year_district_wise_amount_fig, use_container_width=True)

                                                with col2:
                                                        year_district_wise_tc = map_ins_data.loc[(map_ins_data.State == selected_state ) & (map_ins_data.District == selected_district )].groupby(["Year"],as_index = False).Insurance_Count.sum()

                                                        formated_year_district_wise_tc = [Convert.rupees(amount) for amount in year_district_wise_tc['Insurance_Count']]
                                                        year_district_wise_tc_fig = px.bar(year_district_wise_tc, 
                                                                                            x = "Year", 
                                                                                            y = "Insurance_Count", 
                                                                                            color = "Insurance_Count", 
                                                                                            title = f"Year-wise Insurance_Count for State: {selected_state} District {selected_district}",
                                                                                            text = formated_year_district_wise_tc,
                                                                                            color_continuous_scale= px.colors.diverging.Spectral_r)
                                                        year_district_wise_tc_fig.update_traces(hovertemplate="Year: %{x}<br>Insurance Count: %{text}")
                                                        year_district_wise_tc_fig.update_layout(xaxis=dict(title='Year'), 
                                                            yaxis=dict(title='Insurance Count'))
                                                        year_district_wise_tc_fig.update_traces(textposition='outside')
                                                        st.plotly_chart(year_district_wise_tc_fig, use_container_width=True)
                                                st.dataframe(map_ins_data.loc[(map_ins_data.State == selected_state ) & (map_ins_data.District == selected_district )].groupby(["Year"],as_index = False).agg({"Amount":"sum","Insurance_Count":"sum"}).style.format({'Year': '{:.0f}'}),hide_index=True)

                                            else:
                                                st.warning("Please select all the above options")                                               

                                    year_wise_amount_growth_by_dist()



                            if selected_query:
                                if selected_query == districtwise_Insurance_queries[1]:   
                                    def tc_by_dist_state_year_wise():
                                        st.info("You selected: Insurance Amount & Insurance count distribution by district for selected state and year")

                                        selected_state = st.selectbox("Select State", sorted(map_ins_data.State.unique()),index= None)
                                        selected_year = st.selectbox("Select Year", sorted(map_ins_data.Year.unique()),index= None)
                                        state_wise_dist_tc = map_ins_data.loc[(map_ins_data.Year== selected_year) & (map_ins_data.State == selected_state)].groupby(["District","Year"],as_index = False).Insurance_Count.sum()
                                
                                        if st.button("Get"):

                                            if selected_state and selected_year:
                                                st.success(f"Showing insights for State: {selected_state} and Year: {selected_year}")
                                                state_wise_dist_amount = map_ins_data.loc[(map_ins_data.Year== selected_year) & (map_ins_data.State == selected_state)].groupby(["District","Year"],as_index = False).Amount.sum()
                                                formated_state_wise_dist_amount = [Convert.rupees(amount) for amount in state_wise_dist_amount['Amount']]
                                                state_wise_dist_amount_fig = px.scatter(state_wise_dist_amount, 
                                                                                    x="District", 
                                                                                    y="Amount",color_discrete_sequence=["purple"],
                                                                                    title = f"District-wise Insurance Amount Distribution in {selected_state} - {selected_year}")
                                                state_wise_dist_amount_fig.update_traces(hovertemplate="District: %{x}<br>Insurance Amount: %{customdata}", customdata=formated_state_wise_dist_amount, hoverinfo="x+y+text")
                                                state_wise_dist_amount_fig.update_yaxes(type='log', dtick=1, title = "Insurance Amount")
                                                state_wise_dist_amount_fig.update_layout(xaxis_tickangle=-90)
                                                st.plotly_chart(state_wise_dist_amount_fig, use_container_width=True)
                                            

                                                state_wise_dist_tc = map_ins_data.loc[(map_ins_data.Year== selected_year) & (map_ins_data.State == selected_state)].groupby(["District","Year"],as_index = False).Insurance_Count.sum()
                                                formated_state_wise_dist_tc = [Convert.rupees(amount) for amount in state_wise_dist_tc['Insurance_Count']]
                                                state_wise_dist_tc_fig = px.scatter(state_wise_dist_tc, 
                                                                                    x="District", 
                                                                                    y="Insurance_Count",
                                                                                    title = f"District-wise Insurance count Distribution in {selected_state} - {selected_year}")
                                                state_wise_dist_tc_fig.update_traces(hovertemplate="District: %{x}<br>Insurance Count: %{customdata}", customdata=formated_state_wise_dist_tc, hoverinfo="x+y+text")
                                                state_wise_dist_tc_fig.update_yaxes(type='log', dtick=1, title = "Insurance Count")
                                                state_wise_dist_tc_fig.update_layout(xaxis_tickangle=-90)
                                                st.plotly_chart(state_wise_dist_tc_fig, use_container_width=True)
                                                st.dataframe(map_ins_data.loc[(map_trans_data.Year== selected_year) & (map_trans_data.State == selected_state)].groupby(["District","Year"],as_index = False).agg({"Amount":"sum","Insurance_Count": "sum"}).style.format({'Year': '{:.0f}'}),hide_index=True)
                                            else:
                                                st.warning("Please select all the above options")
                                    
                                    tc_by_dist_state_year_wise()

                            if selected_query:
                                if selected_query == districtwise_Insurance_queries[2]:   
                                    def dist_wise_total_amnt_sum():
                                        st.info("You selected: Total Sum of Insurance by District Across All Districts")

                                        selected_state = st.selectbox("Select State", sorted(map_ins_data.State.unique()),index= None)
                                        dist_wise_total_amnt_sum = map_ins_data.loc[(map_ins_data.State == selected_state)].groupby("District",as_index = False).Amount.sum()
                                
                                        if st.button("Get"):

                                            if selected_state:
                                                st.success(f"Showing insights for State: {selected_state}")

                                                formated_dist_wise_total_amnt_sum = [Convert.rupees(amount) for amount in dist_wise_total_amnt_sum['Amount']]
                                                dist_wise_total_amnt_sum_fig = px.bar(dist_wise_total_amnt_sum, 
                                                                                    x = "District",
                                                                                    y = "Amount", 
                                                                                    color_discrete_sequence=["purple"],
                                                                                    title = f"Total Sum of Insurance Amount in {selected_state} by District",
                                                                                    text = formated_dist_wise_total_amnt_sum)
                                                dist_wise_total_amnt_sum_fig.update_traces(hovertemplate="District: %{x}<br>Amount: %{text}")
                                                dist_wise_total_amnt_sum_fig.update_traces(textposition='outside')
                                                dist_wise_total_amnt_sum_fig.update_yaxes(title = "Total Insurance Amount")
                                                dist_wise_total_amnt_sum_fig.update_layout(xaxis_tickangle=-90)
                                                st.plotly_chart(dist_wise_total_amnt_sum_fig, use_container_width=True)


                                                dist_wise_total_tc_sum = map_ins_data.loc[(map_ins_data.State == selected_state)].groupby("District",as_index = False).Insurance_Count.sum()
                                                formated_dist_wise_total_tc_sum = [Convert.rupees(amount) for amount in dist_wise_total_tc_sum['Insurance_Count']]
                                                dist_wise_total_tc_sum_fig = px.bar(dist_wise_total_tc_sum, 
                                                                                    x = "District",
                                                                                    y = "Insurance_Count", 
                                                                                    color_discrete_sequence=["gray"],
                                                                                    title = f"Total Sum of Insurance Count in {selected_state} by District",
                                                                                    text = formated_dist_wise_total_tc_sum)
                                                dist_wise_total_tc_sum_fig.update_traces(hovertemplate="District: %{x}<br>Insurance Count: %{text}")
                                                dist_wise_total_tc_sum_fig.update_traces(textposition='outside')
                                                dist_wise_total_tc_sum_fig.update_yaxes(title = "Insurance Count")
                                                dist_wise_total_tc_sum_fig.update_layout(xaxis_tickangle=-90)
                                                st.plotly_chart(dist_wise_total_tc_sum_fig, use_container_width=True)
                                                st.dataframe(map_ins_data.loc[(map_ins_data.State == selected_state)].groupby("District",as_index = False).agg({"Amount":"sum","Insurance_Count": "sum"}),hide_index=True)

                                            else:
                                                st.warning("Please select all the above options")
                                    
                                    dist_wise_total_amnt_sum()
                            
                        #outer function
                        district_wise_ins()
                filter_ins()                    

            if filter_type == 'Users':
                def filter_users():
                    trans_filter_container =  st.container(border = True)
                    trans_type = trans_filter_container.radio("Select Type", ["State Wise", "District Wise"], index= None,horizontal=True)
                    
                    # State Wise Insurance
                    if trans_type == "State Wise":
                        
                        def state_wise_users():
                            statewise_Insurance_queries = ["Quarter-wise User Count for specific state"]
                            
                            selected_query = st.selectbox("Select a Query", statewise_Insurance_queries,index= None)


                            if selected_query:
                                if selected_query == statewise_Insurance_queries[0]:  # Query 2

                                    def Q_wise_users_dis():
                                        st.info("You selected: Quarter-wise User Count for specific state")
                                        
                                        selected_year = st.selectbox("Select Year", sorted(map_user_data['Year'].unique()),index= None)
                                        selected_state = st.selectbox("Select State", sorted(map_user_data['State'].unique()),index= None)

                                        Q_wise_users_dis = map_user_data.loc[(map_user_data.State == selected_state )&(map_user_data.Year == selected_year)].groupby(["State","Quarter"], as_index = False).Registered_Users.sum()

                                        if st.button("Get"):

                                            if selected_state and selected_year:
                                                st.success(f"Showing insights for Year: {selected_year} and State: {selected_state}")
                                                fig_Q_wise_users_dis = px.bar(Q_wise_users_dis, x = "Quarter", 
                                                                            y = "Registered_Users",
                                                                            title=f'Distribution of Registered Users in {selected_state} ({selected_year})', 
                                                                            text = [Convert.rupees(amount) for amount in Q_wise_users_dis['Registered_Users']],
                                                                            color='Registered_Users',
                                                                            color_continuous_scale = px.colors.sequential.dense,
                                                                            )
                                                fig_Q_wise_users_dis.update_traces(hovertemplate="Quarter: %{x}<br>Registered Users: %{text}")
                                                
                                                fig_Q_wise_users_dis.update_layout(xaxis=dict(title='Quarter'), 
                                                                                                        yaxis=dict(title="Registered Users"))
                                                fig_Q_wise_users_dis.update_traces(textposition='outside')
                                                fig_Q_wise_users_dis.update_xaxes(title_text='Quarter', tickvals=[1, 2, 3, 4], ticktext=['Q1', 'Q2', 'Q3', 'Q4'])
                                                fig_Q_wise_users_dis.update_yaxes(type='log', dtick=1)
                                                st.plotly_chart(fig_Q_wise_users_dis, use_container_width=True)
                                                
                                                st.dataframe(Q_wise_users_dis.loc[:,["Quarter","Registered_Users"]].style.format({'Year': '{:.0f}'}),hide_index=True)
                                 

                                            else:
                                                st.warning("Please select all the above options")
                                    Q_wise_users_dis()
                        
                        state_wise_users()

                    # District Wise Insurance  
                    if trans_type == "District Wise":

                        def district_wise_users():

                            districtwise_Insurance_queries = ["Year-wise Growth of Users by District",
                                                                "User distribution by district for selected state and year",
                                                                "Total Sum of Users by District Across All Districts"]
                            
                            selected_query = st.selectbox("Select a Query", districtwise_Insurance_queries,index= None)

                            if selected_query:
                                if selected_query == districtwise_Insurance_queries[0]:  
                                    
                                    def year_wise_user_growth_by_dist():
                                        st.info("Year-wise Growth of Users by District")

                                        selected_state = st.selectbox("Select State", sorted(map_user_data.State.unique()),index= None)
                                        selected_district = st.selectbox("Select State", sorted(map_user_data[map_user_data.State == selected_state].District.unique()),index= None)
                                        year_district_wise_amount = map_user_data.loc[(map_user_data.State == selected_state ) & (map_user_data.District == selected_district )].groupby(["Year"],as_index = False).Registered_Users.sum()
                                
  

                                        if st.button("Get"):
                                            if selected_state and selected_district:  
                                                st.success(f"Showing insights for State: {selected_state} and District: {selected_district}")
                                            
                            
                                                formated_year_district_wise_user = [Convert.rupees(amount) for amount in year_district_wise_amount['Registered_Users']]
                                                year_district_wise_user_fig = px.bar(year_district_wise_amount, 
                                                                                    x = "Year", 
                                                                                    y = "Registered_Users", 
                                                                                    color = "Registered_Users", 
                                                                                    title = f"Year-wise Registered Users for state {selected_state} District {selected_district}",
                                                                                    text = formated_year_district_wise_user,
                                                                                    color_continuous_scale= px.colors.diverging.Spectral_r)
                                                year_district_wise_user_fig.update_traces(hovertemplate="Year: %{x}<br>Registered Users: %{text}")
                                                year_district_wise_user_fig.update_traces(textposition='outside')
                                                st.plotly_chart(year_district_wise_user_fig, use_container_width=True)
                                                st.dataframe(map_user_data.loc[(map_user_data.State == selected_state ) & (map_user_data.District == selected_district )].groupby(["Year"],as_index = False).agg({"Registered_Users":"sum"}).style.format({'Year': '{:.0f}'}),hide_index=True)

                                            else:
                                                st.warning("Please select all the above options")                                               

                                    year_wise_user_growth_by_dist()



                            if selected_query:
                                if selected_query == districtwise_Insurance_queries[1]:   
                                    def users_by_dist_state_year_wise():
                                        st.info("You selected: User distribution by district for selected state and year")

                                        selected_state = st.selectbox("Select State", sorted(map_user_data.State.unique()),index= None)
                                        selected_year = st.selectbox("Select Year", sorted(map_user_data.Year.unique()),index= None)
                           
                                        if st.button("Get"):

                                            if selected_state and selected_year:
                                                st.success(f"Showing insights for State: {selected_state} and Year: {selected_year}")
                                                state_wise_dist_users = map_user_data.loc[(map_user_data.Year== selected_year) & (map_user_data.State == selected_state)].groupby(["District","Year"],as_index = False).Registered_Users.sum()
                                                formated_state_wise_dist_amount = [Convert.rupees(amount) for amount in state_wise_dist_users['Registered_Users']]
                                                state_wise_dist_users_fig = px.scatter(state_wise_dist_users, 
                                                                                    x="District", 
                                                                                    y="Registered_Users",color_discrete_sequence=["purple"],
                                                                                    title = f"District-wise Insurance Amount Distribution in {selected_state} - {selected_year}")
                                                state_wise_dist_users_fig.update_traces(hovertemplate="District: %{x}<br>Registered Users: %{customdata}", customdata=formated_state_wise_dist_amount, hoverinfo="x+y+text")
                                                state_wise_dist_users_fig.update_yaxes(type='log', dtick=1, title = "Registered Users")
                                                state_wise_dist_users_fig.update_layout(xaxis_tickangle=-90)
                                                st.plotly_chart(state_wise_dist_users_fig, use_container_width=True)
                                                st.dataframe(map_user_data.loc[(map_user_data.Year== selected_year) & (map_user_data.State == selected_state)].groupby(["District","Year"],as_index = False).agg({"Registered_Users":"sum"}).style.format({'Year': '{:.0f}'}),hide_index=True)
                                            else:
                                                st.warning("Please select all the above options")
                                    
                                    users_by_dist_state_year_wise()

                            if selected_query:
                                if selected_query == districtwise_Insurance_queries[2]:   
                                    def dist_wise_total_users_sum():
                                        st.info("You selected: Total Sum of Users by District Across All Districts")

                                        selected_state = st.selectbox("Select State", sorted(map_user_data.State.unique()),index= None)
                                        dist_wise_total_amnt_sum = map_user_data.loc[(map_user_data.State == selected_state)].groupby("District",as_index = False).Registered_Users.sum()
                                
                                        if st.button("Get"):

                                            if selected_state:
                                                st.success(f"Showing insights for State: {selected_state}")

                                                formated_dist_wise_total_user_sum = [Convert.rupees(amount) for amount in dist_wise_total_amnt_sum['Registered_Users']]
                                                dist_wise_total_user_sum_fig = px.bar(dist_wise_total_amnt_sum, 
                                                                                    x = "District",
                                                                                    y = "Registered_Users", 
                                                                                    color_discrete_sequence=["purple"],
                                                                                    title = f"Total Sum of Registered Users in {selected_state} by District",
                                                                                    text = formated_dist_wise_total_user_sum)
                                                dist_wise_total_user_sum_fig.update_traces(hovertemplate="District: %{x}<br>Registered Users: %{text}")
                                                dist_wise_total_user_sum_fig.update_traces(textposition='outside')
                                                dist_wise_total_user_sum_fig.update_yaxes(title = "Total Registered Users")
                                                dist_wise_total_user_sum_fig.update_layout(xaxis_tickangle=-90)
                                                st.plotly_chart(dist_wise_total_user_sum_fig, use_container_width=True)
                                                st.dataframe(map_ins_data.loc[(map_ins_data.State == selected_state)].groupby("District",as_index = False).agg({"Amount":"sum","Insurance_Count": "sum"}),hide_index=True)

                                            else:
                                                st.warning("Please select all the above options")
                                    
                                    dist_wise_total_users_sum()
                            
                        #outer function
                        district_wise_users()
                filter_users() 


    filters()






