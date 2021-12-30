



.PHONY : build
build:
	clear
	sudo python setup.py install

.PHONY : remove
remove:
	sudo rm -rf build
	sudo rm -rf square_pass.egg-info
	sudo rm -rf dist



