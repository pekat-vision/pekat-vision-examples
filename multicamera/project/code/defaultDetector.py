def main(context):
    # make bigger all rectangles
    for rectangle in context['rectangles']:
        rectangle['width'] += 10
        rectangle['height'] += 10
        rectangle['x'] -= 5
        rectangle['y'] -= 5
    return context
