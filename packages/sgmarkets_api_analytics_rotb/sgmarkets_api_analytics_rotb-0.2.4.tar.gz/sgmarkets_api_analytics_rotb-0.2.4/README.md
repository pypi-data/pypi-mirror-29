# SG Markets Analytics API - ROTB - Rates Options Trade Builder v1


## 1- Introduction

This repo is meant to make it easy for clients (and employees) to tap SG Research APIs.  

This is a work in progress and subject to change.  
In particular only a few endpoints of the [Rates Option Trade Builder V1 API](https://analytics-api.sgmarkets.com/rotb/swagger/ui/index) are covered.  

The usual way to expose an API is to make a [swagger](https://swagger.io/) available and also a GUI, typically a web page.  
These have the following drawbacks:
+ A swagger is as precise as it is dull. Unless clients are (working with) IT savvy people they will have a hard time taking advantage of it. In short it is not enough. 
+ A GUI is easy to use but often as much a help as a hindrance: They are very slow/costly to build/adapt, are seldom as flexible as the underlying API, and are no help for industrial use of the API.  

To fill the gap, we introduce the [Jupyter](http://jupyter.org/) notebook as an **API consumption tool** (It as many other uses).  
The associated Python package used here has a very simple interface, but can be arbitrarily modified for (and by) an advanced user. It has the same display capabilities as a web page (being one itself). Most importantly is is written in Python so can be evolved by a business user (as opposed to web front end which is invariably delegated to specialist developpers).


This repo contains:
+ a ready-to-use [demo notebook](http://nbviewer.jupyter.org/urls/gitlab.com/sgmarkets/sgmarkets-api-analytics-rotb/raw/master/demo_sgmarkets_api_analytics_rotb.ipynb)
+ the underlying library in folder [sgmarkets_api_analytics_rotb](https://gitlab.com/sgmarkets/sgmarkets-api-analytics-rotb/tree/master/sgmarkets_api_analytics_rotb)

Here, the notebook is a convenient and versatile interface to
+ hide the plumbing
    + going through the corporate proxy
    + getting the SG API access token (Auth v1.0)
+ make API calls explicit and readable
+ analyse the API response
+ slice and display the results as tables and graphs - and save them


## 2 - Install

From terminal:
```bash
# download and install package from pypi.org
pip install sgmarkets_api_analytics_rotb

# launch notebook
jupyter notebook
```
Create a notebook or run the demo notebook and modify it to your own use case.


## 3 - User guide

Read the [demo notebook](http://nbviewer.jupyter.org/urls/gitlab.com/sgmarkets/sgmarkets-api-analytics-rotb/raw/master/demo_sgmarkets_api_analytics_rotb.ipynb).

The key steps are the following.

### 3.1 - Read the info

The package contains the corresponding API swagger url and contact info:

```python
import sgmarkets_api_analytics_rotb as ROTB
# info about ROTB
ROTB.info()
```

### 3.2 - Define you credentials

See the user guide in the [sgmarkets-api-auth repo](https://gitlab.com/sgmarkets/sgmarkets-api-auth#3-user-guide)


### 3.3 - Pick an endpoint

Select it from the list of those available in the package.  

```python
import sgmarkets_api_analytics_rotb as ROTB
# Examples
ep = ROTB.endpoint..v1_curves
ep = ROTB.endpoint.v1_compute_strategy_components
```

### 3.4 - Create the associated request

Each end point comes with a `Request` object.  

```python
# For all endpoints
rq = ep.request()
```

And fill the object with the necessary data.  
This part is specific to the endpoint selected.  
See the [demo notebook](http://nbviewer.jupyter.org/urls/gitlab.com/sgmarkets/sgmarkets-api-analytics-rotb/raw/master/demo_sgmarkets_api_analytics_rotb.ipynb) for examples.  

Then explore your `Request` object to make sure it is properly set.
```python
# For all endpoints
# display the structure of the object
rq.info()
```

> **IMPORTANT**:  
> You should make sure the request will not overload the server. If not the API call may time out.  
> To this effect the `Request` object will display information, warnings and recommendations.  


### 3.5 - Call the API

You can call the API directly from the `Request` object.  

```python
# For all endpoints
# a is an Api object (see 3.2)
res = rq.call_api(a)
```

The returned object is a `Response` object associated to this endpoint.  
You can explore it starting with

```python
# For all endpoints
# display the structure of the object
res.info()
```

### 3.6 - Save and show the results

As `.csv` and `.xlsx` files.

```python
# For all endpoints
# save to disk
res.save_result(excel=True)
```

The `Response` objects are different for each endpoint.  
See the [demo notebook](http://nbviewer.jupyter.org/urls/gitlab.com/sgmarkets/sgmarkets-api-analytics-rotb/raw/master/demo_sgmarkets_api_analytics_rotb.ipynb) for examples.  


### 3.7 - Slice the results

For those endpoints which return a large amount of data, slicing the result is usually the best/only way to exploit the results.  
Then use the associated `Slice` results down to a 1-D or 2-D or 3-D dataframe.  

```python
# example - see demo notebook for the context
dic_req_fix = {'date': pd.Timestamp('2016-11-11')}
s1 = ep.slice(res, x='expiry', y='tenor', dic_req_fix=dic_req_fix, value='volNormal')

# display the structure of the object
s1.info()

# save to disk
s1.save()
```

### 3.8 - Plot a slice

See the user guide in the [sgmarkets-api-plot repo](https://gitlab.com/sgmarkets/sgmarkets-plot#3-user-guide)
