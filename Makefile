all : clean

parents.zip :
	wget ${ARGS}

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
