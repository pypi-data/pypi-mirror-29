# OZ Holiday

A simple function to check a given date a public holiday or not in Australia, really easy to use.

- Use the data from [data.gov.au](https://data.gov.au/dataset/australian-holidays-machine-readable-dataset)
- Only use Python standard libraries
- Only one function - keep it simple

## Installation
```bash
pip install ozholiday
```

Or

```bash
git clone https://github.com/zhongdai/ozholiday.git
cd ozholiday
python setup.py install
```

## Usage
```python
In [1]: from ozholiday import isholiday

In [2]: isholiday('20170101')
Out[2]: True

In [3]: isholiday('20170101',detail=True)
Out[3]:
{'Applicable To': 'NAT',
 'Date': '20170101',
 'Holiday Name': "New Year's Day",
 'Information': "New Year's Day is the first day of the calendar year and is celebrated each January 1st",
 'More Information': '',
 '_id': 1}

In [5]: isholiday('20170103')
Out[5]: False

In [9]: isholiday('20190102')
ValueError: The date 20190102 is not in current list published by data.gov.au,
 Check here https://data.gov.au/dataset/australian-holidays-machine-readable-dataset
 ```


=======
History
=======

0.1.0 (2018-03-02)
------------------

* First release on PyPI.


