import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pulumi-terraform-module",
    version="0.0.1",
    author="Jelle Hellemans",
    author_email="author@example.com",
    description="Use your battle tested or 3rd party terraform modules directly in your pulumi workflow.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/devops-proficient/pulumi-terraform-module",
    project_urls={
        "Bug Tracker": "https://github.com/devops-proficient/pulumi-terraform-module/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.11",
    test_suite="tests",
)