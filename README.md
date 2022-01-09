# chatbot
A simple chatbot in python. 

main.py: Creates Neural Networks and trains the network to produce appropriate responses to inputted questions from the dataset in 'intents.json' file.
read-dataset.py: Reads a spreadsheet of xls. format with series of question and answer pairs under a specific topic and produces a dictionary in an appropriate format to update 'intents.json' file.
intents.json: Contains the said dataset in the following format:

{"intents": [{"tag": "", 
  "patterns": ["list of questions"], 
  "responses": ["list of responses"], "context_set": ""}]}
  
If you wish to train the chatbot based on a different dataset, replace the question_and_answer_pairs.xls file with another xls with the dataset, but in the same format.


[The existing question_and_answer_pairs.xls was imported and reformatted from Question-Answer Dataset released by Noah Smith et al. at Carnegie Mellon University]
