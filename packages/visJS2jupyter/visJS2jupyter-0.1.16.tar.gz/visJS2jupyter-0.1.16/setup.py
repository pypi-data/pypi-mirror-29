from setuptools import setup

setup(
    name = "visJS2jupyter",
    packages = ["visJS2jupyter"],
    version = "0.1.16",
    description= "visJS2jupyter is a tool to bring the interactivity of networks created with vis.js into Jupyter notebook cells",
	long_description="0.1.16 update: Improved return_node_to_color and return_edge_to_color functions",
    url = "https://github.com/ucsd-ccbb/visJS2jupyter",
    author="Brin Rosenthal (sbrosenthal@ucsd.edu), Mikayla Webster (m1webste@ucsd.edu), Aaron Gary (agary@ucsd.edu), Julia Len (jlen@ucsd.edu)",
    author_email="sbrosenthal@ucsd.edu",
    keywords = ['Jupyter notebook', 'interactive', 'network'],
    license = 'MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
    ]
)
