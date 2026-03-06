from src.agent import Agent
from src.fitness_compiler import compile

import random
from copy import deepcopy
from collections import Counter


class Agent3(Agent):
    def __init__(
        self, 
        tag:str,
        position,
        directions: dict[str, tuple[int, int]], 
        population:int,
        generations:int,
        crossing_rate:float,
        mutation_rate:float,
        map_:dict[tuple[int, int], str],
        fitness_expression:str=None
    ):
        super().__init__(tag, position)
        self.type = 3
        self.directions = directions
        self.population = population
        self.generations = generations
        self.map = map_
        self.crossing_rate = crossing_rate
        self.mutation_rate = mutation_rate
        
        if fitness_expression is None:
            fitness_expression = (
                '((PV * -1) + '
                '(PI * -100) +'
                '(TI * -100) +'
                '(TV * 100) +'
                '(SW * -100) +'
                '(SP * -100) +'
                '(SO * 100) +'
                '(V * 1000)) / T'
                )
        self.fitness_expression = fitness_expression

    def generate_genes(self, amount: int, max_size: int) -> list[dict]:
        genes = []
        for _ in range(amount):
            gene = {
                'chromosome': [],
                'result': [],
                'pts': 0,
            }

            gene_size = random.randint(2, max_size)

            for _ in range(gene_size):
                action = random.choice(list(self.directions.keys()))
                if random.random() < 0.1:
                    gene['chromosome'].append(action.lower())
                else:
                    gene['chromosome'].append(action)
            genes.append(gene)
        
        return genes
 
    def evaluate_gene(self, gene:dict):
        position = (self.start_position[0], self.start_position[1])
        map_temp = deepcopy(self.map)
        result = []
        gold_colected = 0
        for chromosome in gene['chromosome']:
            if chromosome.islower():
                shot_position = (
                    position[0] + self.directions[chromosome.upper()][0],
                    position[1] + self.directions[chromosome.upper()][1],
                )
                if shot_position not in map_temp:
                    result.append('t')
                elif 'W' in map_temp[shot_position]:
                    result.append('T')
                    map_temp[shot_position] = map_temp[shot_position].replace('W', '')
                else:
                    result.append('t')
                continue
            position = (
                position[0] + self.directions[chromosome][0],
                position[1] + self.directions[chromosome][1],
            )
            
            if position not in map_temp:
                result.append('#')
                continue
        
            elif gold_colected > 0 and position == self.start_position:
                result.append('V')
                gold_colected = 0
                continue
            
            if 'P' in map_temp[position]:
                result.append('P')
            elif 'W' in map_temp[position]:
                result.append('W')
            elif 'O' in map_temp[position]:
                result.append('O')
            else:
                result.append(map_temp[position])
            
            if 'O' in map_temp[position]:
                gold_colected += 1
                map_temp[position] = map_temp[position].replace('O', '')
            
        gene['result'] = result

    def fitness(self, gene:dict) -> int:
        count = dict(Counter(gene['result']))
        values = {
            'PV': count.get('', 0),
            'PI': count.get('#', 0),
            'TV': count.get('T', 0),
            'TI': count.get('t', 0),
            'SW': count.get('W', 0),
            'SP': count.get('P', 0),
            'SO': count.get('O', 0),
            'V': count.get('V', 0),
            'T': len(count),
        }
        fitness_function = compile(self.fitness_expression)
        
        gene['pts'] = fitness_function(values)

    def intersection(self, max_size:int, gene_a:dict, gene_b:dict):
        cut_a = random.randint(1, (len(gene_a['chromosome']) - 1))
        cut_b = random.randint(1, (len(gene_b['chromosome']) - 1))

        gene = gene_a['chromosome'][:cut_a]
        gene.extend(gene_b['chromosome'][cut_b:])
        
        while (max_size < len(gene)) or (len(gene) < 2):
            cut_a = random.randint(0, (len(gene_a) - 1))
            cut_b = random.randint(0, (len(gene_b) - 1))

            gene = gene_a['chromosome'][:cut_a]
            gene.extend(gene_b['chromosome'][cut_b:])
        new_gene = {
            'chromosome': gene,
            'result': [],
            'pts': 0,
        }
        for i in range(len(new_gene['chromosome'])):
            if random.random() < self.mutation_rate:
                new_gene['chromosome'][i] = random.choice(list(self.directions.keys()))
        
        return new_gene

    def evolution(self):
        genes = self.generate_genes(self.population, int(len(self.map)*2))

        for g in genes:
            self.evaluate_gene(g)
            self.fitness(g)
        
        genes.sort(key=lambda g: g['pts'], reverse=True)
        
        for generation in range(self.generations):
            number_of_crossings = max(1, int(self.population*self.crossing_rate))
            number_of_crossings = number_of_crossings if number_of_crossings % 2 == 0 else number_of_crossings + 1
            
            # for i in range(int(number_of_crossings/2)):
            for _ in range(0, number_of_crossings):
                try:
                    gene_1 = random.choice(genes)
                    gene_2 = random.choice(genes)
                    son_1 = self.intersection(
                        int(len(self.map)*2),
                        gene_1,
                        gene_2,
                    )
                    son_2 = self.intersection(
                        int(len(self.map)*2),
                        gene_2,
                        gene_1,
                    )
                except IndexError:
                    continue
                self.evaluate_gene(son_1)
                self.fitness(son_1)
                genes.append(son_1)
                self.evaluate_gene(son_2)
                self.fitness(son_2)
                genes.append(son_2)

            if generation == (self.generations - 1):
                print(f'Processamento: {(generation/self.generations*100):.2f}%, Geração: {generation}, População: {len(genes)}')
            else:
                print(f'Processamento: {(generation/self.generations*100):.2f}%, Geração: {generation}, População: {len(genes)}', end='\r')
            
            genes.sort(key=lambda g: g['pts'], reverse=True)
            genes = genes[:self.population]
            
        return genes[0]
    
    def execute(self, data_position):
        if not self.action_queue:
            chromosome = self.evolution()
            for c in range(len(chromosome['chromosome'])):
                self.action_queue.append(chromosome['chromosome'][c])
                
                if 'O' in chromosome['result'][c]:
                    self.action_queue.append('x')
                
                
        
        action = self.action_queue.pop(0)
        
        if not self.action_queue:
            self.game_over = True

        return action