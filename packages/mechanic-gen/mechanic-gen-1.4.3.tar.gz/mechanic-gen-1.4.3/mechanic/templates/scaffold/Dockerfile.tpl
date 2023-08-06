# mechanic save - safe to modify below #
FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

ENV PYTHONPATH=.:$PYTHONPATH
CMD ["gunicorn", "wsgi", "-b 0.0.0.0:8080"]
# END mechanic save #
