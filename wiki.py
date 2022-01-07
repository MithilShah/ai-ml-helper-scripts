#Licensed to the Apache Software Foundation (ASF) under one
#or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.  


# This file parses the wikipedia pages xml and creates text files containing sentences. Each text file 
# has a maximum of 5000000 sentences. install the python library wiki_dump_reader.    https://github.com/CyberZHG/wiki-dump-reader

from wiki_dump_reader import Cleaner, iterate
import nltk.data
import re

sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
cleaner = Cleaner()

# i = 0
j = 1
k=1
w = open(f"/home/ec2-user/SageMaker/data/sentence/wiki_{j}.txt","w")
for title, text in iterate('/home/ec2-user/SageMaker/data/enwiki-20220101-pages-articles.xml.bz2.1.out'):
    #print(text)
    text = cleaner.clean_text(text)
    cleaned_text, links = cleaner.build_links(text)
    if (cleaned_text.startswith("REDIRECT")):
        continue
    if "==" in cleaned_text:
        continue
    cleaned_text = cleaned_text.replace("()","")
    cleaned_text = cleaned_text.replace("( )","")
    cleaned_text = cleaned_text.replace("[","")
    cleaned_text = cleaned_text.replace("]","")
    tokenized = sent_detector.tokenize(cleaned_text.strip())
    for sentence in tokenized:
            if sentence:
                sentence = re.sub(' +', ' ', sentence).replace('\n','')
#                 print(sentence+"\n")
                w.write(sentence+"\n")
                k=k+1
#     i = i+1
#     if (i > 10):
#         break
    if (k > 5000000):
        k=1
        j=j+1
        w.close()
        w = open(f"/home/ec2-user/SageMaker/data/sentence/wiki_{j}.txt","w")
    
w.close()
