# flask_skeleton
to run the app 
## First
Sign up in Google Analytic to get json file with a secret key and place it at the root of the project 

## Second
create a file name it whatever you like and past the following 
```python
from flask_skelton import create_app
# you can either select development or production
app = create_app('development')

app.run()
```
