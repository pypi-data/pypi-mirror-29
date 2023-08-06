# musdb

[![Build Status](https://travis-ci.org/sigsep/sigsep-mus-db.svg?branch=master)](https://travis-ci.org/sigsep/sigsep-mus-db)
[![Coverage Status](https://coveralls.io/repos/github/sigsep/sigsep-mus-db/badge.svg?branch=master)](https://coveralls.io/github/sigsep/sigsep-mus-db?branch=master)
[![Latest Version](https://img.shields.io/pypi/v/musdb.svg)](https://pypi.python.org/pypi/musdb/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/musdb.svg)](https://pypi.python.org/pypi/musdb/)
[![Docs Status](https://readthedocs.org/projects/musdb/badge/?version=latest)](https://musdb.readthedocs.org/en/latest/)


A python package to parse and process the [MUSDB18 dataset](https://sigsep.github.io/musdb) as part of the [MUS task](https://sisec.inria.fr/home/2018-professionally-produced-music-recordings/) of the [Signal Separation Evaluation Campaign (SISEC)](https://sisec.inria.fr/).

## Download Dataset

The dataset can be downloaded [here](https://sigsep.github.io/musdb).

## Installation

### Decoding

As the _MUSDB18_ is encoded as [STEMS](http://www.stems-music.com/), it
relies on ffmpeg to read the multi-stream files. We provide a python wrapper called [stempeg](https://github.com/faroit/stempeg) that allows to easily parse the dataset and decode the stem tracks on-the-fly.
Before you install _musdb_ (that includes the stempeg requirement), it is therefore required to install ffmpeg. The installation differ among operating systems.

E.g. if you use Anaconda you can install ffmpeg on Windows/Mac/Linux using the following command:

```
conda install -c conda-forge ffmpeg
```

Alternatively you can install ffmpeg manually as follows:
* Mac: use homebrew: `brew install ffmpeg`
* Ubuntu Linux: `sudo apt-get install ffmpeg `

#### Use a decoded version

If you have trouble installing stempeg or ffmpeg we also support parse and process the pre-decoded PCM/wav files. We provide [docker based scripts](https://github.com/sigsep/sigsep-mus-io) to decode the dataset to wav files.
If you want to use the decoded musdb dataset, use the `is_wav` parameter when initialsing the dataset.

```python
musdb.DB(is_wav=True)
```

### Package installation

You can install the `musdb` parsing package using pip:

```bash
pip install musdb
```

## Usage

This package should nicely integrate with your existing python code, thus makes it easy to participate in the [SISEC MUS tasks](https://sisec.inria.fr/home/2016-professionally-produced-music-recordings). The core of this package is calling a user-provided function that separates the mixtures from the MUS into several estimated target sources.

### Providing a compatible function

- The function will take an MUS ```Track``` object which can be used from inside your algorithm.
- Participants can access:

 - ```Track.audio```, representing the stereo mixture as an ```np.ndarray``` of ```shape=(nun_sampl, 2)```
 - ```Track.rate```, the sample rate
 - ```Track.path```, the absolute path of the mixture which might be handy to process with external applications, so that participants don't need to write out temporary wav files.

- The provided function needs to return a python ```Dict``` which consists of target name (```key```) and the estimated target as audio arrays with same shape as the mixture (```value```).
- It is the users choice which target sources they want to provide for a given mixture. Supported targets are ```['vocals', 'accompaniment', 'drums', 'bass', 'other']```.
- Please make sure that the returned estimates do have the same sample rate as the mixture track.

Here is an example for such a function separating the mixture into a __vocals__ and __accompaniment__ track:

```python
def my_function(track):
    # get the audio mixture as
    # numpy array shape=(nun_sampl, 2)
    track.audio

    # compute voc_array, acc_array
    # ...

    return {
        'vocals': voc_array,
        'accompaniment': acc_array
    }
```

### Creating estimates for SiSEC evaluation

#### Setting up musdb

Simply import the musdb package in your main python function:

```python
import musdb

mus = musdb.DB(root_dir='path/to/musdb')
```

The ```root_dir``` is the path to the musdb dataset folder. Instead of ```root_dir``` it can also be set system-wide. Just ```export MUSDB_PATH=/path/to/musdb``` inside your terminal environment.

#### Test if your separation function generates valid output

Before processing the full MUS which might take very long, participants can test their separation function by running:
```python
mus.test(my_function)
```
This test makes sure the user provided output is compatible to the musdb framework. The function returns `True` if the test succeeds.

#### Processing the full MUS

To process all 150 MUS tracks and saves the results to the folder ```estimates_dir```:

```python
mus.run(my_function, estimates_dir="path/to/estimates")
```

#### Processing training and testing subsets separately

Algorithms which make use of machine learning techniques can use the training subset and then apply the algorithm on the test data. That way it is possible to apply different user functions for both datasets.

```python
mus.run(my_training_function, subsets="train")
mus.run(my_test_function, subsets="test")
```

##### Access the reference signals / targets

For supervised learning you can use the provided reference sources by loading the `track.targets` dictionary.
E.g. to access the vocal reference from a track:

```python
track.targets['vocals'].audio
```

#### Use multiple cores

##### Python Multiprocessing

To speed up the processing, `run` can make use of multiple CPUs:

```python
mus.run(my_function, parallel=True, cpus=4)
```

Note: We use the python builtin multiprocessing package, which sometimes is unable to parallelize the user provided function to [PicklingError](http://stackoverflow.com/a/8805244).


## Full code Example

```python
import musdb

def my_function(track):
    '''My fancy BSS algorithm'''

    # get the audio mixture as numpy array shape=(num_sampl, 2)
    track.audio

    # get the mixture path for external processing
    track.path

    # get the sample rate
    track.rate

    # return any number of targets
    estimates = {
        'vocals': vocals_array,
        'accompaniment': acc_array,
    }
    return estimates

# initiate musdb
mus = musdb.DB(root_dir="./Volumes/Data/musdb")

# verify if my_function works correctly
if mus.test(my_function):
    print "my_function is valid"

# this might take 3 days to finish
mus.run(my_function, estimates_dir="path/to/estimates")

```
## Baselines

Please check [examples of oracle separation methods](https://github.com/sigsep/sigsep-mus-oracle).
This will show you how oracle performance is computed, i.e. an upper bound for the quality of the separtion.

## Evaluation and Submission

Please refer to our [Submission site](https://github.com/sigsep/sigsep-mus-2018).

## Frequently Asked Questions

##### The mixture is not exactly the sum of its sources, is that intended an actual bug?

This is not a bug. Since we adopted the STEMS format, we used AAC compression and wanted to compression noise of the mixture is different from the sum of the compression noises of the sources, you hear the sum of those 5 noises, since you are adding: the compression for the 4 sources, minus the compression of the mixture (the true sources being cancelled by the subtraction of the true mix underlying those signals). As you mention, we did not have this problem with the DSD100, that was encoded in the WAV format.

## References

LVA/ICA 2018 publication t.b.a
