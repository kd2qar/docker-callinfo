TAG=kd2qar/callinfo

NAME=callquery

all: build

build:
#	cp /data/src/python/getcall/*.cfg .
#	cp /data/src/python/getcall/*.py .
	docker build --rm  --tag ${TAG} .

run:
	docker run  -it --rm --name ${NAME} ${TAG} /bin/bash

shell: build
	docker run  -it --rm --name ${NAME} ${TAG} /bin/bash

