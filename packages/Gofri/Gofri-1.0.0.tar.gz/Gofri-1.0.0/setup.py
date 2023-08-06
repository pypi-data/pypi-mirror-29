from distutils.core import setup

setup(
    name='Gofri',
    version='1.0.0',
    packages=['gofri', 'gofri.lib', 'gofri.lib.pip', 'gofri.lib.xml',
              'gofri.lib.conf', 'gofri.lib.decorate',
              'gofri.lib.project_generator', 'gofri.lib.util',
              'gofri.lib.http'
              ],
    install_requires=[
        'flask',
        'flask_restful',
        'sqlalchemy',
        'importlib',
        'xmltodict',
        'clinodes',
        'inflection'
    ],
    url='https://github.com/ThomasKenyeres/Gofri',
    license='MIT',
    author='thomas',
    author_email='kenyerest97@gmail.com ',
    description='Python web framework'
)
