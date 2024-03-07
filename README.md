# Navin's Pulse Vision

Navin's Pulse Vision is a comprehensive data visualization project focused on analyzing PhonePe Pulse data. PhonePe is a leading Indian digital payments platform that empowers millions of users to seamlessly perform transactions, recharge phones, pay bills, and access various financial services.


## About PhonePe Pulse

PhonePe Pulse is an insightful feature provided by PhonePe that offers users and businesses access to valuable data insights. It provides detailed information on transaction trends, user behavior, and insurance data across different states and districts in India.


## Data Source

The data used in this analysis is derived from PhonePe Pulse, offering reliable and up-to-date information on various aspects of digital transactions, user engagement, and insurance trends.


## Project Overview

Navin's Pulse Vision aims to extract valuable insights from PhonePe Pulse data and present them in an easy-to-understand format. The project analyzes three main types of data:

1. **Transaction Data on States and Districts**: Contains state-wise and district-wise total transaction amount and count.
2. **User Data on States and Districts**: Includes state-wise and district-wise total user count.
3. **Insurance Data on States and Districts**: Provides state-wise and district-wise total insurance amount and insurance count.


## Analysis and Visualization

The project offers insightful analysis and visualization on various aspects of the provided data:


### Transaction Data Analysis:

- **Top 10 States with Highest and Lowest Transaction Amount**: Identifies states with the highest and lowest transaction amounts.
- **Average Transaction Value for Top 10 States**: Calculates the average transaction value for the top 10 states.
- **Top 10 Districts with Highest Transaction Amount**: Highlights districts with the highest transaction amounts.
- **Quarter-wise Transaction Amount Distribution for Specific State**: Visualizes transaction amount distribution across quarters for a specific state.


### User Data Analysis:

- **Top 10 States with Highest and Lowest Users**: Shows states with the highest and lowest number of users.
- **Top 10 Districts with Highest Users**: Highlights districts with the highest number of users.
- **Quarter-wise User Distribution for Specific State**: Presents user distribution across quarters for a specific state.


### Insurance Data Analysis:

- **Top 10 States with Highest and Lowest Insurance Amount**: Identifies states with the highest and lowest insurance amounts.
- **Top 10 Districts with Highest Insurance Amount**: Highlights districts with the highest insurance amounts.
- **Quarter-wise Insurance Amount Distribution for Specific State**: Visualizes insurance amount distribution across quarters for a specific state.


### Additional Insights:

- **Transaction Amount Growth for Specific State & Transaction Type**: Tracks transaction amount growth for a specific state and transaction type.
- **Year-wise Growth of Amount by District**: Illustrates the year-wise growth of transaction amounts by district.
- **Total Sum of Amount by District Across All Districts**: Presents the total sum of transaction amounts across all districts.


## Filter Options

Navin's Pulse Vision provides various filter options to analyze data more efficiently, including:

- Transaction Amount growth for a specific state & specific Transaction Type
- Quarter-wise transaction amount distribution for specific state
- Comparison of data for the specific transaction type, quarter, and year
- Distribution of Transactions Across Different Transaction Types for a specific state
- Year-wise Growth of Amount by District
- Transaction count distribution by district for selected state and year
- Transaction Amount & Transaction count distribution by district for selected state and year
- Year-wise Growth of Users by District
- User distribution by district for selected state and year
- Total Sum of Users by District Across All Districts
- Quarter-wise User Count for specific state
- Year-wise Growth of Insurance Data by District
- Insurance Amount & Insurance count distribution by district for selected state and year
- Total Sum of Amount by District Across All Districts


## Technologies Used

The project leverages a range of technologies to deliver efficient data analysis and visualization:

- **Backend Logic**: Implemented backend logic with Python, utilizing its robust capabilities for data processing and analysis.
- **Data Manipulation**: Utilized the powerful Pandas library for data manipulation, enabling seamless handling and transformation of complex datasets.
- **Interactive Visualization**: Plotly, a versatile graphing library, was employed to create interactive and visually appealing plots and charts. This allows users to explore data dynamically and gain deeper insights.
- **Web Application Development**: Streamlit, a user-friendly framework for web application development, was utilized to create an intuitive and responsive user interface. Streamlit enables rapid prototyping and deployment of data-driven applications.

