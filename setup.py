

from setuptools import setup,find_packages

setup(
    name = "visa",
    version="0.0.1",
    author="Yaganti Ashok",
    author_email="Yagantiashok177@gmail.com",
    packages=find_packages()
)

aws ecr get-login-password --region eu-north-1 | docker login --username AWS --password-stdin 108445731300.dkr.ecr.eu-north-1.amazonaws.com