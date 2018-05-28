Run on macOS 10.13 using Python 3.6.

Setup:

```
pip install -r requirements.txt
```

To run try one of these:

```
python3 normalize_csv.py sample.csv
python3 normalize_csv.py sample-with-broken-utf8.csv
```

Should be complete according to problem statement, except:

1. Floating point seconds calculation not finished
2. No error handling for when Unicode replacement character breaks parsing

I also did not have time to write any automated tests.