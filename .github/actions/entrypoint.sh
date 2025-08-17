#!/bin/sh

DOCS_DIR="$1"
BUILD_DIR="$2"
REQUIREMENTS="$3"
TARGET_BRANCH="gh-pages" # на случай, если кому-то в голову придёт поставить основную ветку.
BUILD_COMMAND="$5"
EXTRA_EXTENSIONS="$6"
COMMIT_MESSAGE="$7"

if [ -n "$EXTRA_EXTENSIONS" ]; then
    echo "Installing extra extensions: $EXTRA_EXTENSIONS"
    pip install $EXTRA_EXTENSIONS
fi

if [ -n "$REQUIREMENTS" ] && [ -f "$REQUIREMENTS" ]; then
    echo "Installing dependencies from $REQUIREMENTS"
    pip install -r "$REQUIREMENTS"
fi

cd "$GITHUB_WORKSPACE"

echo "Building documentation in $DOCS_DIR"
cd "$DOCS_DIR" || exit
# sphinx-apidoc -f -o ./backend ../../backend/api/models
eval "$BUILD_COMMAND"

git config --global user.name "GitHub Actions"
git config --global user.email "actions@github.com"

cd "$GITHUB_WORKSPACE"
TEMP_DIR=$(mktemp -d)

REPO_URL="https://x-access-token:$GITHUB_TOKEN@github.com/$GITHUB_REPOSITORY.git"
git clone "$REPO_URL" --branch "$TARGET_BRANCH" --single-branch "$TEMP_DIR" || \
  {
    git clone "$REPO_URL" "$TEMP_DIR"
    cd "$TEMP_DIR"
    git checkout --orphan "$TARGET_BRANCH"
    git rm -rf .
  }

cd "$TEMP_DIR"
git rm -r * || true
cp -r "$GITHUB_WORKSPACE/$BUILD_DIR/." .
touch .nojekyll

git add .
git commit -m "$COMMIT_MESSAGE"
git push -u -f origin "$TARGET_BRANCH"

rm -rf "$TEMP_DIR"

DEPLOY_URL="https://${GITHUB_REPOSITORY_OWNER}.github.io/${GITHUB_REPOSITORY#*/}"
echo "::set-output name=deploy-url::$DEPLOY_URL"
echo "Documentation deployed to: $DEPLOY_URL"
