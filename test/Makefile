.PHONY: clean provision_docker unit

containers = provision_docker_host_one provision_docker_host_two provision_docker_host_three provision_docker_host_four provision_docker_host_five optimus ironhide megatron starscream

all: provision_docker unit

clean:
	docker rm -f $(containers) || true

provision_docker: clean
	ansible-playbook -i inventory playbooks/test_default.yml -vvv

unit:
	py.test -s unit/ -vv

