# WSChat

## How to run
1. Download repository `git clone https://github.com/Velx/WSChat.git`
2. Choose which config you want to run:
   - For production version with PostgreSQL add `.env` file to root directory with envirements:
      - POSTGRES_USER
      - POSTGRES_PASSWORD
      - POSTGRES_DB
      - SQL_HOST
      - SQL_PORT
      - REDIS_HOST
      - DEBUG
      - SECRET_KEY
   - For development version with SQLite3 go to the next step
3. Run it with docker-compose `docker-compose up -d`
4. Now server is running on port 8000

## Endpoints
- '127.0.0.1:8000/' - chat room
- '127.0.0.1:8000/registration/' - registration page
- '127.0.0.1:8000/login' - login page
