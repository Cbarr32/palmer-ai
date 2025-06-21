#!/bin/bash
# Palmer AI Runner Management Script

case "$1" in
  start)
    echo "Starting Palmer AI runner..."
    cd ~/actions-runner
    ./svc.sh start
    echo "✅ Runner started"
    ;;
  stop)
    echo "Stopping Palmer AI runner..."
    cd ~/actions-runner
    ./svc.sh stop
    echo "✅ Runner stopped"
    ;;
  status)
    echo "Checking Palmer AI runner status..."
    cd ~/actions-runner
    ./svc.sh status
    ;;
  logs)
    echo "Showing runner logs..."
    cd ~/actions-runner
    tail -f _diag/*.log
    ;;
  *)
    echo "Usage: $0 {start|stop|status|logs}"
    exit 1
    ;;
esac
