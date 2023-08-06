from hgl.calculate.line import points_on_curve
from hgl.calculate.box import generate_2d_bounding_box_from_points_iter


# TODO use numpy to store and calculate value

# conic arcs (quadratic) used mainly by truetype
# cubic arcs PostScript Type 1, CFF, and CFF2

def generate_text(font_face_data, text, spacing=-1):
    """ Given a font face from freetype generate a list of lines to render the character
    Args:
      font_face_data (freetype object): freetype font face object
      text (string): text to render
      space: spacing between each letter

    Returns:
      list: list of letters containing list of line segments, each segment containing the points

    Links:
    """
    character_segments = []
    for l in text:
        font_face_data.load_char(l)
        # character_segments += generate_letter(font_face_data=font_face_data)
        character_segments.append(
            generate_letter(font_face_data=font_face_data))

    # TODO lets shrink probably want to generate this value
    size_factor = 0.1
    for s, l, p in step_text_points(character_segments):
        character_segments[s][l][p] = [
            character_segments[s][l][p][0] * size_factor,
            character_segments[s][l][p][1] * size_factor,
            character_segments[s][l][p][2]]

    # work out largest font size and generate a bounding box
    box = generate_2d_bounding_box_from_points_iter(
        [point for segment in character_segments for point in step_text_points(character_segments)])
    shift_x_spacing = 5
    if spacing < 0 is True:
        shift_x_spacing = (box[-1][0] * 2) / len(text)

    for s, l, p in step_text_points(character_segments):
        character_segments[s][l][p] = [
            character_segments[s][l][p][0] + s * shift_x_spacing,
            character_segments[s][l][p][1],
            character_segments[s][l][p][2]]

    return character_segments


def merge_letters_into_list_of_lines(self, character_segments):
    """Helper function that flattens the list into lines
    with out the separation of the letter"""
    return [ls for s in character_segments for ls in s]


def generate_letter(font_face_data):
    """ Given a font face from freetype generate a list of lines to render the character
    Args:
      font_face_data (freetype object): freetype font face object
      letter (string): letter to render

    Returns:
      points: list of lines, each line contaning a line segments points

    Links:
    """
    outline = font_face_data.glyph.outline

    points = []
    point_list = []

    end = 0
    # Iterate over each contour
    for i in range(0, len(outline.contours)):
        start = end
        end = outline.contours[i] + 1
        tags = outline.tags[start:end]
        tags.append(tags[0])

        points = []
        shrink_factor = 1
        for p in outline.points[start:end]:
            points.append([p[0] * shrink_factor, p[1] * shrink_factor, 0])
        points.append([points[0][0] * shrink_factor, points[0][1] * shrink_factor, 0])

        segments = [[points[0], ], ]
        for j in range(1, len(points)):
            segments[-1].append(list(points[j]))
            if tags[j] & (1 << 0) and j < (len(points)-1):
                segments.append([list(points[j]), ])

        for segment in segments:
            if len(segment) == 2:  # line
                point_list.append(segment)
            elif len(segment) == 3:  # conic bezier arc
                point_list.append(points_on_curve(segment, len(segment)))
            elif len(segment) == 4:  # cubic bezier arc
                point_list.append(points_on_curve(segment, len(segment)))
            else:  # cubic bezier arc
                point_list.append(points_on_curve(segment, len(segment)))

    return point_list


def step_letter_points(segments):
    for spos, s in enumerate(segments):
        for ppos, p in enumerate(s):
            yield spos, ppos


def step_text_points(letters):
    for lpos, l in enumerate(letters):
        for spos, s in enumerate(l):
            for ppos, p in enumerate(s):
                yield lpos, spos, ppos

def step_text_lines(letters):
    for lpos, l in enumerate(letters):
        for spos, s in enumerate(l):
            for p in range(0, len(s)-1):
                yield s[p], s[p+1]


def load_font(text, font_face_data):
    """Warning temporary implementation, currently does not use cubic bezier curves
    TODO add cubic bezier curve code """
    # /usr/share/fonts/truetype/ubuntu-font-family/UbuntuMono-B.ttf
    # face = ft.Face('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')
    face = ft.Face(font_path)
    face.set_char_size(12)
    face.load_char(text)
    outline = face.glyph.outline

    points = []
    point_list = []

    end = 0
    # Iterate over each contour
    for i in range(0, len(outline.contours)):
        start = end
        end = outline.contours[i] + 1
        tags = outline.tags[start:end]
        tags.append(tags[0])

        points = []
        shrink_factor = 1
        for p in outline.points[start:end]:
            points.append([p[0] * shrink_factor, p[1] * shrink_factor, 0])
        points.append([points[0][0] * shrink_factor, points[0][1] * shrink_factor, 0])

        segments = [[points[0], ], ]
        for j in range(1, len(points)):
            segments[-1].append(list(points[j]))
            if tags[j] & (1 << 0) and j < (len(points)-1):
                segments.append([list(points[j]), ])

        for segment in segments:
            if len(segment) == 2:  # line
                point_list.append(segment)
            elif len(segment) == 3:  # conic bezier arc
                point_list.append(points_on_curve(segment, len(segment)))
            elif len(segment) == 4:  # cubic bezier arc
                point_list.append(points_on_curve(segment, len(segment)))
            else:  # cubic bezier arc
                point_list.append(points_on_curve(segment, len(segment)))

    return point_list
