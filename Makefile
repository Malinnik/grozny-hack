up:
	docker compose up -d 
down:
	docker compose down
restart:
	docker compose down && docker compose up -d 

back:
	python backend/src/main.py
back-dev:
	fastapi dev backend/src/main.py 
back-build:
	docker build -t horaziy/grozny-hack-backend:latest ./backend
back-push:
	docker push horaziy/grozny-hack-backend:latest
back-req:
	cd backend && pip freeze > ./requirements.txt


front:
	cd frontend && npm run dev
front-build:
	docker build -t horaziy/grozny-hack-frontend:latest ./frontend
front-push:
	docker push horaziy/grozny-hack-frontend:latest



project:
	make back-build
	make front-build
	make up