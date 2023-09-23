import bpy
import os
import mathutils
import json
from functools import wraps


def test_func(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        scenario = args[1]
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

    def run_tests(self, scenarios_):
        for scenario in scenarios_:
            fn = getattr(self, scenario.get_func())
            if fn is not None:
                fn(scenario)
            with open(os.path.join(self.output_path, f"{scenario.get_name()}_info.json"), "w") as json_file:
                json.dump(scenario.get_json(), json_file, indent=4)

    # Functions to create shapes

    @test_func
    def test_arbitrary_shapes(self, scenario):
        collection = bpy.context.collection
        scene = bpy.context.scene
        # Create the cube
        mesh = bpy.data.meshes.new('cube')
        ob = bpy.data.objects.new('cube', mesh)

        collection.objects.link(ob)

        import bmesh
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        bm.to_mesh(mesh)
        bm.free()

        light_data = bpy.data.lights.new('light', type='POINT')
        light = bpy.data.objects.new('light', light_data)
        collection.objects.link(light)
        light.location = mathutils.Vector((3, -4.2, 5))

        cam_data = bpy.data.cameras.new('camera')
        cam = bpy.data.objects.new('camera', cam_data)
        collection.objects.link(cam)
        scene.camera = cam

        cam.location = mathutils.Vector((6, -4, 5))
        cam.rotation_euler = mathutils.Euler((0.9, 0.0, 1.1))

        scene.render.image_settings.file_format = 'PNG'
        scene.render.filepath = f"D:/test_results/{scenario.get_name()}"
        bpy.ops.render.render(write_still=1)

    @test_func
    def test_shapes_and_materials(self, scenario):
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
