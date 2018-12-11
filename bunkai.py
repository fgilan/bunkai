from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

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
        return render_template('index.html', message = message, word = word, title = title,
            hits = hits, hits_number = len(hits))
    else:
        return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(error):
    return redirect(url_for('index'))

def search(word):
    hits = {}
    for article in articles:
        sentences = article.split("。")
        for i in range(len(sentences)):
            if word in sentences[i]:
                idx = sentences[i].index(word)
                hits[sentences[i] + "。"] = idx
    return hits

if __name__ == '__main__':
    app.debug = True
    app.run()
