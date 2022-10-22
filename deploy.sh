#!/bin/bash
set -eux

get_param() {
  local -r name="$1"
  aws ssm get-parameter \
    --name "${name}" \
    --with-decryption \
    --output text \
    --query 'Parameter.Value'
}


channel_access_token=$(get_param '/snupy-bot/prod/channel_access_token')
channel_secret=$(get_param '/snupy-bot/prod/channel_secret')
env_var=$(cat <<EOF
{
  "environment_variables": {
    "CHANNEL_ACCESS_TOKEN": "${channel_access_token}",
    "CHANNEL_SECRET": "${channel_secret}"
  }
}
EOF
)
cp .chalice/config.json{,.bak}
cat .chalice/config.json.bak |
  jq '.stages.prod += '"${env_var}" > .chalice/config.json
chalice deploy --stage prod
mv .chalice/config.json{.bak,}
