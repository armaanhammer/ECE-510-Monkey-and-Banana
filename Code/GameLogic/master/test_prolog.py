#!/home/sburkhar/.virtualenvs/cv/bin/python
import unittest

from pyswip import Prolog

def fun(x):
    return x + 1

# prolog = Prolog()

# prolog.assertz('father(michael, john)')
# prolog.assertz('father(michael, gina)')

# results = list(prolog.query('father(michael, X)'))

# prolog.consult('phase2.pl')


# print(results)

class MyTest(unittest.TestCase):
    def setUp(self):
        self.prolog = Prolog()

        self.prolog.consult('phase2.pl')

        # Test Map: 
        #   [   6   -   -   -   -   -   -   -    ]
        #   [   5   -   -   -   -   -   -   -    ]
        #   [   4   -   -   B   B   B   -   -    ]
        #   [   3   -   -   B   -   B   -   -    ]
        #   [   2   -   -   B   B   B   -   -    ]
        #   [   1   -   -   -   -   -   -   -    ]
        #   [   0   -   -   -   -   -   -   -    ]
        #   [   x   0   1   2   3   4   5   6    ]
        
        # Box coordinates:
        #   Top Left Corner (2,4)
        #   Top Right Corner (4,4)
        #   Bottom Left Corner (2,2)
        #   Bottom Right Corner (4,2)
        # self.ramp_top_left =     {'x': 2, 'y': 4}
        self.ramp_bottom_left =  {'x': 2, 'y': 2}
        self.ramp_top_right =    {'x': 4, 'y': 4}
        # self.ramp_bottom_right = {'x': 4, 'y': 2}

    def test(self):
        self.assertEqual(fun(3), 4)
    
    def test_prolog_connection(self):
        # Arrange
        self.prolog.assertz('father(michael, john)')
        self.prolog.assertz('father(michael, gina)')

        # Act
        obj = 'michael'
        sub = 'X'
        query = 'father({0:},{1:})'.format(obj, sub)
        actual = list(self.prolog.query(query))
        expected = [{sub: 'john'}, {sub: 'gina'}]

        # Assert
        self.assertEqual(actual,expected)

    def test_robot_at_y_center(self):
        # Arrange
        robot_location = {'x': 3, 'y': 3}
       
        query = 'robot_is_at_y_center({},{},{})'.format(
                robot_location['y'],
                self.ramp_bottom_left['y'],
                self.ramp_top_right['y']
                )

        # Act
        result = bool(list(self.prolog.query(query)))

        # Assert
        self.assertTrue(result)
        
    def test_robot_at_x_center(self):
        # Arrange
        robot_location = {'x': 3, 'y': 3}
       
        query = 'robot_is_at_x_center({},{},{})'.format(
                robot_location['x'],
                self.ramp_bottom_left['x'],
                self.ramp_top_right['x']
                )

        # Act
        result = bool(list(self.prolog.query(query)))

        # Assert
        self.assertTrue(result)
         
    def test_robot_at_center(self):
        # Arrange

        #   [   6   -   -   -   -   -   -   -    ]
        #   [   5   -   -   -   -   -   -   -    ]
        #   [   4   -   -   B   B   B   -   -    ]
        #   [   3   -   -   B   R   B   -   -    ]
        #   [   2   -   -   B   B   B   -   -    ]
        #   [   1   -   -   -   -   -   -   -    ]
        #   [   0   -   -   -   -   -   -   -    ]
        #   [   x   0   1   2   3   4   5   6    ]
        robot_location = {'x': 3, 'y': 3}
       
        query = ('robot_is_at_center(' +
            str(robot_location['x']) + ',' + 
            str(robot_location['y']) + ',' + 
            str(self.ramp_bottom_left['x']) + ',' +
            str(self.ramp_top_right['x']) + ',' +
            str(self.ramp_bottom_left['y']) + ',' +
            str(self.ramp_top_right['y']) + ')'
        )

        # Act
        result = bool(list(self.prolog.query(query)))

        # Assert
        self.assertTrue(result)

         
    def test_robot_behind_ramp(self):
        # Arrange

        #   [   6   -   -   -   R   -   -   -    ]
        #   [   5   -   -   -   -   -   -   -    ]
        #   [   4   -   -   B   B   B   -   -    ]
        #   [   3   -   -   B   -   B   -   -    ]
        #   [   2   -   -   B   B   B   -   -    ]
        #   [   1   -   -   -   -   -   -   -    ]
        #   [   0   -   -   -   -   -   -   -    ]
        #   [   x   0   1   2   3   4   5   6    ]
        robot_location = {'x': 3, 'y': 6}
       
        query = ('robot_is_behind_ramp(' +
            str(robot_location['y']) + ',' + 
            str(self.ramp_top_right['y']) + ')'
        )

        # Act
        result = bool(list(self.prolog.query(query)))

        # Assert
        self.assertTrue(result)

    def test_robot_left_of_ramp(self):
        # Arrange

        #   [   6   -   -   -   -   -   -   -    ]
        #   [   5   -   -   -   -   -   -   -    ]
        #   [   4   -   -   B   B   B   -   -    ]
        #   [   3   R   -   B   -   B   -   -    ]
        #   [   2   -   -   B   B   B   -   -    ]
        #   [   1   -   -   -   -   -   -   -    ]
        #   [   0   -   -   -   -   -   -   -    ]
        #   [   x   0   1   2   3   4   5   6    ]
        robot_location = {'x': 0, 'y': 3}
       
        query = ('robot_is_left_of_ramp(' +
            str(robot_location['x']) + ',' + 
            str(self.ramp_bottom_left['x']) + ')'
        )

        # Act
        result = bool(list(self.prolog.query(query)))

        # Assert
        self.assertTrue(result)

    def test_robot_right_of_ramp(self):
        # Arrange

        #   [   6   -   -   -   -   -   -   -    ]
        #   [   5   -   -   -   -   -   -   -    ]
        #   [   4   -   -   B   B   B   -   -    ]
        #   [   3   -   -   B   -   B   -   R    ]
        #   [   2   -   -   B   B   B   -   -    ]
        #   [   1   -   -   -   -   -   -   -    ]
        #   [   0   -   -   -   -   -   -   -    ]
        #   [   x   0   1   2   3   4   5   6    ]
        robot_location = {'x': 6, 'y': 3}
       
        query = ('robot_is_right_of_ramp(' +
            str(robot_location['x']) + ',' + 
            str(self.ramp_top_right['x']) + ')'
        )

        # Act
        result = bool(list(self.prolog.query(query)))

        # Assert
        self.assertTrue(result)

    def test_robot_front_of_ramp(self):
        # Arrange

        #   [   6   -   -   -   -   -   -   -    ]
        #   [   5   -   -   -   -   -   -   -    ]
        #   [   4   -   -   B   B   B   -   -    ]
        #   [   3   -   -   B   -   B   -   -    ]
        #   [   2   -   -   B   B   B   -   -    ]
        #   [   1   -   -   -   -   -   -   -    ]
        #   [   0   -   -   -   R   -   -   -    ]
        #   [   x   0   1   2   3   4   5   6    ]
        robot_location = {'x': 3, 'y': 0}
       
        query = ('robot_is_in_front_of_ramp(' +
            str(robot_location['y']) + ',' + 
            str(self.ramp_bottom_left['y']) + ')'
        )

        # Act
        result = bool(list(self.prolog.query(query)))

        # Assert
        self.assertTrue(result)

    def test_robot_front_center_of_ramp(self):
        # Arrange

        #   [   6   -   -   -   -   -   -   -    ]
        #   [   5   -   -   -   -   -   -   -    ]
        #   [   4   -   -   B   B   B   -   -    ]
        #   [   3   -   -   B   -   B   -   -    ]
        #   [   2   -   -   B   B   B   -   -    ]
        #   [   1   -   -   -   -   -   -   -    ]
        #   [   0   -   -   -   R   -   -   -    ]
        #   [   x   0   1   2   3   4   5   6    ]
        robot_location = {'x': 3, 'y': 0}
       
        query = ('robot_is_front_center_of_ramp(' +
            str(robot_location['x']) + ',' + 
            str(robot_location['y']) + ',' + 
            str(self.ramp_bottom_left['x']) + ',' +
            str(self.ramp_top_right['x']) + ',' +
            str(self.ramp_bottom_left['y']) + ',' + 
            str(self.ramp_top_right['y']) + ')'
        )

        # Act
        result = bool(list(self.prolog.query(query)))

        # Assert
        self.assertTrue(result)

    def test_robot_front_left_of_ramp(self):
        # Arrange

        #   [   6   -   -   -   -   -   -   -    ]
        #   [   5   -   -   -   -   -   -   -    ]
        #   [   4   -   -   B   B   B   -   -    ]
        #   [   3   -   -   B   -   B   -   -    ]
        #   [   2   -   -   B   B   B   -   -    ]
        #   [   1   -   -   -   -   -   -   -    ]
        #   [   0   R   -   -   -   -   -   -    ]
        #   [   x   0   1   2   3   4   5   6    ]
        robot_location = {'x': 0, 'y': 0}
       
        query = ('robot_is_front_left_of_ramp(' +
            str(robot_location['x']) + ',' + 
            str(robot_location['y']) + ',' + 
            str(self.ramp_bottom_left['x']) + ',' +
            str(self.ramp_top_right['x']) + ',' +
            str(self.ramp_bottom_left['y']) + ',' + 
            str(self.ramp_top_right['y']) + ')'
        )

        # Act
        result = bool(list(self.prolog.query(query)))

        # Assert
        self.assertTrue(result)

    def test_robot_front_right_of_ramp(self):
        # Arrange

        #   [   6   -   -   -   -   -   -   -    ]
        #   [   5   -   -   -   -   -   -   -    ]
        #   [   4   -   -   B   B   B   -   -    ]
        #   [   3   -   -   B   -   B   -   -    ]
        #   [   2   -   -   B   B   B   -   -    ]
        #   [   1   -   -   -   -   -   -   -    ]
        #   [   0   -   -   -   -   -   -   R    ]
        #   [   x   0   1   2   3   4   5   6    ]
        robot_location = {'x': 6, 'y': 0}
       
        query = ('robot_is_front_right_of_ramp(' +
            str(robot_location['x']) + ',' + 
            str(robot_location['y']) + ',' + 
            str(self.ramp_bottom_left['x']) + ',' +
            str(self.ramp_top_right['x']) + ',' +
            str(self.ramp_bottom_left['y']) + ',' + 
            str(self.ramp_top_right['y']) + ')'
        )

        # Act
        result = bool(list(self.prolog.query(query)))

        # Assert
        self.assertTrue(result)

    def test_robot_behind_center_ramp(self):
        # Arrange

        #   [   6   -   -   -   R   -   -   -    ]
        #   [   5   -   -   -   -   -   -   -    ]
        #   [   4   -   -   B   B   B   -   -    ]
        #   [   3   -   -   B   -   B   -   -    ]
        #   [   2   -   -   B   B   B   -   -    ]
        #   [   1   -   -   -   -   -   -   -    ]
        #   [   0   -   -   -   -   -   -   -    ]
        #   [   x   0   1   2   3   4   5   6    ]
        robot_location = {'x': 3, 'y': 6}
       
        query = ('robot_is_behind_center_of_ramp(' +
            str(robot_location['x']) + ',' + 
            str(robot_location['y']) + ',' + 
            str(self.ramp_bottom_left['x']) + ',' +
            str(self.ramp_top_right['x']) + ',' +
            str(self.ramp_bottom_left['y']) + ',' + 
            str(self.ramp_top_right['y']) + ')'
        )

        # Act
        result = bool(list(self.prolog.query(query)))

        # Assert
        self.assertTrue(result)


    def test_robot_rotate_270_when_behind_ramp(self):
        # Arrange

        #   [   6   -   -   -   R   -   -   -    ]
        #   [   5   -   -   -   -   -   -   -    ]
        #   [   4   -   -   B   B   B   -   -    ]
        #   [   3   -   -   B   -   B   -   -    ]
        #   [   2   -   -   B   B   B   -   -    ]
        #   [   1   -   -   -   -   -   -   -    ]
        #   [   0   -   -   -   -   -   -   -    ]
        #   [   x   0   1   2   3   4   5   6    ]
        robot_location = {'x': 3, 'y': 6}
       
        query = ('rotate_270_degrees_west_of_ramp(' +
            str(robot_location['x']) + ',' + 
            str(robot_location['y']) + ',' + 
            str(self.ramp_bottom_left['x']) + ',' +
            str(self.ramp_top_right['x']) + ',' +
            str(self.ramp_bottom_left['y']) + ',' + 
            str(self.ramp_top_right['y']) + ')'
        )

        # Act
        result = bool(list(self.prolog.query(query)))

        # Assert
        self.assertTrue(result)

    def test_robot_rotate_270_when_front_right_of_ramp(self):
        # Arrange

        #   [   6   -   -   -   -   -   -   -    ]
        #   [   5   -   -   -   -   -   -   -    ]
        #   [   4   -   -   B   B   B   -   -    ]
        #   [   3   -   -   B   -   B   -   -    ]
        #   [   2   -   -   B   B   B   -   -    ]
        #   [   1   -   -   -   -   -   -   -    ]
        #   [   0   -   -   -   -   -   -   R    ]
        #   [   x   0   1   2   3   4   5   6    ]
        robot_location = {'x': 6, 'y': 0}
       
        query = ('rotate_270_degrees_west_of_ramp(' +
            str(robot_location['x']) + ',' + 
            str(robot_location['y']) + ',' + 
            str(self.ramp_bottom_left['x']) + ',' +
            str(self.ramp_top_right['x']) + ',' +
            str(self.ramp_bottom_left['y']) + ',' + 
            str(self.ramp_top_right['y']) + ')'
        )

        # Act
        result = bool(list(self.prolog.query(query)))

        # Assert
        self.assertTrue(result)

    def test_robot_rotate_90_when_front_left_of_ramp(self):
        # Arrange

        #   [   6   -   -   -   -   -   -   -    ]
        #   [   5   -   -   -   -   -   -   -    ]
        #   [   4   -   -   B   B   B   -   -    ]
        #   [   3   -   -   B   -   B   -   -    ]
        #   [   2   -   -   B   B   B   -   -    ]
        #   [   1   -   -   -   -   -   -   -    ]
        #   [   0   R   -   -   -   -   -   -    ]
        #   [   x   0   1   2   3   4   5   6    ]
        robot_location = {'x': 0, 'y': 0}
       
        query = ('rotate_90_degrees_east_of_ramp(' +
            str(robot_location['x']) + ',' + 
            str(robot_location['y']) + ',' + 
            str(self.ramp_bottom_left['x']) + ',' +
            str(self.ramp_top_right['x']) + ',' +
            str(self.ramp_bottom_left['y']) + ',' + 
            str(self.ramp_top_right['y']) + ')'
        )

        # Act
        result = bool(list(self.prolog.query(query)))

        # Assert
        self.assertTrue(result)

    def test_robot_rotate_180_when_center_left_of_ramp(self):
        # Arrange

        #   [   6   -   -   -   -   -   -   -    ]
        #   [   5   -   -   -   -   -   -   -    ]
        #   [   4   -   -   B   B   B   -   -    ]
        #   [   3   R   -   B   -   B   -   -    ]
        #   [   2   -   -   B   B   B   -   -    ]
        #   [   1   -   -   -   -   -   -   -    ]
        #   [   0   -   -   -   -   -   -   -    ]
        #   [   x   0   1   2   3   4   5   6    ]
        robot_location = {'x': 0, 'y': 3}
       
        query = ('rotate_180_degrees_south_of_ramp(' +
            str(robot_location['x']) + ',' + 
            str(robot_location['y']) + ',' + 
            str(self.ramp_bottom_left['x']) + ',' +
            str(self.ramp_top_right['x']) + ',' +
            str(self.ramp_bottom_left['y']) + ',' + 
            str(self.ramp_top_right['y']) + ')'
        )

        # Act
        result = bool(list(self.prolog.query(query)))

        # Assert
        self.assertTrue(result)

    def test_robot_rotate_180_when_center_right_of_ramp(self):
        # Arrange

        #   [   6   -   -   -   -   -   -   -    ]
        #   [   5   -   -   -   -   -   -   -    ]
        #   [   4   -   -   B   B   B   -   -    ]
        #   [   3   -   -   B   -   B   -   R    ]
        #   [   2   -   -   B   B   B   -   -    ]
        #   [   1   -   -   -   -   -   -   -    ]
        #   [   0   -   -   -   -   -   -   -    ]
        #   [   x   0   1   2   3   4   5   6    ]
        robot_location = {'x': 6, 'y': 3}
       
        query = ('rotate_180_degrees_south_of_ramp(' +
            str(robot_location['x']) + ',' + 
            str(robot_location['y']) + ',' + 
            str(self.ramp_bottom_left['x']) + ',' +
            str(self.ramp_top_right['x']) + ',' +
            str(self.ramp_bottom_left['y']) + ',' + 
            str(self.ramp_top_right['y']) + ')'
        )

        # Act
        result = bool(list(self.prolog.query(query)))

        # Assert
        self.assertTrue(result)

    def test_robot_rotate_180_when_behind_right_of_ramp(self):
        # Arrange

        #   [   6   -   -   -   -   -   -   R    ]
        #   [   5   -   -   -   -   -   -   -    ]
        #   [   4   -   -   B   B   B   -   -    ]
        #   [   3   -   -   B   -   B   -   -    ]
        #   [   2   -   -   B   B   B   -   -    ]
        #   [   1   -   -   -   -   -   -   -    ]
        #   [   0   -   -   -   -   -   -   -    ]
        #   [   x   0   1   2   3   4   5   6    ]
        robot_location = {'x': 6, 'y': 6}
       
        query = ('rotate_180_degrees_south_of_ramp(' +
            str(robot_location['x']) + ',' + 
            str(robot_location['y']) + ',' + 
            str(self.ramp_bottom_left['x']) + ',' +
            str(self.ramp_top_right['x']) + ',' +
            str(self.ramp_bottom_left['y']) + ',' + 
            str(self.ramp_top_right['y']) + ')'
        )

        # Act
        result = bool(list(self.prolog.query(query)))

        # Assert
        self.assertTrue(result)

    def test_robot_rotate_180_when_behind_left_of_ramp(self):
        # Arrange

        #   [   6   R   -   -   -   -   -   -    ]
        #   [   5   -   -   -   -   -   -   -    ]
        #   [   4   -   -   B   B   B   -   -    ]
        #   [   3   -   -   B   -   B   -   -    ]
        #   [   2   -   -   B   B   B   -   -    ]
        #   [   1   -   -   -   -   -   -   -    ]
        #   [   0   -   -   -   -   -   -   -    ]
        #   [   x   0   1   2   3   4   5   6    ]
        robot_location = {'x': 0, 'y': 6}
       
        query = ('rotate_180_degrees_south_of_ramp(' +
            str(robot_location['x']) + ',' + 
            str(robot_location['y']) + ',' + 
            str(self.ramp_bottom_left['x']) + ',' +
            str(self.ramp_top_right['x']) + ',' +
            str(self.ramp_bottom_left['y']) + ',' + 
            str(self.ramp_top_right['y']) + ')'
        )

        # Act
        result = bool(list(self.prolog.query(query)))

        # Assert
        self.assertTrue(result)

    def test_robot_dont_rotate_180_when_behind_center_of_ramp(self):
        # Arrange

        #   [   6   -   -   -   R   -   -   -    ]
        #   [   5   -   -   -   -   -   -   -    ]
        #   [   4   -   -   B   B   B   -   -    ]
        #   [   3   -   -   B   -   B   -   -    ]
        #   [   2   -   -   B   B   B   -   -    ]
        #   [   1   -   -   -   -   -   -   -    ]
        #   [   0   -   -   -   -   -   -   -    ]
        #   [   x   0   1   2   3   4   5   6    ]
        robot_location = {'x': 3, 'y': 6}
       
        query = ('rotate_180_degrees_south_of_ramp(' +
            str(robot_location['x']) + ',' + 
            str(robot_location['y']) + ',' + 
            str(self.ramp_bottom_left['x']) + ',' +
            str(self.ramp_top_right['x']) + ',' +
            str(self.ramp_bottom_left['y']) + ',' + 
            str(self.ramp_top_right['y']) + ')'
        )

        # Act
        result = bool(list(self.prolog.query(query)))

        # Assert
        self.assertFalse(result)

    def test_robot_dont_rotate_180_when_front_center_of_ramp(self):
        # Arrange

        #   [   6   -   -   -   -   -   -   -    ]
        #   [   5   -   -   -   -   -   -   -    ]
        #   [   4   -   -   B   B   B   -   -    ]
        #   [   3   -   -   B   -   B   -   -    ]
        #   [   2   -   -   B   B   B   -   -    ]
        #   [   1   -   -   -   -   -   -   -    ]
        #   [   0   -   -   -   R   -   -   -    ]
        #   [   x   0   1   2   3   4   5   6    ]
        robot_location = {'x': 3, 'y': 0}
       
        query = ('rotate_180_degrees_south_of_ramp(' +
            str(robot_location['x']) + ',' + 
            str(robot_location['y']) + ',' + 
            str(self.ramp_bottom_left['x']) + ',' +
            str(self.ramp_top_right['x']) + ',' +
            str(self.ramp_bottom_left['y']) + ',' + 
            str(self.ramp_top_right['y']) + ')'
        )

        # Act
        result = bool(list(self.prolog.query(query)))

        # Assert
        self.assertFalse(result)

    def test_robot_rotate_0_when_front_center_of_ramp(self):
        # Arrange

        #   [   6   -   -   -   -   -   -   -    ]
        #   [   5   -   -   -   -   -   -   -    ]
        #   [   4   -   -   B   B   B   -   -    ]
        #   [   3   -   -   B   -   B   -   -    ]
        #   [   2   -   -   B   B   B   -   -    ]
        #   [   1   -   -   -   -   -   -   -    ]
        #   [   0   -   -   -   R   -   -   -    ]
        #   [   x   0   1   2   3   4   5   6    ]
        robot_location = {'x': 3, 'y': 0}
       
        query = ('rotate_0_degrees_north_of_ramp(' +
            str(robot_location['x']) + ',' + 
            str(robot_location['y']) + ',' + 
            str(self.ramp_bottom_left['x']) + ',' +
            str(self.ramp_top_right['x']) + ',' +
            str(self.ramp_bottom_left['y']) + ',' + 
            str(self.ramp_top_right['y']) + ')'
        )

        # Act
        result = bool(list(self.prolog.query(query)))

        # Assert
        self.assertTrue(result)

    def test_target_front_and_center_goes_to_can(self):
        # Arrange
        position = 'front_and_center'

        query = ('target({}, X)'.format(position))

        # Act
        actual = list(self.prolog.query(query))
        expected = [{'X': 'can'}]

        # Assert
        self.assertEqual(actual, expected)

    def test_target_front_and_left_goes_to_front_and_center(self):
        # Arrange
        position = 'front_and_left'

        query = ('target({}, X)'.format(position))

        # Act
        actual = list(self.prolog.query(query))
        expected = [{'X': 'front_and_center'}]

        # Assert
        self.assertEqual(actual, expected)

    def test_direction_front_and_left_goes_east(self):
        # Arrange
        position = 'front_and_left'

        query = ('direction({}, X)'.format(position))

        # Act
        actual = list(self.prolog.query(query))
        expected = [{'X': 'east'}]

        # Assert
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()

