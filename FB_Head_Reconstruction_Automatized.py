import bpy
import os
import json
import math
import sys
import signal

from keentools.utils.version import BVersion
from keentools.facebuilder_config import FBConfig, get_fb_settings
from keentools.facebuilder.fbloader import FBLoader
from keentools.facebuilder.utils.exif_reader import (read_exif_to_camera,
                                 auto_setup_camera_from_exif)
from keentools.utils.focal_length import (configure_focal_mode_and_fixes,
                                  update_camera_focal)

# Settings
argv = sys.argv
argv = argv[argv.index("--") + 1:]  # args after --

# Global settings
num_img_loaded = 0
head_num = 0

def add_images(images_directory):
    global num_img_loaded  # Declare variable as global
    head_num=0

    # Get FaceBuilder settings
    settings = get_fb_settings()
    if not settings.is_proper_headnum(head_num):
        print(f'WRONG HEADNUM: {head_num}/'f'{settings.get_last_headnum()}')
        return {'CANCELLED'}

    if not settings.check_heads_and_cams():
        settings.fix_heads()
        return {'CANCELLED'}

    FBLoader.load_model(head_num)
    
    head = settings.get_head(head_num)
    last_camnum = head.get_last_camnum()

    # Iterate through files in the images directory
    for filename in os.listdir(images_directory):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.tif', '.tiff', '.bmp')):
            filepath = os.path.join(images_directory, filename)
            print(f'IMAGE FILE: {filepath}')

            # Add new camera with image
            camera = FBLoader.add_new_camera_with_image(head_num, filepath)
            read_exif_to_camera(head_num, head.get_last_camnum(), filepath)
            camera.orientation = camera.exif.orientation
            
            # Increment the number of loaded images
            num_img_loaded += 1

    for i, camera in enumerate(head.cameras):
            if i > last_camnum:
                auto_setup_camera_from_exif(camera)
                FBLoader.center_geo_camera_projection(head_num, i)

    FBLoader.save_fb_serial_and_image_pathes(head_num)
    print(f'\nAll images are saved\n\n')

def align_face_to_images():   
    head_num = 0 
    for i in range(num_img_loaded):
        bpy.ops.object.select_all(action='DESELECT')
        # Update camera number values
        cam_num = i

        # Recupera il nome dell'immagine corrente
        image_filename = os.path.basename(os.listdir(images_directory)[i])

        print(f'Aligning camera {cam_num} to image: {image_filename}')
        bpy.ops.keentools_fb.select_camera(headnum=head_num, camnum=cam_num)
        bpy.ops.keentools_fb.pickmode_starter(headnum=head_num, camnum=cam_num)
    print(f'\nAll cameras have aligned to images\n')

def bake_texture_create():
    print(f'Creating texture...')
    bpy.context.scene.keentools_fb_settings.heads[0].masks[1] = False #disable eyes model parts
    bpy.context.scene.keentools_fb_settings.heads[0].masks[3] = False  # disable mouth model parts
    bpy.context.scene.keentools_fb_settings.heads[0].masks[4] = False #disable NeckLower model parts

    bpy.context.scene.keentools_fb_settings.heads[0].tex_uv_shape = 'uv4' #change typology of UVmap --> mh
    #bpy.context.scene.keentools_fb_settings.tex_face_angles_affection = 20 #angles_affection modified
    #bpy.context.scene.keentools_fb_settings.tex_equalize_brightness = True #equalize brightness -> enable
    #bpy.context.scene.keentools_fb_settings.tex_equalize_colour = True #equalize color -> enable
    #bpy.context.scene.keentools_fb_settings.tex_fill_gaps = True #autofill -> enable

    bpy.ops.keentools_fb.bake_tex(headnum=0)
    bpy.ops.keentools_fb.tex_selector(headnum=0)

    # Modify shader node
    #print(f'Modify shader node...')
    #bpy.data.materials["FBHead_preview_mat"].node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.2 #specular
    #bpy.data.materials["FBHead_preview_mat"].node_tree.nodes["Principled BSDF"].inputs[9].default_value = 1 #roughness

    print(f'bake_texture_create SUCCED')

