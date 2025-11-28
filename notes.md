# Notes
## Running the program
just use `python main.py`, 
no need to run `fastapi` command

## Main design decision (sorry if this is too long, below is just a quick overview of the files 😅)
The code in main.py (i renamed it to `reference.py.bak`) now splitted into few class/file
|- data
|   |- access
|   |   |- Document Store: This file manages access to qdrant/in memory storage
|   |
|   |- entity
|       |- API request object: this is just a copy paste from original python script
|
|- logic
|   |- embeddings
|   |   |- embedding interface: this is an interface to interact with embedding function
|   |   |- fake embedding: this is where the fake embedding function reside
|   |
|   |- API Controller: this is a class that provide API enpoint via fastapi 
|   |
|   |- workflow
|       |- workflow interface: this is an interface to interact with workflow functions
|       |- simple workflow: this is a bit modified version of workflow where i remove
|                           the database operations from workflow to separate file in
|                           "Document Store" below. 
|
|- Config: Configure things like qdrant collection name, etc. here
|- Main: A main function to run them all

The code primarily uses dependency injection pattern to make swapping to other implementation
easier. So... you can for example swap the fake embeddings with real one just by creating new embedding
class implementing the IEmbeddings, and then passing it to the documentStore by parameter in documentStore's init. 

## Tradeoff that were made
The tradeoff, for this too simple project, is verbosity and boilerplate. the object oriented approach may
make it not so straightforward when reading the code. you should look at different file, and create
class according to the interface (also modify the interface when you need to).  

## How this ver. improve maintainability
This version separates responsibilities in the original file (`reference.py.bak`) to few files.
Each file has it own function described as above (main design decision section).
The dependency injection pattern allows you to swap/test a class with different implementation.
The variables is no longer global too. Everything is contained inside the respective class.