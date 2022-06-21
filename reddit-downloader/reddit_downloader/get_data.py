import requests
from pprint import pprint as pp
import argparse
from datetime import datetime
from typing import Callable, Any
import json
import os

UTC_TIME_DELTA = datetime.now() - datetime.utcnow()
MIN_DATETIME = datetime.fromisoformat('2010-01-01')


def get_comments(query: str, params: dict):
    r = requests.get(f"https://api.pushshift.io/reddit/search/comment/", params=params)
    lis = r.json()["data"]
    pp(lis[0])
    print(len(lis))
    pp(r.headers)


def get_data(**kwargs):
    type: str = kwargs.pop("type","submission")
    query: str = kwargs.pop("query", "")
    start_time: int = kwargs.pop("start_time", int(MIN_DATETIME.timestamp()))
    end_time = kwargs.pop("end_time", None)
    count = kwargs.pop("count", None)
    subreddit: str = kwargs.pop("subreddit", ""),
    post_handler: Callable[[dict], Any] = kwargs.pop("post_handler", lambda x: pp(x))

    if kwargs:
        raise ValueError(f"illegal arguments provided {kwargs}")

    if not count and not end_time:
        raise ValueError("provide either count or end_time!")

    if not end_time:
        end_time = int(datetime.utcnow().timestamp())
    else:
        end_time = int((end_time - UTC_TIME_DELTA).timestamp())

    start_time = int((start_time - UTC_TIME_DELTA).timestamp())
    if start_time > end_time:
        raise ValueError("start_time cannot be bigger than end_time!")
    
    
    

    last_post_time = start_time
    last_post_id = None
    total_count = 0
    previous_last_post_id = "0"
    while total_count < count and last_post_time < end_time:
        print(total_count, "of", count)
        print(last_post_time, "before", end_time)
        params = {
            "query": query,
            "after": start_time,
            "after_id": last_post_id,
            "size": 500,
            "subreddit": subreddit,
        }
        r = requests.get(
            f"https://api.pushshift.io/reddit/search/{type}/", params=params
        )
        if r.status_code != 200:
            # TODO handle status errors
            pass

        post_list = r.json()["data"]
        if len(post_list) + total_count > count:
            post_list = post_list[: (count - total_count)]
        total_count += len(post_list)
        last_post = post_list[-1]
        last_post_id = last_post["id"]
        if last_post_id == previous_last_post_id:
            break
        last_post_time = last_post["created_utc"]
        start_time = last_post_time
        previous_last_post_id = last_post_id
        for post in post_list:
            post_handler(post)
    return last_post


def save_post(post):
    if not os.path.isdir("./posts/"):
        os.makedirs("./posts/")
    with open(f"./posts/{post['id']}.json", "w") as f:
        f.write(json.dumps(post))


def main():
    post_handlers = {
        "save": save_post,
        "print": lambda x: print(x),
        "pprint": lambda x: pp(x)
    }
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str, default="", required=False)
    parser.add_argument("--start_time", type=lambda s: datetime.strptime(s, "%d-%m-%Y"), default=MIN_DATETIME, required=False)
    parser.add_argument("--end_time", type=lambda s: datetime.strptime(s, "%d-%m-%Y"), default=datetime.now(), required=False)
    parser.add_argument("--type", type=str, default="submission", required=False)
    parser.add_argument("--count", type=int, default=99, required=False)
    parser.add_argument("--subreddit", type=str, default="", required=False)
    parser.add_argument("--post_handler", type=lambda s: post_handlers[s], default=pp, required=False)
    args = parser.parse_args()
    pp(vars(args))
    get_data(**vars(args))


if __name__ == "__main__":
    main()
