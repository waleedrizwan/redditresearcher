import praw
import pandas as pd
import time

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
        
        posts_data.append({
            'post_id': post.id,
            'title': post.title,
            'score': post.score,
            'upvote_ratio': post.upvote_ratio,
            'url': post.url,
            'num_comments': post.num_comments,
            'created_utc': post.created_utc,
            'all_comments': " | ".join(all_comments) # Join comments with a separator
        })
        print(f"Processed post: {post.title}")
        time.sleep(0.2) # Be respectful to Reddit's API rate limits

    print(f"Finished fetching data for {len(posts_data)} posts.")
    return posts_data

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