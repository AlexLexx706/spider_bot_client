from setuptools import setup, find_packages

setup(
    name='spider_bot_client',
    version='0.1',
    author='alexlexx',
    author_email='alexlexx1@gmail.com',
    packages=find_packages(),
    license='GPL',
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'calibration= tools.calibration:main',
            'enable_steering = tools.enable_steering:main',
            'read_angles = tools.read_angles:main'
        ],
    }
)
