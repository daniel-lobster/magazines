from flask_app import app, render_template, redirect, request, session, flash
from flask_app.models.user_model import User
from flask_app.models.magazine_model import Magazine
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


# redirect the user to the form
@app.get('/')
def redirect_to_form():
    return render_template('login_reg.html')

# display form to create an album
@app.post('/register')
def new_user():
    if not User.validate_registration(request.form):
        # we redirect to the template with the form.
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    found_user = User.get_by_email(data)
    if not found_user:
        user_id = User.save(data)
        # store user id into session
        session['user_id'] = found_user.id
        session['first_name'] = found_user.first_name
        session['last_name'] = found_user.last_name
        print(session)
        return redirect('/magazines')
    else:
        flash('Email already registered','email')
        return redirect('/')



@app.get('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.post('/login')
def login_user():
    #check to see if they are registered
    data = { "email" : request.form["email"] }
    found_user = User.get_by_email(data)
    if not found_user:
        flash('Invalid Credentials','login')
        return redirect('/')
    
    #if user is in database compare the passwords
    if not bcrypt.check_password_hash(found_user.password,request.form['password']):
        flash('Invalid Credentials','login')
        return redirect('/')

    # store user id into session
    session['user_id'] = found_user.id
    session['first_name'] = found_user.first_name
    session['last_name'] = found_user.last_name
    print(session)
    return redirect('/magazines')

@app.get('/users/<int:user_id>/account')
def user_account(user_id):
    data={
        'id':user_id
    }
    user = User.get_by_id_with_created_magazines(data)
    print(user)
    magazine_subscribers = {}
    for magazine in user.created_magazines:
        data = {
            'id':magazine.id
        }
        magazine_subscribers[magazine.id]=Magazine.get_magazine_by_id_with_num_subscribers(data)
    return render_template('one_user.html', user=user,magazine_subscribers=magazine_subscribers)

@app.post('/users/<int:user_id>/update')
def user_update(user_id):
    data={
        'id':user_id,
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email']
    }
    User.find_by_id_and_update(data)
    return redirect(f'/users/{user_id}/account')
