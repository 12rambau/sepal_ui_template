![sepal_ui template](https://raw.githubusercontent.com/openforis/sepal-doc/master/docs/source/img/sepal_header.png)

# `sepal-ui` template app

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/12rambau/sepal_ui_template/blob/no_default/LICENSE)
[![Black badge](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## About 

Fake application using the `sepal_ui` framework to create an interactive **Voila** dashboard.
Go to the [sepal_ui repository](https://github.com/12rambau/sepal_ui) for more information about the components used in this template.

![full_app](https://raw.githubusercontent.com/12rambau/sepal_ui/master/docs/source/_image/sepal_ui_demo.gif)

## Usage 

This template is bound to the `module_factory` CLI from the [sepal_ui](https://github.com/12rambau/sepal_ui) lib but it can also be used as a stand-alone app. each branch can be used as a specific type of application: 

- `master` and `no_aoi` are empty shells, they just embed the minimal material of a `sepal-ui` based application. It can be used as a template for your own repository. 
- `no_gee` is a `sepal-ui` based application with one panel: the built-in AOI selector of the lib. It's using the GADM administrative boundaries dataset.
- `no_default` is a `sepal-ui` based application with also one panel. The only difference being that the AOI selector is now wired to GEE and produce `ee.imageCollection` in addition to `geopandas.GeoDataframe`. it's based on the FAO GAUL 2015 administrative boundaries dataset.
- `default` is a fully functional `sepal-ui` based app. it's the one build during the main [tutorial](https://sepal-ui.readthedocs.io/en/latest/tutorials/sepalize.html).
- `heroku` is a modified application that is deplyed on Heroku (https://sepal-ui.herokuapp.com)

to install it simply use : 

```
$ git clone https://github.com/12rambau/sepal_ui_template.git
$ cd sepal_ui_template
```
## Contribute

To contribute to this repository please respect the following hierarchy when it comes to modifications so that we can continue to spread them throughout the branches using simple merge. 

- `master` when it comes to general modifications to adapt to recent updates of `sepal-ui`
- `no_gee` if modifications are related to the AOI selector
- `no_default` if modifications are specific to the GEE wired version of the AOI selector 
- `default` if the tutorial changes
- `heroku` to update the deployed app

merge hierarchy: 

```
master
├── no_aoi
│   └── no_gee
│       └── no_default
│           └── default
└── heroku
```


