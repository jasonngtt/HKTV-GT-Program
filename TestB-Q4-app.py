from flask import Flask, request, jsonify

app = Flask(__name__)

def calculate_shipping_fee(parcel):
    # Implement your shipping fee calculation logic here
    # This is a basic example, adjust as needed
    ambient_rate = 10 if parcel['weight'] <= 5 else 15
    chill_rate = 20 if parcel['weight'] <= 5 else 30
    shipping_fee = ambient_rate * parcel['weight'] if parcel['temperature_condition'] == 'Ambient' else chill_rate * parcel['weight']

    return shipping_fee

@app.route('/calculate-shipping-fee', methods=['POST'])
def calculate_shipping_fee_endpoint():
    data = request.json

    parcels = data.get('parcels', [])

    total_shipping_fee = 0
    breakdown = []

    for index, parcel in enumerate(parcels):
        shipping_fee = calculate_shipping_fee(parcel)
        total_shipping_fee += shipping_fee

        breakdown.append({
            'parcel_index': index,
            'item_count': parcel['quantity'],
            'volumetric_weight': (parcel['dimension']['length'] * parcel['dimension']['width'] * parcel['dimension']['height']) / 5000,
            'actual_weight': parcel['weight'],
            'temperature_condition': parcel['temperature_condition'],
            'shipping_fee': shipping_fee
        })

    response_data = {
        'total_shipping_fee': total_shipping_fee,
        'breakdown': breakdown
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)


