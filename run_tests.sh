#!/bin/bash

# Define a list of parameters
parameters=(
  "-lf -r 1080 720 -p gosper_glider_gun"
  "-lf -r 1080 720 -nogui -p gosper_glider_gun"
  "-ls -r 1080 720 -nogui -p gosper_glider_gun"
  "-lg -r 1080 720 -p gosper_glider_gun"
  "-lg -r 1080 720 -nogui -p gosper_glider_gun"

  "-lf -r 1080 720 -p penta_decathlon"
  "-lf -r 1080 720 -nogui -p penta_decathlon"
  "-ls -r 1080 720 -nogui -p penta_decathlon"
  "-lg -r 1080 720 -p penta_decathlon"
  "-lg -r 1080 720 -nogui -p penta_decathlon"
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