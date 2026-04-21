def move_snake(snake, direction):
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    return [new_head] + snake

def check_collision(head, width, height, snake_body):
    if (head[0] < 0 or head[0] >= width or
        head[1] < 0 or head[1] >= height):
        return True
    return head in snake_body

def eat_food(head, food, cell_size):
    return abs(head[0] - food[0]) < cell_size and abs(head[1] - food[1]) < cell_size
