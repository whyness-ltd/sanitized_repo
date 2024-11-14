# syntax=docker/dockerfile:1

# Use Apache 2.4
FROM httpd:2.4
# Don't write .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Force the stdout and stderr streams to be unbuffered

# Set the working directory to /app
WORKDIR /app
# Copy the Django requirements to /app
COPY requirements.txt /app/
# Copy the application to /app
COPY . /app
# Install required modules listed in requirements.txt
RUN apt-get update \
 && apt-get install -y --no-install-recommends python3.9-dev \
 && apt-get install -y python3-pandas \
 && apt-get install -y --no-install-recommends python3-pip python3-venv \
 && apt-get install -y --no-install-recommends libapr1 libapr1-dev \
 && apt-get install -y --no-install-recommends libaprutil1-dev \
 && apt-get install -y --no-install-recommends libapache2-mod-wsgi-py3 \
 && apt-get install -y --no-install-recommends g++ \
 && apt-get install -y --no-install-recommends ffmpeg \
 && apt-get install -y --no-install-recommends postgresql-client-13 \
 && apt-get install -y --no-install-recommends libpq-dev \
 && python3.9 -m venv --system-site-packages /app \
 && python3.9 -m pip install -r /app/requirements.txt --no-cache-dir \
 && apt remove -y libc-dev-bin \
 && apt remove -y libcrypt-dev \
 && apt remove -y libgcc-10-dev \
 && apt remove -y linux-libc-dev \
 && apt remove -y libapr1-dev \
 && apt remove -y g++ \
 && apt remove -y libldap2-dev \
 && apt remove -y libnsl-dev \
 && apt remove -y libpq-dev \
 && rm -rf /var/lib/apt/lists/*
# && apt autoremove -y \
# Set venv
ENV PATH="/app/bin:$PATH"
COPY ./apache2/httpd.conf /usr/local/apache2/conf/httpd.conf
COPY ./apache2/httpd-vhosts.conf /usr/local/apache2/conf/extra/httpd-vhosts.conf
# When a container is run, it will use the following command to start the app
#CMD ["python3", "manage.py", "runserver", "IP.REMOVED:8000"]
#CMD ["gunicorn", "--bind=IP.REMOVED:8000", "whyness_django.wsgi"]
#CMD ["nginx", "-g", "daemon off;"]
EXPOSE 80
CMD ["apachectl", "-D", "FOREGROUND"]
