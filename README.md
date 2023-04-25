# Urban Perceptions

## Setup

Copy the environment.yml.dist file and rename it to environment.yml. If scraping tweets add your twitter bearer token (no quotes need) after the colon on the appropriate line. **DO NOT COMMIT THE TOKEN OR THE ENVIRONMENT.YML FILE!** Environment.yml is gitignored so it shouldn't be committed unless you remove it from the gitignore file. You can commit the environment.yml.dist file (so don't put your token in that), but you'll only need to make changes to the dist file if you add packages.

After creating the environment.yml file set up the conda environment by running

```
conda env create -f environment.yml
```

## Committing and cleanup

The resulting files you get from scraping aren't gitignored, but don't commit them, they can be saved on box.

Again **DO NOT COMMIT ANY TWITTER CREDENTIALS**.

To deactivate your conda environment:

```
conda deactivate
```

You should deactivate your conda environment when you are done running the project, the environment is only for running this project.

## Updating with new packages

If you need to add packages to the environment add them both in the environment.yml and environment.yml.dist (this ensures it runs on your machine and also others will see the new packages in the dist file and can add them to their yml file). You can add them under the dependencies section (where pandas and numpy are). If the package can only be installed using pip add it under the pip section (where search-tweets-v2 is). Then run:

```
conda env update --file environment.yml  --prune
```

## Tweet Gathering

### Before You Scrape

- Uses the [search_tweets_v2](https://pypi.org/project/searchtweets-v2/) python package to interact with the twitter `/2/tweets/search/all` api
- `scrape_tweets/get_liked_tweets_by_user` function written to interact with the twiter `/2/users/:id/liked_tweets` api, [docs here](https://developer.twitter.com/en/docs/twitter-api/tweets/likes/api-reference/get-users-id-liked_tweets)

N.B. this code requires you to have `TWITTER_BEARER_CREDENTIALS` environment variable, and a `.twitter_keys.yaml` file with twitter api credentials.

You'll need a csv file that contains the names of the cities along with their latitude and longitude (the columns should be called city, lat, long respectively).

Finally you also need to have a file called .twitter_keys.yaml (don't forget the leading dot there) in your home directory (e.g. /home/cloft or /Users/davidhackett). Ask for a copy of this file before scraping tweets.

### How you scrape

Activate the conda environment:

```
conda activate urban_perceptions
```

When ready to run

```
python get_city_tweets.py $FILENAME $RESULTS_PER_QUERY $TOTAL_RESULTS_PER_CITY
```

$FILENAME is the file with the cities and their lat longs. $RESULTS_PER_QUERY is the number of results to get each time the script queries a random date for a given city. $TOTAL_RESULTS_PER_CITY is the total target number of tweets to get for 1 city per category (inside/outside).
