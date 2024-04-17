from interact import preprocess_pipeline, get_tasks
import pandas as pd
from tqdm import tqdm

syslist = []
uslist = []
lab1 = []
tuplelist = []

sys2list = []
uslist2 = []
lab2 = []

df = pd.read_csv("extraction.csv")
for i in tqdm(range(len(df))):
    sys = df.iloc[i]["System Prompt"]
    up = df.iloc[i]["User Prompt"]
    up = preprocess_pipeline(up)
    sys2list.append(sys)
    uslist2.append(up)
    lab2.append(0)
    tasks = get_tasks(up)
    for t in range(len(tasks)):
        if(tasks[t].strip() != ""):
            if tasks[t].strip() in tuplelist:
                continue
            syslist.append(sys)
            uslist.append(tasks[t].strip())
            tuplelist.append((tasks[t].strip()))
            lab1.append(0)


df = pd.read_csv("hijacking.csv")
for i in tqdm(range(len(df))):
    sys = df.iloc[i]["System Prompt"]
    up = df.iloc[i]["User Prompt"]
    up = preprocess_pipeline(up)
    sys2list.append(sys)
    uslist2.append(up)
    lab2.append(0)
    tasks = get_tasks(up)
    for t in range(len(tasks)):
        if(tasks[t].strip() != ""):
            if tasks[t].strip() in tuplelist:
                continue
            syslist.append(sys)
            uslist.append(tasks[t].strip())
            tuplelist.append((tasks[t].strip()))
            lab1.append(0)


pd.DataFrame({"System Prompt": syslist, "User Prompt": uslist, "label": lab1}).to_csv("neg-broken.csv")
pd.DataFrame({"System Prompt": sys2list, "User Prompt": uslist2, "label": lab2}).to_csv("neg-full.csv")

df = pd.read_csv("pos-und.csv")
syslist = []
uslist = []
lab1 = []

for i in tqdm(range(len(df))):
    sys = df.iloc[i]["System Prompt"]
    up = df.iloc[i]["User Prompt 1"]
    syslist.append(sys)
    uslist.append(up)
    lab1.append(1)
    up = df.iloc[i]["User Prompt 2"]
    syslist.append(sys)
    uslist.append(up)
    lab1.append(1)
    up = df.iloc[i]["User Prompt 3"]
    syslist.append(sys)
    uslist.append(up)
    lab1.append(1)

pd.DataFrame({"System Prompt": syslist, "User Prompt": uslist, "label": lab1}).to_csv("pos.csv")


df1 = pd.read_csv("neg-full.csv")
df2 = pd.read_csv("pos.csv")

e1 = len(df1)*0.8
e2 = len(df2)*0.8
df = pd.concat([df1[:int(e1)], df2[:int(e2)]])
df = df.sample(frac=1).reset_index(drop=True)
df.to_csv("train_data.csv")


df = pd.concat([df1[int(e1):], df2[int(e2):]])
df = df.sample(frac=1).reset_index(drop=True)
df.to_csv("test_data.csv")

