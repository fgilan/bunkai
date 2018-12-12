from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import MeCab
import collections

app = Flask(__name__)

df1 = pd.read_csv('nhk_articles_toku.csv', header=None)
df2 = pd.read_csv('nhk_articles_newsup.csv', header=None)
df3 = pd.read_csv('nhk_articles_new.csv', header=None)
articles1 = list(df1.iloc[:,2].values)
articles2 = list(df2.iloc[:,2].values)
articles3 = list(df3.iloc[:,2].values)
articles = articles1 + articles2 + articles3
article_count = str(len(articles))
message = '検索したい言葉を入力してください。現在の記事数　' + article_count

def search(word):
    hits = {}
    for article in articles:
        sentences = article.split("。")
        for i in range(len(sentences)):
            if word in sentences[i]:
                #store the index of the word for bolding later
                idx = sentences[i].index(word)
                hits[sentences[i] + "。"] = idx
    return hits

def patterns(hits, word):
    p = MeCab.Tagger('-Owakati')
    counter = collections.Counter()
    avoid = [w for w in word] + [word] + ['\n', '']
    for sentence in hits.keys():
        #get the part of the sentence surrounding the word
        neighborhood = sentence[max(0, hits[sentence] - 5) : min(len(sentence) - 1, hits[sentence] + len(word) + 5)]
        #parse the neighborhood and udpate the counter
        counter.update([w for w in list(p.parse(neighborhood).split()) if w not in avoid and len(w) >= 2])
    return counter.most_common(5)

@app.route('/')
def index():
    title = 'ようこそ'
    return render_template('index.html', title = title, message = message)

@app.route('/post', methods=['GET', 'POST'])
def post():
    title = "こんにちは"
    if request.method == "POST":
        word = request.form['word']
        hits = search(word)
        pat = patterns(hits, word)
        return render_template('index.html', message = message, word = word, title = title,
            hits = hits, hits_number = len(hits), patterns = pat)
    else:
        return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(error):
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.debug = True
    app.run()
