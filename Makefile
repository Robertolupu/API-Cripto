r:
	docker-compose down app
	docker-compose build app
	docker-compose up app -d
	docker-compose logs -f app