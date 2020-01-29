#All the import statements goes here:
import os
import numpy as np
from PIL import Image
import tensorflow as tf

from resizeimage import resizeimage
from werkzeug import secure_filename
from keras_preprocessing import image
from flask import Flask, flash, request, make_response, render_template

#Your directory name where images should be uploaded
UPLOAD_FOLDER = 'uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Your Route
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['image']
        name= file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], name))

        image_file = Image.open("uploads/{}".format(name)) # open colour image
        image_file = image_file.convert('1') # convert image to black and white
        image_file.save('uploads/{}'.format(name))

        with open('uploads/{}'.format(name), 'r+b') as f:
            with Image.open(f) as image:
                cover = resizeimage.resize_cover(image, [28, 28])
                cover.save('uploads/{}'.format(name), image.format)


        img = Image.open('uploads/{}'.format(name))
        array = np.array(img)

        new_model = tf.keras.models.load_model("my_model.h5")

        pred = new_model.predict(np.array([array]))

        pred = np.argmax(pred)

        #labels of images
        class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat','Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
        val = class_names[pred]
       #return "Machine predicted value is: {}".format(val)
        return render_template('predict.html', image_file_name=file.filename, val=val)
    else:
        return render_template("index.html")

@app.route('/upload/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

def create_app():
    load__model()
    return app

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True,use_reloader=False)
