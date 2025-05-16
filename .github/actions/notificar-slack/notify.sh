#!/bin/bash

SHORT_SHA=$(echo "$SHA" | cut -c1-7)
TIMESTAMP=$(date +"%d/%m/%Y %H:%M")
COMMIT_URL="https://github.com/${REPO}/commit/${SHA}"
REPO_URL="https://github.com/${REPO}"

curl -s -X POST -H 'Content-type: application/json' --data "{
  \"blocks\": [
    {
      \"type\": \"header\",
      \"text\": {
        \"type\": \"plain_text\",
        \"text\": \"🏗️ Build Realizado com Sucesso!\",
        \"emoji\": true
      }
    },
    {
      \"type\": \"section\",
      \"fields\": [
        { \"type\": \"mrkdwn\", \"text\": \"📱 *Aplicação:*\n${IMAGE_NAME}\" },
        { \"type\": \"mrkdwn\", \"text\": \"🏷️ *Versão:*\n\`${VERSION}\`\" },
        { \"type\": \"mrkdwn\", \"text\": \"🌱 *Branch:*\n\`${REF_NAME}\`\" },
        { \"type\": \"mrkdwn\", \"text\": \"📦 *Commit:*\n<${COMMIT_URL}|\`${SHORT_SHA}\`>\" },
        { \"type\": \"mrkdwn\", \"text\": \"👤 *Autor:*\n@${ACTOR}\" },
        { \"type\": \"mrkdwn\", \"text\": \"🕘 *Data e Hora:*\n${TIMESTAMP}\" }
      ]
    },
    {
      \"type\": \"context\",
      \"elements\": [
        { \"type\": \"mrkdwn\", \"text\": \"🔗 <${REPO_URL}|Ver repositório>\" }
      ]
    }
  ]
}" "$SLACK_WEBHOOK_URL"
