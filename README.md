To run locally on computer Ensure that chromed is installed

Add .env file with following credentials

```
	DJANGO_SECRET=
	PROXY_HOST=
	PROXY_PORT=
	PROXY_USER=
	PROXY_PASS=
	HOST_DOMAIN=
	X_USER=
	X_PASS=
	DB_STRING=<mabgodb connection sstring>
```

Either allow your ip address in the proxy provider or Use head full proxy chrome method instead of normal one in proxy.py

Run:

`pip install -r requirements.txt`

`python manage.py runserver`
