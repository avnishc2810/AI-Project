from flask import Flask, request, redirect, url_for, render_template
import os

app = Flask(__name__)

# Directory to save uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the file is part of the request
        if 'hello' not in request.files:
            return "No file part", 400
        file = request.files['hello']
        if file.filename == '':
            return "No selected file", 400
        if file:
            # Save the file to the upload folder
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            # Redirect to the new page after uploading
            return redirect(url_for('uploaded_file', filename=file.filename))
    return render_template('index.html')  # Render the upload page

@app.route('/uploaded')
def uploaded_file():
    filename = request.args.get('filename')  # Get the filename from the URL
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    

    # Read the content of the uploaded file as a string
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
    except Exception as e:
        return f"An error occurred: {e}", 500
    print(file_content)

    

    return render_template('uploaded.html', content=file_content)

if __name__ == '__main__':
    app.run(debug=True)
