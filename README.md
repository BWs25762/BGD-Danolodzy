# projekt BGD grupy Danolodzy

## reddit-downloader
### instalacja
w głównym folderze:
```
python -m venv .venv
.venv\Scripts\activate
pip install reddit-downloader\.
```
lub linux:
```
python -m venv .venv
source .venv/bin/activate
pip install reddit-downloader/.
```
### korzystanie z shella
```
python -m reddit_downloader.get_data --argument wartość
```
aktualnie wspierane argumenty:
--query \
--start_time \
--end_time \
--type \
--count \
--subreddit  \
--post_handler \
--min_score \

## MongoDb container(Windows) 
### Prerequisites 
- docker installed
- create mongodb directory in C folder -> C:\mongodb
- inside mongodb create db directory -> C:\mongodb\db

### How to run 
In terminal(ex. powershell) run 
```
docker-compose up
```
To shut down container press ctrl+c


