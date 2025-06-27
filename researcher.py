import praw
import pandas as pd
import time
import spacy
import pytextrank
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download VADER lexicon for sentiment analysis (only needs to be done once)
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except nltk.downloader.DownloadError:
    nltk.download('vader_lexicon')

# Initialize the sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Load spaCy model and add TextRank
nlp = spacy.load("en_core_web_sm")
# increase max length to handle long comment threads
nlp.max_length = 2000000 
nlp.add_pipe("textrank")

def summarize_text(text, limit_sentences=3):
    """
    Summarizes text by extracting the most relevant sentences.
    """
    if not text or not isinstance(text, str) or len(text.strip()) == 0:
        return ""
    doc = nlp(text)
    # Extracting the top sentences from the text
    sentences = [sent.text for sent in doc._.textrank.summary(limit_phrases=15, limit_sentences=limit_sentences)]
    return " ".join(sentences)

def analyze_sentiment(text):
    """
    Analyzes the sentiment of a text and returns a label and a compound score.
    """
    if not text or not isinstance(text, str) or len(text.strip()) == 0:
        return 'Neutral', 0.0
    
    # Get sentiment scores
    scores = sia.polarity_scores(text)
    compound_score = scores['compound']
    
    # Classify sentiment based on compound score
    if compound_score >= 0.05:
        return 'Positive', compound_score
    elif compound_score <= -0.05:
        return 'Negative', compound_score
    else:
        return 'Neutral', compound_score

def get_subreddit_data(client_id, secret_key, username, password, user_agent, subreddit_name, limit=25):
    """
    Fetches posts and comments from a specified subreddit.
    """
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=secret_key,
        username=username,
        password=password,
        user_agent=user_agent
    )

    subreddit = reddit.subreddit(subreddit_name)
    print(f"Fetching top {limit} posts from r/{subreddit_name}...")

    posts_data = []
    
    for post in subreddit.hot(limit=limit):
        # Retrieve all comments, this might take a while for posts with many comments
        post.comments.replace_more(limit=None)
        
        all_comments = []
        for comment in post.comments.list():
            all_comments.append(comment.body)
        
        all_comments_text = " ".join(all_comments)
        sentiment_label, sentiment_score = analyze_sentiment(all_comments_text)
        
        posts_data.append({
            'post_id': post.id,
            'title': post.title,
            'score': post.score,
            'upvote_ratio': post.upvote_ratio,
            'url': post.url,
            'num_comments': post.num_comments,
            'created_utc': post.created_utc,
            'all_comments': all_comments_text,
            'comments_summary': summarize_text(all_comments_text),
            'sentiment_label': sentiment_label,
            'sentiment_score': sentiment_score
        })
        print(f"Processed post: {post.title}")
        time.sleep(0.2) # Be respectful to Reddit's API rate limits

    print(f"Finished fetching data for {len(posts_data)} posts.")
    return posts_data

def save_data(data, subreddit_name):
    """
    Saves the collected data to CSV and Excel files.
    """
    save_to_csv(data, subreddit_name)
    save_to_excel(data, subreddit_name)
    save_to_html(data, subreddit_name)

def save_to_csv(data, subreddit_name):
    """
    Saves the collected data to a CSV file.
    """
    if not data:
        print("No data to save.")
        return

    df = pd.DataFrame(data)
    filename = f"{subreddit_name}_posts.csv"
    
    try:
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving data to CSV: {e}")

def save_to_excel(data, subreddit_name):
    """
    Saves the collected data to an Excel file.
    """
    if not data:
        print("No data to save.")
        return

    df = pd.DataFrame(data)
    filename = f"{subreddit_name}_posts.xlsx"
    
    try:
        df.to_excel(filename, index=False)
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving data to Excel: {e}")

def save_to_html(data, subreddit_name):
    """
    Saves the collected data to a styled HTML file.
    """
    if not data:
        print("No data to save.")
        return

    df = pd.DataFrame(data)
    
    # --- Sentiment Styling ---
    def style_sentiment(label):
        if label == 'Positive':
            return 'color: #28a745; font-weight: bold;'
        elif label == 'Negative':
            return 'color: #dc3545; font-weight: bold;'
        else:
            return 'color: #6c757d;'
            
    df['sentiment_styled'] = df['sentiment_label'].apply(lambda x: f'<span style="{style_sentiment(x)}">{x}</span>')

    # Create clickable links for post titles
    df['title'] = df.apply(lambda row: f'<a href="{row["url"]}" target="_blank">{row["title"]}</a>', axis=1)
    
    # Select and rename columns for the report
    report_df = df[['title', 'comments_summary', 'sentiment_styled', 'score', 'num_comments', 'upvote_ratio']].copy()
    report_df.rename(columns={
        'title': 'Post Title',
        'comments_summary': 'Discussion Summary',
        'sentiment_styled': 'Sentiment',
        'score': 'Score',
        'num_comments': 'Comments',
        'upvote_ratio': 'Upvote Ratio'
    }, inplace=True)

    html = report_df.to_html(index=False, escape=False, border=0, classes='table table-striped')

    html_template = f"""
    <html>
    <head>
    <title>Reddit Research Report: r/{subreddit_name}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ margin: 20px; }}
        h1 {{ color: #d9534f; }}
        table {{ border-collapse: collapse; width: 100%; box-shadow: 0 2px 3px rgba(0,0,0,0.1); }}
        th, td {{ padding: 12px 15px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #f2f2f2; font-weight: bold; }}
        tr:hover {{ background-color: #f5f5f5; }}
        a {{ color: #0275d8; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
    </head>
    <body>
    <div class="container">
        <h1>Reddit Research Report: r/{subreddit_name}</h1>
        {html}
    </div>
    </body>
    </html>
    """

    filename = f"{subreddit_name}_report.html"
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_template)
        print(f"HTML report successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving data to HTML: {e}") 