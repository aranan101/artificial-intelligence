import csv
import sys
import os 
from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}

cwd = os.getcwd() + 'small'
def load_data(directory = cwd):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def path(source, target, frontier = StackFrontier()):
    num_states_explored = 0
    source_id = [n for n in names[source]]
    target_id = set(n for n in names[target])
    # Create initial frontier 
    for s in source_id:
        start = Node(state = s, parent = None, action = 'person')
        frontier.add(start) 
    
    explored = set()
    
    # Loop until you find a solution 
    while True: 
        
        if frontier.empty(): 
            # If no solution then express it 
            return None 
        
        node = frontier.remove()
        num_states_explored += 1 
        if num_states_explored % 1000 == 0: 
            print(num_states_explored)
        
        if node.action == 'movie': 
            for star in movies[node.state]['stars']: 
                if star in target_id:
                    states = [star]
                    while node.parent != None: 
                        states.append(node.state)
                        node = node.parent 
                    actions.reverse()
                    states.reverse()
                    solution = []
                    for i in range(0,len(states),2): 
                        transition = (states[i], states[i+1])
                        solution.append(transition)
                    return solution, num_states_explored 

                
            
        
        explored.add(node.state)
        if node.action == 'person': 
            neighbours = list(people[node.state]['movies'])
            action = 'movie'
            
        elif node.action == 'movie': 
            neighbours = list(movies[node.state]['stars'])
            action = 'person'
        
        for n in neighbours:
            if not frontier.contains_state(n) and n not in explored: 
                child = Node(state= n, parent=node, action=action)
                frontier.add(child)
                
        
def shortest_path(source, target): 
    # Depth first search 
    dfs_solution, dfs_cost = path(source, target, frontier = StackFrontier())
    # Breadth first search 
    bfs_solution, bfs_cost = path(source, target, frontier = QueueFrontier())
    if bfs_cost < dfs_cost: 
        return bfs_solution 
    else: 
        return dfs_solution 
    


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
    

