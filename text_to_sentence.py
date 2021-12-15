
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

# This file iterates through a source folder and for all files in the folder
# creates a corresponding file in the target folder such that the target file has 
# one line per sentence

import os
import nltk.data
import re

sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
dir = "/home/ec2-user/SageMaker/data/pmc/"
for filename in os.listdir(dir):
    #print("processing"+filename)
    with open(dir+"/"+filename) as f:
        try:
            contents = f.read()
        except:
            print("could not read "+filename)
            continue
        tokenized = sent_detector.tokenize(contents.strip())
        w = open(dir+"/"+filename+"_sen","w")
        for sentence in tokenized:
            if sentence:
                sentence = re.sub(' +', ' ', sentence).replace('\n','')
                w.write(sentence+"\n")
        w.close()
    f.close()
    # comment to keep original files
    os.remove(dir+"/"+filename)
             
