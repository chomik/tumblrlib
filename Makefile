all: force
	mkdir {lib,obj}
	gnatmake -Ptumblrlib
run: all
	(cd src; python tumblrClient.py)
clean:
	gnatclean -Ptumblrlib
	rm -f src/*.pyc
	rm -rf {lib,obj}
force:
