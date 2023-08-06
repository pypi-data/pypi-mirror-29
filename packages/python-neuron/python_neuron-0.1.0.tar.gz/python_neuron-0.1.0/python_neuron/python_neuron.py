# -*- coding: utf-8 -*-

"""Main module."""
class Neuron(object):
    """
    Create your own neurons and send messages between them
    
    Dendrite (int) = Branched protoplasmic prolongation of the nerve cell
    type_neuron (str) = According to their function, neurons can be classified as sensory, motor or interneuron.
    remaining_life (float)= remaining useful life percentage of your neuron     
    """
    
    def __init__(self, name='owner_name', dendrite=100, type_neuron='sensory', remaining_life=100):
        self.name = name
        self.dendrite = dendrite
        self.type_neuron = type_neuron
        self.remaining_life = remaining_life
        
    def __str__(self):
        return ("The {} have a neuron with {} branches, with function {} and {}% remaining life").format(self.name, self.dendrite, self.type_neuron, self.remaining_life)  
  
    def evolution(self, percentage):
        return ("{} your neuron is now {}% artificial").format(self.name, percentage)
    
    def synapse(self, n, message):
        return ('{} the message from your neuron 1: {} to neuron 2: {} is: {} ').format(self.name,self.type_neuron, n.type_neuron, message)