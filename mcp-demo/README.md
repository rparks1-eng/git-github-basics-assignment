# Activity 22 MCP and the Python SDK

FastAPI serves a saved random forest iris classifier. An MCP server exposes
two tools that call the API. The Python client discovers the tool metadata
and calls a tool over stdio.

## Run

```sh
uv sync --locked
uv run create_model.py
uv run fastapi dev api.py
```

Keep the API running. In a second terminal in this folder:

```sh
uv run client.py
uv run client.py --tool classify_iris --measurements 6.3 3.3 6.0 2.5
```

The default client call tests iris_probabilities with 6.0, 2.7, 5.1, and 1.6.
It returns setosa 0.00, versicolor 0.68, and virginica 0.32.
The classification command returns virginica.
Swagger at http://127.0.0.1:8000/docs returns setosa for the assignment's
5.1, 3.5, 1.4, and 0.2 example.

The supplied starter files work with MCP SDK 2.3.0. Changes add the probabilities
endpoint and MCP tool, HTTP error checking, optional client arguments, and
compact display of the discovered input schema. The original classify_iris
docstring was restored after testing the vague description.

Screenshots and answers are in this folder. The trained joblib file was
created locally from scikit-learn's built-in iris dataset. Train a fresh copy
with create_model.py if using different dependency versions.
