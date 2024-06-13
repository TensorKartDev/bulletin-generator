import os
import json
from pathlib import Path
from pdfminer.pdfparser import PDFParser, PDFSyntaxError
from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines
import json
import os
from dotenv import load_dotenv 
load_dotenv()
root_folder = os.environ["DEFAULT_LOCATION_FOR_TOPIC_COLLECTION"]
topics = r"Topics"
topics_folder = f"{root_folder}/{topics}"
output_file_name = os.environ["OUTPUT_FILES"]

def load_json(file_path):
   with open(file_path, 'r', encoding='utf-8') as file:
       return json.load(file)

def create_nested_dict(hierarchy_dict):
   def nested_insert(d, keys, value):
       for key in keys[:-1]:
           d = d.setdefault(key, {})
       d[keys[-1]] = value
       return d
   nested_dict = {}
   stack = []
   for key, level in hierarchy_dict.items():
       while len(stack) >= level:
           stack.pop()
       if stack:
           current_dict = nested_dict
           for parent in stack:
               current_dict = current_dict[parent]
           current_dict[key] = {}
           stack.append(key)
       else:
           nested_dict[key] = {}
           stack.append(key)
   return nested_dict

def create_folders_from_json(json_data, root_folder):
   def create_nested_folders(data, current_path):
       for key, value in data.items():
           new_path = os.path.join(current_path, key)
           os.makedirs(new_path, exist_ok=True)
           if isinstance(value, dict):
               create_nested_folders(value, new_path)
   if not os.path.exists(root_folder):
       os.makedirs(root_folder)
   create_nested_folders(json_data, root_folder)
   print("Folders created for Topics")

def sanitize(word):
    return word.replace(".","").replace("-", "").replace("'", "").replace("\“", "").strip()

def extract(input_file_name):
    extracted_outlines = {}
    # Extract the outlines into a dictionary 
    with open(input_file_name, "rb") as fp:
        try:
            parser = PDFParser(fp)
            document = PDFDocument(parser)
            outlines = document.get_outlines()
        
            for (level, title, dest, a, se) in outlines:
                extracted_outlines[sanitize(title)] = level
                #print(level, title)
        except PDFNoOutlines:
            print("No outlines found.")
        except PDFSyntaxError:
            print("Corrupted PDF or non-PDF file.")
        finally:
            parser.close()
    del extracted_outlines["Contents"]
    return extracted_outlines

extracted_outlines = extract()
# Based on the level create a nested dictionary and save to a topics.json file 
nested_dict = create_nested_dict(extracted_outlines)
topics_json_file_path = f"{topics_folder}\\topics.json"
with open(topics_json_file_path, 'w') as f:
    json.dump(nested_dict, f)


# input_file = "200R IM Input.pdf"
# input_file_name = f"{os.environ['INPUT_FILES']}/{input_file}"

# print(input_file_name, output_file_name)