TAG=kd2qar/callinfo

NAME=callquery

all: build

build:
	docker build --rm  --tag ${TAG} .

run:
	docker run  -it --rm --name ${NAME} ${TAG} /bin/bash

shell: build
	docker run  -it --rm --name ${NAME} ${TAG} /bin/bash

testnosql: build
	./callinfo --nosql w1aw
test: build
	./callinfo w1aw
	echo "delete FROM rcforb.rawny_details where callsign = 'w1aw';delete FROM fieldday.qrzdata where fdcall = 'w1aw';" | mariadb
	./callinfo w1aw | mariadb
	./callinfo -t fieldday.qrzdata w1aw | mariadb
	./callinfo w1aw | mariadb
	./callinfo -t fieldday.qrzdata w1aw | mariadb
	echo "delete FROM rcforb.rawny_details where callsign = 'w1aw';delete FROM fieldday.qrzdata where fdcall = 'w1aw';" | mariadb
	./callinfo --noqrz w1aw
	./callinfo --noqrz -t fieldday.qrzdata w1aw | mariadb
	./callinfo --noqrz | mariadb
	./callinfo --noqrz -t fieldday.qrzdata w1aw | mariadb
	./callinfo -t test.temptable_calldata_temptable w1aw | mariadb
