from manim import *
import numpy as np

class AttentionMechanism(Scene):
    def construct(self):
        # Title
        title = Text("Attention Mechanism", font_size=48, color=BLUE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(1)
        
        # Show attention concept with human analogy
        self.show_attention_concept()
        
        # Show self-attention step by step
        self.show_self_attention()
        
        # Show multi-head attention
        self.show_multi_head_attention()
        
        self.wait(2)
    
    def show_attention_concept(self):
        # Human attention analogy
        concept_title = Text("Human Attention Analogy", font_size=36, color=YELLOW)
        concept_title.move_to(UP * 2)
        
        analogy_text = Text(
            "When reading a sentence, we focus on relevant words\n"
            "to understand the current word's meaning",
            font_size=24,
            color=WHITE
        )
        analogy_text.move_to(ORIGIN)
        
        example = Text(
            "Example: 'The cat sat on the mat'\n"
            "When processing 'sat', we pay attention to 'cat'",
            font_size=20,
            color=GREEN
        )
        example.move_to(DOWN * 1.5)
        
        self.play(Write(concept_title))
        self.play(Write(analogy_text))
        self.play(Write(example))
        self.wait(3)
        
        self.play(FadeOut(concept_title), FadeOut(analogy_text), FadeOut(example))
    
    def show_self_attention(self):
        # Self-attention title
        sa_title = Text("Self-Attention Mechanism", font_size=36, color=YELLOW)
        sa_title.move_to(UP * 3)
        self.play(Write(sa_title))
        
        # Input tokens
        tokens = ["The", "cat", "sat"]
        token_objects = []
        
        for i, token in enumerate(tokens):
            token_obj = RoundedRectangle(
                width=1.2,
                height=0.6,
                corner_radius=0.1,
                color=GREEN,
                fill_opacity=0.3
            )
            token_obj.move_to(LEFT * 4 + RIGHT * (i * 2.5) + UP * 1.5)
            
            token_text = Text(token, font_size=20, color=WHITE)
            token_text.move_to(token_obj.get_center())
            
            token_objects.append({'box': token_obj, 'text': token_text})
        
        # Create tokens
        self.play(*[Create(obj['box']) for obj in token_objects])
        self.play(*[Write(obj['text']) for obj in token_objects])
        self.wait(1)
        
        # Show Q, K, V matrices
        qkv_title = Text("Query, Key, Value Matrices", font_size=24, color=BLUE)
        qkv_title.move_to(UP * 0.5)
        self.play(Write(qkv_title))
        
        # Create Q, K, V representations
        qkv_colors = [BLUE, ORANGE, PURPLE]
        qkv_labels = ["Q (Query)", "K (Key)", "V (Value)"]
        qkv_objects = []
        
        for i, (color, label) in enumerate(zip(qkv_colors, qkv_labels)):
            # Create matrix representation
            matrix = Rectangle(
                width=3,
                height=1.5,
                color=color,
                fill_opacity=0.2
            )
            matrix.move_to(LEFT * 4 + RIGHT * (i * 4) + DOWN * 1)
            
            matrix_label = Text(label, font_size=16, color=color)
            matrix_label.next_to(matrix, UP, buff=0.1)
            
            qkv_objects.append({'matrix': matrix, 'label': matrix_label})
        
        self.play(*[Create(obj['matrix']) for obj in qkv_objects])
        self.play(*[Write(obj['label']) for obj in qkv_objects])
        self.wait(1)
        
        # Show attention computation
        self.demonstrate_attention_computation(token_objects)
    
    def demonstrate_attention_computation(self, token_objects):
        # Clear previous elements except title and tokens
        self.play(*[FadeOut(mob) for mob in self.mobjects[4:]])
        
        # Attention computation title
        comp_title = Text("Attention Computation: Q × K^T", font_size=28, color=YELLOW)
        comp_title.move_to(UP * 0.5)
        self.play(Write(comp_title))
        
        # Create attention weight matrix visualization
        attention_matrix = self.create_attention_matrix()
        attention_matrix['grid'].move_to(DOWN * 1)
        # Move all components relative to the grid
        for cell_row in attention_matrix['cells']:
            for cell in cell_row:
                cell.move_to(cell.get_center() + DOWN * 1)
        for label in attention_matrix['labels']:
            label.move_to(label.get_center() + DOWN * 1)
            
        self.play(Create(attention_matrix['grid']))
        self.play(*[Write(label) for label in attention_matrix['labels']])
        
        # Show attention weights as heatmap
        weights = [[0.1, 0.2, 0.7], [0.3, 0.6, 0.1], [0.4, 0.4, 0.2]]
        
        for i in range(3):
            for j in range(3):
                cell = attention_matrix['cells'][i][j]
                weight = weights[i][j]
                
                # Color intensity based on weight
                cell.set_fill(RED, opacity=weight)
                weight_text = Text(f"{weight:.1f}", font_size=14, color=WHITE)
                weight_text.move_to(cell.get_center())
                
                self.play(FadeIn(cell), Write(weight_text), run_time=0.3)
        
        # Explanation
        explanation = Text(
            "Higher values = More attention between tokens",
            font_size=20,
            color=WHITE
        )
        explanation.to_edge(DOWN, buff=1)
        self.play(Write(explanation))
        
        self.wait(2)
    
    def create_attention_matrix(self):
        grid_lines = []
        cells = []
        labels = []
        
        # Create 3x3 grid
        for i in range(4):
            # Vertical lines
            v_line = Line(UP * 1.5 + LEFT * 1.5 + RIGHT * i, DOWN * 1.5 + LEFT * 1.5 + RIGHT * i)
            grid_lines.append(v_line)
            
            # Horizontal lines
            h_line = Line(LEFT * 1.5 + UP * 1.5 + DOWN * i, RIGHT * 1.5 + UP * 1.5 + DOWN * i)
            grid_lines.append(h_line)
        
        # Create cells
        for i in range(3):
            row = []
            for j in range(3):
                cell = Square(side_length=1, color=WHITE, fill_opacity=0)
                cell.move_to(LEFT * 1 + RIGHT * j + UP * 1 + DOWN * i)
                row.append(cell)
            cells.append(row)
        
        # Row and column labels
        tokens = ["The", "cat", "sat"]
        for i, token in enumerate(tokens):
            # Row labels
            row_label = Text(token, font_size=16, color=WHITE)
            row_label.move_to(LEFT * 2.5 + UP * 1 + DOWN * i)
            labels.append(row_label)
            
            # Column labels
            col_label = Text(token, font_size=16, color=WHITE)
            col_label.move_to(LEFT * 1 + RIGHT * i + UP * 2.5)
            labels.append(col_label)
        
        grid = VGroup(*grid_lines)
        
        return {'grid': grid, 'cells': cells, 'labels': labels}
    
    def show_multi_head_attention(self):
        # Clear previous
        self.play(*[FadeOut(mob) for mob in self.mobjects[1:]])
        
        # Multi-head attention title
        mha_title = Text("Multi-Head Attention", font_size=36, color=YELLOW)
        mha_title.move_to(UP * 3)
        self.play(Write(mha_title))
        
        concept_text = Text(
            "Multiple attention 'heads' focus on different aspects",
            font_size=24,
            color=WHITE
        )
        concept_text.move_to(UP * 2)
        self.play(Write(concept_text))
        
        # Create multiple attention heads
        heads = []
        head_colors = [RED, BLUE, GREEN, YELLOW]
        head_names = ["Head 1\n(Syntax)", "Head 2\n(Semantics)", "Head 3\n(Position)", "Head 4\n(Context)"]
        
        for i, (color, name) in enumerate(zip(head_colors, head_names)):
            head = RoundedRectangle(
                width=2,
                height=1.5,
                corner_radius=0.1,
                color=color,
                fill_opacity=0.3
            )
            head.move_to(LEFT * 6 + RIGHT * (i * 3) + UP * 0.5)
            
            head_label = Text(name, font_size=14, color=color)
            head_label.move_to(head.get_center())
            
            heads.append({'box': head, 'label': head_label})
        
        # Animate head creation
        for head in heads:
            self.play(Create(head['box']), Write(head['label']), run_time=0.5)
        
        # Show concatenation
        concat_arrow = Arrow(UP * 0.5, DOWN * 1.5, color=WHITE)
        concat_label = Text("Concatenate", font_size=20, color=WHITE)
        concat_label.next_to(concat_arrow, RIGHT, buff=0.2)
        
        output_box = RoundedRectangle(
            width=8,
            height=1,
            corner_radius=0.1,
            color=PURPLE,
            fill_opacity=0.3
        )
        output_box.move_to(DOWN * 2)
        
        output_label = Text("Final Attention Output", font_size=20, color=PURPLE)
        output_label.move_to(output_box.get_center())
        
        self.play(Create(concat_arrow), Write(concat_label))
        self.play(Create(output_box), Write(output_label))
        
        self.wait(2)


class TransformerArchitecture(Scene):
    def construct(self):
        title = Text("Transformer Architecture", font_size=48, color=BLUE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        
        # Create simplified transformer diagram
        # Input embeddings
        input_box = Rectangle(width=3, height=0.8, color=GREEN, fill_opacity=0.3)
        input_box.move_to(DOWN * 3)
        input_label = Text("Input Embeddings", font_size=16, color=GREEN)
        input_label.move_to(input_box.get_center())
        
        # Positional encoding
        pos_box = Rectangle(width=3, height=0.8, color=ORANGE, fill_opacity=0.3)
        pos_box.next_to(input_box, UP, buff=0.2)
        pos_label = Text("+ Positional Encoding", font_size=16, color=ORANGE)
        pos_label.move_to(pos_box.get_center())
        
        # Multi-head attention layers
        attention_boxes = []
        for i in range(3):
            box = Rectangle(width=4, height=1, color=BLUE, fill_opacity=0.3)
            if i == 0:
                box.next_to(pos_box, UP, buff=0.5)
            else:
                box.next_to(attention_boxes[i-1], UP, buff=0.3)
            
            label = Text(f"Multi-Head Attention {i+1}", font_size=14, color=BLUE)
            label.move_to(box.get_center())
            
            attention_boxes.append({'box': box, 'label': label})
        
        # Output
        output_box = Rectangle(width=3, height=0.8, color=RED, fill_opacity=0.3)
        output_box.next_to(attention_boxes[-1]['box'], UP, buff=0.5)
        output_label = Text("Output", font_size=16, color=RED)
        output_label.move_to(output_box.get_center())
        
        # Animate creation
        self.play(Create(input_box), Write(input_label))
        self.play(Create(pos_box), Write(pos_label))
        
        for attention_data in attention_boxes:
            self.play(Create(attention_data['box']), Write(attention_data['label']))
        
        self.play(Create(output_box), Write(output_label))
        
        # Add arrows
        arrows = []
        components = [input_box, pos_box] + [ab['box'] for ab in attention_boxes] + [output_box]
        
        for i in range(len(components) - 1):
            arrow = Arrow(
                components[i].get_top(),
                components[i+1].get_bottom(),
                buff=0.1,
                color=WHITE
            )
            arrows.append(arrow)
            self.play(Create(arrow), run_time=0.3)
        
        self.wait(3)