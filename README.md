# Longevity testcase realization by Mathgeni task backend
> - This project represents basical RESTful API endpoints for user registration, login, fetching user profile and deleting the account using Django Rest Framework (DRF)
> - Password hashing using Argon2 cryptographic hashing algorithm
> - Custom user model that has email as unique identifier
>- Sending OTP during registration integrated with Redis and Celery
>- Database: PosgreSQL
# Deployment
## Configuration
> - Configure venv on server
> - Install dependencies of a packages from requirements.txt **_$ pip intall -r requirements.txt_**
> - Implement migrations **_$ python3 -m manage migrate_**
## Gunicorn
> - Install Gunicorn as WSGI **_$ pip install gunicorn_**
> - Create socket file for gunicorn
[![1.png](https://i.postimg.cc/X7vrWVdw/1.png)](https://postimg.cc/vDpYLwPB)
> - Create service file for gunicorn
[![2.png](https://i.postimg.cc/d1HLkpK7/2.png)](https://postimg.cc/xJm0Bs8Y)
> - Enable gunicorn **_$ sudo systemctl enable gunicorn.socket || sudo systemctl enable gunicorn.service_**
> - Run gunicorn **_$ sudo systemctl start gunicorn.socket_**
## Nginx
> - Change server block for nginx **_$ sudo nano /etc/nginx/sites-available/Longevity_**
[![3.png](https://i.postimg.cc/02DPLjyW/3.png)](https://postimg.cc/PPXgDtZY)
> - Activate **_$ sudo ln -s /etc/nginx/sites-available/Longevity /etc/nginx/sites-enabled_**
## Redis
> - **_$ sudo apt install redis-server_**
> - Change redis.conf file **_$ sudo nano /etc/redis/redis.conf_**
> - ~~port 6379~~ -> port 7379
> - ~~supervised no~~ -> supervised systemd
> - Restart Redis service **_$ sudo systemctl restart redis.service**
## Celery
> - Configure file **_$ sudo nano /etc/systemd/system/celery.service_**
[![1.png](https://i.postimg.cc/KjQThJYD/1.png)](https://postimg.cc/304Ngjmk)
> - Enable and start Celery **_$ sudo systemctl enable celery || sudo systemctl start celery_**
# Usage
|    Method     |     Route     |      Data     |
| ------------- | ------------- | ------------- |
| POST          | /register/ | email pasword |
| POST          | /verify/  | email otp |
| POST          | /login/  | email password |
| POST          | /api-token-auth/  | username: email password |
| GET         | /user/  | None |
| DELETE         | /delete/  | email password |
