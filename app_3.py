# working with POST requests and form
from fileinput import filename

import pandas as pd, os , uuid
from flask import Flask, render_template,request, Response, send_from_directory

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        # if 'some key' in request.form.keys():
        # username = request.form['username']
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'heritage' and password == 'password':
            return 'Success'
        else:
            return 'Failure'

# file upload
@app.route('/file_upload', methods = ['POST'])
def file_upload():
    file = request.files['file']
    if file.content_type == 'text/plain':
        return file.read().decode()
    elif file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' or file.content_type == 'application/vnd.ms-excel':
        df = pd.read_excel(file)
        return df.to_html()


#convert excel file to csv so user can download

@app.route('/convert_csv', methods =['POST'] )
def convert_csv():
    file = request.files['file']
    df = pd.read_excel(file)
    # so when you upload file you want a response that will convert excel to csv
    response = Response(
        df.to_csv(),
        mimetype= 'text/csv',
        headers={
            'Content-Disposition':'attachment; filename=result.csv'
        }

    )

    return response

# method 2 user downloads converted csv file from a download page instead of an attachment like first method

@app.route('/convert_csv_two', methods = ['POST'])
def convert_csv_two():
    file = request.files['file']
    df = pd.read_excel(file)
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    #     uuid generates random id that is unique, does not repeat

    filename = f'{uuid.uuid4()}.csv'
    df.to_csv(os.path.join('downloads', filename))
    return render_template('download.html', filename=filename)

# endpoint needs to be called to make the endpoint

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory('downloads', filename , download_name= 'result.csv')
    # return send_from_directory(directory: 'downloads',filename,  download_name= 'result.csv')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)