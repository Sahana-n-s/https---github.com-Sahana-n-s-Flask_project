from flask import Flask,render_template,jsonify,request,redirect,send_from_directory,url_for
import os
from flask_uploads import UploadSet,IMAGES,configure_uploads
from flask_wtf import FlaskForm
from wtforms import SubmitField,FileField,widgets
from flask_wtf.file import FileField, FileRequired,FileAllowed
from flask_mysqldb import MySQL,MySQLdb
# app = Flask(__name__)

# app.config['UPLOADED_PHOTOS_DEST']='uploads'

# photos= UploadSet()
# Route to upload image
app=Flask(__name__)

# mysql config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1224'
app.config['MYSQL_DB'] = 'flask'
app.config['MYSQL_CURSORCLASS']='DictCursor'
mysql=MySQL(app)
 

app.config['SECRET_KEY']='sahana'
app.config['UPLOADED_PHOTOS_DEST']='uploads'

photos=UploadSet('photos',IMAGES)

configure_uploads(app,photos)

class UploadForm(FlaskForm):
    photo =FileField( 
        validators=[
        FileRequired('file field should not be empty'), 
        FileAllowed(photos, 'Images only!')
            ]
        
        )
    submit=SubmitField('Upload')

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'],filename)

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    cursor = mysql.connection.cursor()
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    form=UploadForm()
    if form.validate_on_submit():
        f=request.files['photo'].filename
        filename=photos.save(form.photo.data)
        file_url=url_for('get_file',filename=filename)
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO image (filename) VALUES(%s)",[f])
        mysql.connection.commit()
        cursor.close()
        file_url=url_for('view_image',filename=f)
        return redirect(file_url)  
    else:
        file_url=None
        return render_template("upload_image.html",form=form,file_url=file_url)

@app.route('/viewimage/<filename>')
def view_image(filename):

    qs=filename
    
    return render_template("viewimage.html",qs=qs)

if __name__=='__main__':
    app.run(debug=True)