NAMESPACE=kiennt
APP=telebot

.PHONY: install
install: requirements
		python setup.py install
		make clean

.PHONY: run
run: install
		bin/telebot

.PHONY: requirements
requirements:
		pip install -r requirements.txt

.PHONY: clean
clean:
	rm -rf build dist telebot.egg-info
