#!/bin/zsh

# This script will be used to get multiple public GitHub repositories and run SonarQube analysis on them.
# The SonarQube instance is available locally, and running on port 9000 within a Docker container.
# The script will be run from the command line, and will take in a list of GitHub repositories as arguments, as well
# as the SonarQube token to use for the analysis.

# The script will then run the SonarQube analysis on each repository, and output the results to a file.

show_usage() {
  echo "Usage: $0"
  echo "CLI Options:"
  echo "  --sonar-token=SONAR_TOKEN                The SonarQube token to use for the analysis."
  echo "  --sonar-url=SONAR_URL                    The SonarQube URL to use for the analysis. (Token is required to be for this SonarQube instance)"
  echo "  --github-repos-file=GITHUB_REPOS_FILE    The file containing the list of GitHub repositories to analyze."
  echo "  --workdir=WORKDIR                        The directory to clone and run the analysis in."
  echo "  --skip-clone                             Skip cloning the repository."
  echo "  -h, --help                               Show this help message and exit."
}

validate_url() {
  local url=$1

  # Check if the URL is valid
  if ! curl --output /dev/null --silent --head --fail "$url"; then
    echo "ERROR: The URL is not valid."
    exit 1
  fi
}


SONAR_TOKEN=""
SONAR_URL=""
WORKDIR="."
GITHUB_REPOS_FILE=""
GITHUB_REPOS=()
SKIP_CLONE=false

while [ $# -ge 1 ]; do
    case "$1" in
        --sonar-token=*)
            SONAR_TOKEN="${1#*=}"
            shift
            ;;
        --sonar-url=*)
            SONAR_URL="${1#*=}"
            shift
            ;;
        --github-repos-file=*)
            GITHUB_REPOS_FILE="${1#*=}"
            shift
            ;;
        --workdir=*)
            WORKDIR="${1#*=}"
            shift
            ;;
        --skip-clone)
            SKIP_CLONE=true
            shift
            ;;
        -h | --help)
            show_usage
            exit 0
            ;;
        *)
            echo "ERROR: Unknown argument: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Check required arguments are set
if [ -z "$SONAR_TOKEN" ]; then
    echo "ERROR: --sonar-token must be set."
    show_usage
    exit 1
fi

if [ -z "$SONAR_URL" ]; then
    echo "ERROR: --sonar-url must be set."
    show_usage
    exit 1
fi

if [ -z "$GITHUB_REPOS_FILE" ]; then
    echo "ERROR: --github-repos-file must be set."
    show_usage
    exit 1
fi

if [ -z "$WORKDIR" ]; then
    echo "ERROR: --workdir must be set."
    show_usage
    exit 1
fi

# Validate the URL
validate_url "$SONAR_URL"

# Check that workdir is a directory
# If it is not, create the directory in the current working directory
if [ ! -d "$WORKDIR" ]; then
    echo "WARNING: --workdir is not an existing directory."
    echo "WARNING: Creating the directory clone_repos in the current working directory."
    WORKDIR="$PWD"/clone_repos

    # If the directory clone_repos exists in the current working directory, delete it and recreate it
    if [ -d "$WORKDIR" ]; then
        echo "WARNING: The directory clone_repos already exists in the current working directory."
        echo "WARNING: Deleting the directory clone_repos and recreating it."
        rm -rf "$WORKDIR"
    fi

    mkdir "$WORKDIR"
fi

# Parse each repository name from the input json file and store them in an array
# This action will be done with JQ command line tool
if [ -n "$GITHUB_REPOS_FILE" ]; then
    GITHUB_REPOS=($(jq -r '.[]' $GITHUB_REPOS_FILE))
fi

# Check that the JQ command was successful
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to parse the GitHub repositories from the input file."
    exit 1
fi

## Check for skipping the cloning step
if [ "$SKIP_CLONE" = true ]; then
    echo "INFO: Skipping cloning of the repositories."
