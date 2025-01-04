from abc import abstractmethod
import numpy as np
from typing import Callable
import inspect
import logging
import os

class Point:
    def __init__(self, f: Callable[..., float]):
        """
        Abstraction of a Point in the coordinate system made up of the parameters that the function f takes.
        Also takes in the function and is capable of storing the value of the function on this point(set of parameters).
        Args:
            f (Callable[..., float]): The function that the point needs to be evaluated on.
        """
        self.f = f
        self.num_parameters = len(inspect.signature(f).parameters)
        self.dim = self.num_parameters
        self.coordinates = np.zeros(self.dim) # initialize the point to be of the form [0] * n
        self.val_f = 0
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(f'{__name__}.{__class__.__name__}')
        if "OPTIMIZER_LOG_LEVEL" in os.environ:
            try:
                self.logger.setLevel(os.environ.get('OPTIMIZER_LOG_LEVEL'))
            except:
                self.logger.warning('''Value of the Environment variable \"OPTIMIZER_LOG_LEVEL\" is invalid. \n
                      Default to INFO''')

    def execute_function(self, *args, **kwargs) -> float:
        """
        Executes function on any arbitrary set of parameters
        Args:
            *args (tuple): The arguments that the function f takes.
            **kwargs (dict[str, Any]): The keyword arguments that the function f takes.
        Returns:
            float: The value of the function on the given arguments
        """

        return self.f(*args, **kwargs)

    def execute_function_store_value(self):
        """
        Executes function on "self" i.e. the point that the object represents.
        Stores the value in self.val_f
        Args:
            None
        Returns:
            None
        """
        self.val_f = self.execute_function(*self.coordinates)
    
    def change_coordinate(self, new_value, dim):
        """
        Changes the value of a single coordinate of the point to the value specified at the dimension 
        which is also specified as a parameter. 
        Args:
            new_value: New value of the coordinate
            dim: dimension of the coordinate that needs to be changed.
        Returns:
            None
        """
        self.coordinates[dim] = new_value
        self.execute_function_store_value()

    def set_random_coordinates(self, low: float = -1.0, high: float = -1.0):
        """
        Set some random coordinates
        Args:
            None
        Returns:
            None
        """
        if (low == high):
            self.logger.warning("Since low and high are equal (or the range of the parameters are not specified), the random value range of this point will be taken as [-10, 10] by default")
            low = -10
            high = 10
        
        for i in range(self.dim):
            self.coordinates[i] = np.random.randint(low, high)
        
        self.execute_function_store_value()
    
    def get_coordinates(self):
        return self.coordinates
    
    def print_coordinates(self):
        print(f'Coordinates: {self.coordinates}, Value: {self.val_f}')

    def set_coordinates(self, coordinates):
        if coordinates.shape != (self.num_parameters,):
            raise TypeError(f'Invalid shape of coordinates. Expected: ({self.num_parameters}, 1); Got: {coordinates.shape}')
        for i in range(self.num_parameters):
            self.coordinates[i] = coordinates[i]

        self.execute_function_store_value()


class Optimizer:
    def __init__(self):
        self.f = None
        self.num_parameters = 0
        self.num_points = 0
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(f'{__name__}.{__class__.__name__}')
        if "OPTIMIZER_LOG_LEVEL" in os.environ:
            try:
                self.logger.setLevel(os.environ.get('OPTIMIZER_LOG_LEVEL'))
            except:
                self.logger.warning('''Value of the Environment variable \"OPTIMIZER_LOG_LEVEL\" is invalid. \n
                      Default to INFO''')  
                      
    def set_function(self, f: Callable[..., float]):
        """
        set the function on which the optimization needs to be done.

        Args:
            f (Callable[..., float]): The function that evaluates its parameters and returns a float.

        Returns:
            float: The value of the function on given parameters.
        """
        self.f = f
        self.num_parameters = len(inspect.signature(f).parameters)
        self.num_points = self.num_parameters + 1  
        
    @abstractmethod
    def train(self, num_iter: int) -> float:
        """
        perform "training" in the sense of finding the the optimal value.

        Args:
            num_iter (int): The number of iterations for which the training needs to be done.

        Returns:
            float: The value of the function found after training for num_iter.
        """
        raise NotImplementedError("This method is not implemented in the Base class.")


class SimplexOriginal(Optimizer):
    def __init__(self):
        super().__init__()
        
    def sort_points(self, points):
        sorted_points_indices = np.argsort([point.val_f for point in points])
        sorted_points = points[sorted_points_indices]
        return sorted_points
    
    def create_first_iteration_points(self):
        points = np.empty(self.num_points, dtype=Point)
        for i in range(self.num_points):
            pt = Point(self.f)
            pt.set_random_coordinates()
            points[i] = pt
        sorted_points = self.sort_points(points)

        return sorted_points

    def train(self, num_iter: int):
        collected_points = []
        points = self.create_first_iteration_points()
        for point in points:
            collected_points.append(point)
        for i in range(num_iter):
            self.logger.info(f'Running {i}-th iteration')
            x_cap = self.get_x_cap(points)
            points = self.update_points(x_cap, points)
            for point in points:
                collected_points.append(point)

        return x_cap
    
    def get_x_cap(self, points):
        x_cap = np.zeros(self.num_parameters)
        for i in range (0, self.num_points-1): # take sum of the [0, n-1] points
            for j in range(0, self.num_parameters):
                x_cap[j] += points[i].get_coordinates()[j]

        for i in range (0, len(x_cap)): # multiply the total sums by 2/n
            x_cap[i] = x_cap[i] * 2 / self.num_parameters

        for i in range (0, len(x_cap)): # subtract the last (n-th) point
            x_cap[i] -= points[self.num_points-1].get_coordinates()[i]

        new_pt_x_cap = Point(self.f)
        new_pt_x_cap.set_coordinates(x_cap)
        return new_pt_x_cap
    
    def update_points(self, x_cap: Point, points: np.ndarray):
        assert isinstance(points, np.ndarray), "Input must be a NumPy array"
        assert isinstance(points.item(0), Point), "Array elements must be of type Point"
        points = self.sort_points(points)
        F_x_cap = x_cap.val_f
        
        if(F_x_cap < points[self.num_parameters - 1].val_f): # compare with the (n-1)-th variable's function value
            self.logger.debug(f'No Contraction: n-1 th point is {points[self.num_parameters - 1].val_f} and thus {F_x_cap} is smaller than it')
            points = np.delete(points, -1)
            points = np.append(points, x_cap)
            points = self.sort_points(points)
            return points
        else:
            new_points = np.empty(0, dtype=Point)
            self.logger.debug(f'Contraction: n-1 th point is {points[self.num_parameters - 1].val_f} and thus {F_x_cap} is greater than or equal to it')
            new_points = np.append(new_points, points[0])
            for i in range(1, len(points)):
                new_point = Point(self.f)
                for j in range(0, len(points) - 1):
                    new_point.change_coordinate((points[i].get_coordinates()[j] + points[0].get_coordinates()[j]) / 2, j)
                new_points = np.append(new_points, new_point)
            new_points = self.sort_points(new_points) 
            return new_points