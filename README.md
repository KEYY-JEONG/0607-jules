# Paper Summarization and Visualization Web App

This web application allows users to upload research paper PDF files. It then automatically extracts the text, generates a structured summary (Abstract, Introduction, Results, Discussion) using the OpenAI API, creates a descriptive prompt for visualization using the Anthropic (Claude) API, and prepares for image generation using the Gemini API (currently a placeholder). The results, including the AI-generated summary, the visualization prompt, and a placeholder image, are displayed on a user-friendly webpage. Users can also download the summary in Markdown and DOCX formats.

This guide will walk you through setting up and running the project on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

*   **Python 3.7+**: You can download Python from [python.org](https://www.python.org/). During installation, make sure to check the box that says "Add Python to PATH" (or similar) if you are on Windows.
*   **`pip`**: This is the Python package installer and usually comes with Python. If not, search for "install pip" for your OS.
*   **Git**: This is a version control system used to download (clone) the project. You can download Git from [git-scm.com](https://git-scm.com/).

## Setup Instructions

Follow these steps carefully to set up the project. These instructions assume you will clone the project into a directory named `0607_jules` inside your user's home directory (e.g., `/Users/keyy/0607_jules` on macOS/Linux or `C:\Users\keyy\0607_jules` on Windows).

1.  **Clone the Repository:**
    Open your terminal (Command Prompt, PowerShell, Terminal, etc.). First, navigate to the directory where you want to create the project folder. For example, if you want the `0607_jules` folder to be directly inside your user directory (`/Users/keyy/` or `C:\Users\keyy\`):
    ```bash
    # On macOS/Linux
    cd ~
    # On Windows
    cd %USERPROFILE%
    ```
    Then, clone the repository. Replace `<repository_url>` with the actual URL you copied from the Git hosting service (like GitHub).
    ```bash
    git clone <repository_url> 0607_jules
    ```
    This command downloads the project files into a new folder named `0607_jules`.

2.  **Navigate into the Project Directory:**
    Once cloning is complete, move into the newly created project directory:
    ```bash
    cd 0607_jules
    ```
    All subsequent commands should be run from within this `0607_jules` directory.

3.  **Create a Python Virtual Environment:**
    A virtual environment is a self-contained directory tree that includes a Python installation for a particular version of Python, plus a number of additional packages. It's crucial because it helps keep dependencies required by different projects separate.
    ```bash
    python3 -m venv venv
    ```
    (If `python3` doesn't work, try `python` on some systems, especially Windows if Python was installed from the Microsoft Store or if `python.exe` is in your PATH).
    This command creates a new folder named `venv` inside your `0607_jules` project directory. This `venv` folder will contain the project's Python interpreter and installed libraries.

4.  **Activate the Virtual Environment:**
    Before you can install or use packages in the virtual environment, you need to 'activate' it. Activation modifies your shell's PATH to point to the Python interpreter and scripts within the `venv` directory.
    *   **On macOS and Linux (using bash or zsh):**
        ```bash
        source venv/bin/activate
        ```
    *   **On Windows (using Command Prompt):**
        ```bash
        venv\Scripts\activate.bat
        ```
    *   **On Windows (using PowerShell):**
        ```bash
        .\venv\Scripts\Activate.ps1
        ```
        (If you get an error about script execution being disabled on PowerShell, you might need to run `Set-ExecutionPolicy Unrestricted -Scope Process` first, then try activating again. Be sure to understand the security implications or consult your system administrator).

    Once activated, your terminal prompt will usually change to show the name of the virtual environment (e.g., `(venv) Your-Computer:0607_jules Your-User$`). This indicates that `pip` and `python` commands will now use the project's isolated environment.

5.  **Install Dependencies:**
    The `requirements.txt` file lists all the Python libraries this project needs to function. Install them using `pip`:
    ```bash
    pip install -r requirements.txt
    ```
    This command reads the `requirements.txt` file and installs the specified versions of each package into your active virtual environment.

## API Key Configuration

This application interfaces with several AI services, which require API keys for authentication. You'll need to obtain these keys from the respective service providers (OpenAI, Anthropic, Google).

The recommended way to configure these keys is using a `.env` file. This file stores your secret keys locally and is not committed to version control (it's listed in `.gitignore`).

1.  **Create a `.env` File:**
    In the root of your project directory (`0607_jules`), you'll find a file named `.env.example`. This is a template. Create a copy of this file and name it `.env`:
    *   **On macOS/Linux:**
        ```bash
        cp .env.example .env
        ```
    *   **On Windows:**
        ```bash
        copy .env.example .env
        ```

2.  **Edit the `.env` File:**
    Open the newly created `.env` file with a text editor. You will see lines like:
    ```
    OPENAI_API_KEY="YOUR_OPENAI_API_KEY_HERE"
    ANTHROPIC_API_KEY="YOUR_ANTHROPIC_API_KEY_HERE"
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
    FLASK_SECRET_KEY="YOUR_FLASK_SECRET_KEY_HERE_OR_LEAVE_FOR_DEFAULT"
    ```
    Replace `"YOUR_..._KEY_HERE"` with your actual API keys.
    *   **`OPENAI_API_KEY`**: Your API key from OpenAI (platform.openai.com). Used for text summarization.
    *   **`ANTHROPIC_API_KEY`**: Your API key from Anthropic (console.anthropic.com). Used for generating the visualization prompt.
    *   **`GEMINI_API_KEY`**: Your API key for Google AI Studio (makersuite.google.com) or Google Cloud (for Vertex AI). *Note: The application currently uses a placeholder for image generation via Gemini. This key is configured for future full integration or if you wish to experiment.*
    *   **`FLASK_SECRET_KEY`**: This is used by Flask to secure session data. You can generate a random string for this (e.g., using a password manager or an online generator) or use the default provided in `app.py` if you leave it blank (though a custom key is more secure for any actual deployment). For local development, the default is often fine.

    **Save the `.env` file after adding your keys.** The application will automatically load these keys when it starts.

**Alternative: System Environment Variables**
If you prefer not to use a `.env` file, you can set these as system-wide or shell-specific environment variables. The application will prioritize system environment variables if they are set. Refer to your operating system's documentation for how to do this persistently.

## Running the Application

1.  **Ensure your virtual environment is active** (your prompt should show `(venv)`).
2.  **Ensure you are in the project's root directory** (`0607_jules`).
3.  **Ensure your API keys are configured** in the `.env` file or as system environment variables.
4.  **Start the Flask Development Server:**
    ```bash
    python app.py
    ```
    You should see output in your terminal indicating that the Flask server is running, typically on `http://127.0.0.1:5000/`. It might also mention that it's a development server and not for production use.

5.  **Access the Application:**
    Open your web browser (like Chrome, Firefox, Safari, or Edge) and navigate to:
    [http://127.0.0.1:5000](http://127.0.0.1:5000)

## How to Use

1.  The application's homepage will present an upload form.
2.  Click the "Choose File" button and select a research paper in PDF format from your computer.
3.  Click the "Upload and Process" button.
4.  Wait for the application to process the PDF. This involves text extraction, and calls to OpenAI and Anthropic APIs, which may take a few moments depending on the PDF size and API responsiveness.
5.  Once processing is complete, you will be redirected to a results page displaying:
    *   **Structured Summary**: Sections for Abstract, Introduction, Results, and Discussion.
    *   **Visualization Prompt**: The text prompt generated by Anthropic (Claude).
    *   **Visualization Image**: A placeholder image (as Gemini image generation is currently stubbed).
    *   **Download Links**: Links to download the full summary as a Markdown (`.md`) file or a Word document (`.docx`).
6.  If there are issues (e.g., missing API keys, errors from API calls), appropriate error messages or default/mock content will be displayed on the results page.

## Troubleshooting / Common Issues

*   **`python` or `pip` command not found:**
    *   Ensure Python is installed and its installation directory (and its `Scripts` subdirectory on Windows) is added to your system's PATH environment variable.
    *   Try using `python3` or `pip3` if `python` or `pip` don't work.
*   **Virtual environment (`venv`) not activating:**
    *   Double-check the activation command for your specific operating system and shell.
    *   Ensure you are in the project's root directory (`0607_jules`) where the `venv` folder was created.
    *   PowerShell users: You might need to adjust your script execution policy (see activation step).
*   **`ModuleNotFoundError: No module named 'flask'` (or other modules):**
    *   Make sure your virtual environment is active.
    *   Ensure you have run `pip install -r requirements.txt` successfully *while the virtual environment is active*.
*   **API Key Errors (e.g., "OpenAI API key not set" or similar on results page):**
    *   Verify your `.env` file is correctly named (`.env`, not `.env.txt` or `.env.example`).
    *   Ensure the `.env` file is in the project root directory (`0607_jules`).
    *   Check that the API key names in your `.env` file (`OPENAI_API_KEY`, etc.) exactly match those expected by the application.
    *   Confirm the keys themselves are correct and valid for the respective services.
    *   If you set system environment variables, ensure they are correctly set and available in the terminal session where you run `python app.py`. You might need to restart your terminal or even your computer after setting system-wide variables.
*   **Application not starting or errors in the terminal when running `python app.py`:**
    *   Read the error message in the terminal carefully. It often provides clues about syntax errors in the Python code, problems with dependencies, or network issues if it's trying to bind to a port.

## Current Limitations

*   **Gemini Image Generation:** The integration with the Gemini API for generating actual images is currently a placeholder. The application will display a predefined placeholder image instead of a dynamically generated one from your prompt. The structure for full Gemini integration is in place for future development.

---
