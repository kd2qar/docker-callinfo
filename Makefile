TAG=kd2qar/callinfo

NAME=callquery

all: build

build:
	docker build --rm  --tag ${TAG} .

run:
	docker run  -it --rm --name ${NAME} ${TAG} /bin/bash

shell: build
	docker run  -it --rm --name ${NAME} ${TAG} /bin/bash

test: build
	./callinfo w1aw
	echo "delete FROM rcforb.rawny_details where callsign = 'w1aw';delete FROM fieldday.qrzdata where fdcall = 'w1aw';" | mariadb
	./callinfo w1aw | mariadb
	./callinfo w1aw -t fieldday.qrzdata | mariadb
	./callinfo w1aw | mariadb
	./callinfo w1aw -t fieldday.qrzdata | mariadb

