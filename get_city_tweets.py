from argparse import ArgumentParser, Namespace
from datetime import datetime, timedelta
import os
import random
from typing import Dict, Tuple
import pandas as pd

def get_arguments() -> Tuple[str, int, int]:
    #Gets the input file, the amount per query and the total number of tweets per city
    parser : ArgumentParser = ArgumentParser(description='scrapes tweets about a city')

    parser.add_argument("file_path")
    parser.add_argument("results_per_query", type=int)
    parser.add_argument("tweets_per_city", type=int)

    args : Namespace = parser.parse_args()

    return args.file_path, args.results_per_query, args.tweets_per_city

def make_directory_if_not_existing(path : str) -> None:
    #Makes a directory if it doesn't already exist
    if not os.path.exists(path):
        os.makedirs(path)

def get_city_folder_names(city_name : str) -> Tuple[str, str]:
    #Gets the folder names for a given city
    city_path_name : str = city_name.lower().replace(" ", "_")
    path1 : str = f"data/{city_path_name}/inside/"
    path2 : str = f"data/{city_path_name}/outside/"

    return path1, path2

def make_city_folders(city_name : str) -> None:
    #Creates the folders for a given city
    path1, path2 = get_city_folder_names(city_name)

    make_directory_if_not_existing(path1)
    make_directory_if_not_existing(path2)


def call_search_command(args : Dict[str, str]) -> None:
    #Uses search-tweets library, queries tweets and creates json files of matches
    command : str = """
    search_tweets.py \
        --max-tweets  {num_results} \
        --results-per-call {num_results} \
        --query '"{search_term}" {neg}point_radius:[{lon} {lat} 25mi] has:geo -is:reply -is:retweet lang:en' \
        --end-time {random_date_time} \
        --tweet-fields author_id,conversation_id,created_at \
        --expansions in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id,geo.place_id \
        --filename-prefix {path}tweets \
        --no-print-stream \
        --results-per-file {num_results}
    """

    os.system(command.format(**args))

if __name__ == "__main__":

    TWITTER_BEARER_TOKEN = os.environ.get("TWITTER_BEARER_CREDENTIALS")

    file_path, tweets_per_query, tweets_per_city = get_arguments()

    cities : pd.DataFrame = pd.read_csv(file_path)

    city : str
    for city in cities.city.tolist():
        make_city_folders(city)

    total_queries : int = tweets_per_city // tweets_per_query

    start : datetime = datetime(2021, 1, 1, 0, 0, 0)
    end : datetime = datetime(2021, 12, 31, 23, 59, 59)
    total_seconds : int = 365 * 24 * 60 * 60
    random.seed(12345)



    for _ in range(total_queries):
        random_date_time : str = (start + timedelta(seconds=random.randint(0, total_seconds))).strftime("%Y-%m-%dT%I:%M")

        for _, row in cities.iterrows():
           path1, path2 = get_city_folder_names(row.city)

           args : Dict[str, str] = {
               "num_results" : str(tweets_per_query),
               "random_date_time": random_date_time,
               "search_term": row.city,
               "lon": row.long,
               "lat": row.lat,
               "neg": "",
               "path": path1
           }

           call_search_command(args)

           args['neg'] = "-"
           args['path'] = path2
           call_search_command(args)
