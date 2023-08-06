bump-upload:
	bumpversion patch
	git push --tags
	git push --all


	$(MAKE) twine

twine:
	rm -f dist/*
	python setup.py sdist
	twine upload dist/*

vulture:
