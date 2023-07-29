#this will be pur code of flask for currency converter chatbot

from flask import Flask, request,jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']
    
    
    #print(source_currency)
    #print(amount)
    #print(target_currency)
    
    cf = fetch_conversion_factor(source_currency, target_currency)
    final_amount = amount * cf
    final_amount = round(final_amount,2)
    #the result after conversion should be send to chatbot to do it we will following this procedure
    response = {
        'fulfillmentText':"{} {} is {} {}".format(amount,source_currency,final_amount,target_currency)
    }
    #print(final_amount)
    #for returning response to chatbot using jsonify you can test your chatbot
    #after doing this coding part we will deploy our chatbot to telegram
    return jsonify(response)

def fetch_conversion_factor(source, target):
    #paste url form free currency site from documentation part and change currency parts to this "{}_{}"
    #after ending url in double inverted comma add this part .format(source, target)
    url = "https://free.currconv.com/api/v7/convert?q={}_{}&compact=ultra&apiKey=41b20c735c6addc4dba3".format(source,target)
    response = requests.get(url)
    response = response.json()
    
    return response['{}_{}'.format(source, target)]

if __name__ == '__main__':
    app.run(debug=True)