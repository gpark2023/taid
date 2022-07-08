from flask import Flask, url_for, request, redirect, session, render_template
from flask_cors import CORS, cross_origin
import json
from uuid import uuid4
import requests
import json

masternode_url = "http://0.0.0.0:1000"

DONOR = 1
RECIPIENT = 2
SHOP = 3

class User:
	def __init__(self):
		self.admin = []
		self.donors = [{'name': 'gooha', 'id': 'gooha', 'pw': 'gooha', 'wallet': '5c354ad8f4484fb3a39273b1587b1080', 'anonymity': '0'},{'name': 'sam', 'id': 'sam', 'pw': 'sam', 'wallet': '5d354ad8f4484fb3a39273b1587b1080', 'anonymity': '0'},{'name': 'john', 'id': 'john', 'pw': 'john', 'wallet': '5v354ad8f4484fb3a39273b1587b1080', 'anonymity': '0'},{'name': 'Tim', 'id': 'Tim', 'pw': 'Tim', 'wallet': '5p354ad8f4484fb3a39273b1587b1080', 'anonymity': '0'},{'name': 'George', 'id': 'George', 'pw': 'George', 'wallet': '5x354ad8f4484fb3a39273b1587b1080', 'anonymity': '0'}]
		self.recis = [{'name': "Saint Paul's Anna's House", 'id': 'Anna', 'pw': 'Anna', 'wallet': '5f979dfb57624830a91dd6dda787d12f', 'residence': 'Korea, Gyeongsangbuk-do', 'age': 'Retired Nuns', 'story': "This is a community consisted of around 50 retired nuns. We are entriely operated by donations, and we do not receive any government support. Please help us purchase basic neccessities such as toilet paper. If this donation is fully met, this will provide a full 1 month ration for the nuns.       http://www.anna.or.kr/"},{'name': 'Mother Gemma', 'id': 'Gemma', 'pw': 'Gemma', 'wallet': 'c274f599a24f41d797a60d63f356e26b', 'residence': 'Korea, Gyeongsangbuk-do', 'age': '70', 'story': "This is a community consisted of around 50 retired nuns. We are entriely operated by donations, and we do not receive any government support. Please help us purchase basic neccessities such as rice. If this donation is fully met, this will provide a full 1 month ration for the nuns.       http://www.anna.or.kr/\n"},{'name': 'Sister Helena', 'id': 'Helena', 'pw': 'Helena', 'wallet': 'p532q125y71b38p821b26y28b724l52c', 'residence': 'Korea, Gyeongsangbuk-do', 'age': '65', 'story': "This printer will be placed in our office to print paperwork and important documents.   http://www.anna.or.kr/\n"}] # recis 37, won,add website, 8, man wan
		self.shops = [{'name': 'Amazon', 'id': 'amazon', 'pw': 'amazon', 'wallet': 'e4408ab6fdd1443ca5b099afd32588d1', 'region': 'use', 'goods': {'Rice': '370000', 'Toilet Paper': '80000' , 'Printer' : '150000'}}]
		self.userlist = [self.admin, self.donors, self.recis, self.shops]
		#self.new_donor('qq','qq','qq','1','qq')

	def new_donor(self, user_name, user_id, user_pw, wallet, anonymity):
		newbie = {
			'name' : user_name,
			'id' : user_id,
			'pw' : user_pw,
			'wallet' : wallet,
			'anonymity' : anonymity
		}

		self.donors.append(newbie)
		print(newbie)
		#print(self.donors)

	def new_reci(self, user_name, user_id, user_pw, wallet, residence,age, story):
		newbie = {
			'name' : user_name,
			'id' : user_id,
			'pw' : user_pw,
			'wallet' : wallet,
			'residence' : residence,
			'age' : age,
			'story' : story
		}

		self.recis.append(newbie)
		print(newbie)
		#print(self.recis)

	def new_shop(self, user_name, user_id, user_pw, wallet, region, goods):
		newbie = {
			'name' : user_name,
			'id' : user_id,
			'pw' : user_pw,
			'wallet' : wallet,
			'region' : region,
			'goods' : goods
		}

		self.shops.append(newbie)
		print(newbie)
		#print(self.shops)




app = Flask(__name__, static_url_path='', static_folder='static')
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
# app.config['SERVER_NAME'] = "localhost:1234"
app.secret_key = "11112222"

user_db = User()


@app.route('/view/all_chain')
@cross_origin()
def view_chain_all():
	res = requests.get(masternode_url + "/chain")
	data = json.loads(res.text)
	return json.dumps(data)

@app.route('/view/chain/<string:wallet>')
@cross_origin()
def view_chain(wallet):
	res = requests.get(masternode_url + "/chain")
	data = json.loads(res.text)
	data = data['chain']

	ret = []
	for block in data:
		if block['transactions'] == []:
			continue
		for transaction in block['transactions']:
			if transaction['sender'] == wallet or transaction['recipient'] == wallet:
				ret.append({"block_index" : block['index'],"transaction" : transaction})
	return json.dumps(ret)



@app.route('/view/shop/<string:shop_name>',methods = ['GET'])
@cross_origin()
def view_shop(shop_name):
	info = {}
	for shop in user_db.shops:
		if shop['name'] == shop_name:
			info['name'] = shop_name
			info['goods'] = shop['goods']
			info['wallet'] = shop['wallet']
	return json.dumps(info)


@app.route('/view/all_shops',methods = ['GET'])
@cross_origin()
def view_shop_all():
	ret = []
	for shop in user_db.shops:
		info = {}
		info['name'] = shop['name']
		info['goods'] = shop['goods']
		info['wallet'] = shop['wallet']
		ret.append(info)

	return json.dumps(ret)


