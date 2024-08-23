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
	./callinfo --hamqth w1aw
	./callinfo w1aw --noresults
	./callinfo --hamqth w1aw --noresults
test2: build
	echo "test 2"
	 echo "delete FROM fieldday.qrzdata where callsign = 'nj1q';delete FROM fieldday.qrzdata where fdcall = 'nj1q';" | mariadb
	 echo "delete FROM rcforb.rawny_details where callsign = 'nj1q';delete FROM rcforb.rawny_details where callsign = 'nj1q';" | mariadb
	 echo "delete FROM callbook.callinfo where callsign = 'nj1q';delete FROM callbook.callinfo where callsign = 'nj1q';" | mariadb
	./callinfo NJ1Q
	./callinfo NJ1Q | mariadb
	./callinfo NJ1Q | mariadb
	./callinfo NJ1Q --table fieldday.qrzdata
	./callinfo NJ1Q --table fieldday.qrzdata | mariadb
	./callinfo NJ1Q --table fieldday.qrzdata | mariadb
test3: build
	echo "test 3"
	./callinfo w3zr --nosql
	./callinfo w3zr --hamqth --nosql
test4: build
	echo "test 4"
	 echo "delete FROM rcforb.rawny_details where callsign = 'w1aw';delete FROM fieldday.qrzdata where fdcall = 'w1aw';" | mariadb
	./callinfo -t fieldday.qrzdata w1aw
	 ./callinfo -t fieldday.qrzdata w1aw | mariadb
test5: build
	callinfo --refresh --noblanks 5V1JE 5V22FF 5V23LE 5V7A 5V7AA  5V7AD 5V7AK 5V7AS 5V7BB 5V7BD 5V7BJ 5V7BR 5V7C 5V7CC 5V7D 5V7DB 5V7DP 5V7DX 5V7EI 5V7FA 5V7FL 5V7FMD 5V7GD 5V7HR 5V7JD  5V7JG 5V7JH 5V7KS 5V7MA 5V7MAR 5V7MAS 5V7MB 5V7MI 5V7MN 5V7MP 5V7NW 5V7P 5V7PK 5V7PM 5V7PRF 5V7PS 5V7RF 5V7RU 5V7RV 5V7SA 5V7SE 5V7SGA 5V7SI 5V7SM 5V7TD 5V7TH 5V7TT 5V7UF 5V7V 5V7VJ 5V7XO 5V7Z 5V7ZA 5V7ZZ --nosql
test6: build
	callinfo --refresh --nosql 5V7BJ
test7: build
	echo "DELETE FROM callbook.dxcc WHERE dxcc=251 OR dxcc=248;" | mariadb
	callinfo kd2qaq iz5iot  --nosql --refresh
test8: build
	callinfo --refresh co2oq iz7ddc iz8dmz ac7av kk6mu py2wdx sq5hg vk2ly wa3ptf | mariadb
test9: build
	echo  "delete FROM callbook.callinfo where callsign = 've3ma' or callsign='zl1ks' or callsign = 've7eff';" | mariadb
	callinfo --compact w1aw 4x6tt kc3kjq  kd8miv ve7eff zl1ks ve3ma
test: build test1 test2 test3 test4 test5 test6 test7 test8 test9
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
