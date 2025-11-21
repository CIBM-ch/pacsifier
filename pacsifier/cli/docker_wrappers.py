# Copyright 2018-2024 Lausanne University Hospital and University of Lausanne,
# Switzerland & Contributors

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Docker wrapper scripts for PACSIFIER CLI commands.

These scripts provide a convenient way to run PACSIFIER CLI commands via Docker
without needing to remember the full docker run command syntax.
"""

import argparse
import os
import subprocess
import sys


def get_docker_image_name():
    """Get the Docker image name for PACSIFIER.

    Returns:
        str: The Docker image name, defaulting to 'pacsifier:latest'
    """
    return os.environ.get('PACSIFIER_DOCKER_IMAGE', 'pacsifier:latest')


def run_docker_command(command_args, additional_volumes=None, additional_args=None):
    """Run a PACSIFIER command via Docker.

    Args:
        command_args (list): The command and arguments to run inside the container
        additional_volumes (list): Additional volume mounts (optional)
        additional_args (list): Additional Docker arguments (optional)
    """
    docker_image = get_docker_image_name()

    # Base Docker command
    docker_cmd = [
        'docker', 'run', '--rm', '--net=host'
    ]

    # Add additional Docker arguments if provided
    if additional_args:
        docker_cmd.extend(additional_args)

    # Add volume mounts
    volumes = additional_volumes or []
    for volume in volumes:
        docker_cmd.extend(['-v', volume])

    # Add the image and command
    docker_cmd.append(docker_image)
    docker_cmd.extend(command_args)

    # Run the command
    try:
        subprocess.run(docker_cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Docker command: {e}", file=sys.stderr)
        sys.exit(e.returncode)
    except FileNotFoundError:
        print("Error: Docker not found. Please ensure Docker is installed and in your PATH.",
              file=sys.stderr)
        sys.exit(1)


def docker_pacsman():
    """Docker wrapper for the main pacsifier command."""
    parser = argparse.ArgumentParser(
        description="Run pacsifier via Docker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  docker_pacsman -c config.json -i -q query.csv -d /output
  docker_pacsman --config /path/to/config.json --info \\
      --query /path/to/query.csv --directory /output
        """
    )

    # Add all the same arguments as the original pacsifier command
    parser.add_argument('-c', '--config', required=True, help='Path to configuration file')
    parser.add_argument('-i', '--info', action='store_true', help='Get info about DICOM files')
    parser.add_argument('-q', '--query', help='Path to query CSV file')
    parser.add_argument('-d', '--directory', help='Output directory')
    parser.add_argument('--upload', action='store_true', help='Upload DICOM files')
    parser.add_argument('--download', action='store_true', help='Download DICOM files')
    parser.add_argument('--resume', action='store_true', help='Resume extraction by skipping already downloaded series')
    parser.add_argument('--image',
                        help='Docker image name (overrides PACSIFIER_DOCKER_IMAGE env var)')

    args, unknown_args = parser.parse_known_args()

    # Set Docker image if provided
    if args.image:
        os.environ['PACSIFIER_DOCKER_IMAGE'] = args.image

    # Build command arguments
    command_args = ['pacsifier']

    # Add required config file
    command_args.extend(['-c', '/config.json'])

    # Add optional arguments
    if args.info:
        command_args.append('-i')
    if args.query:
        command_args.extend(['-q', '/query.csv'])
    if args.directory:
        command_args.extend(['-d', '/output'])
    if args.upload:
        command_args.append('--upload')
    if args.download:
        command_args.append('--download')
    if args.resume:
        command_args.append('--resume')

    # Add any unknown arguments
    command_args.extend(unknown_args)

    # Build volume mounts
    volumes = []
    if args.config:
        volumes.append(f"{os.path.abspath(args.config)}:/config.json")
    if args.query:
        volumes.append(f"{os.path.abspath(args.query)}:/query.csv")
    if args.directory:
        volumes.append(f"{os.path.abspath(args.directory)}:/output")

    run_docker_command(command_args, additional_volumes=volumes)


def docker_get_pseudonyms():
    """Docker wrapper for the get_pseudonyms command."""
    parser = argparse.ArgumentParser(
        description="Run pacsifier-get-pseudonyms via Docker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  docker_get_pseudonyms -i input.csv -o output.csv
  docker_get_pseudonyms --input /path/to/input.csv --output /path/to/output.csv
        """
    )

    parser.add_argument('-i', '--input', required=True, help='Input CSV file')
    parser.add_argument('-o', '--output', required=True, help='Output CSV file')
    parser.add_argument('--image',
                        help='Docker image name (overrides PACSIFIER_DOCKER_IMAGE env var)')

    args, unknown_args = parser.parse_known_args()

    if args.image:
        os.environ['PACSIFIER_DOCKER_IMAGE'] = args.image

    command_args = ['pacsifier-get-pseudonyms', '-i', '/input.csv', '-o', '/output.csv']
    command_args.extend(unknown_args)

    volumes = [
        f"{os.path.abspath(args.input)}:/input.csv",
        f"{os.path.abspath(os.path.dirname(args.output))}:/output"
    ]

    run_docker_command(command_args, additional_volumes=volumes)


def docker_add_karnak_tags():
    """Docker wrapper for the add_karnak_tags command."""
    parser = argparse.ArgumentParser(
        description="Run pacsifier-add-karnak-tags via Docker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  docker_add_karnak_tags -i input_dir -o output_dir
  docker_add_karnak_tags --input /path/to/input --output /path/to/output
        """
    )

    parser.add_argument('-i', '--input', required=True, help='Input directory')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    parser.add_argument('--image',
                        help='Docker image name (overrides PACSIFIER_DOCKER_IMAGE env var)')

    args, unknown_args = parser.parse_known_args()

    if args.image:
        os.environ['PACSIFIER_DOCKER_IMAGE'] = args.image

    command_args = ['pacsifier-add-karnak-tags', '-i', '/input', '-o', '/output']
    command_args.extend(unknown_args)

    volumes = [
        f"{os.path.abspath(args.input)}:/input",
        f"{os.path.abspath(args.output)}:/output"
    ]

    run_docker_command(command_args, additional_volumes=volumes)


