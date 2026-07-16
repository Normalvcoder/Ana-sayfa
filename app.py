from flask import Flask, render_template

app = Flask(__name__)

# This is your main homepage route
@app.route('/')
def home():
    return render_template('anasayfa.html')

# This is the route for your second page
@app.route('/fiziklab')
def fizik_lab():
    return render_template('vrfiziklab.html')

if __name__ == '__main__':
    app.run(debug=True)