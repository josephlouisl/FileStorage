## Install
```
pip install -r requirements.txt
```
#### [Install MongoDB](https://docs.mongodb.com/manual/installation/)
#### settings.py
* Configurate DB
* Set AWS_BUCKET
* Set AWS_SECRET_ACCESS_KEY
* Set AWS_ACCESS_KEY_ID

## RUN
```
python app.py
```
## Usage
#### Upload file
```
curl -F "file=@PATH_TO_FILE" http://127.0.0.1:8888/upload -X PUT
```
```javascript
{
  "key": KEY
 }
```
#### Get file 
```
curl  http://127.0.0.1:8888/KEY
```
#### Response
```javascript
{
  "file_name": FILE_NAME,
  "file_content": FILE_CONTENT
 }
```
