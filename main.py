import os
import sys
import shutil
from blenderTester import BlenderTester
from Scenario import Scenario

if __name__ == "__main__":
    blender_path = sys.argv[1]
    output_path = sys.argv[2]
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    else:
        shutil.rmtree(output_path)
        os.makedirs(output_path)

    x_resolution = int(sys.argv[3])
    y_resolution = int(sys.argv[4])

    scenarios = [
        Scenario("Scenario 1 - Arbitrary Shapes without Material",
                 "test_arbitrary_shapes",
                 ),
        Scenario("Scenario 2 - Arbitrary Shapes with Material",
                 "test_materials",
                 ),
        Scenario("Scenario 3 - Light Sources",
                 "test_light_source",
                 )
    ]

    tester = BlenderTester(blender_path, output_path, x_resolution, y_resolution)
    tester.run_tests(scenarios)

    print("Testing completed.")
