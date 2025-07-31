from manim import *
import numpy as np

class BasicNeuralNetwork(Scene):
    def construct(self):
        # Title
        title = Text("Basic Neural Network", font_size=48, color=BLUE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(1)
        
        # Create network layers
        input_layer = self.create_layer(3, "Input Layer", LEFT * 4, GREEN)
        hidden_layer = self.create_layer(4, "Hidden Layer", ORIGIN, YELLOW)  
        output_layer = self.create_layer(2, "Output Layer", RIGHT * 4, RED)
        
        # Animate layer creation
        self.play(
            *[Create(neuron) for neuron in input_layer["neurons"]],
            Write(input_layer["label"])
        )
        self.wait(0.5)
        
        self.play(
            *[Create(neuron) for neuron in hidden_layer["neurons"]],
            Write(hidden_layer["label"])
        )
        self.wait(0.5)
        
        self.play(
            *[Create(neuron) for neuron in output_layer["neurons"]],
            Write(output_layer["label"])
        )
        self.wait(1)
        
        # Create connections
        connections = self.create_connections(input_layer, hidden_layer)
        connections.extend(self.create_connections(hidden_layer, output_layer))
        
        self.play(*[Create(line) for line in connections])
        self.wait(1)
        
        # Demonstrate forward propagation
        self.demonstrate_forward_pass(input_layer, hidden_layer, output_layer, connections)
        
        # Show activation function
        self.show_activation_function()
        
        self.wait(2)
    
    def create_layer(self, num_neurons, label_text, position, color):
        neurons = []
        spacing = 1.5
        start_y = (num_neurons - 1) * spacing / 2
        
        for i in range(num_neurons):
            neuron = Circle(radius=0.3, color=color, fill_opacity=0.8)
            neuron.move_to(position + UP * (start_y - i * spacing))
            neurons.append(neuron)
        
        label = Text(label_text, font_size=24, color=WHITE)
        label.next_to(neurons[0], UP, buff=0.5)
        if len(neurons) > 1:
            label.move_to([position[0], neurons[0].get_y() + 0.8, 0])
        
        return {"neurons": neurons, "label": label}
    
    def create_connections(self, layer1, layer2):
        connections = []
        for neuron1 in layer1["neurons"]:
            for neuron2 in layer2["neurons"]:
                line = Line(
                    neuron1.get_center(),
                    neuron2.get_center(),
                    stroke_width=1,
                    color=GRAY
                )
                connections.append(line)
        return connections
    
    def demonstrate_forward_pass(self, input_layer, hidden_layer, output_layer, connections):
        # Add input values
        input_text = Text("Input: [1, 0.5, 0.8]", font_size=20, color=WHITE)
        input_text.next_to(input_layer["label"], DOWN, buff=0.5)
        self.play(Write(input_text))
        
        # Highlight input neurons
        self.play(
            *[neuron.animate.set_fill(GREEN, opacity=1) for neuron in input_layer["neurons"]]
        )
        self.wait(0.5)
        
        # Animate signal propagation to hidden layer
        pulses = []
        for i, neuron1 in enumerate(input_layer["neurons"]):
            for neuron2 in hidden_layer["neurons"]:
                pulse = Dot(radius=0.05, color=BLUE)
                pulse.move_to(neuron1.get_center())
                pulses.append(pulse)
                self.add(pulse)
        
        # Move pulses to hidden layer
        self.play(
            *[pulse.animate.move_to(hidden_layer["neurons"][i % len(hidden_layer["neurons"])].get_center()) 
              for i, pulse in enumerate(pulses)]
        )
        
        # Remove pulses and highlight hidden neurons
        self.remove(*pulses)
        self.play(
            *[neuron.animate.set_fill(YELLOW, opacity=1) for neuron in hidden_layer["neurons"]]
        )
        self.wait(0.5)
        
        # Animate signal propagation to output layer
        pulses = []
        for neuron1 in hidden_layer["neurons"]:
            for neuron2 in output_layer["neurons"]:
                pulse = Dot(radius=0.05, color=BLUE)
                pulse.move_to(neuron1.get_center())
                pulses.append(pulse)
                self.add(pulse)
        
        self.play(
            *[pulse.animate.move_to(output_layer["neurons"][i % len(output_layer["neurons"])].get_center()) 
              for i, pulse in enumerate(pulses)]
        )
        
        # Remove pulses and highlight output neurons
        self.remove(*pulses)
        self.play(
            *[neuron.animate.set_fill(RED, opacity=1) for neuron in output_layer["neurons"]]
        )
        
        # Show output
        output_text = Text("Output: [0.7, 0.3]", font_size=20, color=WHITE)
        output_text.next_to(output_layer["label"], DOWN, buff=0.5)
        self.play(Write(output_text))
        self.wait(1)
    
    def show_activation_function(self):
        # Clear previous elements except title
        self.play(*[FadeOut(mob) for mob in self.mobjects[1:]])
        
        # Create activation function graph
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 1, 0.2],
            x_length=6,
            y_length=4,
            axis_config={"color": WHITE}
        )
        
        # Sigmoid function
        sigmoid = axes.plot(lambda x: 1 / (1 + np.exp(-x)), color=BLUE, x_range=[-4, 4])
        
        # ReLU function  
        relu = axes.plot(lambda x: max(0, x), color=RED, x_range=[-4, 4])
        
        # Labels
        sigmoid_label = Text("Sigmoid", font_size=24, color=BLUE)
        relu_label = Text("ReLU", font_size=24, color=RED)
        
        function_title = Text("Activation Functions", font_size=36, color=WHITE)
        function_title.to_edge(UP, buff=1)
        
        sigmoid_label.next_to(sigmoid, RIGHT, buff=0.5)
        relu_label.next_to(relu, RIGHT, buff=0.5)
        
        self.play(Write(function_title))
        self.play(Create(axes))
        self.play(Create(sigmoid), Write(sigmoid_label))
        self.wait(1)
        self.play(Create(relu), Write(relu_label))
        self.wait(2)


