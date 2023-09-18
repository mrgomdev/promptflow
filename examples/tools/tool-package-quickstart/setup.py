from setuptools import find_packages, setup

PACKAGE_NAME = "my-tools-package-with-cstc"

setup(
    name=PACKAGE_NAME,
    version="0.0.1dev0",
    description="This is my tools package",
    packages=find_packages(),
    entry_points={
        "package_tools": ["my_tools = my_tool_package.tools.utils:list_package_tools"],
    },
    include_package_data=True,   # This line tells setuptools to include files from MANIFEST.in
)
