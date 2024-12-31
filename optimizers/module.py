from abc import abstractmethod
import numpy as np
from typing import Callable, Any, Type
import inspect

class Optimizer:
    def __init__(self):
        self.f = None
        self.parameters = None
        self.num_parameters = 0
        self.sorted_current_points = []

    def set_function(self, f: Callable[..., float], *args, **kwargs): # TODO: remove *args and **kwargs if not required.
        """
        set the function on which the optimization needs to be done.

        Args:
            f (Callable[..., float]): The function that evaluates its parameters and returns a float.

        Returns:
            float: The value of the function on given parameters.
        """
        self.f = f
        self.parameters = inspect.signature(f).parameters
        self.num_parameters = len(self.parameters)

    def call_function(self, *args, **kwargs) -> float:
        return self.f(*args, **kwargs)

    def create_point(self):
        pt = Point(self.f)
        print("pt.point")
        print(pt.point)
        pt.change_coordinate(10, 1)
        pt.change_coordinate(10, 1)
        self.calc_f(pt)

    def calc_f(self, pt: "Point"):
        if not isinstance(pt, Point):
            raise TypeError("Parameter \"pt\" is not an instance of class \"Point\"")
        print(pt)
        value = self.call_function(*pt.point)
        print(value)
        pass
        
        
    @abstractmethod
    def train(self, num_iter: int):
        raise NotImplementedError("This method is not implemented in the Base class.")

    def plot_function(self, name):
        """
        Greets the user with a personalized message.

        Args:
            name (str): The name of the person to greet.

        Returns:
            str: A greeting message.
        """
        return f"Hello, {name}! Welcome to my library."

  
class Point:
    def __init__(self, f: Callable[..., float]):
        self.f = f
        self.parameters = inspect.signature(f).parameters
        self.num_parameters = len(self.parameters)
        self.dim = self.num_parameters
        self.point = np.zeros(self.dim)
        self.val_f = 0
        # print(self.point)
    
    def call_function(self, *args, **kwargs) -> float:
        return self.f(*args, **kwargs)

    def calc_f(self):
        self.val_f = self.call_function(*self.point)
        print(self.val_f)

    def set_function(self, f: Callable[..., float], *args, **kwargs): # TODO: remove *args and **kwargs if not required.
        """
        set the function on which the optimization needs to be done.

        Args:
            f (Callable[..., float]): The function that evaluates its parameters and returns a float.

        Returns:
            float: The value of the function on given parameters.
        """
        self.f = f
        self.parameters = inspect.signature(f).parameters
        self.num_parameters = len(self.parameters)
    
    def change_coordinate(self, new_value, dim):
        self.point[dim] = new_value
        print(self.point)
        self.calc_f()

    def set_random_values(self, low: float = -1.0, high: float = -1.0):
        if (low == high):
            print("since low and high are equal, the random value range will be taken as [-10, 10] by default")
            low = -10
            high = 10
        
        for i in range(self.dim):
            self.point[i] = np.random.randint(low, high)
        
        self.calc_f()
    
    def values(self):
        return self.point
    
    def print_point_value(self):
        print(f'Coordinate: {self.point}, Value: {self.val_f}')


class SimplexOriginal(Optimizer):
    def create_first_iteration_points(self):
        num_points = self.num_parameters + 1
        points = np.empty(num_points, dtype=Point)
        for i in range(num_points):
            pt = Point(self.f)
            pt.set_random_values()
            points[i] = pt
        
        for point in points:
            print(point.print_point_value())

        sorted_points_indices = np.argsort([point.val_f for point in points])
        sorted_points = points[sorted_points_indices]

        for point in sorted_points:
            print(point.print_point_value())


    def train(self, num_iter: int):
        for i in range(num_iter):
            print(f'Running {i}-th iteration')
            x_cap = self.get_x_cap(new_points)
            print(x_cap)
            new_points = self.update_points(x_cap, new_points)
            print(new_points)
    
    def get_x_cap(self, points):
        num_points = len(points)
        num_variables = num_points - 1 
        print(num_points)
        sum_vars = [0 for _ in range(num_variables)]
        for i in range (0, num_points-1): # take sum of the [0, n-1] points
            print(i)
            for j in range(0, num_variables):
                sum_vars[j] += points[i][j]
            print(sum_vars)

        for i in range (0, len(sum_vars)): # multiply the total sums by 2/n
            sum_vars[i] = sum_vars[i] * 2 / num_variables

        for i in range (0, len(sum_vars)): # subtract the last (n-th) point
            sum_vars[i] -= points[num_points-1][i]

        print(sum_vars)
        return sum_vars