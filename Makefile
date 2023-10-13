.PHONY: install

install:
ifneq (,$(findstring Python 3,$(shell python3 --version)))
	python3 -m venv venv;
	. venv/bin/activate; pip install -r requirements.txt;
endif

run: install
	. venv/bin/activate; python convert_coordinates.py

clean: 
	rm -rf venv
	rm -rf input
	rm -rf output
