from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Ensure the 'data' directory exists
if not os.path.exists('data'):
    os.makedirs('data')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    db_details = {
        'DB': request.form['DB'],
        'IP': request.form['IP'],
        'Host': request.form['Host'],
        'PORT': request.form['PORT'],
        'USERNAME': request.form['USERNAME'],
        'PASSWORD': request.form['PASSWORD'],
        'SERVICE_NAME': request.form['SERVICE_NAME']
    }

    # Write the details to a text file
    with open('data/db_details.txt', 'a') as file:
        file.write(','.join(db_details.values()) + '\n')

    return jsonify(success=True)

@app.route('/edit', methods=['POST'])
def edit():
    original_data = request.form['originalData']
    updated_data = ','.join(request.form[key] for key in db_details.keys())

    # Read existing data from the text file
    with open('data/db_details.txt', 'r') as file:
        lines = file.readlines()

    # Find the line to be edited and remove it
    for i, line in enumerate(lines):
        if line.strip() == original_data:
            del lines[i]
            break

    # Write the updated data back to the text file
    with open('data/db_details.txt', 'w') as file:
        file.write(updated_data + '\n')
        file.writelines(lines)

    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)
