import xlrd
import json
import sys
 
# Give the location of the file
with open("intents.json") as file:
    data_intents = json.load(file)
loc = ("question_answer_pairs.xls")
 
# To open Workbook
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
sheet.cell_value(0,0)


tag = []

def get_tags():
    for i in range(1, sheet.nrows):
        tag.append(sheet.cell_value (i, 0))
    return tag

tag = list(dict.fromkeys(get_tags()))

def update_dict(dict, new_index):
    for j in range(0, len(tag)):
            
            
        to_append = {"tag": "",
                            "patterns": [],
                                "responses": [],
                                "context_set": ""
                            }
        q_list = []
        a_list = []
        for i in range(new_index, 1458):
            if sheet.cell_value(i, 0) == tag[j-1]:
                q_list.append(sheet.cell_value(i, 1))
                a_list.append(sheet.cell_value(i, 2))
            else:
                new_index = i 
                break
        
        to_append["tag"] = tag[j]
        to_append["patterns"].append(q_list)
        to_append["responses"].append(a_list)
        dict["intents"].append(to_append)
    return dict

a_file = open("intents.json", "r")
json_object = json.load(a_file)
a_file.close()

json_object = update_dict(data_intents, 2)

a_file = open("intents.json", "w")
json.dump(json_object, a_file)
a_file.close()

"""
def new_data(data, temp, initial_i):
    while initial_i < 1450:
        for tag_i in range(len(tag) - 1):
            
            questions = []
            answers = []
            to_append = {"tag": "",
                        "patterns": "",
                            "responses": "",
                            "context_set": ""
                        }

            while tag[tag_i] == sheet.cell_value(initial_i, 0):
                questions.append(sheet.cell_value(initial_i, 1))
                answers.append(sheet.cell_value(initial_i, 2))
                initial_i = initial_i + 1
                
            to_append["tag"] = temp
            to_append["patterns"] = questions
            to_append["responses"] = answers
            to_append["context_set"] = ""
            
            data["intents"].append(to_append)
    return data


to_append = {"tag": "",
                        "patterns": [],
                            "responses": [],
                            "context_set": ""
                        }

def new_dict(data, q_list, a_list, index, prev):
    if index >= 700: # number of rows in dataset spreadsheet
        return data
    else:
        if prev == str(sheet.cell_value(index, 0)):
            q_list.append(str(sheet.cell_value(index, 1)))
            a_list.append(str(sheet.cell_value(index, 2)))
            return new_dict(data, q_list, a_list, (index+1), 
                            (str(sheet.cell_value(index,0))))
        else:
            to_append["tag"] = prev
            to_append["patterns"].append(q_list)
            to_append["responses"].append(a_list)
            to_append["context_set"] = ""
            
            print(prev)
            data["intents"].append(to_append)
        
            return new_dict(data, [], [], index, 
                            (str(sheet.cell_value(index, 0))))
        

print(new_dict(data_intents, [], [], 0, (str(sheet.cell_value(1, 0)))))
"""
"""
to_append as arg? 
allow anyone to put in xls file and create their own dataset

make new dictionary at every iteration
later collapse all dictionaries in intents if they have the same tag

"""


