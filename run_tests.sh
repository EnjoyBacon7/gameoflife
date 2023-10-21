#!/bin/bash

# Define a list of parameters
parameters=(
  "-lf -r 1080 720"
  "-lf -r 1080 720 -nogui"
  "-ls -r 1080 720 -nogui"
  "-lg -r 1080 720"
  "-lg -r 1080 720 -nogui"
  "-lf -r 1920 1080"
  "-lf -r 1920 1080 -nogui"
  "-ls -r 1920 1080 -nogui"
  "-lg -r 1920 1080"
  "-lg -r 1920 1080 -nogui"
)

# Loop over the parameters and run the Python script for each
for param in "${parameters[@]}"; do
  python3 main.py $param

  # Check the exit status of the Python script
  if [ $? -eq 0 ]; then
    echo "Finished : $param"
  else
    echo "Python script encountered an error"
  fi
done