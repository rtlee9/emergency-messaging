all : clean

parents.zip :
	wget 'https://www.dropbox.com/s/z7hvm3r9rsq1jnl/parents.zip'

.unzip : parents.zip
	unzip parents.zip
	touch .unzip

.import: .unzip enrollment/students/management/commands/import_data.py
	python manage.py import_data
	touch .import

.PHONY: clean
clean : .import
	rm parents.zip
	rm -rf data
	rm .unzip
	rm .import
