import setuptools

setuptools.setup(
    name="mstpylib",
    version="0.2.8",
    author="Missouri University of Science and Technology - Information Technology",
    author_email="it-ai@mst.edu",
    description="A collection of code snippets for interfacing python with our applications infrastructure",
    url="https://git.mst.edu/project/mstpylib",
    packages=["mstpylib", "mstpylib.sqlalchemy"],
    package_dir={
        "mstpylib": "mstpylib",
        "mstpylib.sqlalchemy": "mstpylib/sqlalchemy"
    },
    python_requires=">=3.8",
    install_requires=[
        "ttl_cache",
        "mysql-connector-python",
        "httplib2",
        "sqlalchemy",
        "pymysql"
    ]
)
