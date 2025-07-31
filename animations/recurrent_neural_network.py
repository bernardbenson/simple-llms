from manim import *
import numpy as np

class RecurrentNeuralNetwork(Scene):
    def construct(self):
        # Title
        title = Text("Recurrent Neural Network (RNN)", font_size=42, color=BLUE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(1)
        
        # Show the concept of memory first
        self.show_memory_concept()
        
        # Show RNN cell
        self.show_rnn_cell()
        
        # Show unrolled RNN
        self.show_unrolled_rnn()
        
        # Demonstrate sequence processing
        self.demonstrate_sequence_processing()
        
        self.wait(2)
    
    def show_memory_concept(self):
        # Memory concept explanation
        memory_text = Text("Key Concept: Memory", font_size=36, color=YELLOW)
        memory_text.move_to(ORIGIN)
        
        explanation = Text(
            "RNNs can remember information from previous inputs",
            font_size=24,
            color=WHITE
        )
        explanation.next_to(memory_text, DOWN, buff=0.5)
        
        self.play(Write(memory_text))
        self.play(Write(explanation))
        self.wait(2)
        
        self.play(FadeOut(memory_text), FadeOut(explanation))
    
    def show_rnn_cell(self):
        # Create RNN cell
        rnn_cell = RoundedRectangle(
            width=2,
            height=1.5,
            corner_radius=0.2,
            color=BLUE,
            fill_opacity=0.3
        )
        rnn_cell.move_to(ORIGIN)
        
        # RNN label
        rnn_label = Text("RNN", font_size=24, color=WHITE)
        rnn_label.move_to(rnn_cell.get_center())
        
        # Input arrow
        input_arrow = Arrow(LEFT * 3, rnn_cell.get_left(), color=GREEN)
        input_label = Text("Input\nx(t)", font_size=20, color=GREEN)
        input_label.next_to(input_arrow, LEFT, buff=0.2)
        
        # Output arrow
        output_arrow = Arrow(rnn_cell.get_right(), RIGHT * 3, color=RED)
        output_label = Text("Output\nh(t)", font_size=20, color=RED)
        output_label.next_to(output_arrow, RIGHT, buff=0.2)
        
        # Hidden state feedback loop
        feedback_start = rnn_cell.get_top() + UP * 0.5
        feedback_end = rnn_cell.get_left() + LEFT * 0.5
        
        feedback_path = CurvedArrow(
            feedback_start,
            feedback_end,
            angle=-TAU/3,
            color=YELLOW,
            stroke_width=3
        )
        
        hidden_label = Text("Hidden State\nh(t-1)", font_size=16, color=YELLOW)
        hidden_label.next_to(feedback_path.get_top(), UP, buff=0.2)
        
        # Animate creation
        self.play(Create(rnn_cell), Write(rnn_label))
        self.play(
            Create(input_arrow), Write(input_label),
            Create(output_arrow), Write(output_label)
        )
        self.play(Create(feedback_path), Write(hidden_label))
        
        self.wait(2)
        
        # Store for later use
        self.rnn_components = {
            'cell': rnn_cell,
            'label': rnn_label,
            'input_arrow': input_arrow,
            'input_label': input_label,
            'output_arrow': output_arrow,
            'output_label': output_label,
            'feedback': feedback_path,
            'hidden_label': hidden_label
        }
    
    def show_unrolled_rnn(self):
        # Clear previous
        self.play(*[FadeOut(comp) for comp in self.rnn_components.values()])
        
        # Create unrolled RNN
        subtitle = Text("Unrolled RNN Through Time", font_size=32, color=YELLOW)
        subtitle.move_to(UP * 2.5)
        self.play(Write(subtitle))
        
        # Create time steps
        time_steps = 4
        cells = []
        connections = []
        
        for t in range(time_steps):
            # RNN cell
            cell = RoundedRectangle(
                width=1.5,
                height=1.2,
                corner_radius=0.1,
                color=BLUE,
                fill_opacity=0.3
            )
            cell.move_to(LEFT * 4 + RIGHT * (t * 2.5))
            
            # Time label
            time_label = Text(f"t={t}", font_size=16, color=WHITE)
            time_label.move_to(cell.get_center())
            
            # Input
            input_circle = Circle(radius=0.2, color=GREEN, fill_opacity=0.8)
            input_circle.move_to(cell.get_center() + DOWN * 1.5)
            
            input_text = Text(f"x{t}", font_size=14, color=GREEN)
            input_text.move_to(input_circle.get_center())
            
            # Output
            output_circle = Circle(radius=0.2, color=RED, fill_opacity=0.8)
            output_circle.move_to(cell.get_center() + UP * 1.5)
            
            output_text = Text(f"h{t}", font_size=14, color=RED)
            output_text.move_to(output_circle.get_center())
            
            # Input arrow
            input_arrow = Arrow(
                input_circle.get_top(),
                cell.get_bottom(),
                buff=0.1,
                color=GREEN,
                stroke_width=2
            )
            
            # Output arrow
            output_arrow = Arrow(
                cell.get_top(),
                output_circle.get_bottom(),
                buff=0.1,
                color=RED,
                stroke_width=2
            )
            
            cells.append({
                'cell': cell,
                'time_label': time_label,
                'input_circle': input_circle,
                'input_text': input_text,
                'output_circle': output_circle,
                'output_text': output_text,
                'input_arrow': input_arrow,
                'output_arrow': output_arrow
            })
            
            # Hidden state connection (except for first cell)
            if t > 0:
                connection = Arrow(
                    cells[t-1]['cell'].get_right(),
                    cell.get_left(),
                    buff=0.1,
                    color=YELLOW,
                    stroke_width=3
                )
                connections.append(connection)
        
        # Animate creation
        for i, cell_components in enumerate(cells):
            self.play(
                *[Create(comp) for comp in cell_components.values()],
                run_time=0.5
            )
            if i < len(connections):
                self.play(Create(connections[i]), run_time=0.3)
        
        self.wait(2)
        
        # Store for sequence demo
        self.unrolled_cells = cells
        self.connections = connections
        self.subtitle = subtitle
    
    def demonstrate_sequence_processing(self):
        # Clear and set up for sequence demo
        self.play(*[FadeOut(mob) for mob in self.mobjects[1:]])  # Keep title
        
        # Demo title
        demo_title = Text("Processing Sequence: 'Hello'", font_size=32, color=YELLOW)
        demo_title.move_to(UP * 3)
        self.play(Write(demo_title))
        
        # Create sequence processing visualization
        sequence = ['H', 'e', 'l', 'l', 'o']
        time_steps = len(sequence)
        
        # Create cells for sequence
        cells = []
        hidden_states = []
        
        for t in range(time_steps):
            # Position
            x_pos = LEFT * 6 + RIGHT * (t * 3)
            
            # RNN cell
            cell = RoundedRectangle(
                width=1.8,
                height=1.5,
                corner_radius=0.1,
                color=BLUE,
                fill_opacity=0.3
            )
            cell.move_to(x_pos)
            
            # Input character
            char_text = Text(sequence[t], font_size=32, color=GREEN)
            char_text.move_to(cell.get_center() + DOWN * 2)
            
            # Hidden state visualization (changing colors/shapes)
            hidden_state = Circle(
                radius=0.4,
                color=interpolate_color(PURPLE, ORANGE, t / (time_steps - 1)),
                fill_opacity=0.6
            )
            hidden_state.move_to(cell.get_center() + UP * 2)
            
            # Time step label
            time_label = Text(f"t={t+1}", font_size=16, color=WHITE)
            time_label.next_to(cell, DOWN, buff=1.5)
            
            cells.append({
                'cell': cell,
                'char': char_text,
                'hidden': hidden_state,
                'time': time_label
            })
        
        # Animate sequence processing step by step
        for i, cell_data in enumerate(cells):
            # Show current input
            self.play(
                Create(cell_data['cell']),
                Write(cell_data['char']),
                Write(cell_data['time'])
            )
            
            # Process and show hidden state
            self.play(Create(cell_data['hidden']))
            
            # Show connection to next state if not last
            if i < len(cells) - 1:
                connection = Arrow(
                    cell_data['hidden'].get_right(),
                    cells[i+1]['cell'].get_left() + UP * 2,
                    color=YELLOW,
                    stroke_width=3
                )
                self.play(Create(connection))
            
            self.wait(0.5)
        
        # Final explanation
        final_text = Text(
            "Each hidden state carries information from all previous inputs",
            font_size=24,
            color=WHITE
        )
        final_text.to_edge(DOWN, buff=1)
        self.play(Write(final_text))
        
        self.wait(3)


class RNNProblems(Scene):
    def construct(self):
        title = Text("RNN Challenges", font_size=48, color=BLUE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        
        # Vanishing gradient problem
        problem1 = Text("1. Vanishing Gradient Problem", font_size=32, color=RED)
        problem1.move_to(UP * 1.5)
        
        explanation1 = Text(
            "Information from early time steps gets lost",
            font_size=24,
            color=WHITE
        )
        explanation1.next_to(problem1, DOWN, buff=0.3)
        
        # Long-term dependency problem
        problem2 = Text("2. Long-term Dependencies", font_size=32, color=RED)
        problem2.move_to(DOWN * 0.5)
        
        explanation2 = Text(
            "Difficulty remembering information over long sequences",
            font_size=24,
            color=WHITE
        )
        explanation2.next_to(problem2, DOWN, buff=0.3)
        
        self.play(Write(problem1))
        self.play(Write(explanation1))
        self.wait(1)
        self.play(Write(problem2))
        self.play(Write(explanation2))
        
        # Solution preview
        solution = Text("Solution: Attention Mechanism!", font_size=36, color=GREEN)
        solution.to_edge(DOWN, buff=1)
        self.play(Write(solution))
        
        self.wait(3)