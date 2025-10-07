#!/usr/bin/env bash

set -e

# Flags
JSON_MODE=false
FORCE_SEED=false

# Parse command line arguments
for arg in "$@"; do
    case "$arg" in
        --json)
            JSON_MODE=true
            ;;
        --force-seed)
            # Explicitly overwrite IMPL_PLAN from template (use with care)
            FORCE_SEED=true
            ;;
        --help|-h)
            echo "Usage: $0 [--json] [--force-seed]"
            echo "  --json         Output results in JSON format"
            echo "  --force-seed   Overwrite plan.md from template (dangerous; normally not needed)"
            echo "  --help         Show this help message"
            exit 0
            ;;
        *)
            # ignore unknown args to be forward-compatible
            ;;
    esac
done

# Get script directory and load common functions
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# Get all paths and variables from common functions
eval $(get_feature_paths)

# Check if we're on a proper feature branch (only for git repos)
check_feature_branch "$CURRENT_BRANCH" "$HAS_GIT" || exit 1

# Ensure the feature directory exists
mkdir -p "$FEATURE_DIR"

# Seed plan from template ONLY if it does not exist, unless --force-seed
TEMPLATE="$REPO_ROOT/.specify/templates/plan-template.md"
if [[ -f "$TEMPLATE" ]]; then
    if [[ "$FORCE_SEED" == "true" ]]; then
        cp "$TEMPLATE" "$IMPL_PLAN"
        echo "Seeded plan from template (forced) → $IMPL_PLAN"
    elif [[ ! -f "$IMPL_PLAN" || ! -s "$IMPL_PLAN" ]]; then
        cp "$TEMPLATE" "$IMPL_PLAN"
        echo "Seeded new plan from template → $IMPL_PLAN"
    else
        # Non-destructive: do not overwrite existing plan
        # echo kept quiet on purpose to avoid noisy logs
        :
    fi
else
    # If template missing and plan absent, create an empty file so downstream steps have a path
    if [[ ! -f "$IMPL_PLAN" ]]; then
        touch "$IMPL_PLAN"
    fi
fi

# Output results
if $JSON_MODE; then
    printf '{"FEATURE_SPEC":"%s","IMPL_PLAN":"%s","SPECS_DIR":"%s","BRANCH":"%s","HAS_GIT":"%s"}\n' \
        "$FEATURE_SPEC" "$IMPL_PLAN" "$FEATURE_DIR" "$CURRENT_BRANCH" "$HAS_GIT"
else
    echo "FEATURE_SPEC: $FEATURE_SPEC"
    echo "IMPL_PLAN: $IMPL_PLAN"
    echo "SPECS_DIR: $FEATURE_DIR"
    echo "BRANCH: $CURRENT_BRANCH"
    echo "HAS_GIT: $HAS_GIT"
fi
