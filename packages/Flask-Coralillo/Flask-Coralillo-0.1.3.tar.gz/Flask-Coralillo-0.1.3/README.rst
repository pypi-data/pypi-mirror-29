Flask Coralillo
===============

Integrates the Coralillo Redis ORM into flask

Usage
-----

This is an easy application that stores and retrieves cars from redis database.

.. code-block:: python

    # app.py
    from flask import Flask, request, redirect
    from flask_coralillo import Coralillo
    from coralillo import Model, fields

    app = Flask(__name__)

    engine = Coralillo(app)

    class Car(Model):
        name = fields.Text()

        class Meta:
            engine = engine

    @app.route('/')
    def list_cars():
        res = '<h1>Cars</h1><ul>'

        for car in Car.get_all():
            res += '<li>{}</li>'.format(car.name)

        res += '</ul><h3>Add car</h3>' + \
            '<form method="POST">' + \
            '<input name="name">' + \
            '<input type="submit" value="Add">' + \
            '</form>'

        return res

    @app.route('/', methods=['POST'])
    def add_car():
        newcar = Car.validate(**request.form.to_dict()).save()

        return redirect('/')

    if __name__ == '__main__':
        app.run()

Now if you run ``python app.py`` and you visit ``http://localhost:5000`` you will be able to intercact with your brand new Flask-Coralillo application.

For more information visit https://getfleety.github.io/coralillo/
