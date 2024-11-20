import bpy
import math

def create_nozzle(throat_area, exit_area, convergent_angle, divergent_angle):

    throat_radius = math.sqrt(throat_area / math.pi)
    exit_radius = math.sqrt(exit_area / math.pi)
    
    convergent_length = throat_radius / math.tan(math.radians(convergent_angle))
    divergent_length = (exit_radius - throat_radius) / math.tan(math.radians(divergent_angle))
    
    total_length = convergent_length + divergent_length
    
    vertices = [
        (0, 0, 0),  
        (0, throat_radius, convergent_length),  
        (0, exit_radius, convergent_length + divergent_length),  
    ]
    
    curve_data = bpy.data.curves.new(name="NozzleCurve", type="CURVE")
    curve_data.dimensions = '3D'
    spline = curve_data.splines.new(type='POLY')
    spline.points.add(len(vertices) - 1) 
    for i, vert in enumerate(vertices):
        spline.points[i].co = (*vert, 1) 
    
    curve_obj = bpy.data.objects.new("NozzleCurve", curve_data)
    bpy.context.collection.objects.link(curve_obj)
    
    bpy.context.view_layer.objects.active = curve_obj
    bpy.ops.object.modifier_add(type='SCREW')
    curve_obj.modifiers["Screw"].axis = 'Z'

    curve_obj.modifiers["Screw"].angle = math.radians(360)
    curve_obj.modifiers["Screw"].steps = 64
    curve_obj.modifiers["Screw"].render_steps = 64

    print(f"Nozzle created with throat radius {throat_radius:.4f} m, exit radius {exit_radius:.4f} m, "
          f"convergent angle {convergent_angle}°, and divergent angle {divergent_angle}°.")

throat_area = 0.0003  
exit_area = 0.0055  
convergent_angle = 45  
divergent_angle = 12  

create_nozzle(throat_area, exit_area, convergent_angle, divergent_angle)
