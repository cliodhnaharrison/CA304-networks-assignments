docker-build: Dockerfile server.py
	docker build -t chat-server .

docker-run:
	docker run -it --rm --network=host chat-server

clean:
	docker image rm chat-server
