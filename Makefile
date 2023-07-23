# Run the Django development server
run:
	python manage.py runserver

# Create and apply database migrations
migrate:
	python manage.py makemigrations
	python manage.py migrate

# Create a superuser for the admin interface
createsuperuser:
	python manage.py createsuperuser

# startapp command for creating app
startapp:
	python manage.py startapp $(app)

# Run tests
test:
	python manage.py test

# Install project dependencies
install:
	pip install -r requirements.txt

# Clean up generated files
clean:
	rm -rf __pycache__ */__pycache__ */*/__pycache__ *.pyc */*.pyc */*/*.pyc
