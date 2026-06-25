# Steps to modify

## app

* install python, using the start menu in windows
* follow the Readme.md  Running Locally steps.  You may need to preced teh commands with "py -m" to 
get round python not being on teh PATH

## Ollama

* install in power shell > irm https://ollama.com/install.ps1 | iex
* download a model , which make take over an hour >   ollama pull gemma4   
* ollama serve

## modify app

* edit the app.py and chat.py  to add an option to use ollama/model. 

This should be in the cambridge branch of  the repo

* laucnh with > py -m streamlit run streamlit_app.py 
* use web interface,  you will have to enter junk text for an api key. 
A future poitnt to imrpove maybe, as there is no api key needed. 


