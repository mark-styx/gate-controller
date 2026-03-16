#!/bin/bash

#######################################################################
# Example Alert Script for Gate Controller Monitor
#
# This script is called by monitor.py when issues are detected.
# Customize this to send alerts via your preferred method.
#
# Usage: ./alert.sh <level> <message>
#   level: INFO, WARNING, CRITICAL
#   message: Alert message
#
# Setup:
#   1. Make executable: chmod +x alert.sh
#   2. Configure your notification method below
#   3. Run monitor with: python3 monitor.py --alert-script ./alert.sh
#######################################################################

LEVEL=$1
MESSAGE=$2
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Log to file
LOG_FILE=~/logs/alerts.log
echo "[$TIMESTAMP] [$LEVEL] $MESSAGE" >> "$LOG_FILE"

# Choose your alert method (uncomment/modify as needed)

#-----------------------------------------------------------------------
# Option 1: Email (requires mailutils: sudo apt-get install mailutils)
#-----------------------------------------------------------------------
# echo "$MESSAGE" | mail -s "Gate Alert [$LEVEL]" your-email@example.com

#-----------------------------------------------------------------------
# Option 2: Pushover (push notifications to phone)
# Sign up at: https://pushover.net
#-----------------------------------------------------------------------
# PUSHOVER_TOKEN="your-app-token"
# PUSHOVER_USER="your-user-key"
# 
# curl -s \
#   --form-string token="$PUSHOVER_TOKEN" \
#   --form-string user="$PUSHOVER_USER" \
#   --form-string title="Gate Controller [$LEVEL]" \
#   --form-string message="$MESSAGE" \
#   --form-string priority="$([ "$LEVEL" = "CRITICAL" ] && echo "1" || echo "0")" \
#   https://api.pushover.net/1/messages.json

#-----------------------------------------------------------------------
# Option 3: Slack Webhook
# Create webhook: https://api.slack.com/messaging/webhooks
#-----------------------------------------------------------------------
# SLACK_WEBHOOK="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
#
# COLOR=$([ "$LEVEL" = "CRITICAL" ] && echo "danger" || echo "warning")
#
# curl -s -X POST \
#   -H 'Content-type: application/json' \
#   --data "{
#     \"attachments\": [{
#       \"color\": \"$COLOR\",
#       \"title\": \"Gate Controller Alert\",
#       \"text\": \"$MESSAGE\",
#       \"fields\": [
#         {\"title\": \"Level\", \"value\": \"$LEVEL\", \"short\": true},
#         {\"title\": \"Time\", \"value\": \"$TIMESTAMP\", \"short\": true}
#       ]
#     }]
#   }" \
#   "$SLACK_WEBHOOK"

#-----------------------------------------------------------------------
# Option 4: Discord Webhook
# Create webhook in Discord channel settings
#-----------------------------------------------------------------------
# DISCORD_WEBHOOK="https://discord.com/api/webhooks/YOUR/WEBHOOK"
#
# curl -s -X POST \
#   -H 'Content-type: application/json' \
#   --data "{
#     \"embeds\": [{
#       \"title\": \"Gate Controller Alert\",
#       \"description\": \"$MESSAGE\",
#       \"color\": \"$([ "$LEVEL" = "CRITICAL" ] && echo "15158332" || echo "15844367")\",
#       \"fields\": [
#         {\"name\": \"Level\", \"value\": \"$LEVEL\"},
#         {\"name\": \"Time\", \"value\": \"$TIMESTAMP\"}
#       ]
#     }]
#   }" \
#   "$DISCORD_WEBHOOK"

#-----------------------------------------------------------------------
# Option 5: Telegram Bot
# Create bot: https://core.telegram.org/bots#creating-a-new-bot
#-----------------------------------------------------------------------
# TELEGRAM_TOKEN="your-bot-token"
# TELEGRAM_CHAT_ID="your-chat-id"
#
# curl -s -X POST \
#   "https://api.telegram.org/bot$TELEGRAM_TOKEN/sendMessage" \
#   -d chat_id="$TELEGRAM_CHAT_ID" \
#   -d text="*$LEVEL*: $MESSAGE" \
#   -d parse_mode="Markdown"

#-----------------------------------------------------------------------
# Option 6: SMS via Twilio
# Sign up at: https://www.twilio.com
#-----------------------------------------------------------------------
# TWILIO_SID="your-account-sid"
# TWILIO_TOKEN="your-auth-token"
# TWILIO_FROM="+1234567890"
# TWILIO_TO="+0987654321"
#
# curl -s -X POST \
#   "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_SID/Messages.json" \
#   -u "$TWILIO_SID:$TWILIO_TOKEN" \
#   -d From="$TWILIO_FROM" \
#   -d To="$TWILIO_TO" \
#   -d Body="[$LEVEL] $MESSAGE"

#-----------------------------------------------------------------------
# Option 7: Local LED indicator (if you have an LED on GPIO)
#-----------------------------------------------------------------------
# LED_PIN=18  # BCM pin number
#
# if [ "$LEVEL" = "CRITICAL" ]; then
#     # Blink LED rapidly
#     for i in {1..10}; do
#         echo 1 > /sys/class/gpio/gpio$LED_PIN/value
#         sleep 0.1
#         echo 0 > /sys/class/gpio/gpio$LED_PIN/value
#         sleep 0.1
#     done
# fi

#-----------------------------------------------------------------------
# Option 8: Simple HTTP webhook (IFTTT, Zapier, custom server, etc.)
#-----------------------------------------------------------------------
# WEBHOOK_URL="https://maker.ifttt.com/trigger/gate_alert/with/key/your-key"
#
# curl -s -X POST \
#   -H 'Content-type: application/json' \
#   --data "{\"value1\":\"$LEVEL\",\"value2\":\"$MESSAGE\"}" \
#   "$WEBHOOK_URL"

#-----------------------------------------------------------------------
# Option 9: Desktop notification (if running with GUI)
#-----------------------------------------------------------------------
# if [ "$LEVEL" = "CRITICAL" ]; then
#     notify-send -u critical "Gate Controller" "$MESSAGE"
# else
#     notify-send "Gate Controller" "$MESSAGE"
# fi

#-----------------------------------------------------------------------
# Option 10: Log to systemd journal
#-----------------------------------------------------------------------
# logger -t gate-controller "[$LEVEL] $MESSAGE"

#-----------------------------------------------------------------------
# Default: Print to console and log
#-----------------------------------------------------------------------
echo "[$TIMESTAMP] [$LEVEL] $MESSAGE"

# Print suggestion based on level
case $LEVEL in
    CRITICAL)
        echo "⚠️  CRITICAL: Check system immediately!"
        echo "   Run: ./gate.sh status"
        echo "   Logs: ./gate.sh logs"
        ;;
    WARNING)
        echo "⚠️  Warning: Monitor the situation"
        ;;
    INFO)
        echo "ℹ️  Informational"
        ;;
esac
