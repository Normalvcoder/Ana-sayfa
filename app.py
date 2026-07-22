from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
import db

app = Flask(__name__)
app.secret_key = 'oyadsavtek_local_secret_session_key_12345'

# Initialize the SQLite database on startup
db.init_db()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Bu sayfaya erişmek için önce giriş yapmalısınız.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or session['user']['role'] != 'admin':
            flash('Bu işlem için yönetici yetkisi gereklidir.', 'error')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def intro():
    return render_template('intro.html')

@app.route('/anasayfa')
@login_required
def home():
    return render_template('anasayfa.html')

@app.route('/fiziklab')
@login_required
def fizik_lab():
    return render_template('vrfiziklab.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = db.authenticate_user(username, password)
        if user:
            session['user'] = user
            flash(f'Hoş geldiniz, {username}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Hatalı kullanıcı adı veya şifre.', 'error')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Başarıyla çıkış yapıldı.', 'success')
    return redirect(url_for('intro'))

@app.route('/account')
@login_required
def account():
    users_list = []
    if session['user']['role'] == 'admin':
        users_list = db.get_all_users()
    return render_template('account.html', users=users_list)

@app.route('/admin/add-user', methods=['POST'])
@login_required
@admin_required
def add_user_route():
    new_username = request.form.get('new_username')
    new_password = request.form.get('new_password')
    new_role = request.form.get('new_role', 'user')
    
    if not new_username or not new_password:
        flash('Lütfen kullanıcı adı ve şifre giriniz.', 'error')
    else:
        success = db.add_user(new_username, new_password, new_role)
        if success:
            flash(f'"{new_username}" kullanıcısı başarıyla eklendi.', 'success')
        else:
            flash(f'"{new_username}" kullanıcı adı zaten mevcut.', 'error')
            
    return redirect(url_for('account'))

if __name__ == '__main__':
    app.run(debug=True)