def docker_anonymize_dicoms():
    """Docker wrapper for the anonymize_dicoms command."""
    parser = argparse.ArgumentParser(
        description="Run pacsifier-anonymize via Docker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  docker_anonymize_dicoms -i input_dir -o output_dir
  docker_anonymize_dicoms --input /path/to/input --output /path/to/output
        """
    )

    parser.add_argument('-i', '--input', required=True, help='Input directory')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    parser.add_argument('--image',
                        help='Docker image name (overrides PACSIFIER_DOCKER_IMAGE env var)')

    args, unknown_args = parser.parse_known_args()

    if args.image:
        os.environ['PACSIFIER_DOCKER_IMAGE'] = args.image

    command_args = ['pacsifier-anonymize', '-i', '/input', '-o', '/output']
    command_args.extend(unknown_args)

    volumes = [
        f"{os.path.abspath(args.input)}:/input",
        f"{os.path.abspath(args.output)}:/output"
    ]

    run_docker_command(command_args, additional_volumes=volumes)


def docker_extract_carestream_report():
    """Docker wrapper for the extract_carestream_report command."""
    parser = argparse.ArgumentParser(
        description="Run pacsifier-extract-carestream-report via Docker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  docker_extract_carestream_report -d data_folder
  docker_extract_carestream_report --data_folder /path/to/data
        """
    )

    parser.add_argument('-d', '--data_folder', required=True, help='Path to data folder')
    parser.add_argument('--image',
                        help='Docker image name (overrides PACSIFIER_DOCKER_IMAGE env var)')

    args, unknown_args = parser.parse_known_args()

    if args.image:
        os.environ['PACSIFIER_DOCKER_IMAGE'] = args.image

    command_args = ['pacsifier-extract-carestream-report', '-d', '/data']
    command_args.extend(unknown_args)

    volumes = [
        f"{os.path.abspath(args.data_folder)}:/data"
    ]

    run_docker_command(command_args, additional_volumes=volumes)


def docker_move_dumps():
    """Docker wrapper for the move_dumps command."""
    parser = argparse.ArgumentParser(
        description="Run pacsifier-move-csv via Docker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  docker_move_dumps -d dicom_path -o info_folder
  docker_move_dumps --data_folder /path/to/dicom --info_folder /path/to/info
        """
    )

    parser.add_argument('-d', '--data_folder', required=True, help='Path to dicom folder')
    parser.add_argument('-o', '--info_folder', required=True, help='Path to info folder')
    parser.add_argument('--image',
                        help='Docker image name (overrides PACSIFIER_DOCKER_IMAGE env var)')

    args, unknown_args = parser.parse_known_args()

    if args.image:
        os.environ['PACSIFIER_DOCKER_IMAGE'] = args.image

    command_args = ['pacsifier-move-csv', '-d', '/dicom', '-o', '/info']
    command_args.extend(unknown_args)

    volumes = [
        f"{os.path.abspath(args.data_folder)}:/dicom",
        f"{os.path.abspath(args.info_folder)}:/info"
    ]

    run_docker_command(command_args, additional_volumes=volumes)


def docker_create_dicomdir():
    """Docker wrapper for the create_dicomdir command."""
    parser = argparse.ArgumentParser(
        description="Run pacsifier-create-dicomdir via Docker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  docker_create_dicomdir -o output_path
  docker_create_dicomdir --output /path/to/output
        """
    )

    parser.add_argument('-o', '--output', required=True, help='Output path')
    parser.add_argument('--image',
                        help='Docker image name (overrides PACSIFIER_DOCKER_IMAGE env var)')

    args, unknown_args = parser.parse_known_args()

    if args.image:
        os.environ['PACSIFIER_DOCKER_IMAGE'] = args.image

    command_args = ['pacsifier-create-dicomdir', '-o', '/output']
    command_args.extend(unknown_args)

    volumes = [
        f"{os.path.abspath(os.path.dirname(args.output))}:/output"
    ]

    run_docker_command(command_args, additional_volumes=volumes)


if __name__ == "__main__":
    print("This module contains Docker wrapper functions for PACSIFIER CLI commands.")
    print("Use the individual wrapper scripts (docker_pacsman, docker_get_pseudonyms, etc.)")
    sys.exit(1)
