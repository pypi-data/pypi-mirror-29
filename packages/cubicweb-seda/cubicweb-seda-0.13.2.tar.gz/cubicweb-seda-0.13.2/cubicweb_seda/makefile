
all:
	python xsd2yams.py > schema/seda2.py
	python xsd2uicfg.py | grep -v 'unsupported merge' | grep -v 'extending cards' > views/uicfg.py
	python xsd2entities.py | grep -v 'unsupported merge' | grep -v 'extending cards' > entities/generated.py

lcsv:
	python xsd2concepts.py migration/data
