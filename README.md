# yapistir_io Source Code

yapistir.io servisine ait kaynak kodları barındıran repo

# Kurulum

Python 3.10.x ile birlikte PostgreSQL gerekmektedir.

.env aşağıdaki gibi olmalı ve TPaste içerisine yerleştirilmelidir.

```
DEBUG=False
SITE_URL=
SECRET_KEY=
GOOGLE_RECAPTCHA_SECRET_KEY=
ALLOWED_HOSTS=*
DATABASE_URL=psql://postgres:2855@127.0.0.1:5432/yapistir_io
EMAIL_HOST=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=noreply@yapistir.io
```

Ardından uygulama aşağıdaki şekilde geliştirme sunucusu çalıştırılabilir.

```
poetry update
python manage.py migrate
python manage.py runsslserver
```
