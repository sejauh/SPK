from http import HTTPStatus
from flask import Flask, request, abort
from flask_restful import Resource, Api 
from models import coffeeshops as coffeeshopsModel
from engine import engine
from sqlalchemy import select
from sqlalchemy.orm import Session

session = Session(engine)

app = Flask(__name__)
api = Api(app)        

class BaseMethod():

    def __init__(self):
        self.raw_weight = {'kualitas_kopi': 2, 'pelayanan': 4, 'lokasi': 3, 'harga': 2, 'wifi': 4}

    @property
    def weight(self):
        total_weight = sum(self.raw_weight.values())
        return {k: round(v/total_weight, 2) for k, v in self.raw_weight.items()}

    @property
    def data(self):
        query = select(coffeeshopsModel.nama_coffeeshop, coffeeshopsModel.kualitas_kopi, coffeeshopsModel.pelayanan, coffeeshopsModel.lokasi, coffeeshopsModel.harga, coffeeshopsModel.wifi)
        result = session.execute(query).fetchall()
        print(result)
        return [{'nama_coffeeshop': coffeeshops.nama_coffeeshop, 'kualitas_kopi': coffeeshops.kualitas_kopi, 'pelayanan': coffeeshops.pelayanan, 'lokasi': coffeeshops.lokasi, 'harga': coffeeshops.harga, 'wifi': coffeeshops.wifi} for coffeeshops in result]

    @property
    def normalized_data(self):
        kualitas_kopi_values = []
        pelayanan_values = []
        lokasi_values = []
        harga_values = []
        wifi_values = []

        for data in self.data:
            kualitas_kopi_values.append(data['kualitas_kopi'])
            pelayanan_values.append(data['pelayanan'])
            lokasi_values.append(data['lokasi'])
            harga_values.append(data['harga'])
            wifi_values.append(data['wifi'])

        return [
            {'nama_coffeeshop': data['nama_coffeeshop'],
             'kualitas_kopi': min(kualitas_kopi_values) / data['kualitas_kopi'],
             'pelayanan': data['pelayanan'] / max(pelayanan_values),
             'lokasi': data['lokasi'] / max(lokasi_values),
             'harga': data['harga'] / max(harga_values),
             'wifi': data['wifi'] / max(wifi_values)
             }
            for data in self.data
        ]

    def update_weights(self, new_weights):
        self.raw_weight = new_weights

class WeightedProductCalculator(BaseMethod):
    def update_weights(self, new_weights):
        self.raw_weight = new_weights

    @property
    def calculate(self):
        normalized_data = self.normalized_data
        produk = []

        for row in normalized_data:
            product_score = (
                row['kualitas_kopi'] ** self.raw_weight['kualitas_kopi'] *
                row['pelayanan'] ** self.raw_weight['pelayanan'] *
                row['lokasi'] ** self.raw_weight['lokasi'] *
                row['harga'] ** self.raw_weight['harga'] *
                row['wifi'] ** self.raw_weight['wifi']
            )

            produk.append({
                'nama_coffeeshop': row['nama_coffeeshop'],
                'produk': product_score
            })

        sorted_produk = sorted(produk, key=lambda x: x['produk'], reverse=True)

        sorted_data = []

        for product in sorted_produk:
            sorted_data.append({
                'nama_coffeeshop': product['nama_coffeeshop'],
                'score': product['produk']
            })

        return sorted_data


class WeightedProduct(Resource):
    def get(self):
        calculator = WeightedProductCalculator()
        result = calculator.calculate
        return result, HTTPStatus.OK.value
    
    def post(self):
        new_weights = request.get_json()
        calculator = WeightedProductCalculator()
        calculator.update_weights(new_weights)
        result = calculator.calculate
        return {'data': result}, HTTPStatus.OK.value
    

class SimpleAdditiveWeightingCalculator(BaseMethod):
    @property
    def calculate(self):
        weight = self.weight
        result = {row['nama_coffeeshop']:
                  round(row['kualitas_kopi'] * weight['kualitas_kopi'] +
                        row['pelayanan'] * weight['pelayanan'] +
                        row['lokasi'] * weight['lokasi'] +
                        row['harga'] * weight['harga'] +
                        row['wifi'] * weight['wifi'], 2)
                  for row in self.normalized_data
                  }
        sorted_result = dict(
            sorted(result.items(), key=lambda x: x[1], reverse=True))
        return sorted_result

    def update_weights(self, new_weights):
        self.raw_weight = new_weights

class SimpleAdditiveWeighting(Resource):
    def get(self):
        saw = SimpleAdditiveWeightingCalculator()
        result = saw.calculate
        return result, HTTPStatus.OK.value

    def post(self):
        new_weights = request.get_json()
        saw = SimpleAdditiveWeightingCalculator()
        saw.update_weights(new_weights)
        result = saw.calculate
        return {'data': result}, HTTPStatus.OK.value


class coffeeshops(Resource):
    def get_paginated_result(self, url, list, args):
        page_size = int(args.get('page_size', 10))
        page = int(args.get('page', 1))
        page_count = int((len(list) + page_size - 1) / page_size)
        start = (page - 1) * page_size
        end = min(start + page_size, len(list))

        if page < page_count:
            next_page = f'{url}?page={page+1}&page_size={page_size}'
        else:
            next_page = None
        if page > 1:
            prev_page = f'{url}?page={page-1}&page_size={page_size}'
        else:
            prev_page = None
        
        if page > page_count or page < 1:
            abort(404, description=f'Halaman {page} tidak ditemukan.') 
        return {
            'page': page, 
            'page_size': page_size,
            'next': next_page, 
            'prev': prev_page,
            'Results': list[start:end]
        }

    def get(self):
        query = select(coffeeshopsModel)
        data = [{'nama_coffeeshop': coffeeshops.nama_coffeeshop, 'kualitas_kopi': coffeeshops.kualitas_kopi, 'pelayanan': coffeeshops.pelayanan, 'lokasi': coffeeshops.lokasi, 'harga': coffeeshops.harga, 'wifi': coffeeshops.wifi} for coffeeshops in session.scalars(query)]
        return self.get_paginated_result('coffeeshops/', data, request.args), HTTPStatus.OK.value


api.add_resource(coffeeshops, '/coffeeshops')
api.add_resource(WeightedProduct, '/wp')
api.add_resource(SimpleAdditiveWeighting, '/saw')

if __name__ == '__main__':
    app.run(port='5005', debug=True)