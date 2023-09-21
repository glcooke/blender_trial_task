import subprocess
import os
import json
from functools import wraps
from scenarios import BlenderTest
import bpy


def test_func(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        scenario = args[0]
        scenario.start_test()
        result = func(*args, **kwargs)
        scenario.end_test()
        return result
    return timeit_wrapper


class BlenderTester:
    def __init__(self, blender_path_, output_path_, x_resolution_, y_resolution_):
        self.blender_path = blender_path_
        self.output_path = output_path_
        self.x_resolution = x_resolution_
        self.y_resolution = y_resolution_

    @test_func
    def run_scenario(self, scenario):
        cmd = [
            self.blender_path,
            "-b", scenario["blend_file"],
            "-o", os.path.join(self.output_path, scenario["output_image"]),
            "-f", "1",
            "-x", str(self.x_resolution),
            "-y", str(self.y_resolution),
            "--render-output", os.path.join(self.output_path, "frame_"),
        ]

        with open(os.path.join(self.output_path, scenario["output_log"]), "w") as log_file:
            subprocess.run(cmd, stdout=log_file, stderr=log_file)

    def run_tests(self, scenarios_):
        for scenario in scenarios_:
            self.run_scenario(scenario)
            # Save test info as JSON
            with open(os.path.join(self.output_path, f"{scenario['name']}_info.json"), "w") as json_file:
                json.dump(scenario.get_json(), json_file, indent=4)

    def test_shapes_and_materials(self):
        # Clear existing data
        bpy.ops.wm.read_factory_settings(use_empty=True)

        # Create a new scene
        bpy.ops.scene.new(type='NEW')

        # Create a cube
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0))
        cube = bpy.context.object

        # Create a material
        material = bpy.data.materials.new(name="CubeMaterial")
        material.diffuse_color = (0.8, 0.1, 0.1, 1)
        cube.data.materials.append(material)

        # Set up lighting (you can customize this as needed)
        bpy.ops.object.light_add(type='SUN', align='WORLD', location=(0, 0, 10))
        self.render_scene()

    # Function to render the scene
    def render_scene(self):
        bpy.context.scene.render.image_settings.file_format = 'PNG'
        bpy.context.scene.render.filepath = self.output_path
        bpy.context.scene.render.resolution_x = self.x_resolution
        bpy.context.scene.render.resolution_y = self.y_resolution

        bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    blender_path = "path/to/blender.exe"
    output_path = "test_results"
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    x_resolution = 1920
    y_resolution = 1080

    scenarios = [
        BlenderTest("Scenario 1 - Arbitrary Shapes without Material",
                    "scenario1.blend",
                    "scenario1.png",
                    "scenario1_log.txt"
                    ),
        BlenderTest("Scenario 1 - Arbitrary Shapes with Material",
                    "scenario2.blend",
                    "scenario2.png",
                    "scenario2_log.txt"
                    )
    ]

    tester = BlenderTester(blender_path, output_path, x_resolution, y_resolution)
    tester.run_tests(scenarios)

    print("Testing completed.")
