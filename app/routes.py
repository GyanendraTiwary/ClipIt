# app/routes.py

import os
import random
import string
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from app import mongo

main = Blueprint('main', __name__)

def generate_pin():
    pin = ''.join(random.choices(string.digits, k=6))
    if mongo.db.clipboard.find_one({'pin': pin}):
        return generate_pin()
    return pin

@main.route('/', methods=['GET', 'POST'])
def index():
    pin = None  # Define pin with a default value

    if request.method == 'POST':
        content = request.form['content']
        file = request.files.get('file')
        protect = request.form.get('protect')  # Check if protect checkbox is selected
        password = request.form.get('password') if protect else None  # Retrieve the password input if protect is selected
        pin = generate_pin()

        if file:
            filename = secure_filename(file.filename)
            print(filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            entry = {'pin': pin, 'content': content, 'file_path': file_path, 'password': password, 'password_protected': protect}  # Store the password in the database
        else:
            entry = {'pin': pin, 'content': content, 'password': password, 'password_protected': protect}  # Store the password in the database
        
        mongo.db.clipboard.insert_one(entry)
        flash(f'Your unique pin is {pin}', 'success')

    return render_template('index.html', pin=pin)

@main.route('/retrieve', methods=['GET', 'POST'])
def retrieve():
    if request.method == 'POST':
        pin = request.form['pin']
        entry = mongo.db.clipboard.find_one({'pin': pin})

        if not entry:
            flash('Invalid PIN, please try again.', 'danger')
            return redirect(url_for('main.retrieve'))

        return render_template('retrieve.html', entry=entry)

    return render_template('retrieve_pin.html')

# Update the verify_password route to handle the password verification
@main.route('/verify_password/<pin>', methods=['POST'])
def verify_password(pin):
    password = request.form.get('password')
    entry = mongo.db.clipboard.find_one({'pin': pin})

    if not entry:
        flash('Invalid PIN, please try again.', 'danger')
        return redirect(url_for('main.retrieve'))

    if entry['password'] == password:
        # Password is correct, render the retrieve.html template with the entry
        return render_template('retrieve.html', entry=entry, password_verified=True, password_correct=True)
    else:
        flash('Incorrect password, please try again.', 'danger')
        return render_template('retrieve.html', entry=entry, password_verified=True, password_correct=False)




@main.route('/delete/<pin>', methods=['POST'])
def delete(pin):
    mongo.db.clipboard.delete_one({'pin': pin})
    flash('Entry deleted successfully.', 'success')
    return redirect(url_for('main.index'))