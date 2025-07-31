from manim import *
import numpy as np

class LLMOverview(Scene):
    def construct(self):
        # Title
        title = Text("Large Language Model Overview", font_size=42, color=BLUE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(1)
        
        # Show the complete pipeline
        self.show_tokenization()
        self.show_embeddings()
        self.show_transformer_stack()
        self.show_generation()
        
        self.wait(2)
    
    def show_tokenization(self):
        # Tokenization process
        tokenization_title = Text("Step 1: Tokenization", font_size=32, color=YELLOW)
        tokenization_title.move_to(UP * 2.5)
        self.play(Write(tokenization_title))
        
        # Input text
        input_text = Text('"Hello world"', font_size=28, color=GREEN)
        input_text.move_to(UP * 1)
        
        # Arrow
        arrow1 = Arrow(UP * 0.5, DOWN * 0.5, color=WHITE)
        
        # Tokens
        token_boxes = []
        tokens = ["Hello", "world"]
        
        for i, token in enumerate(tokens):
            box = RoundedRectangle(
                width=1.5,
                height=0.8,
                corner_radius=0.1,
                color=BLUE,
                fill_opacity=0.3
            )
            box.move_to(LEFT * 1.5 + RIGHT * (i * 2) + DOWN * 1.5)
            
            token_text = Text(token, font_size=20, color=WHITE)
            token_text.move_to(box.get_center())
            
            token_boxes.append({'box': box, 'text': token_text})
        
        self.play(Write(input_text))
        self.play(Create(arrow1))
        
        for token_data in token_boxes:
            self.play(
                Create(token_data['box']),
                Write(token_data['text']),
                run_time=0.5
            )
        
        self.wait(1)
        
        # Store for later
        self.tokenization_objects = [tokenization_title, input_text, arrow1] + \
                                  [td['box'] for td in token_boxes] + \
                                  [td['text'] for td in token_boxes]
    
    def show_embeddings(self):
        # Clear tokenization
        self.play(*[FadeOut(obj) for obj in self.tokenization_objects])
        
        # Embeddings title
        embedding_title = Text("Step 2: Token Embeddings", font_size=32, color=YELLOW)
        embedding_title.move_to(UP * 2.5)
        self.play(Write(embedding_title))
        
        # Token to vector conversion
        token_box = RoundedRectangle(
            width=1.5,
            height=0.8,
            corner_radius=0.1,
            color=BLUE,
            fill_opacity=0.3
        )
        token_box.move_to(LEFT * 3 + UP * 0.5)
        
        token_text = Text("Hello", font_size=20, color=WHITE)
        token_text.move_to(token_box.get_center())
        
        # Arrow
        arrow = Arrow(LEFT * 1.5, RIGHT * 1.5, color=WHITE)
        arrow.move_to(UP * 0.5)
        
        # Embedding vector
        vector_elements = []
        values = [0.2, -0.1, 0.8, 0.3]
        
        for i, val in enumerate(values):
            element = Text(f"{val}", font_size=16, color=GREEN)
            element.move_to(RIGHT * 3 + UP * (1 - i * 0.4))
            vector_elements.append(element)
        
        # Vector bracket
        bracket = Text("[", font_size=40, color=WHITE)
        bracket.move_to(RIGHT * 2.5 + UP * 0.3)
        
        bracket_close = Text("]", font_size=40, color=WHITE)
        bracket_close.move_to(RIGHT * 3.5 + UP * 0.3)
        
        self.play(Create(token_box), Write(token_text))
        self.play(Create(arrow))
        self.play(Write(bracket), Write(bracket_close))
        
        for element in vector_elements:
            self.play(Write(element), run_time=0.3)
        
        # Positional encoding
        pos_title = Text("+ Positional Encoding", font_size=24, color=ORANGE)
        pos_title.move_to(DOWN * 1)
        self.play(Write(pos_title))
        
        self.wait(2)
        
        # Store objects
        self.embedding_objects = [embedding_title, token_box, token_text, arrow, bracket, bracket_close] + \
                               vector_elements + [pos_title]
    
    def show_transformer_stack(self):
        # Clear embeddings
        self.play(*[FadeOut(obj) for obj in self.embedding_objects])
        
        # Transformer stack title
        transformer_title = Text("Step 3: Transformer Layers", font_size=32, color=YELLOW)
        transformer_title.move_to(UP * 3)
        self.play(Write(transformer_title))
        
        # Create transformer layers
        layers = []
        layer_names = [
            "Multi-Head\nAttention",
            "Feed Forward\nNetwork",
            "Multi-Head\nAttention",
            "Feed Forward\nNetwork"
        ]
        colors = [BLUE, PURPLE, BLUE, PURPLE]
        
        for i, (name, color) in enumerate(zip(layer_names, colors)):
            layer_box = RoundedRectangle(
                width=3,
                height=1,
                corner_radius=0.1,
                color=color,
                fill_opacity=0.3
            )
            layer_box.move_to(UP * (1.5 - i * 0.8))
            
            layer_text = Text(name, font_size=14, color=WHITE)
            layer_text.move_to(layer_box.get_center())
            
            layers.append({'box': layer_box, 'text': layer_text})
        
        # Animate layer creation
        for layer in layers:
            self.play(
                Create(layer['box']),
                Write(layer['text']),
                run_time=0.5
            )
        
        # Add skip connections
        skip_connections = []
        for i in range(0, len(layers), 2):
            if i + 1 < len(layers):
                start_point = layers[i]['box'].get_right()
                end_point = layers[i+1]['box'].get_right()
                
                # Curved arrow for skip connection
                skip_arrow = CurvedArrow(
                    start_point,
                    end_point,
                    angle=PI/3,
                    color=YELLOW,
                    stroke_width=2
                )
                skip_connections.append(skip_arrow)
                self.play(Create(skip_arrow), run_time=0.3)
        
        # Add data flow arrows
        flow_arrows = []
        for i in range(len(layers) - 1):
            arrow = Arrow(
                layers[i]['box'].get_bottom(),
                layers[i+1]['box'].get_top(),
                buff=0.1,
                color=WHITE,
                stroke_width=2
            )
            flow_arrows.append(arrow)
            self.play(Create(arrow), run_time=0.2)
        
        self.wait(2)
        
        # Store objects
        self.transformer_objects = [transformer_title] + \
                                 [l['box'] for l in layers] + \
                                 [l['text'] for l in layers] + \
                                 skip_connections + flow_arrows
    
    def show_generation(self):
        # Clear transformer stack
        self.play(*[FadeOut(obj) for obj in self.transformer_objects])
        
        # Generation title
        generation_title = Text("Step 4: Next Token Generation", font_size=32, color=YELLOW)
        generation_title.move_to(UP * 2.5)
        self.play(Write(generation_title))
        
        # Output layer
        output_layer = Rectangle(
            width=4,
            height=1,
            color=RED,
            fill_opacity=0.3
        )
        output_layer.move_to(UP * 1)
        
        output_label = Text("Output Layer", font_size=20, color=RED)
        output_label.move_to(output_layer.get_center())
        
        self.play(Create(output_layer), Write(output_label))
        
        # Probability distribution
        prob_title = Text("Probability Distribution", font_size=24, color=WHITE)
        prob_title.move_to(DOWN * 0.5)
        self.play(Write(prob_title))
        
        # Sample probabilities
        words = ["the", "cat", "dog", "house"]
        probs = [0.4, 0.3, 0.2, 0.1]
        
        bars = []
        for i, (word, prob) in enumerate(zip(words, probs)):
            # Probability bar
            bar = Rectangle(
                width=prob * 4,
                height=0.3,
                color=interpolate_color(RED, GREEN, prob),
                fill_opacity=0.8
            )
            bar.move_to(LEFT * 2 + RIGHT * (prob * 2) + DOWN * (1.5 + i * 0.5))
            
            # Word label
            word_label = Text(word, font_size=16, color=WHITE)
            word_label.move_to(LEFT * 3.5 + DOWN * (1.5 + i * 0.5))
            
            # Probability label
            prob_label = Text(f"{prob:.1f}", font_size=14, color=WHITE)
            prob_label.move_to(bar.get_right() + RIGHT * 0.3)
            
            bars.append({'bar': bar, 'word': word_label, 'prob': prob_label})
        
        for bar_data in bars:
            self.play(
                Create(bar_data['bar']),
                Write(bar_data['word']),
                Write(bar_data['prob']),
                run_time=0.5
            )
        
        # Selection
        selection = Text("Selected: 'the'", font_size=24, color=GREEN)
        selection.to_edge(DOWN, buff=1)
        self.play(Write(selection))
        
        self.wait(2)
        
        # Show autoregressive process
        self.show_autoregressive_generation()
    
    def show_autoregressive_generation(self):
        # Clear previous
        self.play(*[FadeOut(mob) for mob in self.mobjects[1:]])
        
        # Autoregressive title
        auto_title = Text("Autoregressive Generation", font_size=36, color=YELLOW)
        auto_title.move_to(UP * 3)
        self.play(Write(auto_title))
        
        # Show sequence generation
        sequence = ["Hello", "world", "how", "are", "you"]
        generated_tokens = []
        
        for i, token in enumerate(sequence):
            token_box = RoundedRectangle(
                width=1.2,
                height=0.8,
                corner_radius=0.1,
                color=BLUE,
                fill_opacity=0.3
            )
            token_box.move_to(LEFT * 4 + RIGHT * (i * 1.5) + UP * 1)
            
            token_text = Text(token, font_size=16, color=WHITE)
            token_text.move_to(token_box.get_center())
            
            generated_tokens.append({'box': token_box, 'text': token_text})
            
            # Show generation process
            if i == 0:
                # First token
                process_text = Text(f"Generate: '{token}'", font_size=20, color=GREEN)
                process_text.move_to(DOWN * 1)
                self.play(Write(process_text))
            else:
                # Subsequent tokens
                context = " ".join(sequence[:i])
                process_text = Text(f"Context: '{context}' → '{token}'", font_size=16, color=GREEN)
                process_text.move_to(DOWN * 1)
                self.play(Transform(self.mobjects[-1], process_text))
            
            # Create token
            self.play(
                Create(token_box),
                Write(token_text),
                run_time=0.8
            )
            
            self.wait(0.5)
        
        # Final explanation
        final_text = Text(
            "Each new token is generated based on all previous tokens",
            font_size=20,
            color=WHITE
        )
        final_text.to_edge(DOWN, buff=1)
        self.play(Write(final_text))
        
        self.wait(3)


class LLMCapabilities(Scene):
    def construct(self):
        title = Text("LLM Capabilities", font_size=48, color=BLUE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        
        # Capabilities list
        capabilities = [
            "Text Generation",
            "Language Translation",
            "Question Answering",
            "Code Generation",
            "Creative Writing",
            "Reasoning & Analysis"
        ]
        
        capability_objects = []
        for i, capability in enumerate(capabilities):
            cap_text = Text(f"• {capability}", font_size=24, color=WHITE)
            cap_text.move_to(UP * (2 - i * 0.6) + LEFT * 2)
            capability_objects.append(cap_text)
        
        # Animate capabilities
        for cap in capability_objects:
            self.play(Write(cap), run_time=0.5)
            self.wait(0.3)
        
        # Key insight
        insight = Text(
            "All from learning patterns in text data!",
            font_size=28,
            color=YELLOW
        )
        insight.to_edge(DOWN, buff=1)
        self.play(Write(insight))
        
        self.wait(3)