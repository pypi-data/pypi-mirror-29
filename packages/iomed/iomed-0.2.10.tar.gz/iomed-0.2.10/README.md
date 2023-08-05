IOMED Medical Language API
==========================

## Installation instructions

1. Obtain a key to the IOMED Medical Language API visiting [https://console.iomed.es](https://console.iomed.es).
2. Export your key in your `~/.bashrc`:

```bash
export IOMED_MEL_KEY="your-key-here"
```

3. Install `iomed`:

```bash
pip3 install iomed
```

## Usage as cli

```bash
text=$(cat text)
iomed "$text"
```

## Usage as python library

There is a [limitation](/pricing/#limits) of a certain amount of characters per request. If you want to annotate a big text, you will have to split it. We will provide a way to do it automatically with this library in the future.

### Simplest usage

```python
from iomed import MEL
mel = MEL('your-api-key')
result = mel.parse('dolor en el pecho desde hace dos horas')
```

### Parallel usage, for larger amounts of data

```python
from iomed import ParallelMEL

n_workers = multiprocessing.cpu_count() * 2 + 1
pmel = ParallelMEL(num_workers=n_workers)

# add the cloud MEL service
pmel.add_api('https://api.iomed.es/tagger/annotation', 'your-api-key-1')
# add another service, e.g. a local installation of MEL.
# this is optional! you can use it with a single API endpoint, for the
# sake of easy parallelization.
pmel.add_api('http://localhost:5000/annotation', 'your-api-key-2')

with open('text.txt') as fh:
    sentences = fh.readlines()

results = pmel.process(sentences)
```
