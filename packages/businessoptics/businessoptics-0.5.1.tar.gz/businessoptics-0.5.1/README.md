BusinessOptics Client
=====================

Easy access to the BusinessOptics API, based on the python requests library.

For example:

```python
from businessoptics import Client

print Client(auth=('user@example.com', 'apikey')).workspace(123).query('ideaname').tuples()
```

Installation
------------
```bash
pip install businessoptics
```

Authentication
--------------

Construct a new Client. 

Authentication details can either be passed in directly:
```python
client = Client(auth=('user@example.com', 'apikey'))
```

or be extracted from environment variables:

* BUSINESSOPTICS_EMAIL
* BUSINESSOPTICS_APIKEY

so you can go 

```python
client = Client()
```

or from a `~/.businessoptics_client.config` JSON file of the form

```json
{ 
  "user@example.com": "<apikey>",
  "other@example.com": "<apikey>" 
}
```

so you can easily switch between multiple users and create a client as below

```python
client = Client(auth="user@example.com")
```

Usage
-----

The client uses logging to show what it's doing, so make sure you have logging configured. A quick way to do this is as follows:

```python
from businessoptics import setup_quick_console_logging

setup_quick_console_logging()
```

### Run a query and download tuples

```python
client = Client()
workspace = client.workspace(123)

# For a single idea:
tuples = workspace.query('idea_name1').tuples()
# tuples is now a list of dictionaries

# For multiple ideas:
query = workspace.query(['idea_name1', 'idea_name2'])
tuples1 = query.tuples('idea_name1')
tuples2 = query.tuples('idea_name2')

# For large numbers of tuples:
for tup in query.tuple_generator('idea_name1'):
    process(tup)
    
# Get a (possibly cached) pandas dataframe of tuples:
df = query.to_df('idea_name1')

# Quick queries have a similar API, e.g.
tuples = workspace.quick('idea_name1').tuples()
```

### Upload tuples to a dataset

```python
dataset = client.dataset(456)
dataset.upload_tuples(
    [{'id': 1, 'name': 'alice'}],
    [{'id': 2, 'name': 'bob'}],
)

# Or use a generator for large amounts of tuples, e.g.
def tuples():
    for i, tup in enumerate(large_database_query()):
        tup['id'] = i
        yield tup

dataset.upload_tuples(tuples())

# Or upload a pandas DataFrame
df = pd.read_csv(...)
dataset.upload_df(df) # Uploads all the columns, but not the indexes
dataset.upload_df(df.reset_index()) # Uploads all the indexes as well

```

### Download a file from Google Drive

```python
from businessoptics import gdrive_file

# Get URL by clicking on a file and then 'Get shareable link' in Google Drive
gfile = gdrive_file('https://drive.google.com/open?id=ABCDEF123')

gfile.path()  # The path to the downloaded file
gfile.open()  # Open the file
gfile.unzip() # Unzip the file, returning a similar object. The zip must only contain one file
gfile.untar() # Untar the file. Similar to the above, but use for '.tar.gz'.
gfile.unzip('the_only_file_you_need.csv')  # extract a specific file when there are many

# Read a zipped CSV into Pandas
df = pd.read_csv(gfile.unzip().path())
```

### Upload a file to Google Drive

```python
from businessoptics import upload_to_google_drive

# File will be called 'a_local_file.csv' on Google Drive
upload_to_google_drive('path/to/a_local_file.csv')

# File will be called 'name_on_drive.csv' on Google Drive
upload_to_google_drive('path/to/a_local_file.csv', 'name_on_drive.csv')

# File will be zipped before upload and will be called 'a_local_file.csv.zip' on Google Drive 
upload_to_google_drive('path/to/a_local_file.csv', zipit=True)
```

### Controlling the download cache

If the `/global_cache` folder is present (e.g. it is on jupyter.businessoptics.net) then by default cached files (from `gdrive_file()` or `.to_df()`) are stored there and shared by everyone. This may lead to strange behaviour if multiple people are downloading the same behaviour. You can avoid this and only use the cache in your home folder as follows:

```python
from businessoptics import isolate_cache

isolate_cache()
```

### Generic API usage

