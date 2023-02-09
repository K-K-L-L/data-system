# Imports
import json
from langdetect import detect
import nltk
import random
from datetime import datetime
# The list for the punctuation marks
list2 = ["؟", "،", "!", "?", "¿", ".", ","]

# The main class
class DataSystem:

  def __init__(self):
    # The files needed for the NLTK library
    nltk.download("punkt")
    nltk.download('stopwords')


  # The SummarizeText method
  def SummarizeText(self, text, ratio):
    sentences = nltk.sent_tokenize(text)
    word_count = len(nltk.word_tokenize(text))
    target_word_count = int(ratio * word_count)
    total_words = 0
    summary = []
    for sent in sentences:
      words = len(nltk.word_tokenize(sent))
      if total_words + words <= target_word_count:
        summary.append(sent)
        total_words += words
      else:
        break
    summary = " ".join(summary)
    for word in list2:
      summary = summary.replace(word, "")
    return summary


  # The GetTitle method
  def GetTitle(self, text):
    with open('WordsToRemove.json', 'r', encoding='utf8',errors='ignore') as f:
      data = str(f.read())
    data_list = json.loads(data)
    data = data_list["Arabic_And_English_Words"]
    words = text.split()
    text = ' '.join(words[:10])
    text = text.lower()
    text = ' '.join([word for word in text.split() if word not in data])
    for word in list2:
      if word in list2:
        text = text.replace(word, "")
    text = text.title()
    self.SummarizeText(text, 0.5)
    return text


  # The SaveData method
  def SaveData(self, website_text, title="", file_name="", file_extension=".json", url="", debug=True):
    ratio = 0.5
    # Uses the SummarizeText method to summarize the text
    self.SummarizeText(website_text, ratio)
    # Checks if the file extension is supported
    if file_extension not in [".json", ".txt"]:
      return print("file not supported")
    # Checks if the user inputed the file name
    if not file_name:
      file_name = str(random.randint(0, 9999999))

    filename = f"{file_name}{file_extension}"
    if(title):
      pass
    else:
      title = self.GetTitle(website_text)
    # The data that's gonna be in the JSON file (UNFINISHED)
    data = {
      "title" : title,
      "text": website_text,
      "url": url,
      # Gets the time
      "time_crawled": str(datetime.now())
    }

    # Writes the file as a .txt file
    if file_extension == ".txt":
      with open(filename, "a", encoding="utf-8") as f:
        f.write(f"text: {website_text}\nurl: {url}\n\n")
      if debug:
        return print(f"file saved as {filename}")
    else:
      # Reads the data in the .json file (if found)
      try:
        with open(filename, "r", encoding="utf-8") as f:
          existing_data = json.load(f)
      except FileNotFoundError:
        existing_data = []
      except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        existing_data = []
      # Appends the data
      existing_data.append(data)
      # Writes the file as a .json file
      try:
        with open(filename, "w", encoding="utf-8") as f:
          json.dump(existing_data, f, indent=4, ensure_ascii=False)
      except Exception as e:
        print(f"An error occurred while writing to the file: {e}")
      else:
        if debug:
          print("Data written to the file successfully!")
 

dt = DataSystem()
text = "This is a sample text. This text can be summarized. The goal of summarization is to keep the most important information."
language = "en"
ratio = 0.5

# Uses the SummarizeText method in the DataSystem class to summarize the text
print(dt.SummarizeText(text, ratio))
# Uses the GetTitle method in the DataSystem class to get the title
print(dt.GetTitle(text))
# Uses the SaveData method in the DataSystem class to save the data
print(dt.SaveData("example text", None, "example", ".json", None, True))
