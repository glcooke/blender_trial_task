import os
import sys
import shutil
from blenderTester import BlenderTester
from Scenario import Scenario

if __name__ == "__main__":
    # Get the Blender executable path, output path, and resolution from command line arguments.
    blender_path = sys.argv[1]
    output_path = sys.argv[2]

    # Ensure the output directory exists, if not, create it. If it exists, delete its contents.
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    else:
        shutil.rmtree(output_path)
        os.makedirs(output_path)

    # Get the X and Y resolution from command line arguments.
    x_resolution = int(sys.argv[3])
    y_resolution = int(sys.argv[4])

    # Define a list of test scenarios with names and identifiers.
    scenarios = [
        Scenario("Scenario 1 - Arbitrary Shapes without Material",
                 "test_arbitrary_shapes"),
        Scenario("Scenario 2 - Arbitrary Shapes with Material",
                 "test_materials"),
        Scenario("Scenario 3 - Light Sources",
                 "test_light_source")
    ]

    # Create an instance of the BlenderTester class.
    tester = BlenderTester(blender_path, output_path, x_resolution, y_resolution)

    # Run the tests for the defined scenarios using the BlenderTester.
    tester.run_tests(scenarios)

    print("Testing completed.")