Required Libraries:

- **Python Libraries**: 
  - pandas
  - plotly
  - streamlit
  - streamlit-option-menu
  - numpy
  - pillow
  - sqlalchemy
  - pymysql
    

## Usage

To run the application locally, follow these steps:

1. Clone the repository to your local machine.
2. Install the required dependencies by running:
```pip install -r requirements.txt```
3. Run the Streamlit app by executing:
```streamlit run app.py```


## How to get Data
To include instructions on how to obtain the clone link for the PhonePe Pulse data repository, you can modify the Markdown file as follows:
### How to Clone PhonePe Pulse Data Repository

1. Open your web browser and navigate to the GitHub repository for PhonePe Pulse: [PhonePe Pulse Repository](https://github.com/PhonePe/pulse).

2. On the repository page, click on the green "Code" button located towards the top right. This will reveal a dropdown menu.
![Screenshot](https://i.postimg.cc/htxhywgv/Screenshot-2024-03-07-222731.png)  

3. In the dropdown menu, click on the clipboard icon next to the HTTPS link to copy the clone URL.
![Screenshot](https://i.postimg.cc/gkyPxgWG/Screenshot-2024-03-07-232326.png)  

4. Open Git Bash on your computer.

5. Navigate to the directory where you want to clone the repository:
   ```
   cd path/to/destination/directory
   ```
   Replace `path/to/destination/directory` with the actual path where you want to clone the repository.

6. Clone the PhonePe Pulse data repository using the following command:
   ```
   git clone <paste_clone_url_here>
   ```
   Replace `<paste_clone_url_here>` with the URL you copied from the GitHub repository page.

7. Press Enter to execute the command.

![Screenshot](https://i.postimg.cc/sgWY5Hc0/Screenshot-2024-03-07-232326-copy.png)  

8. Git will clone the repository to your specified directory. Once the cloning process is complete, you will have a local copy of the PhonePe Pulse data repository on your computer.

9. You can now navigate to the cloned repository directory and access its contents using Git Bash or any file explorer.

**Note:** Make sure you have Git installed on your computer before following these instructions. You can download Git from [here](https://git-scm.com/).


### Otherwise
1. Open your web browser and navigate to the GitHub repository for PhonePe Pulse: [PhonePe Pulse Repository](https://github.com/PhonePe/pulse). 
2. On the repository page, click on the green "Code" button located towards the top right. This will reveal a dropdown menu.
![Screenshot](https://i.postimg.cc/htxhywgv/Screenshot-2024-03-07-222731.png)  
3. In the dropdown menu, click on the download zip option,it will start download.
![Screenshot](https://i.postimg.cc/K8f166pm/Screenshot-2024-03-07-222709.png)  
4.After successful download you need to unzip the folder and then you can use.


## Deployment

The project has been deployed and is accessible [click here](https://navinspulsevision.streamlit.app/). Feel free to explore Navin's Pulse Vision and gain valuable insights from PhonePe Pulse data.



## References

- [Python Documentation](https://docs.python.org/)
- [Plotly Documentation](https://plotly.com/python/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PyMySQL Documentation](https://pymysql.readthedocs.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

  
## Disclaimer

The data and analysis presented in this dashboard are for informational purposes only and do not constitute financial advice. Please note that the data presented in this dashboard is limited to the period until 2023.


## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).


## About the Developer

Navin's Pulse Vision is developed by Navin Kumar S, a dedicated tech enthusiast with a passion for the sea of data science and AI. My goal is to become a skilled data scientist.

Beyond the lines of code, my aim is to innovate and be a part of transformative technological evolution. The world needs solutions that not only solve problems but redefine them. I'm here to create change.


For reference and further information on PhonePe Pulse, visit [PhonePe Pulse](https://www.phonepe.com/pulse/).

---

Explore Navin's Pulse Vision to gain valuable insights from PhonePe Pulse data. For any inquiries or suggestions, please contact the project owner, Navin.


## Contact

- **LinkedIn:** [Navin](https://www.linkedin.com/in/navinkumarsofficial/)
- **Email:** navinofficial1@gmail.com

Feel free to connect with me on LinkedIn or reach out via email for any inquiries or collaboration opportunities.

