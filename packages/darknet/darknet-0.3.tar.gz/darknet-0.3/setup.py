from setuptools import setup, find_packages

setup(
    name = 'darknet',
    version = '0.3',
    keywords = ('basic tools','utils'),
    description = 'basic package for using',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
      ],
    license = 'MIT License',
    #install_requires = ['simplejson>=1.1'],

    author = 'wangjj',
    author_email = 'hzwangjj@gmail.com',

    #packages = find_packages(),
    packages = ["darknet/file","darknet/image","darknet/network","darknet/text"],
    #packages = ["darknet"],
    #package_dir ={ "file": "darknet"},
    platforms = "any"
)
