from setuptools import setup

__author__ = 'Takatada Yoshima'
__version__ = '0.1.0'


setup(
    name='github2slack',
    version=__version__,
    author=__author__,
    author_email='yoshima@shiimaxx.com',
    url='https://github.com/shiimaxx/github2slack',
    description="Post to Slack GitHub unread notifications",
    packages=['github2slack'],
    install_requires=['PyGithub'],
    license='MIT License',
    include_package_data=True,
)
