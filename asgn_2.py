import re
import random
from math import log
from collections import defaultdict


tri_counts=defaultdict(int) #counts of all trigrams in input

possibility = defaultdict(int)
letter_set = set()
test_list=[]

def preprocess_line(line):
    line = line.lower()
    line = re.sub("[0-9]","0",line)
    line = re.sub("[^0|^a-z|^.|^ ]","",line)
    line = "##" + line + "#"
    return line




def read_data_set (file):
    with open(file) as f:
        for line in f:
            line = preprocess_line(line) #doesn't do anything yet.
            for j in range(len(line)-(3)):
                trigram = line[j:j+3]
                letter_set.update(set(trigram))
                tri_counts[trigram] += 1


def trigram_language_model(tridict,possibility):
    double_counts = defaultdict(int)
    for i in tridict.keys():
        double_counts[i[:2]] += tridict[i]
    for i in sorted(double_counts.keys()):
        sum = 0
        for j in sorted(letter_set):
            sum+=(tridict[i+j]+1)/(double_counts[i]+len(letter_set))
            possibility[i+j] = (tridict[i+j]+1)/(double_counts[i]+len(letter_set))



def write_to_file(path):
    f = open(path,"w")
    for key in sorted(possibility.keys()):
        f.write(key+"\t"+str("%.3e"%float(possibility[key]))+"\n")

def random_pick(c,p):  #按照可能性随机一个字母
    x = random.uniform(0, 1)
    cum_prob = 0

    for item,item_p in zip(c,p):
        cum_prob+=item_p

        if x < cum_prob:
            return item




def generate_from_LM(dict,N,set):  #生成句子开头是两个空格生成时删掉
    str = "  "
    keyc = list(set)
    for i in range(N):
        temp = str[len(str)-2]+str[len(str)-1]
        prob=[]
        for m in keyc:
            key = temp+m
            if dict[key]!=0:
                prob.append(dict[key])

            else:
                prob.append(1/(len(keyc)))

        temp =random_pick(keyc, prob)
        str += temp

    return str[2:]

def string_to_key_value(string):
    key = string[:3]
    list=string.split()
    value = list[-1]
    return key,float(value)

def read_file_makedic(path):
    dict=defaultdict(int)
    f = open(path)
    str=""
    line = f.readline()
    key,value = string_to_key_value(line)
    dict[key] = value
    while line:
        str+=key
        line = f.readline()
        if len(line) > 3:
            key, value = string_to_key_value(line)
            dict[key] = value
    f.close()
    return dict,set(str)

def get_test_lists(file):
    with open(file) as f:
        for line in f:
            line = preprocess_line(line) #doesn't do anything yet.
            for j in range(len(line)-(3)):
                trigram = line[j:j+3]
                test_list.append(trigram)



def caulate_perplexity(string_list,prob_dict,deauft_set=letter_set):
    result=0
    for i in range(len(string_list)):
        prob = prob_dict[string_list[len(string_list)-1-i]]
        if prob==0:
            result+=log(1/len(deauft_set),2)
        else:
            result+=log(prob,2)
    return 2**(-1*(1/len(string_list))*result)







read_data_set("training.en")
trigram_language_model(tri_counts,possibility)
result=generate_from_LM(possibility,300,letter_set)
print(result)

print(len(result))
d1,set1=read_file_makedic("model-br.en")
result=generate_from_LM(d1,300,set1)

print(result)
print(len(result))
get_test_lists("test")
print("perplexity",caulate_perplexity(test_list,possibility))
print("perplexity",caulate_perplexity(test_list,d1,set1))
# write_to_file("write_test")
# for trigram in sorted(possibility.keys()):
# print(trigram, ": ", possibility[trigram])
# print(letter_set)
# print(len(letter_set))
# for tri_count in sorted(tri_counts.items(), key=lambda x:x[1], reverse = True):
#     print(tri_count[0], ": ", str(tri_count[1]))

