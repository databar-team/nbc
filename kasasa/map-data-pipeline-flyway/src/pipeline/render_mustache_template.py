"""
GIVEN a mustache template named pipeline-definition.mustache
AND a file named common-input.yaml
AND a file named ${environment}-input.yaml
WHEN render_mustache_template_template.py runs
AND it is passed the environment as the parameter
AND it is passed the output directory
THEN it generates pipeline-definition.json in the specificed output directory.
"""
import pystache
import os
import sys
import yaml

# TODO: Use argument parser
if (len(sys.argv) != 4):
    print "Syntax: %s environment scriptsSrc output_directory"%(sys.argv[0],)
    print """
environment                        -  The environment. For example, sandbox
scriptsSrc                         -  The S3 bucket/prefix that provides the location of the scripts that the pipeline uses.
output_directory                   -  The directory where this script will store pipeline-definition.json.
"""
    sys.exit(1)


# Absolute path to the mustache template
dirname = os.path.dirname(__file__)
template = "pipeline-definition.mustache"
absolute_path = os.path.abspath(os.path.join(dirname, template))

# Input parameters
environment = sys.argv[1]
s3_bucket_location = sys.argv[2]
output_directory = sys.argv[3]

# Opinionated inputs
common_input = "common-input.yaml"
environment_specific_input = "%s-input.yaml"%(environment,)
output_filename = "pipeline-definition.json"

# Load the enviroment specific parameters
common_parameters_file = os.path.abspath(os.path.join(dirname, common_input))
with open(common_input, 'r') as stream:
    parameters = yaml.load(stream)

# Load the enviroment specific parameters
environment_parameters_file = os.path.abspath(os.path.join(dirname, environment_specific_input))
with open(environment_parameters_file, 'r') as stream:
    environment_specific_parameters = yaml.load(stream)

parameters.update(environment_specific_parameters)

# The template refers to the environment itself through the template parameter
# named env
parameters['env'] = environment

parameters['scriptsSrc'] = s3_bucket_location

# Render the above template with the above parameters
renderer = pystache.Renderer()
rendered = renderer.render_path(absolute_path, parameters)

# Save the rendered result.
output_file = os.path.abspath(os.path.join(output_directory, output_filename))
try:
    with open(output_file, 'w') as stream:
        stream.write(rendered)

    print "Applied environment=%s, and " \
        "parameters from %s and %s to template %s to " \
        "generate %s"%(environment, common_parameters_file, environment_parameters_file, \
            template, output_file)
except IOError as e:
    print e
    sys.stderr.write("Could not write to %s"%(output_file,))
