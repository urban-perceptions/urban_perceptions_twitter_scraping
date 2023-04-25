import argparse
from typing import List, Tuple
import pandas as pd
from os import listdir
import json


def get_arguments() -> Tuple[str, str]:
    #Gets filepaths for input and output
    parser : argparse.ArgumentParser = argparse.ArgumentParser(description='combines json tweet data into dataframe')

    parser.add_argument("input_filepath")
    parser.add_argument("output_filepath")
    args : argparse.Namespace = parser.parse_args()

    return args.input_filepath, args.output_filepath


def get_all_jsonfiles(folderpath: str) -> List[str]:
    #Get the relative paths of all json files in a folder

    filepaths : List[str] = [f"{folderpath}/{file}" for file in listdir(folderpath)\
         if file.endswith( ".json" )]

    return filepaths


def tweet_json_to_dataframe(filepath: str) -> pd.DataFrame:
    #Converts a single tweet json into a dataframe

    all_data : List[pd.DataFrame] = []

    with open(filepath) as file:
        lines : List[str] = file.readlines()

        line : str
        for line in lines:
            all_data.append(json.loads(line))

    return pd.concat(map(lambda x: pd.json_normalize(x, record_path="data"), all_data))

def multiple_tweet_json_to_dataframe(folderpath: str) -> pd.DataFrame:
    #Combines all tweet json files in a folder into one dataframe

    filenames : List[str] = get_all_jsonfiles(folderpath)
    return pd.concat(map(tweet_json_to_dataframe, filenames))

def combine_all_tweet_data(file_path : str) -> pd.DataFrame:
    #Combines all the tweet data adding columns for the city and inside

    cities : pd.DataFrame = pd.read_csv(file_path)
    all_dfs : List[pd.DataFrame] = []

    city : str
    for city in cities.city.tolist():
        city_name : str = city.lower().replace(" ", "_")
        df1 : pd.DataFrame = multiple_tweet_json_to_dataframe(f"data/{city_name}/inside")
        df2 : pd.DataFrame = multiple_tweet_json_to_dataframe(f"data/{city_name}/outside")
        df1['city'] = city
        df2['city'] = city
        df1['inside'] = 1
        df2['inside'] = 0
        all_dfs.append(df1)
        all_dfs.append(df2)

    return pd.concat(all_dfs)


if __name__ == "__main__":
    input_file, output_file = get_arguments()
    df : pd.DataFrame = combine_all_tweet_data(input_file)
    df.to_csv(output_file)
