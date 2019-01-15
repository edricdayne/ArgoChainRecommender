from app import app

from flask import url_for, render_template, request

@app.route('/')
@app.route('/index')
def index():

    return render_template('index.html')


@app.route('/recommendations', methods=['POST'])
def recommendations():

    location = request.form['location']
    crop = request.form['crop']
    price_top = request.form['price-top']
    price_low = request.form['price-low']
    quantity = request.form['quantity']

    if price_low == '': price_low = 0
    if price_top == '': price_top = 0
    if quantity == '': quantity = 0

    average_price = (int(price_top) + int(price_low)) //2

    f = open('app/static/farmers.txt', 'r')
    farmers = f.readlines()

    results = []

    for farmer in farmers:
        farmer = farmer.strip().split(',')
        if farmer[1] == location and farmer[3] == crop and int(farmer[4]) >= int(quantity):

            rating_score = float(farmer[2]) * 2
            price_score = int(((1000 - min((int(farmer[5]) - average_price), 1000))/1000)*10)

            total_score = (rating_score + price_score)//2

            results.append([farmer[0], farmer[2], farmer[5], total_score])

    resultsflag = True if len(results) > 0 else False

    results.sort(key=lambda x:x[3], reverse=True)

    return render_template('recommendations.html', farmers=results, results=resultsflag)
