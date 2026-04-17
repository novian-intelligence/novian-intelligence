#!/bin/bash

# Novian Bridge: Collaborative Browser Script
# Leverages macOS AppleScript to interact with the active Chrome tab.

COMMAND=$1
shift

case $COMMAND in
  "info")
    osascript -e 'tell application "Google Chrome"
      set theUrl to URL of active tab of window 1
      set theTitle to title of active tab of window 1
      return theUrl & " | " & theTitle
    end tell'
    ;;
  "html")
    # This requires "Allow JavaScript from Apple Events" to be enabled in Chrome
    osascript -e 'tell application "Google Chrome" to execute active tab of window 1 javascript "document.documentElement.outerHTML"'
    ;;
  "js")
    # This requires "Allow JavaScript from Apple Events" to be enabled in Chrome
    JS_CODE="$*"
    osascript -e "tell application \"Google Chrome\" to execute active tab of window 1 javascript \"$JS_CODE\""
    ;;
  "open")
    # Opens a URL in the existing Chrome instance
    URL="$1"
    if [ -z "$URL" ]; then
      echo "Error: URL required for 'open' command."
      exit 1
    fi
    open -a "Google Chrome" "$URL"
    ;;
  "focus")
    # Brings Chrome to the front
    osascript -e 'tell application "Google Chrome" to activate'
    ;;
  "screenshot")
    # Captures the Chrome window specifically
    # Bring to front first
    osascript -e 'tell application "Google Chrome" to activate'
    sleep 0.5
    
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    OUTPUT="${1:-/Users/mira/Documents/Novian_Intelligence/bridge_screenshot_$TIMESTAMP.png}"
    
    # Try capturing the whole screen for now as it is more reliable in the VM
    screencapture -x "$OUTPUT"
    echo "Screenshot saved to: $OUTPUT"
    ;;
  *)
    echo "Usage: $0 {info|html|js <script>|open <url>|focus|screenshot [path]}"
    exit 1
    ;;
esac

