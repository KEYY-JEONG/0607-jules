# Paper Summarization and Visualization Web App

This web application allows users to upload research paper PDF files, automatically extracts text, generates a structured summary (Abstract, Introduction, Results, Discussion) using OpenAI, generates a visualization prompt using Anthropic (Claude), and prepares for image generation using Gemini (currently a placeholder). The results, including the summary, visualization prompt, and a placeholder image, are displayed on a webpage, with options to download the summary in Markdown and DOCX formats.

## Prerequisites

*   Python 3.7+
*   `pip` (Python package installer)
*   Git

## Setup Instructions

Follow these steps to set up and run the project locally. These instructions assume you will clone the project into a directory like `/Users/keyy/0607_jules`.

1.  **Clone the Repository:**
    Open your terminal or command prompt and navigate to the directory where you want to place the project (e.g., `/Users/keyy/` if you want the project folder to be `0607_jules` directly inside it). Then clone the repository:
    ```bash
    git clone <repository_url> 0607_jules
    ```
    (Replace `<repository_url>` with the actual URL of the Git repository).

2.  **Navigate into the Project Directory:**
    ```bash
    cd 0607_jules
    ```

3.  **Create a Python Virtual Environment:**
    It's highly recommended to use a virtual environment to manage project dependencies.
    ```bash
    python3 -m venv venv
    ```
    This creates a `venv` folder in your project directory.

4.  **Activate the Virtual Environment:**
    *   **On macOS and Linux (bash/zsh):**
        ```bash
        source venv/bin/activate
        ```
    *   **On Windows (Command Prompt):**
        ```bash
        venv\Scriptsctivate.bat
        ```
    *   **On Windows (PowerShell):**
        ```bash
        venv\Scripts\Activate.ps1
        ```
    Your terminal prompt should change to indicate that the virtual environment is active (e.g., `(venv) your-prompt$`).

5.  **Install Dependencies:**
    With the virtual environment active, install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## API Key Configuration

This application requires API keys for OpenAI and Anthropic to function correctly. The Gemini API key is also configured, though its image generation feature currently uses a placeholder. You need to set these keys as environment variables.

**How to Set Environment Variables (Example for macOS/Linux using bash/zsh):**

You can set them temporarily for your current terminal session, or add them to your shell's configuration file (e.g., `~/.bashrc`, `~/.zshrc`) for persistence across sessions.

To set for the current session (replace `your_actual_key_here` with your real API keys):
```bash
export OPENAI_API_KEY="your_actual_openai_key_here"
export ANTHROPIC_API_KEY="your_actual_anthropic_key_here"
export GEMINI_API_KEY="your_actual_gemini_key_here"
```

*   **`OPENAI_API_KEY`**: Your API key for OpenAI services (used for text summarization).
*   **`ANTHROPIC_API_KEY`**: Your API key for Anthropic (Claude) services (used for generating visualization prompts).
*   **`GEMINI_API_KEY`**: Your API key for Google Gemini services. (Note: The application currently uses a placeholder for image generation via Gemini. This key is for future full integration.)

**Important:** If you add these to `~/.bashrc` or `~/.zshrc`, remember to source the file (e.g., `source ~/.bashrc`) or open a new terminal window for the changes to take effect. For other shells or operating systems, please refer to their specific documentation on setting environment variables.

## Running the Application

1.  **Ensure your virtual environment is active** and you are in the project's root directory (`0607_jules`).
2.  **Make sure your API keys are set** as environment variables.
3.  **Run the Flask Application:**
    ```bash
    python app.py
    ```
4.  **Access the Application:**
    Open your web browser and go to:
    [http://127.0.0.1:5000](http://127.0.0.1:5000)

## How to Use

1.  Once the application is running, you will see an upload page.
2.  Click the "Choose File" button and select a PDF research paper from your computer.
3.  Click "Upload and Process."
4.  The application will process the PDF, call the AI services, and then display a results page.
5.  The results page will show:
    *   The structured summary (Abstract, Introduction, Results, Discussion).
    *   The text prompt generated for visualization.
    *   A placeholder image for the visualization.
    *   Download links for the summary in Markdown (`.md`) and Word (`.docx`) formats.
6.  If API keys are missing or there are errors during API calls, relevant error messages will be displayed.

## Current Limitations

*   **Gemini Image Generation:** The integration with Gemini API for generating images is currently a placeholder. The application will display a predefined placeholder image instead of a dynamically generated one. The structure for full Gemini integration is in place for future development.

---
