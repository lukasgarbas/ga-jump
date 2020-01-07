from ga import GeneticAlgorithm
from figure import Polygon, Figure
from display import Display
from simulation import Simulation


# Parameters for Genetic algorithm
population_size = 50
num_generations = 150

# Runtime for a single simulation (in seconds)
sim_runtime = 8.6

# Creating polygons for the figure
center_poly = Polygon((0, 0), (20, 0), (30, 35), (-10, 30))
left_poly = Polygon((30,35), (100,45), (70, 60), (50, 60), mass=0.1)
right_poly = Polygon((-10, 30), (-20, 50), (-80, 40), (-30, 25), mass=0.1)

# Creating the figure out of 3 polygons
fig = Figure()
fig.create_center_poly(center_poly)
fig.create_left_poly(left_poly)
fig.create_right_poly(right_poly)

# Running Genetic algorithm with our figure
print('---Running GA for {} generations---'.format(num_generations))
ga = GeneticAlgorithm(fig, population_size, num_generations, sim_runtime)
ga.run()
actions = ga.best_individual.actions

# Displaying the simulation using actions calculated by GA
label = 'Generation ' + str(num_generations)
d = Display(actions, fig, label, sim_runtime)

print('----Displaying best individual----')
start_display = input("Enter 'S' to display: ")
if start_display.lower() == 's':
    d.display_simulation()
print('Score: {}'.format(int(d.get_score())))
