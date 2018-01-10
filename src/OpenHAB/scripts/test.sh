#!/bin/bash                                                                                                                                                                                     
curl -d '{"name" : "TEST", "type" : "GUT"}' -H "Content-Type: application/json" -X POST http://localhost:5000/animal
