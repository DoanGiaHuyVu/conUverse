from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required to use flash messages


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']

        # Replace this with actual authentication logic
        if '@live.concordia.ca' in email:
            # If login is successful, redirect to the home page
            return redirect(url_for('home'))
        else:
            # If login fails, flash a message and reload the login page
            flash('Invalid email or password. Please try again.')
            return redirect(url_for('login'))

    # Render the login page if it's a GET request
    return render_template('login_page.html')


@app.route('/home')
def home():
    return render_template('home_page.html')  # Replace with your home page HTML


if __name__ == '__main__':
    app.run(debug=True)
