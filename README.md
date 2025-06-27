# Reddit Research Assistant

This project is a Python-based tool that automates the process of fetching, analyzing, and reporting on discussions from any public subreddit. It uses the Reddit API to gather post and comment data, performs NLP analysis to extract insights, and generates a comprehensive HTML dashboard, along with raw data files in CSV and Excel formats.

## Features

-   **Data Collection**: Fetches the top posts and all corresponding comments from a specified subreddit.
-   **Text Summarization**: Uses `pytextrank` to extract the most significant sentences from comment threads, providing a coherent summary of the discussion.
-   **Sentiment Analysis**: Leverages `nltk`'s VADER to analyze the sentiment of the comments, classifying them as positive, negative, or neutral.
-   **Multiple Export Formats**: Saves the collected data in three different formats for various use cases:
    -   `_posts.csv`: Raw data in CSV format.
    -   `_posts.xlsx`: Raw data in an Excel spreadsheet.
    -   `_report.html`: A styled HTML dashboard for easy viewing and analysis.
-   **Interactive HTML Report**: The generated HTML report includes color-coded sentiment scores and clickable links to the original Reddit posts.

## Setup

Follow these steps to set up and run the project locally.

### 1. Initial Setup

First, clone or download the repository to your local machine. It is highly recommended to use a Python virtual environment to manage dependencies.

```bash
# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate
```

### 2. Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

### 3. Additional NLP Setup

This project uses `spaCy` for text summarization and `nltk` for sentiment analysis, which require one-time downloads of their language models.

-   **Download the spaCy model:**
    ```bash
    python -m spacy download en_core_web_sm
    ```
-   **Download the NLTK VADER lexicon:**
    Run the following in a Python interpreter:
    ```python
    import nltk
    nltk.download('vader_lexicon')
    ```

### 4. Configure Credentials

The script requires access to the Reddit API. You will need to create a `.env` file in the root of the project to store your credentials securely.

1.  Create a file named `.env`.
2.  Add your Reddit API credentials to it, following this format:

    ```env
    REDDIT_CLIENT_ID="YOUR_CLIENT_ID"
    REDDIT_CLIENT_SECRET="YOUR_CLIENT_SECRET"
    REDDIT_USERNAME="YOUR_REDDIT_USERNAME"
    REDDIT_PASSWORD="YOUR_REDDIT_PASSWORD"
    REDDIT_USER_AGENT="A_DESCRIPTIVE_USER_AGENT"
    ```

## Usage

1.  **Specify the Subreddit**: Open the `main.py` file and change the `SUBREDDIT_TO_RESEARCH` variable to the name of the subreddit you wish to analyze.

    ```python
    # in main.py
    SUBREDDIT_TO_RESEARCH = "datascience" # Change this to your target subreddit
    ```

2.  **Run the Script**: Execute the main script from your terminal.

    ```bash
    python3 main.py
    ```

## Output

After the script finishes running, you will find three new files in your project directory:

-   `{subreddit_name}_posts.csv`
-   `{subreddit_name}_posts.xlsx`
-   `{subreddit_name}_report.html`

You can open the HTML file in any web browser to view the interactive report. 