Every Client instance has a base URL. All requests made from it start from that base, and you can optionally add more to the URL for the request. For example:

```python
client = Client()  # client.base_url is ''
workspace = client.workspace(123)  # workspace.base_url is '/api/v2/workspace/123'

# sends a GET request to /api/v2/workspace/123, returning metadata about the workspace
workspace.get()

# sends a GET request to /api/v2/workspace/123/query, returning the query history
# of the workspace
workspace.get('query')
```

The API responds with JSON which is automatically parsed into Python data structures, with a dictionary at the top.

If you want to send a POST, PUT, or DELETE request, use the `post/put/delete` method. You will probably need to specify the `json` keyword argument with some dictionary for the body of the request.

If there was an error, an `APIError` exception will be raised.

### Resource classes

`Client` has several subclasses, each representing different resources in the app and having different methods. Here is how you would create instances of these classes and a brief overview of what you can do with them. For more details see the source code and docstrings.

All of these classes have base URLs which accept a plain `get()` to get metadata about the resource.

```python
from businessoptics import Client, Workspace, DataCollection, Dataset, Query, IdeaResult, Dashboard

client = Client()

# Workspace

workspace = client.workspace(123)
workspace = client.workspace('workspace name')
workspace = Workspace.at(client, '/api/v2/workspace/123/')

## Initialise a training run
training_run = workspace.train(['idea1', 'idea2'])
## Wait for it to complete
training_run.await()

# Query

## Get an existing, previously initiated query:
query = client.query(456)
query = Query.at(client, '/api/v2/query/456')

## Run a new query:
query = workspace.query(['idea_name1', 'idea_name2'])
### Pass knowledge parameters:
query = workspace.query('idea_name', parameters={'param1': 1, 'param2': 2})
### Run using hadoop:
query = workspace.query('idea_name', execution_mode='hadoop')

## To get tuples, use the tuples(), tuple_generator(), or to_df() methods that
## exist in IdeaResult. You don't have to separately get the result, just pass
## the idea name as the first argument, e.g. you can do:
tuples = query.tuples('idea_name')
## which is equivalent to:
tuples = query.result('idea_name').tuples()

## You can also run quick queries by replacing workspace.query with workspace.quick

# IdeaResult

result = query.result('idea_name1')
result = IdeaResult.at(client, '/api/v2/query/456/result/idea_name1')
tuples = result.tuples()

## For large numbers of tuples:
for tup in result.tuple_generator():
    process(tup)
    
## Get a dataframe:
df = result.to_df() 

## Reingest into a dataset
data_update = result.reingest_into_existing_dataset(456)
## Wait for the reingestion to finish
data_update.await()

# DataCollection

collection = client.datacollection(123)
collection = client.datacollection('collection name')
collection = DataCollection.at(client, '/api/v2/datacollection/123')
collection = client.dataset(456).collection  # NOT the datacollection method

# Dataset
dataset = client.dataset(456)
dataset = collection.dataset('dataset name')
dataset = Dataset.at(client, '/api/v2/dataset/456')

## For uploading tuples, see section above

## Downloading tuples is similar to IdeaResult: 
## use the methods tuples(), tuple_generator(), and to_df()
## You can also specify filters for the first two methds - see the docstring for tuple_generator

## Create a new dataset:
dataset = collection.create_tablestore_dataset(
            name='test',
            dimensions=[
                dict(name='col1', type='integer', default='-1', key=False),
                dict(name='col2', type='integer', default='-1', key=False),
            ]
        )
## or from a dataframe (see docstring):
dataset = collection.create_tablestore_dataset_from_df('df test', df)
        
## Duplicate a dataset
dataset_name = dataset.get()['name']
new_dataset_name = 'new.' + dataset_name
new_dataset = dataset.duplicate(new_dataset_name)  # see docstring for more parameters

## Rename a dataset:
new_dataset.rename(dataset_name)

## Delete a dataset:
dataset.delete()

## Delete tuples:
dataset.delete_tuples()  # see docstring for how to specify filter

# Dashboard
dashboard = client.dashboard(456)
dashboard = workspace.dashboard('dashboard name')
dashboard = Dashboard.at('/api/v2/dashboard/456')
```
