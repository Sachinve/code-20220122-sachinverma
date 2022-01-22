# Process a big JSON file

## Installing locally

- Create a python virtualenv
- Install the package locally to your virtualenv



```bash
$ git clone git@github.com:Sachinve/code-20220122-sachinverma.git code-20220122-sachinverma
$ cd code-20220122-sachinverma
$ pip install -e .

```

## Sample data

- Use file `bigjsonprocessor/input.json` as your input file
- Generate sample data with following script if you want

```python

import sys
import random
  
FMT_STRING = '{{"Gender": "{0}", "HeightCm": {1}, "WeightKg": {2} }},\n'

gender = ['Male', 'Female']

with open(sys.argv[1], 'wt') as fp:
    fp.write('[\n')
    for _ in range(int(sys.argv[2])):
        g = random.choice(gender)
        height = random.randint(100, 230)
        weight = random.randint(30, 200)
        fp.write(FMT_STRING.format(g,height, weight))
    fp.write(']\n')
```

---

### Generate 1000 records in the input json
```sh
$ python gen_data.py input.json 1000

```


## Sample usage of the module

```python
from bigjsonprocessor.processor import big_json_transformer

big_json_transformer('input.json', 'output.json')

```

### Sample Output

```bash

>>> from bigjsonprocessor.processor import big_json_transformer
>>> big_json_transformer('input.json', 'output.json')
Height cannot be zero
_num_records ==> 99999
moderately_obese ==> 8336
normal_weight ==> 10303
over_weight ==> 8218
severely_obese ==> 8111
under_weight ==> 14498
very_severely_obese ==> 50533
>>> 

```
