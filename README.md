# Weather Dashboard Web Application README (main branch)

## 1. Project Overview
The Weather Dashboard is a feature-rich web application for weather queries. It aims to provide users with a convenient way to obtain weather information. Users can either manually enter the name of a city or use the auto-location function to get the real-time weather conditions, today's weather forecast, and the 5-day weather prediction for a specific city. Additionally, the application is equipped with a RESTful API interface, facilitating data interaction and secondary development for developers.

## 2. Functional Features
1. **Current Weather Query**: Based on the city name entered by the user or the location information obtained through auto-location, the application calls the OpenWeatherMap API to retrieve current weather data, including temperature, humidity, weather condition descriptions, and corresponding weather icons.
2. **Today's Weather Information**: It fetches the weather data for different time periods of the day, extracts wind speed and direction information, and generates a wind rose diagram to visually display the wind conditions of the day.
3. **5-Day Weather Prediction**: The application acquires the 5-day weather prediction data, calculates and presents the daily maximum temperature, minimum temperature, and average temperature. It also shows weather icons, weather condition descriptions, and precipitation probabilities, visually presenting the weather change trends through charts and tables.
4. **Visualization**: By using various visualization methods such as temperature progress bars, humidity gauges, wind rose diagrams, temperature charts, and precipitation probability pie charts, the weather data is presented to users in an intuitive and understandable way.
5. **RESTful API Interface**: A RESTful API is provided, which supports the retrieval of real-time weather data, today's weather data, and 5-day weather prediction data, enabling other applications to integrate and use this weather data.
6. **Auto-Location Function**: Leveraging the browser's geolocation feature, the application obtains the user's geographical coordinates and converts them into the city name through the OpenWeatherMap API, realizing auto-location for weather queries.

## 3. Technology Stack
1. **Programming Language**: Python, which utilizes its rich libraries and concise syntax for development.
2. **Web Frameworks**:
    - `fastapi` and `fasthtml` is used to build the main web application logic, handling user requests and responses.
    - `flask` is employed to set up the RESTful API interface for data interaction.
3. **Data Acquisition**: The `httpx` library is used to send requests to the OpenWeatherMap API to obtain weather data.
4. **Data Processing**: The `numpy` library is applied for data calculation and processing, such as when generating visualization charts.
5. **Visualization**: The `matplotlib` library is utilized to create various visualization charts, like temperature progress bars and humidity gauges, to visually display weather data.
6. **HTML Generation**: The `fasthtml.common` python module and `HTMLx` are used to generate HTML pages and construct the user interface.

## 4. Installation and Running
1. **Clone the Project Repository**:
    - Open a command-line tool (such as Git Bash, Windows Command Prompt, or PowerShell).
    - Use the following command to clone the repository of the main branch of the project:
      ```bash
      git clone [Project Repository URL]
      ```
    - Enter the cloned project directory:
      ```bash
      cd weatherdashboard2.0
      ```
2. **Check Python Version**:
    - Ensure that the installed Python version is equal to or higher than 3.12.0. Enter the following command in the command line to check the Python version:
      ```bash
      python --version
      ```
    - If the version does not meet the requirement, please visit the [official Python website](https://www.python.org/downloads/) to download and install the appropriate version.
3. **Install Dependencies**:
    - In the root directory of the project, use the following commands to install the required dependencies:
      ```bash
      python -m pip install --upgrade pip
      pip install -r requirements.txt
      ```
    - This process may take some time, depending on your network speed and computer performance. Please be patient and wait for the installation to complete. During the installation, if any dependency installation errors occur, please troubleshoot and solve them according to the error prompts. Common problems may include network connection issues and missing system dependencies.
4. **Obtain the OpenWeatherMap API Key**:
    - Visit the [OpenWeatherMap website](https://openweathermap.org/) and register an account. If you already have an account, log in directly.
    - After logging in, find and obtain your API key in the personal profile or API-related page.
5. **Configure the API Key**:
    - Open the `getdata.py` file and find the following code sections (the line numbers may vary slightly depending on code adjustments, usually near the specified lines):
        - Around line 55: `OPENWEATHERMAP_API_KEY = "your_api_key_here"`, replace the content within the double quotes with the API key you obtained.
        - Around line 117: Similarly, find the assignment of `OPENWEATHERMAP_API_KEY` and replace it.
        - Around line 180: Repeat the above replacement operation.
    - Open the `autolocation_process.py` file and find around line 24: `api_key="your_api_key_here"`, replace the content within the double quotes with your API key.
6. **Run the Main Program**:
    - In the command line in the root directory of the project, run the `main_app.py` file. Depending on your Python environment, you may use one of the following commands:
      ```bash
      python main_app.py
      ```
      Or, if both Python 2 and Python 3 are installed on your system, you may need to use:
      ```bash
      python3 main_app.py
      ```
    - After the program starts, visit `http://localhost:8000` in your browser, and you can enter the weather query interface. Users can enter the city name in the interface or click the "Auto Locate" button to query the weather through auto-location.
7. **Run the API**:
    - Run the `make_API_runnable.py` file, also using the following command in the command line:
      ```bash
      python make_API_runnable.py
      ```
    - Enter the city name as prompted, and the program will output the API URLs for the real-time data, today's data, and 5-day forecast data of the corresponding city. You can access the corresponding weather data through these URLs. Note that when running the API, you need to close the running main program to avoid port conflicts.

## 5. Directory Structure
weatherdashboard2.0/
│ ├── getdata.py # Functions to fetch weather data from the OpenWeatherMap API
│ ├── processingdata.py # Functions to process raw weather data
│ ├── get_icon.py # Functions to obtain weather icons
│ ├── visualization.py # Functions to create visualization charts
│ ├── restful_api.py # Code for building the RESTful API
│ ├── make_API_runnable.py # Script to run the API and generate URLs
│ ├── autolocation_process.py # Functions to obtain the city name through auto - location
│ ├── main_app.py # The main program, containing the routes and logic of the web application
│ ├── mypy.ini # Configuration file for mypy static type checking
│ ├── requirements.txt # List of project - dependent libraries
│ ├── .github/
│ │ └── workflows/
│ │ └── main.yaml # GitHub workflow configuration file for CI/CD



## 6. API Usage Instructions
1. **Get All Weather Data**: Send a GET request to `/weatherdashboard/api/v1.0/weatherdatas` to obtain all the data including real-time weather, today's weather, and 5-day weather prediction.
2. **Get Weather Data with a Specific ID**: Send a GET request to `/weatherdashboard/api/v1.0/weatherdatas/<int:weatherdata_id>`, where `weatherdata_id` is 1 for real-time data, 2 for today's data, and 3 for 5-day forecast data.
3. **Create a New Weather Data Record**: Send a POST request to `/weatherdashboard/api/v1.0/weatherdatas` with `title` and `data` fields in the request body to create a new weather data record.
4. **Update a Weather Data Record with a Specific ID**: Send a PUT request to `/weatherdashboard/api/v1.0/weatherdatas/<int:weatherdata_id>`, and specify the fields to be updated in the request body to update the corresponding weather data record.
5. **Delete a Weather Data Record with a Specific ID**: Send a DELETE request to `/weatherdashboard/api/v1.0/weatherdatas/<int:weatherdata_id>` to delete the specified weather data record.


## 7. GitHub Pages Documentation

The `gh-pages` branch contains HTML documentation files for each module of the project. These documents provide detailed explanations and usage instructions for all components of the Weather Dashboard application.

**Please read the documentation for more information.**

## If you have any questions or find any errors in the documentation, please contact the project author.
Author: kei-linyugui20223638023
Email: 20223638023@m.scnu.edu.cn
