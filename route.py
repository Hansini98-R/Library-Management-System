@app.route('/admin')
def admin():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    return render_template('admin.html')

@app.route('/students', methods=['GET', 'POST'])
def students():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    form = StudentForm()
    if form.validate_on_submit():
        student = Student(name=form.name.data, email=form.email.data)
        db.session.add(student)
        db.session.commit()
        flash('Student added successfully')
        return redirect(url_for('students'))
    students = Student.query.all()
    return render_template('students.html', form=form, students=students)

@app.route('/books', methods=['GET', 'POST'])
def books():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    form = BookForm()
    if form.validate_on_submit():
        book = Book(title=form.title.data, author=form.author.data, isbn=form.isbn.data)
        db.session.add(book)
        db.session.commit()
        flash('Book added successfully')
        return redirect(url_for('books'))
    books = Book.query.all()
    return render_template('books.html', form=form, books=books)

@app.route('/issue', methods=['GET', 'POST'])
def issue():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    form = IssueForm()
    if form.validate_on_submit():
        book = Book.query.get(form.book_id.data)
        student = Student.query.get(form.student_id.data)
        if book and student and book.available:
            issue = Issue(book_id=book.id, student_id=student.id, issue_date=datetime.now())
            book.available = False
            db.session.add(issue)
            db.session.commit()
            flash('Book issued successfully')
        else:
            flash('Invalid book or student ID, or book not available')
    return render_template('issue.html', form=form)

@app.route('/return', methods=['GET', 'POST'])
def return_book():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    form = ReturnForm()
    if form.validate_on_submit():
        issue = Issue.query.filter_by(book_id=form.book_id.data, student_id=form.student_id.data, return_date=None).first()
        if issue:
            issue.return_date = datetime.now()
            book = Book.query.get(issue.book_id)
            book.available = True
            db.session.commit()
            flash('Book returned successfully')
        else:
            flash('No such issued book found')
    return render_template('return.html', form=form)
