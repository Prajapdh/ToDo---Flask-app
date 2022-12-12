# Flask Book: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)\


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    desc = db.Column(db.String(500),nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)

    #to define behaviour of printing
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# Creation of the database tables within the application context.
# with app.app_context():
#     db.create_all()

@app.route('/', methods = ['GET', 'POST'])
def hello_user():
    # return 'Hello, Daksh!'
    #to add item everytime user refreshes the page
    # todo = Todo(title="First to do", desc = "Start investing in stock market")
    # db.session.add(todo)
    # db.session.commit()
    if request.method=='POST':
        # print(request.form['title'])
        todo = Todo(title=request.form['title'], desc = request.form['desc'])
        db.session.add(todo)
        db.session.commit()
    data = Todo.query.all()
    return render_template("index.html", allTodo = data)

@app.route('/delete/<int:sno>')
def delete_task(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>', methods = ['GET','POST'])
def update_task(sno):
    if request.method =='POST':
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html", todo = todo)

if __name__ == "__main__":
    app.run(debug=True)