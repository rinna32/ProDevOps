
from flask import Flask, render_template, jsonify, request
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUESTS = Counter('app_requests_total', 'Total number of requests') #создаём метрику-счётчик для prom: общее число запросов к главной странице
LIKES = Counter('app_likes_total', 'Total number of likes') #создаём метрику-счётчик для prom: общее число лайков

total_views = 0
total_likes = 0

@app.route('/') #маршрут для главной страницы ("/")
def hello():
    global total_views
    total_views += 1
    REQUESTS.inc()  # Увеличиваем метрику prom для запросов (чтобы prom видел рост)
    return render_template('index.html', likes=total_likes, views=total_views)

@app.route('/like', methods=['POST'])
def like():
    global total_likes
    total_likes += 1
    LIKES.inc()     #увеличиваем метрику prom для лайков
    return jsonify({'likes': total_likes})

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}
    #generate_latest() возвращает все метрики в текстовом формате, понятном prom

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)  #host="0.0.0.0" - слушаем на всех сетевых интерфейсах
