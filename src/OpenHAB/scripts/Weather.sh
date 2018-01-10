#!/bin/bash
curl -X "DELETE" http://localhost:5000/window/Site
sleep 1
curl -d '{"name" : "Weather", "type" : "Site"}' -H "Content-Type: application/json" -X POST http://localhost:5000/window
