# QTI Learning App

## Backend Setup
go to ```/backend``` and then run:
``` python -m venv .venv ```

in ```/backend``` install the requirements.txt
```pip install -r requirements.txt```

## Setup

### 1. Install Node.js >= 16
QTI 3 Item Player Controller was originally built and tested with Node v16.14.  As of November 2023, QTI 3 Item Player Controller has been built and tested with Node v20.9.0.

### 2. Project Setup
run
```sh
npm install
```

### 3. Compiles and hot-reloads for development
```sh
npm run serve
```

### 4. Open Browser
Open http://localhost:8080/ in the browser.

## Questions
You can see the sample questions under public/qti/. 
You can add your own questions and tests (QTI 3.0!) to this directory.
Make sure to add the path to your tests to the constant `filenames` aswell:

```js
async function bootstrap() {
  // Dateinamen angeben, die unter public/qti/tests liegen
  const filenames = [
    'test1.xml',
    'test2.xml',
    'cloud_computing_test.xml'
    // ..alle anderen QTI-XMLs
  ]
```
