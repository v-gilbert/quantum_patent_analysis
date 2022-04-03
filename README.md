# Quantum Patent Analysis

In this analysis we study:
- Companies publishing patents in the quantum field
- Specialization of each actor
- Scientists publishing most patents

Data of this project was exctracted from [INPI](https://data.inpi.fr/) (Institut National de la Propriété Industrielle)
database which is the French patent office.

# How to run the code

This code require MongoDB database. You can install it following this [guide](https://www.mongodb.com/docs/manual/installation/).
It also require the INPI database. To do this you need to send a request to the INPI: [here](https://data.inpi.fr/content/editorial/lien-serveur-ftp-PI)

Create a virtual environment
```shell
python -m venv venv
```

Install dependencies
```shell
pip install -r requirements.txt
```

You're all set ! You can now run the code !