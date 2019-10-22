all : clean

parents.zip :
	wget 'https://www.dropbox.com/s/n4epgi5vr1awvrh/parents.zip'

.unzip : parents.zip
	unzip parents.zip
	touch .unzip

.import: .unzip
	python manage.py import_data
	touch .import

.PHONY: clean
clean : .import
	rm parents.zip
	rm -rf Emergency\ Notification\ System/
	rm .unzip
	rm .import
