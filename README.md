
# Django PDF

A small app that will allow the users to login and upload PDF and image documents. The server will generate text from the image/document using OCR or Optical Character Recognition.

This Django web app uses pytesseract(https://pypi.org/project/pytesseract/) for OCR.

Note: This app requires you to install https://github.com/tesseract-ocr/tesseract to be able to use the OCR. Also, this app is a MVP.

## Features

- User authentication and login
- Handles both PDF and image files 
- Copy and generate text from images or PDF docs using OCR
- Ability to download the original upload files

## Installation

This app uses PostgreSQL for DBMS. Download it from - https://github.com/tesseract-ocr/tesseract

Make sure you download and install tesseract(https://github.com/tesseract-ocr/tesseract) for OCR.

## Run Locally

Clone the project

```bash
  git clone https://github.com/PallavMarwaha/django-pdf
```

Go to the project directory

```bash
  cd django-pdf
```

Create and activate a new virtual environment

```bash
  python3 -m venv venv
  source venv/Scripts/activate or venv/Scripts/activate
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  python manage.py runserver
```


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file in the root folder

`SECRET_KEY`

`DB_NAME`

`DB_USER`

`DB_PASSWORD`

`DB_HOST`

`DB_PORT`


## Tech Stack

**Client:** HTML, CSS, TailwindCSS

**Server:** Python, Django, PostgreSQL





