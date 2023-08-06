from setuptools import setup, find_packages

setup(
    name = "wagtail-polls",
    version = "2.0.0",
    author = "David Burke",
    author_email = "david@thelabnyc.com",
    description = ("A small polls app in wagtail"),
    license = "Apache License",
    keywords = "django wagtail poll",
    url = "https://gitlab.com/thelabnyc/wagtail_polls",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        'Environment :: Web Environment',
        'Framework :: Django',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: Apache Software License",
    ],
    install_requires=[
        'wagtail>=2.0',
    ]
)
