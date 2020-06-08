#!/bin/bash
function verify_prerequisites() {
	command -v curl 2>&1 > /dev/null
	if [ $? -ne 0 ]; then
		echo "This script expects curl to be available and it failed to find it."
		echo "This should not be an issue if this scripts executes on a true unix clone or in a Git Bash shell."
		echo "This failure maybe because this script executed in a windows command shell."
		echo "This script will now abort."
		exit 1
	fi
}
cfg_usage() {
	echo Configure with the file pipeline-runner.properties
	echo " DESIRED_BUILD_VERSION"

	exit 1
}

# Download the file from the specified URL and store in the specified output file.
# Parameter 1 - the download URL
# Parameter 2 - the output filename
function download() {
	local URL=$1
	local OUTPUT_FILE=$2

	curl -# -o ${OUTPUT_FILE} "${URL}"
}
source ./pipeline-runner.properties
PIPELINE_RUNNER_DIRECTORY=.pipeline-runner
BIN_PATH="${PIPELINE_RUNNER_DIRECTORY}/pipeline-runner.sh"
CURRENT_VERSION_PATH="${PIPELINE_RUNNER_DIRECTORY}/pipeline-runner.version"
BIN_DIR=$(dirname $BIN_PATH)
FILE_PATH=${BIN_DIR}/pipeline-runner.tar.gz
if [ -z "DESIRED_BUILD_VERSION" ]; then
	cfg_usage
fi

# If there is already a current build version of ${BIN_PATH}
if [ -f ${CURRENT_VERSION_PATH} ]; then
	CURRENT_BUILD_VERSION=$(cat ${CURRENT_VERSION_PATH})
else
	CURRENT_BUILD_VERSION=
fi

# If the DESIRED_BUILD_VERSION does not match the CURRENT_BUILD_VERSION
# then remove $BIN_PATH so that this wrapper will download the desired
# version of the runner.
if [ "${CURRENT_BUILD_VERSION}" != "${DESIRED_BUILD_VERSION}" ]; then
	rm -rf $(dirname $BIN_PATH)
	CURRENT_BUILD_VERSION=${DESIRED_BUILD_VERSION}
fi

verify_prerequisites

if [ ! -f $BIN_PATH ]; then
	echo "Download version ${CURRENT_BUILD_VERSION} of the pipeline-runner"

	mkdir -p ${BIN_DIR}

	# Download the artifact.
	download "http://sonatype.bvops.net/nexus/service/local/artifact/maven/content?g=com.bancvue&a=dw-pipeline-runner&v=${CURRENT_BUILD_VERSION}&r=release-candidate&e=tar.gz" \
		${FILE_PATH}

	# Extract
	tar -C ${BIN_DIR} -xpvzf ${FILE_PATH}

    chmod +x $BIN_PATH
	rm ${FILE_PATH}

	echo ${CURRENT_BUILD_VERSION} > ${CURRENT_VERSION_PATH}
fi

ARGS=( "$@" )

PIPELINE_RUNNER_DIRECTORY=${PIPELINE_RUNNER_DIRECTORY} \
SCRIPT_NAME=$0 \
	./$BIN_PATH ${ARGS[@]}