class WeightVisualization(Scene):
    def construct(self):
        title = Text("Neural Network Weights", font_size=48, color=BLUE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        
        # Create simplified 2x2 network
        input_neurons = [
            Circle(radius=0.3, color=GREEN, fill_opacity=0.8).move_to(LEFT * 3 + UP),
            Circle(radius=0.3, color=GREEN, fill_opacity=0.8).move_to(LEFT * 3 + DOWN)
        ]
        
        output_neurons = [
            Circle(radius=0.3, color=RED, fill_opacity=0.8).move_to(RIGHT * 3 + UP),
            Circle(radius=0.3, color=RED, fill_opacity=0.8).move_to(RIGHT * 3 + DOWN)
        ]
        
        # Create connections with different weights
        weights = [[0.5, 0.8], [0.3, 0.9]]
        connections = []
        weight_labels = []
        
        for i, input_neuron in enumerate(input_neurons):
            for j, output_neuron in enumerate(output_neurons):
                weight = weights[i][j]
                
                # Connection thickness represents weight strength
                line = Line(
                    input_neuron.get_center(),
                    output_neuron.get_center(),
                    stroke_width=weight * 10,
                    color=interpolate_color(BLUE, YELLOW, weight)
                )
                connections.append(line)
                
                # Weight label
                label = Text(f"{weight}", font_size=16, color=WHITE)
                label.move_to(line.get_center())
                weight_labels.append(label)
        
        # Animate creation
        self.play(*[Create(neuron) for neuron in input_neurons + output_neurons])
        self.play(*[Create(line) for line in connections])
        self.play(*[Write(label) for label in weight_labels])
        
        # Explanation text
        explanation = Text(
            "Thicker lines = Stronger connections (higher weights)",
            font_size=24,
            color=WHITE
        )
        explanation.to_edge(DOWN, buff=1)
        self.play(Write(explanation))
        
        self.wait(3)