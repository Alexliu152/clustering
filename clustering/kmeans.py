from collections import defaultdict
from math import inf
from math import sqrt
from math import pow
import random
import csv
import statistics

def point_avg(points):
    """
    Accepts a list of points, each with the same number of dimensions.
    (points can have more dimensions than 2)
    
    Returns a new point which is the center of all the points.
    """
    center = []
    for dim in range(len(points[0])):
        dim_data = []
        for p in points:
            dim_data.append(p[dim])
        center.append(statistics.mean(dim_data))
    return center


def update_centers(data_set, assignments):
    """
    Accepts a dataset and a list of assignments; the indexes 
    of both lists correspond to each other.
    Compute the center for each of the assigned groups.
    Return `k` centers in a list
    """
    centers = []
    merge_dict = defaultdict(list)
    for assignment, point in zip(assignments, data_set):
        merge_dict[assignment].append(point)

    for assignment, points in merge_dict.items():
        centers.append(point_avg(points))
    
    return centers


def assign_points(data_points, centers):
    """
    Assign points to each center
    """
    assignments = []
    for point in data_points:
        shortest = inf  # positive infinity
        shortest_index = 0
        for i in range(len(centers)):
            val = distance(point, centers[i])
            if val < shortest:
                shortest = val
                shortest_index = i
        assignments.append(shortest_index)
    return assignments


def distance(a, b):
    """
    Returns the Euclidean distance between a and b
    """
    distance = 0
    for dim in range(len(a)):
        distance += pow((a[dim] - b[dim]), 2)
    return sqrt(distance)



def generate_k(data_set, k):
    """
    Given `data_set`, which is an array of arrays,
    return a random set of k points from the data_set
    """
    return random.sample(data_set, k)


def get_list_from_dataset_file(dataset_file):
    data_set = []
    with open(dataset_file) as csv_file:
        csv_reader = csv.reader(csv_file)

        for line in csv_reader:
            row = []
            for var in line:
                row.append(int(var))
            data_set.append(row)
    return data_set


def cost_function(clustering):
    if len(clustering) == 0:
        return
    cost = 0.0
    for points in clustering.values():
        center = point_avg(points)
        for p in points:
            cost += pow(distance(p, center), 2)
    return cost


def k_means(dataset_file, k):
    dataset = get_list_from_dataset_file(dataset_file)
    k_points = generate_k(dataset, k)
    assignments = assign_points(dataset, k_points)
    old_assignments = None
    while assignments != old_assignments:
        new_centers = update_centers(dataset, assignments)
        old_assignments = assignments
        assignments = assign_points(dataset, new_centers)
    clustering = defaultdict(list)
    for assignment, point in zip(assignments, dataset):
        clustering[assignment].append(point)
    return clustering
