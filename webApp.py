from flask import Flask, request, redirect, url_for
import os
import openai
import sys

app = Flask(__name__)
UPLOAD_FOLDER = os.path.abspath("uploads")
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

try:
    openai.api_key = "ENTER API KEY HERE"
except KeyError:
    sys.stderr.write("""
    You haven't set up your API key yet.
    """)
    exit(1)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r') as f:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant"},
                        {"role": "user", "content": f.read()},
                        {"role": "user", "content": "Simplify this document"}
                    ]
                )
                return '<body style="background-color: #1D1E1F; color: white;">' + response.choices[0].message.content + '</body>'
    return '''
    <!doctype html>
    <html>
    <head>
    <title>LegalEase</title>
    <style>
    body {
        font-family: Arial, sans-serif;
        background-color: #1D1E1F; 
        text-align: center;
    }
    
    form {
        margin-top: 2rem;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    input[type=file] {
        margin-bottom: 1rem;
        padding: 0.5rem;
        border-radius: 0.25rem;
        border: none;
        background-color: #3e8e41;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    input[type=submit] {
        background-color: #4CAF50;
        color: black;
        font-weight: bold;
        padding: 0.5rem 1.5rem;
        border: none;
        border-radius: 0.25rem;
        cursor: pointer;
        transition: background-color 0.3s ease-in-out;
    }
    
    input[type=submit]:hover {
        background-color: #3e8e41;
        color: black;
    }

    .upload-container {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    </style>
    </head>
    <body>
    <form action="" method=post enctype=multipart/form-data>
    <div class="upload-container">
    <input type=file name=file>
    <input type=submit value=Upload>
    </div>
    </form>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
