import praw
import pandas as pd
import time
import spacy
import pytextrank

# Load spaCy model and add TextRank
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("textrank")

def summarize_text(text, limit_phrases=5):
    """
    Summarizes text using pytextrank to extract key phrases.
    """
    if not text or not isinstance(text, str) or len(text.strip()) == 0:
        return ""
    doc = nlp(text)
    phrases = [p.text for p in doc._.phrases[:limit_phrases]]
    return ". ".join(phrases)

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
        
        all_comments_text = " | ".join(all_comments)
        
        posts_data.append({
            'post_id': post.id,
            'title': post.title,
            'title_summary': summarize_text(post.title),
            'score': post.score,
            'upvote_ratio': post.upvote_ratio,
            'url': post.url,
            'num_comments': post.num_comments,
            'created_utc': post.created_utc,
            'all_comments': all_comments_text, # Join comments with a separator
            'comments_summary': summarize_text(all_comments_text)
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
    
    # Create clickable links for post titles
    df['title'] = df.apply(lambda row: f'<a href="{row["url"]}" target="_blank">{row["title"]}</a>', axis=1)
    
    # Select and rename columns for the report
    report_df = df[['title', 'comments_summary', 'score', 'num_comments', 'upvote_ratio']].copy()
    report_df.rename(columns={
        'title': 'Post Title',
        'comments_summary': 'Discussion Summary',
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