'''Converts notebooks to interactive HTML pages or Gitbook pages.

Usage:
  nbinteract init
  nbinteract NOTEBOOKS ...
  nbinteract [options] NOTEBOOKS ...
  nbinteract (-h | --help)

`nbinteract init` initializes a GitHub project for nbinteract. It
provides guided help to set up a requirements.txt file (if needed) and a Binder
image for the project.

`nbinteract NOTEBOOKS ...` converts notebooks into HTML pages. Note that
running this command outside a GitHub project initialized with `nbinteract
init` required you to specify the --spec SPEC option.

Arguments:
  NOTEBOOKS  List of notebooks or folders to convert. If folders are passed in,
             all the notebooks in each folder are converted. The resulting HTML
             files are created adjacent to their originating notebooks and will
             clobber existing files of the same name.

             By default, notebooks in subfolders will not be converted; use the
             --recursive flag to recursively convert notebooks in subfolders.

Options:
  -h --help                  Show this screen
  -s --spec                  BinderHub spec for Jupyter image. Must be in the
                             format: `{username}/{repo}/{branch}`. For example:
                             'SamLau95/nbinteract-image/master'. This flag is
                             required unless a .nbinteract.json file exists in
                             the project root with the "spec" key.
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
import sys
from textwrap import wrap
import subprocess
import json

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

BINDER_BASE_URL = 'https://mybinder.org/v2/gh/'
REQUIREMENTS_DOCS = 'http://mybinder.readthedocs.io/en/latest/using.html#id8'
DOCKER_DOCS = 'https://mybinder.readthedocs.io/en/latest/dockerfile.html'

ERROR = 1
SUCCESS = 0


def binder_spec_from_github_url(github_url):
    """
    Converts GitHub origin into a Binder spec.

    For example:
    git@github.com:SamLau95/nbinteract.git -> SamLau95/nbinteract/master
    https://github.com/Calebs97/riemann_book -> Calebs97/riemann_book/master
    """
    tokens = re.split(r'\W+', github_url.replace('.git', ''))
    # The username and reponame are the last two tokens
    return '{}/{}/master'.format(tokens[-2], tokens[-1])


def flatmap(fn, iterable, *args, **kwargs):
    return [
        mapped for item in iterable for mapped in fn(item, *args, **kwargs)
    ]


def color(text, text_color):
    return text_color + text + NOCOLOR


def log(text='', line_length=80, heading='[nbinteract] ', text_color=BLUE):
    width = line_length - len(heading)
    for line in wrap(text, width) or ['']:
        print(color(heading, text_color) + line)


def error(text='', line_length=80, heading='[nbinteract] '):
    log(text, line_length, heading, text_color=RED)


def yes_or_no(question, default="yes"):
    """Ask a yes/no question via input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(
            '{}[nbinteract]{} {}{}'.format(BLUE, NOCOLOR, question, prompt)
        )
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write(
                "Please respond with 'yes' or 'no' "
                "(or 'y' or 'n').\n"
            )


def main():
    """
    Parses command line options and runs nbinteract.
    """
    arguments = docopt(__doc__)
    if arguments['init']:
        return_code = init()
        sys.exit(return_code)

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


def init():
    '''
    Initializes git repo for nbinteract.

    1. Checks for requirements.txt or Dockerfile, offering to create a
       requirements.txt if needed.
    2. Sets the Binder spec using the `origin` git remote in .nbinteract.json.
    3. Prints a Binder URL so the user can debug their image if needed.
    '''
    log('Initializing folder for nbinteract.')
    log()

    log('Checking to see if this folder is the root folder of a git project.')
    if os.path.isdir('.git'):
        log("Looks like we're in the root of a git project.")
    else:
        error(
            "This folder doesn't look like the root of a git project. "
            "Please rerun nbinteract init in the top-level folder of a "
            "git project."
        )
        return ERROR
    log()

    log('Checking for requirements.txt or Dockerfile.')
    if os.path.isfile('Dockerfile'):
        log(
            'Dockerfile found. Note that Binder will use the Dockerfile '
            'instead of the requirements.txt file, so you should make sure '
            'your Dockerfile follows the format in {docker_docs}'
            .format(docker_docs=DOCKER_DOCS)
        )
    elif os.path.isfile('requirements.txt'):
        log('requirements.txt found.')
    else:
        log('No requirements.txt file found.')
        yes = yes_or_no(
            'Would you like to create a sample requirements.txt file?'
        )
        if yes:
            # TODO(sam): Don't hard-code requirements.txt
            with open('requirements.txt', 'w') as f:
                f.writelines(['numpy\n', 'nbinteract\n'])
            log(
                'Created requirements.txt. Edit this file now to include the '
                'rest of your dependencies, then rerun nbinteract init.'
            )
            return SUCCESS
        else:
            log(
                'Please manually create a requirements.txt file, then rerun '
                'nbinteract init.'
            )
            return SUCCESS
    log()

    log('Generating .nbinteract.json file...')
    if os.path.isfile('.nbinteract.json'):
        log(
            ".nbinteract.json already exists, skipping generation. If you'd "
            "like to regenerate the file, remove .nbinteract.json and rerun "
            "this command."
        )
        log()
        log("Initialization success!")
        return SUCCESS

    try:
        github_origin = str(
            subprocess.check_output(
                'git remote get-url origin',
                stderr=subprocess.STDOUT,
                shell=True
            ), 'utf-8'
        ).strip()
    except subprocess.CalledProcessError as e:
        error(
            "No git remote called origin found. Please set up your project's"
            "origin remote to point to a GitHub URL.\ngit error: {}".format(e)
        )
        return ERROR

    if 'github' not in github_origin:
        error(
            "Your project's origin remote {} doesn't look like a github "
            "URL. This may cause issues with Binder, so please double check "
            "your .nbinteract.json file after this script finishes. "
            "Continuing as planned..."
        )

    binder_spec = binder_spec_from_github_url(github_origin)
    with open('.nbinteract.json', 'w') as f:
        json.dump({'spec': binder_spec}, f, indent=4)
    log('Created .nbinteract.json file successfully')
    log()

    log(
        'Initialization complete! Now, you should make a git commit with the '
        'files created by in this process and push your commits to GitHub.'
    )
    log()
    log(
        'After you push, you should visit {} and verify that your Binder image'
        'successfully starts.'.format(BINDER_BASE_URL + binder_spec)
    )


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

    if not SPEC_REGEX.match(arguments['--spec']):
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
