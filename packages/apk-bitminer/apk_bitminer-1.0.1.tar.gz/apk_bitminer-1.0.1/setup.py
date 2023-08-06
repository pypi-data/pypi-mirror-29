import setuptools



setuptools.setup(
    name='apk_bitminer',
    package_dir={'': 'src'},
    packages=setuptools.find_packages('src'),
    include_package_data=True,
    namespace_packages=[],
    license='BSD2',
    version='1.0.1',
    scripts=['src/apk_bitminer/pydexdump',
             'src/apk_bitminer/pyaxmldump']
)
