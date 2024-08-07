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
test1: build
	echo "test 1"
	./callinfo w1aw
test2: build
	echo "test 2"
	 echo "delete FROM fieldday.qrzdata where callsign = 'nj1q';delete FROM fieldday.qrzdata where fdcall = 'nj1q';" | mariadb
	 echo "delete FROM rcforb.rawny_details where callsign = 'nj1q';delete FROM rcforb.rawny_details where callsign = 'nj1q';" | mariadb
	./callinfo NJ1Q
	./callinfo NJ1Q | mariadb
	./callinfo NJ1Q | mariadb
	./callinfo NJ1Q --table fieldday.qrzdata
	./callinfo NJ1Q --table fieldday.qrzdata | mariadb
	./callinfo NJ1Q --table fieldday.qrzdata | mariadb
test3: build
	echo "test 3"
	./callinfo w3zr --hamqth --nosql
test4: build
	echo "test 4"
	 echo "delete FROM rcforb.rawny_details where callsign = 'w1aw';delete FROM fieldday.qrzdata where fdcall = 'w1aw';" | mariadb
	./callinfo -t fieldday.qrzdata w1aw
	 ./callinfo -t fieldday.qrzdata w1aw | mariadb
test: build test1 test2 test3 test4
	echo "test"
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
