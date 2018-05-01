# Onestopshop

This is an e-commerce application built using django. Allows an user to purchase while authenticated as well as a guest. Perisisting cart between for a guest after authenticating. Provides suggestions based on previous purchases for authenticated user. Sends custom emails using mailchimp for registered users. Uses stripe for payment. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development.

### Prerequisites

Install the following
* python 3.6.3
* pip
* virtual env
* django- 1.11

### Installing

Download/clone the repository. Recommended to use a virtual environment. Open terminal and run these commands to start the server.  
```python
cd your-local-repository-path
python3 -m venv Restaurants
cd project-directory
source bin/activate
cd src
pip install -r requirements.txt
```  
Run the following after setting up and every time you want to start server
```
python3 mange.py runserver
```
### Built With

* python
* django
* PostgresQL
* AWS s3
* Stripe
* Mailchimp
* Heroku
* pyCharm
* bootstrap
* Jquery

### License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/vykuntaharsha/onestopshop/blob/master/LICENSE) file for details.
