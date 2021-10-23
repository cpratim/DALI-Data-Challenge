from web import app
import gunicorn

if __name__ == '__main__':
	app.run(threaded = True)