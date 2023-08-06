# Serverboards Mock Library -- SMock

SMock is a simple mocking library that helps automated testing of Python code.

Basic usage is to create a yaml file with the mocked functions as keys, and a
list of marching `args` list/`kwargs` object to a `result`.

All possible matches are checked in order, and if any matches, that response is
given to the caller. A special `*` marker can be used to match any.

## Example of use

Generate a yaml file with the data to mock, `mock.yaml`:

```yaml
requests.get:
  - args: https://example.com/item/1
  - result:
    status_code: 200
    json:
      desription: Mocked
requests.get:
  - args: "*"
    result:
      status_code: 404
      content: Not found
```

This file says that if the user asks for the `https://mock.example`, it gets a
`status_code` `200` and more info. Any other request, gets a `404`.

To use it:

```python
import requests

def get_item_description(id):
  data = requests.get("https://example.com/item/%s" % id)
  return data.json()["description"]

def test():
  smock import SMock
  smock = SMock("data.yaml")
  requests.get = smock.mock_method("requests.get")

  assert get_item_description(1) == "Mocked"

if __name__ == "__main__":
  test()

```

Tis hypotetical library, has a function `get_item_description`. When calling
this file as a script (`__main__`), the test is called which monkey patches the
`requests.get` function with our mocked data.

This mocked data returns a special object that behaves like a dict, an object a
callable function and so on. In this case we call the `json()` virtual method
to just get an object with a `description` field.

## Contributing

If you have ideas, improvements or comments, please open a github issue.

