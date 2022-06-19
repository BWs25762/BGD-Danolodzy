import requests
from pprint import pprint as pp
import argparse



def get_comments(query: str, params: dict):
    r = requests.get(f"https://api.pushshift.io/reddit/search/comment/?q={query}", params=params)
    lis = r.json()['data']
    pp(lis[0])
    print(len(lis))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-q','--query')
    args = parser.parse_args()
    get_comments(args.query, {"size": 1000})

if __name__ == "__main__":
    main()