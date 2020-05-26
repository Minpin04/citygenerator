import os
import json


# INPUT:    List, Dict, Dict
# OUTPUT:   -
def city_to_json(road_network, major_segment_coords, vertices, land_usages):
    output = {}

    # Save all vertices in road network.
    output['roadSegments'] = []
    output['roadVertices'] = []
    for vertex in vertices:
        output["roadVertices"].append({
            "position": {
                'x' : float(vertex.position[0]),
                'y' : float(vertex.position[1])
            }
        })

    # Save all segments in road network.
    for segment in road_network:
        output["roadSegments"].append({
            "startVertIndex" : vertices.index(segment.start_vert),
            "endVertIndex" : vertices.index(segment.end_vert)
        })
        
    output['majorRoads'] = []
    # Save all segments in road network.
    for road in major_segment_coords:
        output["majorRoads"].append({
            "startPosition": {
                'x' : float(road.start_vert.position[0]),
                'y' : float(road.start_vert.position[1])
            },
            "endPosition": {
                'x' : float(road.end_vert.position[0]),
                'y' : float(road.end_vert.position[1])
            }
        })

    # Save all polygons w/ land usage, population density, and population.
    output["land_usages"] = land_usages

    # Dump to json file.
    with open(os.getcwd() + "/output/roadnetwork_major.json", "w") as out:
        json.dump(output, out)
