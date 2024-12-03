# Atomic ACO Freebies Web Application

## Project Hosting
- This project is hosted on https://freebies.atomicaco.com/signup and is actively being used by paying customers at my company, Atomic ACO.

## Project Overview
This web application, built using Flask, serves as a platform for users to sign up for freebies through a multi-step process. It integrates various APIs such as Stripe for payment processing and Discord for OAuth authentication. The app also uses Google Sheets for data persistence, mimicking database functionalities to store user information securely.

## Usage Guidelines
To use this application, follow these steps:
1. **Initial Setup:**
   - Clone the repository and install the dependencies listed below.
   - Set up the required environment variables or `.env` file as outlined in the dependencies section. Additionally, create a gsheets_api_key.json and a hidden_vars_for_public_repo.py. In the gsheets api key, place the json key from the google sheets portal online. For the hidden vars, input the vars into that python document. 

2. **Running the Application:**
   - Execute `python main.py` from the terminal within the project directory to start the Flask server.
   - Access the web application by navigating to `http://localhost:5000` in your web browser.

3. **Navigating the Application:**
   - Start by registering or signing into the platform.
   - Follow the prompts to enter your information and proceed through the signup steps.
   - Utilize the coupon code feature if applicable to receive discounts.
   - Complete the payment process through Stripe to finalize the registration for freebies.

## Dependencies
- Flask: `pip install Flask`
- gspread: `pip install gspread`
- oauth2client: `pip install oauth2client`
- requests: `pip install requests`
- stripe: `pip install stripe`
- python-dotenv: `pip install python-dotenv`

**Environment Variables:**
- Ensure the following variables are set in your `.env` file:
  - `STRIPE_API_KEY`: Your Stripe API key for processing payments.
  - `OAUTH2_CLIENT_ID`: The Client ID for Discord OAuth.
  - `OAUTH2_CLIENT_SECRET`: The Client Secret for Discord OAuth.
  - `BOT_TOKEN`: Your Discord bot token.
  - Also include OAUTH2_CLIENT_ID, OAUTH2_CLIENT_SECRET, BOT_TOKEN, GUILD_ID, STRIPE_API_KEY, STRIPE_PRICE in hidden_vars_for_public_repo.py

## Project Structure
- `main.py`: Contains the Flask application setup and routes.
- `templates/`: Folder containing HTML/CSS files for the web interface.
- `.env`: A file storing environment variables (ensure this file is in `.gitignore`).

## Collaboration Information
- This project was developed individually, but I had assistance from one of the developers that works at my company for the coupon code section.
- AI was used to write a majority of the readme file as well as provide assistance for syntax in main.py. I wrote the skeleton for the html pages and had AI make it look more visually appealing.

## Acknowledgments
- Stripe API for handling payment processes.
- Discord for OAuth authentication services.
- Google Sheets API for data management and storage.

## Reflection
This project allowed me to practice the skills I previously had while also allowing me to incorporate things I have learned in this class. This was a very big project and I had limited time to compleate it so it taught me a lot about how to plan a project as well as how to get a working build out super quick and under pressure. I did have a previous simple version of this, but I basically rewrote everything to make the program better because when I origionally wrote it I barely had any coding experience. Additionally, this project is hosted on https://freebies.atomicaco.com/signup and is actively being use by paying customers at my company, Atomic ACO.
