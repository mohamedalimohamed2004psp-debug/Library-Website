from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_super_secret_key_12345'

# إعدادات الاتصال بقاعدة بيانات المكتبة (library_db)
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'sql2304105',
    'database': 'library_db'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# صفحة تسجيل الدخول
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user.get('id', user.get('user_id'))
            session['user_name'] = user['name']
            return redirect(url_for('dashboard'))
        else:
            error = 'البريد الإلكتروني أو كلمة المرور غير صحيحة.'
            
    return render_template('login.html', error=error)

# صفحة إنشاء حساب جديد
@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            error = 'كلمات المرور غير متطابقة.'
        else:
            hashed_password = generate_password_hash(password)
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
                conn.commit()
                cursor.close()
                conn.close()
                return redirect(url_for('login'))
            except Exception as e:
                error = 'البريد الإلكتروني مستخدم من قبل أو حدث خطأ.'
                
    return render_template('register.html', error=error)

# لوحة التحكم الرئيسية (عرض كتب ومؤلفي المستخدم الحالي فقط)
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # جلب مؤلفي هذا المستخدم فقط
    cursor.execute("SELECT * FROM AUTHOR WHERE user_id = %s", (user_id,))
    authors = cursor.fetchall()
    
    # جلب كتب هذا المستخدم فقط
    cursor.execute("SELECT * FROM BOOK WHERE user_id = %s", (user_id,))
    books = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('dashboard.html', user_name=session['user_name'], authors=authors, books=books)

# إضافة مؤلف جديد (مربوط بالمستخدم الحالي)
@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        name = request.form['name']
        country = request.form['country']
        user_id = session['user_id']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO AUTHOR (name, country, user_id) VALUES (%s, %s, %s)", (name, country, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('dashboard'))
        
    return render_template('add_author.html')

# إضافة كتاب جديد (مربوط بالمستخدم الحالي)
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        author_id = request.form['author_id']
        
        # التأكد أن المؤلف يتبع لهذا المستخدم قبل ربط الكتاب به
        cursor.execute("SELECT * FROM AUTHOR WHERE author_id = %s AND user_id = %s", (author_id, user_id))
        if cursor.fetchone():
            cursor.execute("INSERT INTO BOOK (title, price, author_id, user_id) VALUES (%s, %s, %s, %s)", (title, price, author_id, user_id))
            conn.commit()
            
        cursor.close()
        conn.close()
        return redirect(url_for('dashboard'))
        
    # جلب مؤلفي المستخدم الحالي فقط لاختيارهم في القائمة
    cursor.execute("SELECT * FROM AUTHOR WHERE user_id = %s", (user_id,))
    authors = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('add_book.html', authors=authors)

# تعديل بيانات مؤلف (بشرط أن يملكه المستخدم الحالي)
@app.route('/edit_author/<int:author_id>', methods=['GET', 'POST'])
def edit_author(author_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        name = request.form['name']
        country = request.form['country']
        cursor.execute("UPDATE AUTHOR SET name = %s, country = %s WHERE author_id = %s AND user_id = %s", (name, country, author_id, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('dashboard'))
        
    cursor.execute("SELECT * FROM AUTHOR WHERE author_id = %s AND user_id = %s", (author_id, user_id))
    author = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not author:
        return redirect(url_for('dashboard'))
        
    return render_template('edit_author.html', author=author)

# تعديل بيانات كتاب (بشرط أن يملكه المستخدم الحالي)
@app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        author_id = request.form['author_id']
        cursor.execute("UPDATE BOOK SET title = %s, price = %s, author_id = %s WHERE book_id = %s AND user_id = %s", (title, price, author_id, book_id, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('dashboard'))
        
    cursor.execute("SELECT * FROM BOOK WHERE book_id = %s AND user_id = %s", (book_id, user_id))
    book = cursor.fetchone()
    
    if not book:
        cursor.close()
        conn.close()
        return redirect(url_for('dashboard'))
        
    cursor.execute("SELECT * FROM AUTHOR WHERE user_id = %s", (user_id,))
    authors = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('edit_book.html', book=book, authors=authors)

# حذف مؤلف (للمستخدم الحالي فقط)
@app.route('/delete_author/<int:author_id>', methods=['POST'])
def delete_author(author_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM AUTHOR WHERE author_id = %s AND user_id = %s", (author_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('dashboard'))

# حذف كتاب (للمستخدم الحالي فقط)
@app.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM BOOK WHERE book_id = %s AND user_id = %s", (book_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('dashboard'))

# تسجيل الخروج
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)