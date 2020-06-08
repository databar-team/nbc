#!/bin/bash
function render() {
    local INPUT_YAML=$1
    # Extract the environment name.
    local ENV=$(echo ${INPUT_YAML} | sed 's/-input\.yaml//')
    local OUTPUT_DIRECTORY=$2
    local VERSION=$3
    local S3_SOURCE=s3://dw-s3-code-${ENV}-us-west-2/map-data-pipeline-flyway/${VERSION}
    local ENVIRONMENT_SPECIFIC_OUTPUT_DIRECTORY=${OUTPUT_DIRECTORY}/${ENV}

    mkdir -p ${ENVIRONMENT_SPECIFIC_OUTPUT_DIRECTORY}
    # Render the pipeline definition
    python ${MUSTACHE_TEMPLATE_RENDERER_NAME} \
        ${ENV} \
        ${S3_SOURCE} \
        ${ENVIRONMENT_SPECIFIC_OUTPUT_DIRECTORY}

    if [ $? -ne 0 ]; then
        exit 1
    fi
}

if [ $# -ne 2 ]; then
    echo "Syntax: $0 <definitions_output_directory> <version>"
    exit 1
fi

RELATIVE_OUTPUT_DIRECTORY=$1
VERSION=$2

# Constants
MUSTACHE_TEMPLATE_RENDERER_NAME=render_mustache_template.py
TEMPLATES_DIR=src/pipeline
COMPONENT_NAME=map-data-pipeline-flyway
OUTPUT_DIRECTORY=$(pwd)/${RELATIVE_OUTPUT_DIRECTORY}
S3_SOURCE=${SCRIPT_ROOT}/src
TEMP_DIRECTORY=$(mktemp -d)
VIRTUAL_ENVIRONMENT_NAME=venv
# Install virtualenv into the temp directory so that subsequent libraries
# do not pollute the global namespace
# pip install virtualenv -t ${TEMP_DIRECTORY}
# python ${TEMP_DIRECTORY}/virtualenv.py venv
# virtualenv ${VIRTUAL_ENVIRONMENT_NAME}
virtualenv ${VIRTUAL_ENVIRONMENT_NAME}
source ${VIRTUAL_ENVIRONMENT_NAME}/bin/activate

# Setup dependencies to render mustache templates
pip --trusted-host pypi.python.org install -r requirements.txt

rm -rf ${OUTPUT_DIRECTORY}
mkdir -p ${OUTPUT_DIRECTORY}

# The mustache template has dependent templates. Therefore, switch to the
# templates directory to allow relative paths to work correctly.
pushd ${TEMPLATES_DIR}

# Enumerate the environments based on the ${ENV}-input.yaml files.
# This process takes into account that common-input.yaml is a file that is
# common to all environments, and therefore, ignores common-input.yaml.
# This allows the files in source control to determine the environments
# for which this script will build definitions.
for input in $(ls *-input.yaml)
do
    # Render the pipeline definition based on all files except common-input.yaml.
    if [ ${input} != "common-input.yaml" ]; then
        render ${input} ${OUTPUT_DIRECTORY} ${VERSION}
    fi
done

# Pop the push ${TEMPLATES_DIR}
popd

# Cleanup
rm -rf ${TEMP_DIRECTORY}
deactivate
# rm -rf ${VIRTUAL_ENVIRONMENT_NAME}
