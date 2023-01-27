import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="tagbase-aws-cdk",
    version="0.1.0",
    description="An AWS CDK Python app for tagbase-server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="tagbase-server development team",
    install_requires=[
        "aws-cdk-lib==2.62.2",
        "constructs>=10.0.0,<11.0.0",
    ],
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
)
