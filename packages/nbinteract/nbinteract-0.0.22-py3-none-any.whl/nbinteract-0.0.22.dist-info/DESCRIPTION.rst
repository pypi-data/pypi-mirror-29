nbinteract
=================

[![Read the Docs](https://img.shields.io/badge/docs-gitbook-green.svg)][docs]
[![PyPI](https://img.shields.io/pypi/v/nbinteract.svg)](https://pypi.python.org/pypi/nbinteract/)
[![npm](https://img.shields.io/npm/v/nbinteract.svg)](https://www.npmjs.com/package/nbinteract)

`nbinteract` is a set of tools to create interactive webpages using Jupyter
notebooks. Before, creating an interactive webpage required authors to know
HTML, CSS, and Javascript. With `nbinteract`, if you know Python you know how
to create an interactive webpage. `nbinteract` makes explanations that make use
of data especially easy because of its support for interactive visualizations.

Currently, `nbinteract` is in an alpha stage because of its quickly-changing
API.

## Demo

![nbinteract](https://user-images.githubusercontent.com/2468904/34280356-01a147a2-e66c-11e7-8c81-6e06b5445e38.gif)

[Click this link to view live.][demo]

## Use Cases

`nbinteract` can be used by:

- Data scientists that want to create an interactive blog post without having
  to know / work with Javascript.
- Instructors that want to include interactive examples in their textbooks.
- Students that want to publish data analysis that contains interactive demos.

## Tutorial and Documentation

[Here's a link to the tutorial and docs for this project.][docs]

## Getting Started

To install the package, you must first have
[Jupyter Notebook installed][install-nb]. Then, run:

```
pip install nbinteract
```

Navigate to a folder containing notebooks you'd like to convert, then run:

```
nbinteract YOUR_NOTEBOOK.ipynb
```

Replace `YOUR_NOTEBOOK.ipynb` with the name of your notebook file. You will now
have an HTML file in the same directory. You can open that HTML file in your
browser and interact with widgets there.

## Developer Install

If you are interested in developing this project locally, run the following:

```
git clone https://github.com/SamLau95/nbinteract
cd nbinteract

# Installs the nbconvert exporter
pip install -e .

# To export a notebook to interactive HTML format:
jupyter nbconvert --to interact notebooks/Test.ipynb

pip install -U ipywidgets
jupyter nbextension enable --py --sys-prefix widgetsnbextension

brew install yarn
yarn install

# Start notebook and webpack servers
make -j2 serve
```

## Contributors

This project is developed by [Sam Lau][sam] and Caleb Siu as part of a Masters
project at UC Berkeley.

[demo]: https://samlau95.gitbooks.io/nbinteract/content/examples/Correlation.html
[ipywidgets]: https://github.com/jupyter-widgets/ipywidgets
[bqplot]: https://github.com/bloomberg/bqplot
[widgets]: http://jupyter.org/widgets.html
[gh-pages]: https://pages.github.com/
[gitbook]: http://gitbook.com/
[install-nb]: http://jupyter.readthedocs.io/en/latest/install.html
[docs]: https://samlau95.gitbooks.io/nbinteract/content/
[sam]: http://www.samlau.me/


