import bpy
import os
import sys
import json
import random
import math
from functools import wraps


# Wrapper
def test_func(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        result = None
        scenario = args[1]
        scenario.start_test()

        try:
            result = func(*args, **kwargs)
        except:
            scenario.end_test()
            scenario.set_status("FAIL")
            print(f'Test case {scenario.get_name()} FAIL')
        else:
            scenario.end_test()
            scenario.set_status("OK")
            print(f'Test case {scenario.get_name()} OK')

        return result

    return timeit_wrapper


def cleanup():
    bpy.ops.wm.read_factory_settings()
    if "Cube" in bpy.data.objects:
        bpy.data.objects["Cube"].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects["Cube"]

    bpy.ops.object.delete()


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
                cleanup()
                os.makedirs(self.output_path + '/' + scenario.get_name())
                fn(scenario)

            with open(os.path.join(self.output_path + '/' + scenario.get_name(), f"test_info.json"), "w") as json_file:
                json.dump(scenario.get_json(), json_file, indent=4)

    # Functions to create shapes
    @test_func
    def test_arbitrary_shapes(self, scenario):
        cleanup()

        verts = 12
        angle_step = math.tau / verts

        for i in range(verts):
            cur_angle = i * angle_step

            x = math.cos(cur_angle)
            y = math.sin(cur_angle)

            random_number = random.randint(1, 4)
            match random_number:
                case 1:
                    bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, 0), radius=0.15)
                case 2:
                    bpy.ops.mesh.primitive_cylinder_add(location=(x, y, 0), radius=0.15, depth=0.2)
                case 3:
                    bpy.ops.mesh.primitive_cube_add(location=(x, y, 0), size=0.2)
                case 4:
                    bpy.ops.mesh.primitive_monkey_add(location=(x, y, 0), size=0.3)

        self.render_scene(scenario)

    @test_func
    def test_materials(self, scenario):
        cleanup()
        verts = 12
        angle_step = math.tau / verts

        for i in range(verts):
            cur_angle = i * angle_step

            x = math.cos(cur_angle)
            y = math.sin(cur_angle)

            random_number = random.randint(1, 4)
            match random_number:
                case 1:
                    bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, 0), radius=0.15)
                case 2:
                    bpy.ops.mesh.primitive_cylinder_add(location=(x, y, 0), radius=0.15, depth=0.2)
                case 3:
                    bpy.ops.mesh.primitive_cube_add(location=(x, y, 0), size=0.2)
                case 4:
                    bpy.ops.mesh.primitive_monkey_add(location=(x, y, 0), size=0.3)

        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                mat = bpy.data.materials.new(name="Material")
                mat.use_nodes = True
                node_tree = mat.node_tree
                nodes = node_tree.nodes
                bsdf = nodes.get("Principled BSDF")
                bsdf.inputs['Base Color'].default_value = (random.uniform(0, 1),
                                                           random.uniform(0, 1),
                                                           random.uniform(0, 1),
                                                           1)
                obj.data.materials.append(mat)

        self.render_scene(scenario)

    @test_func
    def test_light_source(self, scenario):
        cleanup()

        scene = bpy.context.scene

        # Remove default light source
        for obj in scene.objects:
            if obj.type == 'LIGHT':
                bpy.data.objects.remove(obj, do_unlink=True)

        verts = 12
        angle_step = math.tau / verts
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.context.scene.eevee.use_bloom = True

        for i in range(verts):
            cur_angle = i * angle_step

            x = math.cos(cur_angle)
            y = math.sin(cur_angle)

            random_number = random.randint(1, 4)
            match random_number:
                case 1:
                    bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, 0), radius=0.15)
                case 2:
                    bpy.ops.mesh.primitive_cylinder_add(location=(x, y, 0), radius=0.15, depth=0.2)
                case 3:
                    bpy.ops.mesh.primitive_cube_add(location=(x, y, 0), size=0.2)
                case 4:
                    bpy.ops.mesh.primitive_monkey_add(location=(x, y, 0), size=0.3)

        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                mat = bpy.data.materials.new(name="Material")
                mat.use_nodes = True
                node_tree = mat.node_tree
                nodes = node_tree.nodes
                bsdf = nodes.get("Principled BSDF")
                bsdf.inputs['Base Color'].default_value = (random.uniform(0, 1),
                                                           random.uniform(0, 1),
                                                           random.uniform(0, 1),
                                                           1)
                bsdf.inputs["Specular"].default_value = 0.8
                bsdf.inputs["Roughness"].default_value = 0.2
                obj.data.materials.append(mat)

        glow_material = bpy.data.materials.new(name="GlowMaterial")
        glow_material.use_nodes = True
        node_tree = glow_material.node_tree
        bpy.data.materials["GlowMaterial"].node_tree.nodes.clear()
        emission_node = node_tree.nodes.new(type='ShaderNodeEmission')
        emission_node.inputs["Color"].default_value = (0.151736, 0.0997155, 1, 1)
        emission_node.inputs["Strength"].default_value = 10.0
        material_output_node = node_tree.nodes.new(type='ShaderNodeOutputMaterial')
        node_tree.links.new(
            glow_material.node_tree.nodes["Emission"].outputs[0],
            glow_material.node_tree.nodes["Material Output"].inputs[0]
        )
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                if random.uniform(0, 1) < 0.3:
                    obj.data.materials[0] = glow_material

        self.render_scene(scenario)

    # Function to render the scene
    def render_scene(self, scenario):
        # Redirecting log output
        logfile = self.output_path + '/' + scenario.get_name() + f'/blender.log'
        open(logfile, 'w+').close()
        old = os.dup(sys.stdout.fileno())
        sys.stdout.flush()
        os.close(sys.stdout.fileno())
        fd = os.open(logfile, os.O_WRONLY)

        bpy.context.scene.render.image_settings.file_format = 'PNG'
        bpy.context.scene.render.filepath = self.output_path + '/' + scenario.get_name() + '/render'
        bpy.context.scene.render.resolution_x = self.x_resolution
        bpy.context.scene.render.resolution_y = self.y_resolution

        bpy.ops.render.render(write_still=True)

        # Closing log output
        os.close(fd)
        os.dup(old)
        os.close(old)
