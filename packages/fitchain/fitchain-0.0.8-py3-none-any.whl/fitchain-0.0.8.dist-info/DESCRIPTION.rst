### What is this repository for? ###

* python based SDK  
* v0.1

This repo implements the SDK to manage projects and models on a local fitchain pod

### Feedback ###
Reach out and tell us how we can improve this SDK to make it easier for you to work with the pod and build your models. 

You may always drop us a mail at ```code@fitchain.io``` 


### Getting Started ###
First install the fitchain sdk using pip:
```bash
pip install fitchain
```

Once the fitchain sdk has been installed, you can use the library:

```python
from fitchain import FitChain

fc = FitChain()
```

Call the ```projects()``` method to get an overview of all available projects. You may even enter a query string to 
filter your results.

```python
projects = fc.projects()
```

Once a project has been chosen, the datasources linked to the project can be retrieved using the ```datasources``` property
```python
project = projects[...]
project_datasources = project.datasources
```

Data for a specific datasource can be loaded by calling the ```load(<datasource_id)``` method on the project
```python
project_datasource_id = ...
project.load(project_datasource_id)
```

### Reference
The following methods are available as part of the SDK

##### Pod Identity #####
```python
identity = fc.identity()
```

##### List projects #####
```python
projects = fc.projects()
```

##### List workspaces #####
```python
workspaces = fc.workspaces()
```

##### List providers #####
```python
providers = fc.providers()
```

##### List Owned Datasources #####
```python
datasources = fc.datasources()
```

##### List jobs #####
```python
jobs = fc.jobs()
```

