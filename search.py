import pandas as pd

df = pd.read_csv('nhk_articles1.csv', header=None)
articles = df.iloc[:,2].values
while(True):
    words = input('検索したい言葉をスペース区切りで入力してください\n').split("　")
    if words=='。':
        break
    hits = []
    for article in articles:
        sentences = article.split("。")
        for i in range(len(sentences)):
            for word in words:
                if word in sentences[i]:
                    hits.append(sentences[i])
    print("{} matches".format(len(hits)), "\n")
    for hit in hits:
        print(hit, '\n')
