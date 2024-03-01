.PHONY: test
test:
	docker run -ti --rm -u1000 \
		-v $(PWD):/local/ansible_collections/petardo/simplevault \
		-w /local/ansible_collections/petardo/simplevault $(shell docker build -q .) \
		ansible-test units --venv
