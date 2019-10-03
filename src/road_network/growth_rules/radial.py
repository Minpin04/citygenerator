import random
import numpy as np
from src.utilities import rotate
from src.road_network.vertex import Vertex
from src.road_network.segment import Segment

# INPUT:    ConfigLoader, Segment, Float
# OUTPUT:   List
def radial(config, segment, population_density):
    road_straight_probability = config.radial_straight_road_probability
    road_turn_probability = config.radial_road_turn_probability
    road_mininum_length = config.radial_road_min_length
    road_maximum_length = config.radial_road_max_length

    suggested_segments = []

    # Compute the unit vector of the given segment to determine direction.
    segment_unit_vector = (segment.end_vert.position - segment.start_vert.position)/segment.segment_norm()

    # Find the nearest centroid for given segment.
    nearest_center = config.radial_centers[np.argmin(np.linalg.norm(segment.end_vert.position - config.radial_centers, axis=1))]

    # In the case that the current segment ends at the radial center,
    # we return an empty list because the radial vector cannot be computed
    if np.array_equal(nearest_center, segment.end_vert.position):
        return suggested_segments

    radial_vector = segment.end_vert.position - nearest_center
    radial_unit_vector = radial_vector / np.linalg.norm(radial_vector)

    # Find degree between segment_unit_vector and radial_unit_vector.
    alpha = np.degrees(np.arccos(np.clip(np.dot(segment_unit_vector, radial_unit_vector), -1.0, 1.0)))

    if (alpha >= 45 and alpha < 90) or (alpha >= 225 and alpha < 270): 
        alpha -= 90
    elif (alpha >= 90 and alpha < 135) or (alpha >= 270 and alpha < 315):
        alpha += 90
    elif alpha >= 135 and alpha < 225:
        alpha -= 180

    rotated_unit_vector = rotate(segment_unit_vector, alpha)

    # We multiply the probability with the population density because we
    # want to increase the probability of turning the closer to the density.  
    road_turn_probability = road_turn_probability * (population_density + 1)
    
    # Generate a new segment going straight.
    if random.uniform(0, 1) <= road_straight_probability:
        straight_segment_array = random.uniform(road_mininum_length, road_maximum_length) * rotated_unit_vector
        straight_segment_array += segment.end_vert.position

        new_segment = Segment(segment_start=segment.end_vert, segment_end=Vertex(straight_segment_array))
        suggested_segments.append(new_segment)
    
    # Generate a new segment turning right.
    if random.uniform(0, 1) <= road_turn_probability:
        rotated_unit_vector = rotate(segment_unit_vector, 90)
        turn_road_segment_array = random.uniform(road_mininum_length, road_maximum_length) * rotated_unit_vector
        turn_road_segment_array += segment.end_vert.position

        new_segment = Segment(segment_start=segment.end_vert, segment_end=Vertex(turn_road_segment_array))
        suggested_segments.append(new_segment)

    # Generate a new segment turning left.
    if random.uniform(0, 1) <= road_turn_probability:
        rotated_unit_vector = rotate(segment_unit_vector, -90)
        turn_road_segment_array = random.uniform(road_mininum_length, road_maximum_length) * rotated_unit_vector
        turn_road_segment_array += segment.end_vert.position

        new_segment = Segment(segment_start=segment.end_vert, segment_end=Vertex(turn_road_segment_array))
        suggested_segments.append(new_segment)

    return suggested_segments