@app.route('/view/recipient/<string:wallet>',methods = ['GET'])
@cross_origin()
def view_recipient(wallet):
	res = requests.get(masternode_url + "/chain")
	data = json.loads(res.text)
	data = data['chain']
	print(wallet)
	ret = []
	for tmp in data:
		if tmp['transactions'] == []:
			continue
		# find donation request tranaction
		for transaction in tmp['transactions']:
			if transaction['purpose'] == "Donation Request" and transaction['sender'] == wallet:
				#print(transaction)
				info = dict()
				# find reci who has this wallet
				for reci in user_db.recis:
					if reci['wallet'] == transaction['sender']:
						info['name'] = reci['name']
						info['wallet'] = reci['wallet']
						info['residence'] = reci['residence']
						info['age'] = reci['age']
						info['message'] = transaction['message']
						info['story'] = reci['story']
						info['required'] = transaction['amount']
						info['current'] = 0
						info['trail'] = []

				ret.append(info)
			elif transaction['purpose'] == "Donation Response" and transaction['recipient'] == wallet:
				for info in ret:
					if info['wallet'] == transaction['recipient']:
						info['current'] += transaction['amount']
						trail = {}
						for donor in user_db.donors:
							if donor['wallet'] == transaction['sender']:
								if donor['anonymity'] == 1:
									transaction['name'] = "Anonymous"
									trail = {"type" : "Donation", "info" : transaction}
								else:
									transaction['name'] = donor['name']
									trail = {"type" : "Donation" , "info" : transaction}
						if len(trail) > 0:
							info['trail'].append(trail)
			elif transaction['purpose'] == "Buy" and transaction['sender'] == wallet:
				for info in ret:
					if info['wallet'] == transaction['sender']:
						shop_name = ""
						for shop in user_db.shops:
							if shop['wallet'] == transaction['recipient']:
								shop_name = shop['name']
						transaction['name'] = shop_name
						trail = {"type" : "Using Donations", "info" : transaction}
						info['trail'].append(trail)
	print(ret)
	return json.dumps(ret)



@app.route('/')
def maint():
	return render_template('index.html')


@app.route('/view/all_recipient',methods=['GET'])
@cross_origin()
def view_recipient_all():
	res = requests.get(masternode_url + "/chain")
	data = json.loads(res.text)
	data = data['chain']

	ret = []
	for tmp in data:
		if tmp['transactions'] == []:
			continue
		# find donation request tranaction
		for transaction in tmp['transactions']:
			if transaction['purpose'] == "Donation Request":
				#print(transaction)
				info = dict()
				# find reci who has this wallet
				for reci in user_db.recis:
					#print(reci)
					if reci['wallet'] == transaction['sender']:
						info['name'] = reci['name']
						info['wallet'] = reci['wallet']
						info['residence'] = reci['residence']
						info['message'] = transaction['message']
						info['required'] = transaction['amount']
						info['current'] = 0
						info['trail'] = []

				ret.append(info)
			elif transaction['purpose'] == "Donation Response":
				for info in ret:
					if info['wallet'] == transaction['recipient']:
						info['current'] += transaction['amount']
						trail = {}
						for donor in user_db.donors:
							if donor['wallet'] == transaction['sender']:
								if donor['anonymity'] == 1:
									transaction['name'] = "Anonymous"
									trail = {"type" : "Donation", "info" : transaction}
								else:
									transaction['name'] = donor['name']
									trail = {"type" : "Donation" , "info" : transaction}
						info['trail'].append(trail)

			elif transaction['purpose'] == "Buy":
				for info in ret:
					if info['wallet'] == transaction['sender']:
						shop_name = ""
						for shop in user_db.shops:
							if shop['wallet'] == transaction['recipient']:
								shop_name = shop['name']
						transaction['name'] = shop_name
						trail = {"type" : "Using Donations", "info" : transaction}
						info['trail'].append(trail)
	print(json.dumps(ret))
	return json.dumps(ret)


@app.route('/register', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def register():
	values = request.get_json()
	print(values)
	#POST
	if request.method == 'POST':
		wallet = str(uuid4()).replace('-', '')
		if values['type'] == DONOR:
			user_db.new_donor(values['name'],values['id'],values['pw'],wallet, values['anonymity'])
		elif values['type'] == RECIPIENT:
			print(values['story'])
			user_db.new_reci(values['name'],values['id'],values['pw'],wallet, values['residence'], values['age'], values['story'])
		elif values['type'] == SHOP:
			user_db.new_shop(values['name'],values['id'],values['pw'],wallet, values['region'], values['goods'])
		else:
			return "Error", 404
		return wallet


	#GET
	if values['type'] == DONOR:
		return "Donor register page", 200
	elif values['type'] == RECIPIENT:
		return "Recipient register page", 200
	elif values['type'] == SHOP:
		return "Shop register page", 200
	else:
		return "Error", 404

@app.route('/login', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def login():
	values = request.get_json()
	#GET
	if request.method == 'GET':
		return render_template('login.html'), 200

	#POST
	user_id = values['id']
	user_pw = values['pw']
	user_type = values['type']
	for tmp in user_db.userlist[user_type]:
		if tmp['id'] == user_id and tmp['pw'] == user_pw:
			session['id'] = user_id
			print(session)
			return "login success page", 200
	return "login fail page", 201

@app.route('/logout')
def logout():
	session.clear()
	return "logged out"

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=80, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
