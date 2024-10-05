# forecast-api

## Table of Contents
1. [Project Overview](#project-overview)
2. [Software Requirements](#software-requirements)
3. [Setup and Installation Instructions](#setup-and-installation-instructions)
4. [How to Run the Project](#how-to-run-the-project)
5. [Common Issues and Troubleshooting](#common-issues-and-troubleshooting)
6. [Additional Notes](#additional-notes)
7. [Contact Information](#contact-information)

## Project Overview
CliMate is a weather application that provides weather information, within Malaysia for a 14 day window, 7 days in the past and 7 days in the future.

The application is a web app that is built using NodeJS, SvelteKit, TailwindCSS, etc.

There is a machine learning component to this web app, which predicts the weather for the next 7 days. This component is hosted in another repository.

## Software Requirements
- python3==3.9+
- tensorflow==2.17.0
- scikit-learn==1.5.1
- joblib==1.4.2
- numpy==1.26.4
- seaborn==0.13.2
- pandas==2.2.2
- matplotlib==3.9.2
- requests-cache==1.2.1
- openmeteo-requests
- retry-requests
- firebase-admin==6.5.0
- google-cloud-firestore==2.17.2
- google-cloud-core==2.4.1
- fastapi==0.112.1
- uvicorn==0.30.6
- protobuf==3.20.3

## API Docs

### Current weather
Request: POST localhost:8000/current <br><br>

Body: { <br>
    location: str <br>
} <br><br>

Response: https://openweathermap.org/current#example_JSON<br><br>

### Forecast
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

### Getting location, forecastType and variables
Request: GET localhost:8000/location<br>
Request: GET localhost:8000/forecastTypes<br>
Request: GET localhost:8000/variables<br>

### Get all profiles:
Request: GET localhost:8000/profiles<br>

### Get specifc profile:
Request: POST localhost:8000/profiles/{uid}

Response: {<br>
  "detail": [ <br>
    {<br>
      "loc": [<br>
        "string",<br>
        0<br>
      ],<br>
      "msg": "string",<br>
      "type": "string"<br>
    }<br>
  ]<br>
}<br><br>

### Get specific profile saved locations:
Request: POST localhost:8000/profiles/{uid}/get_locations

Response: {<br>
  "detail": [<br>
    {<br>
      "loc": [<br>
        "string",<br>
        0<br>
      ],<br>
      "msg": "string",<br>
      "type": "string"<br>
    }<br>
  ]<br>
}<br><br>

### Get forecast of saved locations:
Request: POST localhost:8000/profiles/{uid}/preferences/forecast

Response: {<br>
  "detail": [<br>
    {<br>
      "loc": [<br>
        "string",<br>
        0<br>
      ],<br>
      "msg": "string",<br>
      "type": "string"<br>
    }<br>
  ]<br>
}<br><br>

### Get email of all profiles that has subscribed to email notifications
Request: POST localhost:8000/profiles/subscriptions

Response: {<br>
    "success": bool<br>
    "data": [str]<br>
}<br><br>

## Setup and Installation Instructions

1. Execute the following command in a new Terminal to download all required dependencies and packages:
    `pip install -r requirements.txt --user` <br>

2. Email `dlim0036@student.monash.edu` to request for the Firebase Access and  `serviceAccountKey.json` file.<br>
3. Put the `serviceAccountKey.json` into the root directory of the code base.<br><br>

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
