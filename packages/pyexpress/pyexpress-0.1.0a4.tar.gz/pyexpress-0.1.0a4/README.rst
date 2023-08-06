ExpressPy
=======================

This project is inspired by ExpressJS.

It helps to create a simple HTTP server.

The source for this project is available on GitHub: `<https://github.com/drubay/pyexpress>`_.


Installation
=====

.. code:: bash

    pip install pyexpress

Examples
=========

.. code:: python

    from expresspy import HttpServerHelper


    PORT = 8080

    def post_hello(req, res, next):
        print("POST /hello")
        print("body: " + str(req.body))
        res.status(204).send()


    def get_hello(req, res, next):
        print("GET /hello/:helloId")
        print("helloId: " + req.path_params['helloId'])
        res.status(200).send('Hello'.encode('UTF-8'))


    HttpServerHelper.post("/hello", post_hello)
    HttpServerHelper.get("/hello", get_hello)
    HttpServerHelper.static("dist")
    HttpServerHelper.start(PORT)

    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass


See example.py for more details.