def export_data(images_dir):
    # Define outputs path

    # Normalize images_dir path to remove double bars (//)
    images_dir = os.path.normpath(images_dir)
    # extract the folder name of 'images_dir'
    images_dir_name = os.path.basename(images_dir)
    # Get the parent directory of images_dir
    parent_path = os.path.dirname(images_dir)
    path_output= parent_path+"\_Results_"
    # create the directory for outputs
    output_dir = os.path.join(path_output, f'{images_dir_name}_HEAD_RECONSTRUCTION')
    os.makedirs(output_dir, exist_ok=True)

    # Export texture .png
    texture_output=os.path.join(output_dir, f'{images_dir_name}_texture.png')
    bpy.ops.keentools_fb.texture_file_export(filepath=texture_output, headnum=0)

    # Export FBX and GLB: FBHead
    bpy.ops.object.select_all(action='DESELECT')
    head_name = "FBHead"
    head = bpy.data.objects.get(head_name)
    if head:
        # If the object is found, select it
        bpy.context.view_layer.objects.active = head
        head.select_set(True)

        # Specify the full FBX file path to export
        export_path_fbx = os.path.join(output_dir, f'{images_dir_name}_head.fbx')

        # Export the selected object as FBX
        bpy.ops.export_scene.fbx(filepath=export_path_fbx, use_selection=True)

        print(f"Mesh '{head_name}' exported to {export_path_fbx}")

        # Specify the full GLB file path to export
        export_path_glb = os.path.join(output_dir, f'{images_dir_name}_head.glb')

        # Export the selected object as GLB
        bpy.ops.export_scene.gltf(filepath=export_path_glb, export_format='GLB')

        print(f"Mesh '{head_name}' exported to {export_path_glb}")
    else:
        print(f"Object '{head_name}' not found.")

    # Optional --> Save the .blend and Save Cameras Info in Json
    optional_saving(output_dir, images_dir_name)

def optional_saving(output_dir, images_dir_name):
    ## Optional
    # Save the .blend
    blend_file_path = os.path.join(output_dir, f'{images_dir_name}_scene.blend')
    bpy.ops.wm.save_as_mainfile(filepath=blend_file_path)
    print(f"\n.blend saved!\n")
    
    # Save Cameras Info in Json
    json_camera_info= os.path.join(output_dir, f'{images_dir_name}_CamerasInfo.json')
    save_cameras_info(json_camera_info)

def save_cameras_info(output_json_path): 
    # Extract camera information for Unreal
    camera_info = []

    for obj in bpy.data.objects:
        if obj.type == 'CAMERA':
            # Convert location from meters to centimeters and handle Y coordinate sign
            location_cm = {"X": obj.location.x * 100, "Y": abs(obj.location.y) * 100, "Z": obj.location.z * 100}

            # Calculate field of view from focal length
            sensor_width = obj.data.sensor_width
            focal_length_mm = obj.data.lens
            fov = 2 * math.degrees(math.atan(sensor_width / (2 * focal_length_mm)))

            # Get camera resolution
            resolution_x = bpy.context.scene.render.resolution_x
            resolution_y = bpy.context.scene.render.resolution_y

            rotation_degrees = {"Pitch": math.degrees(obj.rotation_euler.y),
                                "Yaw": math.degrees(obj.rotation_euler.z),
                                "Roll": math.degrees(obj.rotation_euler.x)}

            camera_data = {
                "Name": obj.name,
                "Location": location_cm,
                "Rotation": rotation_degrees,
                "FocalLength": focal_length_mm,
                "Filmback": [resolution_x, resolution_y]
            }

            camera_info.append(camera_data)

    # Save camera information to a JSON file
    with open(output_json_path, "w") as file:
        json.dump(camera_info, file, indent=4)

    print(f"Camera information extracted and saved to '{output_json_path}'.")

def head_reconstruction_automatized(images_dir):
    # Check for the FaceBuilder addon
    addon_name = "keentools"
    if addon_name in bpy.context.preferences.addons:
        # Clear default objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        # Create a new head
        bpy.ops.keentools_fb.add_head()

        # Add Images
        add_images(images_dir)
        
        # Align Face
        align_face_to_images()

        # Create Texture
        bake_texture_create()

        # Export Texture and Head  --> Optional Save .blend ed Cameras Info
        export_data(images_dir)

        print(f"\n\nHEAD RECONSTRUCTION SUCCESS!\n")

    else:
        print(f"The addon {addon_name} is not installed.")


if __name__ == "__main__":
    if len(argv) < 1:
        print("Usage: blender -b -P script.py -- images_directory")
        sys.exit(1)

    images_directory = argv[0]
    head_reconstruction_automatized(images_directory)


   


