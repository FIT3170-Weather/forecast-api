# forecast-api

## Table of Contents
1. [Project Overview](#project-overview)
2. [Software Requirements](#software-requirements)
3. [Hardware Requirements](#hardware-requirements)
4. [Setup and Installation Instructions](#setup-and-installation-instructions)
5. [How to Run the Project](#how-to-run-the-project)
6. [Common Issues and Troubleshooting](#common-issues-and-troubleshooting)
7. [Additional Notes](#additional-notes)
8. [Contact Information](#contact-information)

## Project Overview
CliMate is a weather application that provides weather information, within Malaysia for a 14 day window, 7 days in the past and 7 days in the future.

The application is a web app that is built using NodeJS, SvelteKit, TailwindCSS, etc.

There is a machine learning component to this web app, which predicts the weather for the next 7 days. This component is hosted in another repository.

## Software Requirements
List all software, dependencies, and versions required to run the project. This may include:
- Programming languages (e.g., Python 3.x)
- Libraries and frameworks (e.g., MetPy, Flask, etc.)
- Any other software (e.g., IDEs, build tools)

### Example:
- Python 3.9+
- Flask 2.1.0
- MetPy 1.3.1
- Jupyter Notebook

## Hardware Requirements
If applicable, mention any specific hardware requirements or considerations:
- Sensors
- Development boards
- Specific configurations needed for testing

## API Docs

## Current weather
Request: POST localhost:8000/current <br><br>

Body: { <br>
    location: str <br>
} <br><br>

Response: https://openweathermap.org/current#example_JSON<br><br>

## Forecast
Request: POST localhost:8000/forecast<br><br>

Body: {<br>
    location: str<br>
    forecastType: str<br>
    variables: list[str]<br>
}<br><br>

Response: {<br>
        success: bool<br>
        temperature: list[float] (optional, only if requested)<br>
        humidity: list[float] (optional, only if requested)<br>
        precipitation: list[float] (optional, only if requested)<br>
}<br><br>

## Getting location, forecastType and variables
Request: GET localhost:8000/location<br>
Request: GET localhost:8000/forecastTypes<br>
Request: GET localhost:8000/variables<br>

## Setup and Installation Instructions
Provide step-by-step instructions on how to set up the development environment and install the necessary dependencies.

### Example:

## How to Run the Project
Explain how to run the application or scripts, including any commands or parameters.

Run "/main.py" (NOTE: NOT /src/main.py) <br>
You may have to pip install dependencies such as uvicorn, fastapi etc. <br><br>

### Example:

## Common Issues and Troubleshooting

List common errors or issues developers might encounter, along with their solutions. This section is especially helpful for future developers.

### Example:

## Additional Notes
Provide any extra information that doesn’t fit in the other sections

## Contact Information

| Name                       | Email                       | Student ID |
| -------------------------- | --------------------------- | ---------- |
| Suman Datta                | sdat0004@student.monash.edu | 30668786   |
| Daryl Lim                  | dlim0036@student.monash.edu | 33560757   |
| Ryan Choo Yan Jhie         | rcho0046@student.monash.edu | 33455775   |
| Nicholas Yew               | nyew0001@student.monash.edu | 33642478   |
| Lim Zhi Cheng              | zlim0052@student.monash.edu | 33204128   |
| Mohamed Ammar Ahamed Siraj | amoh0157@student.monash.edu | 33187762   |
| Nicholas Lee               | nlee0060@student.monash.edu | 32840594   |
| Shyam Borkar               | sbor0018@student.monash.edu | 32801459   |
| Lai Carson                 | lcar0029@student.monash.edu | 32238436   |
| Hanideepu Kodi             | hkod0003@student.monash.edu | 33560625   |
