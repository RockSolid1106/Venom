#Copyright © 2021  RockSolid1106
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

from flask import Flask, render_template, make_response, request
from threading import Thread


app = Flask('')

@app.route('/', methods=['GET', 'POST'])
def main():
		resp = "Hey"
		user_agent = request.headers.get('User-Agent')
		user_agent = user_agent.lower()
		print(user_agent)
		if "iphone" in user_agent or "android" in user_agent:
			return render_template('mobile.html')
		else:
			return render_template('dashboard.html')
		return resp 



def run():
    app.run(host="0.0.0.0", port=8080)

@app.route('/get-cookie')
def get_cookie():
	username = request.cookies.get('somecookiename')
	return username
	if username=="mQGNBGECT/oBDADPao":
		return render_template('dashboard.html')
		


def keep_alive():
    server = Thread(target=run)
    server.start()