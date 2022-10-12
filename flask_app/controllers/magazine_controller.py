from flask_app import app, render_template, redirect, request,session,flash
from flask_app.models.magazine_model import Magazine

@app.get('/magazines')
def redirect_to_all_magazines():
    if 'user_id' not in session:
        return redirect("/")
    magazines = Magazine.find_all()
    #print(magazines)
    return render_template('all_magazines.html', magazines=magazines)

# display one magazine by id
@app.get('/magazines/<int:magazine_id>')
def one_magazine(magazine_id):
    data = {
        'id': magazine_id
    }
    magazine = Magazine.find_by_id_with_subscribers(data)
    print(f'**** FOUND - MAGAZINE ID: {magazine.id} ****')
    return render_template('one_magazine.html', magazine = magazine)

# process form and create a magazine
@app.post('/magazines/new')
def create_magazine():
    print(f'**** CREATED - MAGAZINE ID: {request.form} ****')
    print(f'**** CREATED - MAGAZINE ID: {session} ****')
    magazine_id = Magazine.save(request.form)
    print(f'**** CREATED - MAGAZINE ID: {magazine_id} ****')
    return redirect('/magazines')

@app.get('/magazines/new')
def new_magazine():
    return render_template('new_magazine.html')

# display form to edit a magazine by id
@app.get('/magazines/<int:magazine_id>/edit')
def edit_magazine(magazine_id):
    data = {
        'id': magazine_id
    }
    magazine = Magazine.find_by_id(data)
    print(f'**** FOUND - MAGAZINE ID: {magazine.id} ****')
    return render_template('edit_magazine.html', magazine = magazine)

# process form and update a magazine by id
@app.post('/magazines/<int:magazine_id>/update')
def update_magazine(magazine_id):
    data = {
        'id': magazine_id,
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date': request.form['date'],
        'under_30': request.form['under_30']
    }
    Magazine.find_by_id_and_update(data)
    print(f'**** UPDATED - MAGAZINE ID: {magazine_id} ****')
    return redirect(f'/magazines/{magazine_id}')

# delete one magazine by id
@app.get('/magazines/<int:magazine_id>/delete')
def delete_magazine(magazine_id):
    data = {
        'id': magazine_id
    }
    print(data)
    Magazine.find_by_id_and_delete(data)
    print(f'**** DELETED - MAGAZINE ID: {magazine_id} ****')
    return redirect('/magazines')

@app.get('/magazines/<int:magazine_id>/subscribe')
def subscribe_to_magazine(magazine_id):
    unique_subscription = Magazine.subscribe_to_magazine(magazine_id)
    print(unique_subscription)
    return redirect('/magazines')

