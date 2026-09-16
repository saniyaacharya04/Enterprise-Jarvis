.PHONY: help install run-backend run-frontend test docker-up docker-down

help:
	@echo "Available commands:"
	@echo "  make install       - Install backend and frontend dependencies"
	@echo "  make run-backend   - Start FastAPI backend server on port 8000"
	@echo "  make run-frontend  - Start Streamlit frontend on port 8501"
	@echo "  make test          - Run automated pytest suite"
	@echo "  make docker-up     - Start all services with Docker Compose"
	@echo "  make docker-down   - Stop Docker Compose services"

install:
	pip install -r backend/requirements.txt
	pip install -r frontend/requirements.txt

run-backend:
	cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

run-frontend:
	streamlit run frontend/streamlit_app.py

test:
	pytest backend/tests -v

docker-up:
	docker-compose up --build

docker-down:
	docker-compose down
