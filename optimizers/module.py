from abc import abstractmethod
import numpy as np
from typing import Callable, Any, Type
import inspect

class Optimizer:
    def __init__(self):
        self.f = None
        self.parameters = None
        self.num_parameters = 0
        self.num_points = 0
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
        self.num_points = self.num_parameters + 1

    def call_function(self, *args, **kwargs) -> float:
        return self.f(*args, **kwargs)

    def create_point(self):
        pt = Point(self.f)
        print("pt.point")
        print(pt.point)
        pt.change_coordinate(10, 1)
        pt.change_coordinate(10, 1)
        # self.calc_f(pt)

    # def calc_f(self, pt: "Point"):
    #     if not isinstance(pt, Point):
    #         raise TypeError("Parameter \"pt\" is not an instance of class \"Point\"")
    #     print(pt)
    #     value = self.call_function(*pt.point)
    #     print(value)
    #     pass
        
        
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
    
    def val_f(self):
        return self.val_f

    # def set_function(self, f: Callable[..., float], *args, **kwargs): # TODO: remove *args and **kwargs if not required.
    #     """
    #     set the function on which the optimization needs to be done.

    #     Args:
    #         f (Callable[..., float]): The function that evaluates its parameters and returns a float.

    #     Returns:
    #         float: The value of the function on given parameters.
    #     """
    #     self.f = f
    #     self.parameters = inspect.signature(f).parameters
    #     self.num_parameters = len(self.parameters)
    
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

    def set_values(self, coordinates):
        print(coordinates)
        if coordinates.shape != (self.num_parameters,):
            raise TypeError(f'Invalid shape of coordinates. Expected: ({self.num_parameters}, 1); Got: {coordinates.shape}')
        for i in range(self.num_parameters):
            self.point[i] = coordinates[i]

        self.calc_f()
        


class SimplexOriginal(Optimizer):
    def __init__(self):
        super().__init__()
        # self.num_points = self.num_parameters + 1

    def sort_points(self, points):
        print("points")
        print(points)
        sorted_points_indices = np.argsort([point.val_f for point in points])
        sorted_points = points[sorted_points_indices]
        return sorted_points
    
    def create_first_iteration_points(self):
        points = np.empty(self.num_points, dtype=Point)
        for i in range(self.num_points):
            pt = Point(self.f)
            pt.set_random_values()
            points[i] = pt
        
        for point in points:
            print(point.print_point_value())

        sorted_points = self.sort_points(points)
        for point in sorted_points:
            print(point.print_point_value())

        return sorted_points


    def train(self, num_iter: int):
        points = self.create_first_iteration_points()
        for i in range(num_iter):
            print(f'Running {i}-th iteration')
            x_cap = self.get_x_cap(points)
            print("x_cap.print_point_value()")
            print(type(x_cap))
            points = self.update_points(x_cap, points)
            print(points)
        
        return x_cap.val_f
    
    def get_x_cap(self, points):
        print(self.num_points)
        sum_pars = np.zeros(self.num_parameters)
        
        for i in range (0, self.num_points-1): # take sum of the [0, n-1] points
            print(i)
            for j in range(0, self.num_parameters):
                sum_pars[j] += points[i].values()[j]
        
        print("sum_pars")
        print(sum_pars)

        for i in range (0, len(sum_pars)): # multiply the total sums by 2/n
            sum_pars[i] = sum_pars[i] * 2 / self.num_parameters

        print("sum_pars")
        print(sum_pars)

        for i in range (0, len(sum_pars)): # subtract the last (n-th) point
            sum_pars[i] -= points[self.num_points-1].values()[i]

        print(sum_pars)
        new_pt = Point(self.f)
        new_pt.set_values(sum_pars)
        return new_pt
    
    def update_points(self, x_cap: Point, points: np.ndarray):
        assert isinstance(points, np.ndarray), "Input must be a NumPy array"
        assert isinstance(points.item(0), Point), "Array elements must be of type Point"
        points = self.sort_points(points)
        print("x_cap")
        print(x_cap)
        print(type(x_cap))
        F_x_cap = x_cap.val_f
        print(F_x_cap)

        # num_points = len(points)
        # num_variables = num_points - 1 

        print(points[self.num_parameters - 1])
        if(F_x_cap < points[self.num_parameters - 1].val_f): # compare with the (n-1)-th variable's function value
            print(f'n-1 th point is {points[self.num_parameters - 1]} and thus {F_x_cap} is smaller than it')
            # points.pop(-1)
            points = np.delete(points, -1)
            points = np.append(points, x_cap)
            print(points)
            points = self.sort_points(points)
            print("sorting the points again")
            print(points)
            return points
        else:
            new_points = np.empty(0, dtype=Point)
            print("new_points are this")
            print(new_points)
            print(f'Contration needs to be performed! n-1 th point is {points[self.num_parameters - 1]} and thus {F_x_cap} is greater than or equal to it')
            print("original points")
            print(points)
            new_points = np.append(new_points, points[0])
            for i in range(1, len(points)):
                new_point = Point(self.f)
                for j in range(0, len(points) - 1):
                    new_point.change_coordinate((points[i].values()[j] + points[0].values()[j]) / 2, j)
                print(new_point)
                new_points = np.append(new_points, new_point)
            new_points = self.sort_points(new_points) 
            print(new_points)
            return new_points
