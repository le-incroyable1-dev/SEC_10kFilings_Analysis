import streamlit as st
import streamlit
import os
import sec_edgar_downloader
import re
from typing import Optional
from bs4 import BeautifulSoup
import requests
import json
import ast
import time
import sys

save_dir = './sec_filings'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

filings = []

from sec_edgar_downloader import Downloader

user_input = ""
user_input = streamlit.text_input("Enter the company ticker to analyze financial trends : ", "")
companies = []
companies.append(user_input)

while user_input == "":
   time.sleep(5)

start_year = 1995
end_year = 2023

dl = Downloader("FSIL", "auravaces@gmail.com", "./sec_filings/")
processed = 0

for company in companies:
    if processed == 1:
       break

    st.info(f"Downloading filings for {company}...")
    try:
        dl.get("10-K", company, after="{}-01-01".format(start_year), before="{}-01-01".format(end_year + 1))

        st.info(f"Success! Downloaded {company} 10-K filing")
    except Exception as e:
        st.info(f"Error downloading {company} 10-K filing: {e}")
        sys.exit()

st.info("All filings downloaded successfully!")


filings = []
for company in companies:
  folder_path = "./sec_filings/sec-edgar-filings/{}/".format(company)

  # Walk through the directory tree and search for .txt files
  for root, dirs, files in os.walk(folder_path):
      for file in files:
          if file.endswith(".txt"):
            filings.append(os.path.join(root, file))


print(len(filings))

# used to extract between two items to get a section
PATTERN1: re.Pattern = re.compile(r"item\s*8\.")
PATTERN2: re.Pattern = re.compile(r"item\s*9\.")


def extract_section(file_path: str) -> Optional[str]:

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file.read(), "html.parser")
    except (FileNotFoundError, UnicodeDecodeError) as e:
        raise e

    parsed_text: str = soup.get_text()
    lower_parsed_text: str = parsed_text.lower()

    item_7_matches = [
        match.start() for match in PATTERN1.finditer(lower_parsed_text)
    ]
    item_8_matches = [
        match.start() for match in PATTERN2.finditer(lower_parsed_text)
    ]

    if not item_7_matches or not item_8_matches:
        return "section not found."

    start_idx = item_7_matches[1] if len(item_7_matches) > 1 else item_7_matches[0]
    end_idx = item_8_matches[1] if len(item_8_matches) > 1 else item_8_matches[0]

    section_content: str = parsed_text[start_idx:end_idx].strip()
    section_content = " ".join(section_content.split())
    section_content = BeautifulSoup(section_content, "html.parser").get_text()

    return section_content

all_financial_data = ""
for file in filings:
  if processed == 1:
     break
  print("extracting content from ", file , " .....")
  content = extract_section(file)
  all_financial_data += content + "\n"

st.info("Extracted financial data from all files!")

maxPromptLen = min(199999, len(all_financial_data)) # according to max prompt length for request
st.info("Fitting Data into the Maximum Prompt Length")
all_financial_data = all_financial_data[:maxPromptLen - 325] # force trim the data to fit in the available limits, change accordingly
prompt = "\n\nHuman: Here are the financial data sections from sec 10k filings : {} . Give me the revenue, expenses, profitability of the different years mentioned in the data in the form of arrays (array name = array) and an array called years for the years as well. Only return the arrays in the response and no other text. \n\nAssistant:".format(all_financial_data)

processed = 1 # mark processed

  # post a request to anthropic to get the insights from the extracted sections
OPTION = ""
st.info("Currently the app runs on Anthropic API, can be extended in the future!")
OPTION = streamlit.text_input("Enter 1 if you have a valid Anthropic Api Key or enter 0 to display a demo from GOOGL : ", "")
while OPTION == "":
   time.sleep(5)

print("OPTION : ", OPTION)

APIKEY = ""
if OPTION == "1":
   APIKEY = streamlit.text_input("Enter an ANTHROPIC API Key with Credits (Can get 5$ of credits for free) : ", "")
elif OPTION == "0":
   APIKEY = "xyz"
else:
   sys.exit()
   
while APIKEY == "":
   time.sleep(5)

print("APIKEY : ", APIKEY)

response = requests.post(
    "https://api.anthropic.com/v1/complete",
    headers={
        "accept": "application/json",
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
        "x-api-key": APIKEY
    },
    json={
        "model": "claude-2.1",
        "prompt": "{}".format(prompt),
        "max_tokens_to_sample": 2000
    }
)
print("RESPONSE : ", response)
data_dict = json.loads(response.text)

result = ""
if "completion" not in data_dict:
   result = "Here are the revenue, expenses, cost of revenue, operating income, net income, and years in array form based on the financial data provided: ```js const revenues = [182527, 257637, 282836]; const expenses = [141303, 178923, 207994];  const costOfRevenues = [84732, 110939, 126203]; const operatingIncome = [41224, 78714, 74842]; const netIncome = [40269, 76033, 59972]; const years = [2020, 2021, 2022]; ```"
else:
   result = data_dict["completion"]

def find_indexes(text):
    indexes = []
    for i, char in enumerate(text):
        if char == '[':
            indexes.append(i)
    return indexes

# if a valid key was entered and a response was generated correctly
# it will get the array positions, else use the store result
array_positions = find_indexes(result)
print(array_positions)

# # -_

array_names = [] # to store the names of the arrays we create
for pos in array_positions:
  # let's get the array first
  i = pos
  arr = ""
  while result[i] != ']':
    arr += result[i]
    i += 1
  arr += ']'
  array = ast.literal_eval(arr)

  # now let's get the array name
  i = pos - 4
  name = ""
  while result[i].isalpha():
    name += result[i]
    i -= 1

  name = name[::-1]

  array_names.append(name)
  globals()[name] = array

import matplotlib.pyplot as plt

st.info("PLOTTING....")

years = globals()["years"]
for name in array_names:
  print(name)
  arr = globals()[name]
  print(arr)
  if name != "years":
    plt.plot(years, arr, marker='o', linestyle='-', label=name)

# Adding labels and title
plt.title('Financial Trends Across Years')
plt.xlabel('Year')
plt.ylabel('Trends')

# Adding legend
plt.legend()

# Displaying the plot
plt.grid(True)
plt.tight_layout()
streamlit.pyplot()


st.info("Thanks for stopping by :)")
