import pytest
from snake_logic import move_snake, check_collision, eat_food

def test_move_snake():
    snake = [(100, 100), (80, 100), (60, 100)]
    direction = (20, 0)
    new_snake = move_snake(snake, direction)
    assert new_snake == [(120, 100), (100, 100), (80, 100)]

def test_check_collision_wall():
    head = (400, 200)
    width, height = 400, 400
    assert check_collision(head, width, height, [])

def test_check_collision_self():
    head = (100, 100)
    snake_body = [(100, 100), (80, 100)]
    assert check_collision(head, 400, 400, snake_body)

def test_eat_food():
    head = (100, 100)
    food = (100, 100)
    cell_size = 20
    assert eat_food(head, food, cell_size)
    
    head = (110, 110)
    food = (100, 100)
    cell_size = 20
    assert not eat_food(head, food, cell_size)
