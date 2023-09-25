# Blender Task

This is a project that tests Blender operation using bpy and Jenkins.

## Description

The script runs 3 simple Blender renders, randomly choosing primitive shapes, materials and light sources to render
As an output, it creates folders for each scenario, each of them containing render log, rendered image and JSON dump with scenario information.
The project contains python version necessary for bpy and jenkins pipeline source code, as well as requirements file to run.

### Prerequisites

* Python 3.10
* bpy
* psutil
