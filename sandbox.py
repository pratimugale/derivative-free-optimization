from optimizers.module import Optimizer, SimplexOriginal

def funct(x, y):
    return 2*x**2 + y**2 - 20

opt = Optimizer()
opt.set_function(funct)
sum = opt.call_function(y=1, x=3)

print("done")

opt.create_point()

opt = SimplexOriginal()
opt.set_function(funct)
sum = opt.call_function(y=1, x=3)
print(sum)

opt.create_first_iteration_points()
