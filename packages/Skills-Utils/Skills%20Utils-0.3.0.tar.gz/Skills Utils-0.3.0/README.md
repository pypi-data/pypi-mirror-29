# skills-utils
Open Skills Project shared utilities

[![Build Status](https://travis-ci.org/workforce-data-initiative/skills-utils.svg?branch=master)](https://travis-ci.org/workforce-data-initiative/skills-utils)
[![codecov](https://codecov.io/gh/workforce-data-initiative/skills-utils/branch/master/graph/badge.svg)](https://codecov.io/gh/workforce-data-initiative/skills-utils)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

Through the Open Skills Project we have a need for common utilities that need to be shared between different repositories. Usually these are more low-level and not of particular interest for skills research, but do make Open Skills work easier.

The library is pip-installable, though not through PyPi. You can install it from github:

`pip install git+git://github.com/workforce-data-initiative/skills-utils.git`

## Utility modules

`es` - Elasticsearch utilities. Ranging from wrappers to the Python Elasticsearch module to an 'zero downtime index' context manager that uses aliases to perform lengthy indexing operations and switch the alias to the completed version only when successful, with no downtime

`fs` - Filesystem utilities. For instance, a decorator that caches the JSON-serializable output of any function. This is helpful when downloading large datasets.

`hash` - Hashing utilities. Used to standardize boilerplate string hashing used throughout the project.

`io` - Input/Output utilities. For instance, streaming JSON lines from a file

`iteration` - Iteration utilities. For instance, breaking an iterable into configurably-sized batches.

`job_posting_import` - Job Posting import utilities. Defines a base class for defining quarterly importers of job postings, and transforming them into a common schema.

`metta` - [metta-data](http://github.com/dssg/metta-data) utilities. Metta-data is a project that defines a standardized matrix/metadata storage utility. It makes it possible to different projects to store design matrices in a way that outsiders can easily use to test model training on real datasets, and know enough about the dataset in order to make sense of it. This module has a prototype for storing an ONET SOC Code classifier using metta.

`s3` - S3 utilities. Some thin wrappers around some boto functionality to reduce boilerplate.

`testing` - Testing utilities. Including a unittest.TestCase subclass to be used to for testing JobPostingImportBase subclasses to ensure some level of confirmity with our common job posting schema.

`time` - Time utilities. The Open Skills Project heavily utilizes quarterly time windows, so most of the utilities in this module involve quarter conversions.
