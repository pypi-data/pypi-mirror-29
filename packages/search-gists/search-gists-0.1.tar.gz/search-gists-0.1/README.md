# Class 7: Gist Search

This project provides basic search functionality for a user's public gists.

### Usage

```bash
$ python main.py -u <username> -d [description] -f [file-name]
```

* **`username`** (required): owner of the gists to search for
* **`description`** (optional): Description of gists must contain the passed parameter
* **`file-name`** (optional): The gist contains a file with the given parameter.

**Example**

```bash
# searches all the gists which contain the word "time" in the description
$ python main.py -u <santiagobasulto> -d time

# searches all the gists which have at least 1 file that contains the word "time" in the name
$ python main.py -u <santiagobasulto> -f time
```

# Instructions to publish your project to pypi

[Full Docs](https://packaging.python.org/tutorials/distributing-packages/)

**Step 1: Edit setup.py**

Modified the required names or emails in `setup.py`.

**Step 2: Build the dist and wheel**

```bash
$ pip install wheel  # install wheel first
$ python setup.py sdist
$ python setup.py bdist_wheel --universal
```

**Step 3: Upload your package**

```bash
$ pip install twine
```
?bjzjrdbVCck7yDp/Ykow3q
demo_account_students
