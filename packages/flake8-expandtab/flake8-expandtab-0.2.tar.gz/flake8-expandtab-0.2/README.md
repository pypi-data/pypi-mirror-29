# flake8-expandtab

## Introduction

[flake8](https://github.com/PyCQA/flake8) for tab junkies. This extension allows
you to pre-expand tabs into spaces before flake8 parses files, to get around
flake8's 8-space tab assumption.

## Installation

Install it via pip:

```sh
$ pip install flake8 flake8-expandtab
```

## Configuration

You can specify `--tab-width` to an integer value to activate this extension, or
specify `tab-width` in your config.

## Authors

* **Chow Loong Jin** - *Initial work* - [hyperair](https://github.com/hyperair)

See also the list
of [contributors](https://github.com/hyperair/flake8-expandtab/contributors) who
participated in this project.

## License

This project is licensed under the MIT License - see
the [LICENSE](LICENSE) file for details

## Acknowledgments

* [README-Template.md from PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* [flake8](https://github.com/PyCQA/flake8) -- a great linting tool that really
  hates tabs
* [Rejected pycodestyle smart-tabs PR](https://github.com/PyCQA/pycodestyle/pull/397) --
  kudos to [dsedivec](https://github.com/dsedivec) for the initial attempt at
  making flake8 usable with tab indentation
