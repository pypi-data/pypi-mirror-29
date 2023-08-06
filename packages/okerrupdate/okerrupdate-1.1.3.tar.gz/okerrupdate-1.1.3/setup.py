from setuptools import setup

setup(name='okerrupdate',
    version='1.1.3',
    description='micro client for okerr cloud monitoring system',
    url='http://okerr.com/',
    author='Yaroslav Polyakov',
    author_email='xenon@sysattack.com',
    license='MIT',
    packages=['okerrupdate'],
    scripts=['scripts/okerrupdate'],
#    data_files = [
#        ('okerrclient/conf',['data/conf/okerrclient.conf']),
#        ('okerrclient/init.d', ['data/init.d/okerrclient']),
#        ('okerrclient/systemd',['data/systemd/okerrclient.service']),
#    ], 
    install_requires=['requests','future'],
#    include_package_data = True,
    zip_safe=False
)    