else
    echo "INFO: Cloning the repositories..."
    for REPO_URL in $GITHUB_REPOS; do
      REPO_NAME=$(echo "$REPO_URL" | awk -F/ '{print $NF}' | sed 's/.git//')
      echo "Cloning repository $REPO_NAME into $WORKDIR"

      # Check if the repository that we are cloning has main or master branch
      if [ "$(git ls-remote --heads "$REPO_URL" main | wc -l)" -eq 1 ]; then
        echo "Cloning repository $REPO_URL into $WORKDIR/$REPO_NAME"
        git clone "$REPO_URL" "$WORKDIR"/"$REPO_NAME" --branch main --single-branch
      else
        echo "Cloning repository $REPO_URL into $WORKDIR/$REPO_NAME"
        git clone "$REPO_URL" "$WORKDIR"/"$REPO_NAME" --branch master --single-branch
      fi

      echo "Cloning is done successful!"

      # Create the binaries for each repository before running the analysis
      cd "$WORKDIR"/"$REPO_NAME" || exit 1

      echo "INFO: Creating the binaries for the repository $REPO_NAME"

      mvn clean package -DskipTests > /dev/null 2>&1

      if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create the binaries for the repository $REPO_NAME"
        exit 1
      fi

      echo "INFO: Successfully created the binaries for the repository $REPO_NAME"

      cd - || exit 1

      # Find all the projects that contain the subdirectory "target/classes" and create there a sonar-project.properties file.
      # Set the project as value to the sonar binaries
      for PACKAGE in $(find "$WORKDIR/$REPO_NAME" -type d -name "classes"); do
          # Remove the first directory from the path
          PACKAGE=$(echo "$PACKAGE" | cut -d'/' -f2-)
          echo "Found the package $PACKAGE"

          # Get the second directory from the PACKAGE path
          CURRENT_DIR=$(echo "$PACKAGE" | cut -d'/' -f2)
          echo "Found directory is $CURRENT_DIR"

          # Create the sonar-project.properties file in the repository that we cloned
          # Check if a file named sonar-project.properties already exists at the root of the repository that we cloned
          if [ -f "$REPO_NAME/$CURRENT_DIR/sonar-project.properties" ]; then
              echo "WARNING: A sonar-project.properties file already exists in the repository $REPO_NAME/$CURRENT_DIR"
              echo "WARNING: Deleting the sonar-project.properties file and recreating it"
              rm -rf "$REPO_NAME/$CURRENT_DIR/sonar-project.properties"
          fi

          SONAR_PROPERTIES_FILE=$REPO_NAME/$CURRENT_DIR/sonar-project.properties
          touch "$SONAR_PROPERTIES_FILE"

          # Configure SonarQube server URL and authentication token
          echo "sonar.host.url=$SONAR_URL" >> "$SONAR_PROPERTIES_FILE"
          echo "sonar.token=$SONAR_TOKEN" >> "$SONAR_PROPERTIES_FILE"

          echo "$PACKAGE"
          echo "sonar.java.binaries=target/classes" >> "$SONAR_PROPERTIES_FILE"

          # Run the SonarQube analysis
          sonar-scanner \
            -Dsonar.projectKey="$CURRENT_DIR" \
            -Dsonar.projectName="$REPO_NAME/$CURRENT_DIR" \
            -Dsonar.projectVersion=1.0 \
            -Dsonar.sources=. \
            -Dsonar.host.url="$SONAR_URL" \
            -Dsonar.token="$SONAR_TOKEN" \
            -Dsonar.projectBaseDir="$WORKDIR"/"$REPO_NAME"/$CURRENT_DIR
      done

    done
    exit 0

    # Retrieve all the active project-keys and find Java classes that contain Code Smells per project with the given key
    API_URL="${SONAR_URL}/api/components/search"
    API_PARAMS="qualifiers=TRK&metrics=code_smells&ps=500"

    echo "INFO: The API URL is $API_URL"
    echo "INFO: The API parameters are $API_PARAMS"
    echo "INFO: Sending the API request to SonarQube server to retrieve the project-keys..."

    # Send a GET request to the SonarQube Web API to retrieve the project-keys and store the result in an array
    PROJECT_KEYS=("${(@f)$(curl -s -u "$SONAR_TOKEN": "$API_URL?$API_PARAMS" | jq -r '.components[].key')}")

    # Check that the JQ command was successful
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to parse the project-keys from the API response."
        exit 1
    fi

    echo "INFO: Successfully retrieved the project-keys from the API response."

    # If the 'csv_files' folder does not exist, create a folder for the csv files
    if [ ! -d "csv_files" ]; then
        mkdir csv_files
    fi

    # Store the project-keys in a file
    echo "$PROJECT_KEYS" > csv_files/project-keys.txt
    CSV_FILE="csv_files/all_classes_and_rules.csv"

    echo "Class,RuleId,RuleName,Severity,Line" > "${CSV_FILE}"

    # For each project key, extract the list of Java classes with technical debt
    for PROJECT_KEY in "${PROJECT_KEYS[@]}"; do
        # Send a GET request to the SonarQube Web API to retrieve the analysis report that contains classes with Code Smells
        # Use pagination and iterate through all the pages until the last page is reached
        PAGE_SIZE=500
        PAGE_NUMBER=1
        HAS_PAGES=True

        # Set Browse permission for the project
        curl -X POST "${SONAR_URL}/api/permissions/add_user" \
          -H "Content-Type: application/x-www-form-urlencoded" \
          -d "login=admin" \
          -d "permission=browse" \
          -d "projectKey=${PROJECT_KEY}"

        # Extract the metrics information per project and add the data to the already existing metrics.json file
        METRICS_DATA=$(curl -s -H "Authorization: Bearer ${SONAR_TOKEN}" "${SONAR_URL}/api/measures/component?component=${PROJECT_KEY}&metricKeys=code_smells,bugs,vulnerabilities,complexity,duplicated_lines_density,critical_violations,development_cost,classes,lines,statements"| jq -r)

        # save the METRICS_DATA in a .json file
        echo "INFO: Writing the metrics data in a .json file"
        echo ${METRICS_DATA} > csv_files/${PROJECT_KEY}_metrics.json

        CSV_FILE_PER_PROJECT="csv_files/${PROJECT_KEY}_classes_and_rules.csv"

        echo "Class,RuleId,RuleName,Severity,Line" > "${CSV_FILE_PER_PROJECT}"


        while [ "$HAS_PAGES" = "True" ]; do
          URL="${SONAR_URL}/api/issues/search"
          PARAMS="componentKeys=${PROJECT_KEY}&status=OPEN&ps=${PAGE_SIZE}&p=${PAGE_NUMBER}&types=CODE_SMELL"

          echo "INFO: Extracting the list of Java classes with technical debt for project key: ${PROJECT_KEY} on page ${PAGE_NUMBER}"

          # Send the API request and extract the list of Java classes with technical debt and the rule that was violated
          CLASSES_AND_RULES_AND_LINE_AND_MESSAGE=$(curl -s -H "Authorization: Bearer ${SONAR_TOKEN}" -H "Content-Type: application/json" "${URL}?${PARAMS}" | jq -r '.issues[] | {component, rule, line}')

          # Check if the response is empty or has failed
          if [ -z "$CLASSES_AND_RULES_AND_LINE_AND_MESSAGE" ]; then
              echo "ERROR: The response is empty or has failed"
              HAS_PAGES=False
              break
          fi

          # Extract classes and rules into separate variables
          CLASSES=("${(@f)$(echo "${CLASSES_AND_RULES_AND_LINE_AND_MESSAGE}" | jq -r '.component')}")
          RULES=("${(@f)$(echo "${CLASSES_AND_RULES_AND_LINE_AND_MESSAGE}" | jq -r '.rule')}")
          # MESSAGES=("${(@f)$(echo "${CLASSES_AND_RULES_AND_LINE_AND_MESSAGE}" | jq -r '.message')}")

          lines=()
          # Loop through each JSON object and extract the "line" field
          while IFS= read -r line; do
            # Add the line number to the array
            lines+=($line)
          done < <(echo "${CLASSES_AND_RULES_AND_LINE_AND_MESSAGE}" | jq -r '.line')


          # Loop through each class and rule, retrieve rule message, and add to CSV file
          for (( i=1; i<=${#CLASSES[@]}; i++ )); do
              RULE=$(echo "${RULES[i]}" | cut -d':' -f2)
              # MESSAGE=$(echo "${MESSAGES[i]}" | cut -d':' -f2)

              #RULE_MESSAGE=("${(@f)$(curl -s -H "Authorization: Bearer ${SONAR_TOKEN}" -H "Content-Type: application/json" "${SONAR_URL}/api/rules/show?key=java:${RULE}" | jq -r '.rule.name')}")
              SEVERITY=("${(@f)$(curl -s -H "Authorization: Bearer ${SONAR_TOKEN}" -H "Content-Type: application/json" "${SONAR_URL}/api/rules/show?key=java:${RULE}" | jq -r '.rule.severity')}")

              echo "\"${CLASSES[i]}\",${RULE},${SEVERITY},${lines[i]}" >> ${CSV_FILE}
              echo "\"${CLASSES[i]}\",${RULE},${SEVERITY},${lines[i]}" >> ${CSV_FILE_PER_PROJECT}
          done

          # Increment the page number
          PAGE_NUMBER=$((PAGE_NUMBER + 1))

        done
    done

fi

exit 0


