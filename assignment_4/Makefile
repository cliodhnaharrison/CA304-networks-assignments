docker-build: Dockerfile assignment_4.py allegiance.csv templates
	docker build -t allegiance .

docker-run:
	docker run -it --rm --network=host allegiance

clean:
	docker image rm allegiance
