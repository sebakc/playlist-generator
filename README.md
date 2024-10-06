# Playlist Generator

This project generates playlists using the OpenAI API.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/playlist-generator.git
    cd playlist-generator
    ```

2. Create and activate a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Configuration

1. Create a `.env` file in the root directory and add your OpenAI API key:
    ```dotenv
    # OpenAI API Key
    OPENAI_API_KEY=your_openai_api_key_here
    ```

2. Create a `client_secrets.json` file in the root directory with your Google API credentials:
```json
{
  "installed": {
    "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
    "project_id": "YOUR_PROJECT_ID",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "YOUR_CLIENT_SECRET",
    "redirect_uris": ["http://localhost"]
  }
}
```

## How to Create YouTube API Credentials (`client_secrets.json`)

To interact with the YouTube API and create playlists, you need to set up OAuth 2.0 credentials and download a `client_secrets.json` file. Follow these steps to create the necessary credentials:

### 1. Go to the Google Developers Console
- Open your web browser and navigate to the [Google Developers Console](https://console.cloud.google.com/).

### 2. Create or Select a Project
- If you don’t already have a project, click on **Select a Project** in the top navigation bar and then **New Project**.
- Give your project a name and click **Create**.

### 3. Enable the YouTube Data API v3
- In the **APIs & Services** section on the left sidebar, click on **Library**.
- In the API library, search for **YouTube Data API v3**.
- Click on the **YouTube Data API v3** result and then click **Enable**.

### 4. Create OAuth 2.0 Credentials
- Go to **APIs & Services > Credentials** in the left sidebar.
- Click the **+ CREATE CREDENTIALS** button at the top, then select **OAuth client ID**.
- If prompted to configure the OAuth consent screen:
  - Click **Configure Consent Screen**.
  - Choose **External** as the user type and click **Create**.
  - Fill in the required fields (e.g., app name, user support email).
  - Under **Scopes**, you don't need to add any additional scopes for this application, so you can skip this step.
  - Click **Save and Continue** until you reach the end, then click **Back to Dashboard**.
- Now, you should be back at the **Create OAuth client ID** page:
  - **Application type**: Select **Desktop app**.
  - **Name**: Give the OAuth client a name (e.g., "YouTube Playlist Generator").
- Click **Create**.

### 5. Download the `client_secrets.json` File
- After creating the OAuth 2.0 client, you will see a dialog with the **Client ID** and **Client Secret**. Click the **Download** button to save the `client_secrets.json` file.
- Place the downloaded `client_secrets.json` file in the root directory of your project.

### 6. Structure of `client_secrets.json`
The downloaded file will look something like this:

```json
{
  "installed": {
    "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
    "project_id": "YOUR_PROJECT_ID",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "YOUR_CLIENT_SECRET",
    "redirect_uris": [
      "urn:ietf:wg:oauth:2.0:oob",
      "http://localhost"
    ]
  }
}
```

## Usage

1. Run the application:
    ```sh
    python app.py
    ```
2. Follow the on-screen instructions to generate your playlist or clean up previously created playlists using the --clean flag:
    ```sh
    python app.py --clean
    ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
