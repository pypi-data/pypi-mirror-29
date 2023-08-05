# A profiler for Django

Application measures metrics of current request and renders them in details.

## Installation
Install package.

```bash
pip install djang-webprofiler
```

Enable app:
```python
# settings.py
INSTALLED_APPS = [
    # ...
    'webprofiler',
    # ...
]
``` 

Enable middleware
```python
# settings.py
MIDDLEWARE = [
    # ...
    'webprofiler.middleware.WebProfilerMiddleware',
    # ...
]
``` 

Run migrations
```bash
./manage.py migrate
```
Done.

## Usage
The app will automatically draw a panel at the bottom of the page.

## Included panels
* request / response

* performance
* ajax profiling
* user
* exception trace
* sql queries
* mongodb (if `pymongo` is installed)
* elasticseasrch (if `elasticsearch` is installed)
* ...more is coming


## Credits
* Symfony WebProfilerBundle
* Django Debug Toolbar
