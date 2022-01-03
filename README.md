# tikka

This repo contains Python tools for converting and analysing documents, including a [Flask](https://palletsprojects.com/p/flask/) web frontend to upload, serve and analyse documents. The web frontend is Heroku-ready and works out of the box with Python 3.10.

## Usage

First, spin up an [Apache Tika](https://tika.apache.org/1.24.1/gettingstarted.html) instance in Docker mapped to a local port. By default, the new instance of [docker-tikaserver](https://github.com/LogicalSpark/docker-tikaserver) will run on port 9998.

```sh
sudo docker pull logicalspark/docker-tikaserver
sudo docker run -d -p 9998:9998 logicalspark/docker-tikaserver
```

Next, start the Flask web server in development mode running on port 5000 (by default).

```sh
pip install -r requirements.txt
source env/bin/activate
flask run
```

## Getting hungry?

Yes, me too.

<img src="https://pinchofyum.com/wp-content/uploads/Chicken-Tikka-Masala-2-4-768x1152.jpg" height="400">

## License

The app is available as open source under the terms of the [MIT License](http://opensource.org/licenses/MIT).
