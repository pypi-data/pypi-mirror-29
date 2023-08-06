from setuptools import setup

setup(
	name="porter-db",
	version="0.0.6",
	description="a simple document based database manager",
	url="https://github.com/wrecodde/porter-db",
	author="Deji Joseph",
	author_email="wrecodde@gmail.com",
	license="MIT",
        packages=["porter_db"],
        long_description=open("README.txt").read()
)
