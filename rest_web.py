from flask import Flask, redirect, url_for, request, render_template
import mysql.connector

app = Flask(__name__, static_url_path='')

# Connect to the database
conn = mysql.connector.connect(user='root', password='',
                               host='127.0.0.1',
                               database='zipcodes',
                               buffered=True)
cursor = conn.cursor()

# Search zipcodes in the database
@app.route('/search', methods=['GET'])
def searchzipcodes():
    searchzip = request.args.get('zip')
    # Execute SQL query to retrieve data from the database
    cursor.execute("SELECT * FROM `zipcodes` WHERE zip=%s", (searchzip,))
    result = cursor.fetchall()
    if not result:
        return searchzip + " was not found"
    else:
        return 'Success! Here you go: %s' % result

# Update population of a specified zip code in the database
# Update population of a specified zip code in the database
@app.route('/update', methods=['POST'])
def update():
    try:
        updatezip = request.form['zip']
        updatePOP = request.form['population']  # Changed 'pop' to 'population'

        # Execute SQL query to update the population of the zip code
        cursor.execute("UPDATE `zipcodes` SET population = %s WHERE zip = %s;", (updatePOP, updatezip))  # Changed 'Pop' to 'population'
        conn.commit()  # Commit the transaction

        # Check if the population update was successful
        cursor.execute("SELECT * FROM `zipcodes` WHERE zip = %s AND population = %s", (updatezip, updatePOP))  # Changed 'Pop' to 'population'
        result = cursor.fetchall()
        if not result:
            return 'Failed to update population for zip: %s' % updatezip
        else:
            return 'Population has been updated successfully for zip: %s' % updatezip
    except mysql.connector.Error as err:
        return 'Error occurred while updating population: %s' % err


# Root of the web server and goes to template (login.html)
@app.route('/')
def root():
    return render_template('login.html')

# Main
if __name__ == '__main__':
    app.run(debug=True)
