
import time
import requests
import datadog
from dd_agent.checks import AgentCheck
from hashlib import md5

class RandomCheck(AgentCheck):
    def check(self, instance):
        random_val = random.random()
        self.gauge('test.support.random', random_val)

a= RandomCheck()
a.check()
# def get_metrics():
#     start_time = time.time()
#     r = requests.get('http://127.0.0.1:8000/')
#     duration = time.time() - start_time
#     statsd.increment('page.views.home')
#     # statsd.histogram('latency.home', duration)
#     # statsd.histogram('database.query.time', duration)
#
#
# get_metrics()

# def home():
#     start = time.time()
#     r = requests.get('http://127.0.0.1:8000/')
#     duration = time.time() - start
#     statsd.increment('page.views', tags=['support', 'page:home'])
#
# def login():
#     start_time = time.time()
#     r = requests.get('http://127.0.0.1:8000/login')
#     duration = time.time() - start_time
#     statsd.increment('page.views', tags=['support', 'page:login'])
#
#
# def register():
#     start_time = time.time()
#     r = requests.get('http://127.0.0.1:8000/register')
#     duration = time.time() - start_time
#     statsd.increment('page.views', tags=['support', 'page:register'])
#
home()
login()
# register()
