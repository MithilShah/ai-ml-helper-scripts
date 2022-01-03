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

# This file parses the code from ftp.ncbi.nlm.nih.gov//pub/litarch/ 
# and gets the text of the body

import os
import glob
import tarfile
import xml.etree.ElementTree as ET
import nltk.data
import re
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

dir = "/home/ec2-user/SageMaker/data/ncbi/"
sentence_file = "/home/ec2-user/SageMaker/data/ncbi/sentence_file.txt"
def process_extracted(extracted_file):
    root = ET.parse(extracted_file).getroot()
    for body in root.findall('body'):
        for p in body.findall('p'):
            if p.text:
                 tokenized = sent_detector.tokenize(p.text.strip())
                 for sentence in tokenized:
                     if sentence:
                         sentence = re.sub(' +', ' ', sentence).replace('\n','')
                         f.write(sentence)
    
    
    
def process_tar_gz_file(filename):
    try:
        file = tarfile.open(filename, "r:gz")
        members = file.getmembers()
        for member in members:
            if member.isfile():
                name = member.name
                if name.endswith("xml"):
                    extracted = file.extractfile(member)
                    process_extracted(extracted)
    except:
        print("cant process " + filename)
        return             

for filename in glob.iglob(dir + '**/*.gz', recursive=True):
     with open(sentence_file,"w") as f:
        process_tar_gz_file(filename)
     f.close()
        