# FaceR
Vue.js SPA served over Flask microframework

* Python: 3.7
* Vue.js: 2.5.16
* axios: 0.16.2

## Build Setup

``` bash
# install front-end
cd FaceRWeb
npm install
# serve with hot reload at localhost:8080
npm run dev
# build for production/Flask with minification
npm run build
# install back-end
cd ../FaceRService
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
cd ..
# serve back-end at localhost:5000
FLASK_APP=run.py flask run
```
