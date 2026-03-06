from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from analyzer import IdentityAnalyzer

app = Flask(__name__)
app.secret_key = 'supersecretkey_for_demo_purposes'
app.config['UPLOAD_FOLDER'] = 'data/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

analyzer = IdentityAnalyzer()

@app.route('/')
def dashboard():
    risks = analyzer.analyze_risks()
    chart_data = analyzer.get_dashboard_data()
    # Pass data for the table as well
    recent_entries = analyzer.df.tail(10).to_dict('records') if not analyzer.df.empty else []
    return render_template('dashboard.html', risks=risks, chart_data=chart_data, recent_entries=recent_entries)

@app.route('/add', methods=['GET', 'POST'])
def add_data():
    if request.method == 'POST':
        entry = {
            'Name': request.form['name'],
            'Email': request.form['email'],
            'Phone': request.form['phone'],
            'Username': request.form['username'],
            'Platform': request.form['platform'],
            'PasswordStrength': request.form['password_strength']
        }
        analyzer.add_entry(entry)
        flash('Identity record added successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_data.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        if file and file.filename.endswith('.csv'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            success, message = analyzer.process_csv(filepath)
            if success:
                flash(message, 'success')
                return redirect(url_for('dashboard'))
            else:
                flash(f'Error processing file: {message}', 'error')
        else:
            flash('Invalid file type. Please upload a CSV.', 'error')
    return render_template('upload.html')

@app.route('/reset')
def reset_data():
    # Clear the dataframe and save empty
    import pandas as pd
    analyzer.df = pd.DataFrame(columns=['Name', 'Email', 'Phone', 'Username', 'Platform', 'PasswordStrength'])
    analyzer.save_data()
    flash('All data has been reset.', 'info')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
