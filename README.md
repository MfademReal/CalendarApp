
# Calendar App

This is a Flask-based web application that displays a weekly calendar with events.

## Project Structure

- `app.py`: The main Flask application.
- `static/styles.css`: The CSS file for styling the calendar.
- `templates/index.html`: The main HTML template for the calendar.
- `credentials.json`: Credentials for API access (ignored in `.gitignore`).
- `token.json`: OAuth token for authentication (ignored in `.gitignore`).

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Calendar-App.git
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Google API credentials by following these steps:

   ### Steps to Set Up Google API Credentials:

   1. **Go to the Google Cloud Console**:
      - Open the [Google Cloud Console](https://console.cloud.google.com/).
      - If you haven't already, create a new project.

   2. **Enable Google Calendar API**:
      - In the Google Cloud Console, go to the **API Library**.
      - Search for "Google Calendar API" and click on it.
      - Click **Enable** to activate the Google Calendar API for your project.

   3. **Create OAuth 2.0 Credentials**:
      - Navigate to the **Credentials** page in the Cloud Console.
      - Click on **Create Credentials** and select **OAuth 2.0 Client IDs**.
      - Choose **Desktop App** or **Web Application** as the application type.
      - After creation, download the `credentials.json` file. This file contains the client ID and secret required for OAuth authentication.

   4. **Add `credentials.json` to Your Project**:
      - Place the downloaded `credentials.json` file into the root directory of your project.

   5. **Authentication Flow**:
      - The first time you run the app, it will open a browser window asking you to log in with your Google account and give permission for the app to access your Google Calendar.
      - After authentication, a `token.json` file will be created to store your access and refresh tokens.

4. Run the app:
   ```bash
   python app.py
   ```

## License

[MIT License](LICENSE)

```

This version includes the necessary steps for obtaining and using Google API credentials. It also details the authentication flow with the Google Calendar API.
