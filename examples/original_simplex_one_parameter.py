from optimizers.module import SimplexOriginal

def funct(x):
    return 4*(x ** 4) - 5*(x**3) - 2*(x**2) + 2*x

opt = SimplexOriginal()
opt.set_function(funct)
minima = opt.train(20)

print(f'Found Minima: {minima.val_f} at the coordinates(centroid of simplex): {minima.coordinates}')
