# chaosiq client

[![Build Status](https://travis-ci.org/chaosiq/chaosiq.svg?branch=master)](https://travis-ci.org/chaosiq/chaosiq)

Client to the [ChaosIQ][chaosiq] services.

[chaosiq]: http://www.chaosiq.io/
[chaostoolkit]: http://chaostoolkit.org/

## Overview

This open-source project provides a simple client to the [ChaosIQ][chaosiq]
services. Namely it supports the following features:

* a command line interface to manage your local chaosiq configuration
* an extension to the [chaostoolkit][chaostoolkit] `discover`, `init` and `run`
  commands which interface with the ChaosIQ API to enrich your user experience
  of the chaostoolkit default behavior.

## Install

Once you have installed the requirements below, you can install the
`chaosiq` client as follows:

```console
(chaosiq) $ pip install -U chaosiq
```

## Usage

### The chaosiq CLI

The `chaosiq` client comes with a `chaosiq` command line interface. That CLI
provides a few commands to manage your local chaosiq configuration.

From your virtual environment, invoke it as follows:

```console
(chaosiq) $ chaosiq --help
```

#### Create a default configuration

To talk with the ChaosIQ services, you will need a token, stored locally
in your configuration file. You can intiailize such configuration file as
follows:

```console
(chaosiq) $ chaosiq config init
```

The configuration is located at `~/.chaosiq/config`.

#### Add your token

You must add your ChaosIQ token to the configuration file under `auth/token`.
To do so, simply run:

```console
(chaosiq) $ chaosiq login
Email:
Token:
```

### The chaostoolkit CLI overloading

In addition to its own set of commands, the client overloads the chaostoolkit
CLI to enrich it.

#### The `discover` overloading

The chaosiq client overloads the `discover` command by taking its output and
sending it to the [ChaosIQ][chaosiq] API endpoint. The returned output from
that call is added to the original discovery result.

So here is what happens when you run:

```console
$ chaos discover chaostoolkit-kubernetes
```

As you have installed the chaosiq client, the chaoostoolkit `discover` command
will perform as usual, and discover capabilities from the given extension
package (as well as discovering your system, Kubernetes in this case). That is
the builtin `discover` support from chaostoolkit. On top of that, `chaosiq`
will extend this by sending discovered features to the chaosiq API which will
return a set of potential experiments that could be run with those parameters.

#### The `init` overloading

The chaosiq client overloads the `init` command by offering you the possibility
to initialize your experiment from one of the suggested experiments found via
the `discover` command. This makes it easier to get started as you don't have
to create an experiment step by step. Notice, that you may still do so when
none of the suggested experiments is appropriate.

#### The `run` overloading

The chaosiq client overloads the `run` command. It merely sends the journal to
the ChaosIQ service for better suggestions next time around.

## Requirements

### Python

To install this client, you need [Python 3.5][python] or above installed on your
machine:

[python]: https://www.python.org/

On MacOSX:

```console
$ brew install python3
```

On Debian/Ubuntu:

```console
$ sudo apt-get install python3 python3-venv
```

On CentOS:

```console
$ sudo yum -y install https://centos7.iuscommunity.org/ius-release.rpm
$ sudo yum -y install python35u
```

Notice, on CentOS, the Python 3.5 binary is named python3.5 rather than
python3 as other systems.

On Windows:

[Download the latest binary installer][wininst] from the Python website.

[wininst]: https://www.python.org/downloads/windows/

### Virtual Environment

Once Python is installed, create a [Python virtual environment][venv]:

[venv]: https://docs.python.org/3/tutorial/venv.html

```console
$ python3 -m venv ~/.venvs/chaosiq
```

Make sure to activate thsi environment every time you want to run chaosiq:

```console
$ source  ~/.venvs/chaosiq/bin/activate
```

## Contribute

If you wish to contribute more functions to this package, you are more than
welcome to do so. Please, fork this project, make your changes following the
usual [PEP 8][pep8] code style, sprinkling with tests and submit a PR for
review.

[pep8]: https://pycodestyle.readthedocs.io/en/latest/

[chaosiq][chaosiq] requires all contributors must sign a
[Developer Certificate of Origin][dco] on each commit they would like to merge
into the master branch of the repository. Please, make sure you can abide by
the rules of the DCO before submitting a PR.

[dco]: https://github.com/probot/dco#how-it-works


