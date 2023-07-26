from flask import Flask, render_template, request
import requests
import smtplib
import os
import math
app = Flask(__name__)

api_endpoint = os.environ["api_endpoint"]

response = requests.get(api_endpoint)
data = response.json()


def send_mail(name, email, phone, message):
    e_mail = "fatihharsx4@gmail.com"
    password = os.environ["password"]
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=e_mail, password=password)
        connection.sendmail(from_addr=e_mail,
                            to_addrs=e_mail,
                            msg=f"Subject:Blog New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}".encode('utf-8'))


@app.route("/name-card.html")
def my_site():
    return render_template("name-card.html")

@app.route('/')
@app.route('/index.html')
def home():
    return render_template("index.html", data=data)

@app.route('/about.html')
def about():
    return render_template("about.html")

@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]
        send_mail(name, email, phone, message)
        return render_template("contact.html", method=request.method)
    else:
        return render_template("contact.html")


@app.route('/post/<int:index>')
def post(index):
    global new_data
    for i in data:
        if i["id"] == index:
            new_data = i
    return render_template("post.html", index_num=index, data=new_data)



if __name__ == "__main__":
    app.run(debug=True)