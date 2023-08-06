import subprocess

from setuptools import Command, setup

# -----------------------------------------------------------------------------


def system(command):
    class SystemCommand(Command):
        user_options = []

        def initialize_options(self):
            pass

        def finalize_options(self):
            pass

        def run(self):
            subprocess.check_call(command, shell=True)

    return SystemCommand


# -----------------------------------------------------------------------------

setup(
    name="oauth-token-manager",
    version='0.1.0',
    description="OAuth 2.0 token manager",
    url='https://github.com/4Catalyzer/oauth-token-manager',
    author="Jimmy Jia",
    author_email='tesrin@gmail.com',
    license='MIT',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ),
    keywords='oauth token',
    py_modules=('oauth_token_manager',),
    python_requires='>=3',
    install_requires=('requests',),
    cmdclass={
        'clean': system('rm -rf build dist *.egg-info'),
        'package': system('python setup.py pandoc sdist bdist_wheel'),
        'pandoc': system('pandoc README.md -o README.rst'),
        'publish': system('twine upload dist/*'),
        'release': system('python setup.py clean package publish'),
        'test': system('tox'),
    },
)
