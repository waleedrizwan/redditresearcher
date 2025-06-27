from researcher import get_subreddit_data, save_to_csv
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# get the credentials from the .env file
client_id = os.getenv("REDDIT_CLIENT_ID")
client_secret = os.getenv("REDDIT_CLIENT_SECRET")
username = os.getenv("REDDIT_USERNAME")
password = os.getenv("REDDIT_PASSWORD")
user_agent = os.getenv("REDDIT_USER_AGENT")

# Specify the subreddit you want to research
# You can change this to any subreddit you're interested in
SUBREDDIT_TO_RESEARCH = "datascience"

if __name__ == "__main__":
    try:
        print(f"\nStarting data retrieval for r/{SUBREDDIT_TO_RESEARCH}. This may take a few minutes.")
        
        # Get the data from the specified subreddit
        subreddit_data = get_subreddit_data(
            client_id, 
            client_secret, 
            username, 
            password, 
            user_agent, 
            SUBREDDIT_TO_RESEARCH
        )
        
        if subreddit_data:
            print(f"\nSuccessfully retrieved data for {len(subreddit_data)} posts.")
            
            # Save the data to a CSV file
            print("Saving data to CSV file...")
            save_to_csv(subreddit_data, SUBREDDIT_TO_RESEARCH)
            print(f"\nSuccess! Data has been written to {SUBREDDIT_TO_RESEARCH}_posts.csv")
        else:
            print("No data was retrieved. Exiting.")
            
    except Exception as e:
        print(f"\nERROR: An error occurred: {str(e)}")
        print(f"ERROR TYPE: {type(e).__name__}")
        import traceback
        print(f"FULL TRACEBACK:\n{traceback.format_exc()}")
        
        # Additional debug info
        print(f"\nDEBUG INFO:")
        print(f"client_id exists: {client_id is not None}")
        print(f"client_secret exists: {client_secret is not None}")
        print(f"username exists: {username is not None}")
        print(f"password exists: {password is not None}")
        print(f"user_agent exists: {user_agent is not None}")

