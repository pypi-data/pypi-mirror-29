#!/usr/bin/env python
'''Converts notebooks to interactive HTML pages or Gitbook pages.

Usage:
  nbinteract SPEC NOTEBOOKS ...
  nbinteract [options] SPEC NOTEBOOKS ...
  nbinteract (-h | --help)

Arguments:
  SPEC       BinderHub spec for Jupyter image. Must be in the format:
             `{username}/{repo}/{branch}`. For example:
             'SamLau95/nbinteract-image/master'.

  NOTEBOOKS  List of notebooks or folders to convert. If folders are passed in,
             all the notebooks in each folder are converted. The resulting HTML
             files are created adjacent to their originating notebooks and will
             clobber existing files of the same name.

             By default, notebooks in subfolders will not be converted; use the
             --recursive flag to recursively convert notebooks in subfolders.

Options:
  -h --help                  Show this screen
  -t TYPE --template TYPE    Specifies the type of HTML page to generate. Valid
                             types: full (standalone page), partial (embeddable
                             page), or gitbook (embeddable page for GitBook).
                             [default: full]
  -B --no-top-button         If set, doesn't generate button at top of page.
  -r --recursive             Recursively convert notebooks in subdirectories.
  -o FOLDER --output=FOLDER  Outputs HTML files into FOLDER instead of
                             outputting files adjacent to their originating
                             notebooks. All files will be direct descendants of
                             the folder even if --recursive is set.
  -i FOLDER --images=FOLDER  Extracts images from HTML and writes into FOLDER
                             instead of encoding images in base64 in the HTML.
                             Requires -o option to be set as well.
'''
from docopt import docopt, DocoptExit
from glob import glob
import os
import re

import nbformat
from traitlets.config import Config
from .exporters import InteractExporter

BLUE = "\033[0;34m"
RED = "\033[91m"
NOCOLOR = "\033[0m"

VALID_TEMPLATES = set(['full', 'gitbook', 'partial', 'local'])

SPEC_REGEX = re.compile('\S+/\S+/\S+')

# Used to ensure all the closing div tags are on the same line for Markdown to
# parse them properly
CLOSING_DIV_REGEX = re.compile('\s+</div>')


def flatmap(fn, iterable, *args, **kwargs):
    return [
        mapped for item in iterable for mapped in fn(item, *args, **kwargs)
    ]


def log(text):
    print('{}[nbinteract]{} {}'.format(BLUE, NOCOLOR, text))


def error(text):
    print('{}[nbinteract]{} {}'.format(RED, NOCOLOR, text))


def main():
    """
    Parses command line options and runs nbinteract.
    """
    arguments = docopt(__doc__)
    check_arguments(arguments)

    notebooks = flatmap(
        expand_folder,
        arguments['NOTEBOOKS'],
        recursive=arguments['--recursive']
    )

    exporter = init_exporter(
        extract_images=arguments['--images'],
        spec=arguments['SPEC'],
        template_file=arguments['--template'],
        button_at_top=(not arguments['--no-top-button'])
    )

    log('Converting notebooks to HTML...')

    for notebook in notebooks:
        output_file = convert(
            notebook,
            exporter=exporter,
            output_folder=arguments['--output'],
            images_folder=arguments['--images']
        )
        log('Converted {} to {}'.format(notebook, output_file))

    log('Done!')

    if arguments['--images']:
        log('Resulting images located in {}'.format(arguments['--images']))


def check_arguments(arguments):
    if arguments['--images'] and not arguments['--output']:
        error(
            'If --images is specified, --output must also be specified. '
            'Exiting...'
        )
        raise DocoptExit()

    if arguments['--template'] not in VALID_TEMPLATES:
        error(
            'Unsupported template: "{}". Template must be one of: \n{}'
            .format(arguments['--template'], VALID_TEMPLATES)
        )
        raise DocoptExit()

    if not SPEC_REGEX.match(arguments['SPEC']):
        error(
            'Spec must be in the format {username}/{repo}/{branch}. '
            'Exiting...'
        )
        raise DocoptExit()


def expand_folder(notebook_or_folder, recursive=False):
    """
    If notebook_or_folder is a folder, returns a list containing all notebooks
    in the folder. Otherwise, returns a list containing the notebook name.

    If recursive is True, recurses into subdirectories.
    """
    if os.path.isfile(notebook_or_folder):
        return [notebook_or_folder]
    elif os.path.isdir(notebook_or_folder):
        matcher = '{}/**/*.ipynb' if recursive else '{}/*.ipynb'
        return glob(matcher.format(notebook_or_folder), recursive=recursive)
    else:
        raise ValueError(
            '{} is neither an existing file nor a folder.'
            .format(notebook_or_folder)
        )


def init_exporter(extract_images, **exporter_config):
    """
    Returns an initialized exporter.
    """
    config = Config(InteractExporter=exporter_config)

    if extract_images:
        # Use ExtractOutputPreprocessor to extract the images to separate files
        config.InteractExporter.preprocessors = [
            'nbconvert.preprocessors.ExtractOutputPreprocessor',
        ]

    exporter = InteractExporter(config=config)
    return exporter


def convert(notebook_path, exporter, output_folder=None, images_folder=None):
    """
    Converts notebook into an HTML file, outputting notebooks into
    output_folder if set and images into images_folder if set.

    Returns the path to the resulting HTML file.
    """
    if output_folder:
        os.makedirs(output_folder, exist_ok=True)
    if images_folder:
        os.makedirs(images_folder, exist_ok=True)

    # Computes notebooks/ch1 and <name>.ipynb from notebooks/ch1/<name>.ipynb
    path, filename = os.path.split(notebook_path)
    # Computes <name> from <name>.ipynb
    basename, _ = os.path.splitext(filename)
    # Computes <name>.html from notebooks/<name>.ipynb
    outfile_name = basename + '.html'

    extract_output_config = {
        # This results in images like AB_5_1.png for a notebook called AB.ipynb
        'unique_key': basename,
        'output_files_dir': images_folder,
    }

    notebook = nbformat.read(notebook_path, as_version=4)
    html, resources = exporter.from_notebook_node(
        notebook,
        resources=extract_output_config,
    )

    # Remove newlines before closing div tags
    final_output = CLOSING_DIV_REGEX.sub('</div>', html)

    # Write out HTML. If output_folder is not set, we default to the original
    # folder of the notebook
    out_folder = path if not output_folder else output_folder
    outfile_path = os.path.join(out_folder, outfile_name)
    with open(outfile_path, 'w') as outfile:
        outfile.write(final_output)

    # Write out images. If images_folder wasn't specified, resources['outputs']
    # is None so this loop won't run
    for image_path, image_data in resources.get('outputs', {}).items():
        with open(image_path, 'wb') as outimage:
            outimage.write(image_data)

    return outfile_path


if __name__ == '__main__':
    main()
