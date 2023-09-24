import os
import shutil
from blenderTester import BlenderTester
from Scenario import Scenario

if __name__ == "__main__":
    blender_path = "C:/Program Files/Blender Foundation/Blender 3.3/blender.exe"
    output_path = "D:/test_results"
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    else:
        shutil.rmtree(output_path)
        os.makedirs(output_path)

    x_resolution = 1920
    y_resolution = 1080

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
