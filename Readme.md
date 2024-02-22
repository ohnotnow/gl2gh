# GitLab CI to GitHub Actions Converter

This Python script provides an easy and automated way to convert GitLab CI/CD scripts into GitHub Actions workflows using OpenAI's APIs.

## Purpose

The script is designed to assist developers in transitioning their CI/CD pipelines from GitLab to GitHub, making the process seamless and less time-consuming. It offers options for both quick and thorough conversions, catering to different needs and preferences.

## Installation

### Prerequisites

- Python 3.x
- pip (Python package manager)

### Steps

1. Clone the repository to your local machine.
2. Navigate to the directory containing the script.
3. Install the required Python packages:

   ```
   pip install -r requirements.txt
   ```

## Usage

To run the script, use the following command:

```
python main.py [options]
```

### Options

- `--file`: Specify the GitLab CI file to convert (default: `.gitlab-ci.yml`).
- `--show-usage`: Display the cost/token usage of the API calls.
- `--thorough`: Opt for an extra-thorough conversion process.
- `--quick`: Opt for a quicker/cheaper conversion process.

### Example

```
python main.py --file your-gitlab-ci-file.yml --thorough
```

This command will convert `your-gitlab-ci-file.yml` from GitLab CI format to GitHub Actions using a thorough conversion process.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
