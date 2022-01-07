
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

#This file parses the files from ftp.ncbi.nlm.nih.gov/pub/pmc/ and creates sentences

import os
import nltk.data
import re
import random

sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
dir = "/home/ec2-user/SageMaker/data/pmc_noncomm/"
j = 1
k=1
w = open(f"/home/ec2-user/SageMaker/data/sentence/pmc_nc_{j}.txt","w")
for filename in os.listdir(dir):
    print(filename)
    with open(dir+"/"+filename,encoding="utf8", errors='ignore') as f:
        try:
            contents = f.read() 
            split_contents = contents.split("====")
            if (len(split_contents) > 2):
                contents = split_contents[2].strip()
            tokenized = sent_detector.tokenize(contents)
            for sentence in tokenized:
                i = random.randint(1, 4)
                if (sentence and i==2) :
                    sentence = re.sub(' +', ' ', sentence).replace('\n','')
                    w.write(sentence+"\n")
                    k=k+1    
        except Exception as e:
            print(e)
            continue
    if (k > 5000000):
        k=1
        j=j+1
        w.close()
        w = open(f"/home/ec2-user/SageMaker/data/sentence/pmc_nc_{j}.txt","w")
w.close()
