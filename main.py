"""
Simple LLMs Educational Animation Suite

This module provides a collection of Manim animations to explain Large Language Models
to a general audience. The animations progress from basic neural networks through
attention mechanisms to complete LLM architectures.

Usage:
    # Render a single animation
    manim main.py BasicNeuralNetwork
    
    # Render at different quality levels
    manim -q m main.py AttentionMechanism  # Medium quality
    manim -q h main.py LLMOverview        # High quality
    
    # Render all animations in sequence
    python main.py --render-all

Animation Sequence:
    1. BasicNeuralNetwork - Fundamental concepts
    2. RecurrentNeuralNetwork - Adding memory  
    3. AttentionMechanism - The breakthrough concept
    4. LLMOverview - Putting it all together
"""

from animations.basic_neural_network import BasicNeuralNetwork, WeightVisualization
from animations.recurrent_neural_network import RecurrentNeuralNetwork, RNNProblems
from animations.transformer_attention import AttentionMechanism, TransformerArchitecture
from animations.llm_overview import LLMOverview, LLMCapabilities
import sys
import subprocess

def render_all_animations():
    """Render all animations in the educational sequence."""
    animations = [
        ("BasicNeuralNetwork", "Basic neural network concepts and forward propagation"),
        ("WeightVisualization", "How weights affect network behavior"),
        ("RecurrentNeuralNetwork", "RNNs and the concept of memory"),
        ("RNNProblems", "Limitations that led to transformer development"),
        ("AttentionMechanism", "The attention mechanism breakthrough"),
        ("TransformerArchitecture", "Complete transformer architecture"),
        ("LLMOverview", "Complete LLM pipeline from input to output"),
        ("LLMCapabilities", "What LLMs can do")
    ]
    
    print("🎬 Rendering Simple LLMs Educational Animation Suite")
    print("=" * 60)
    
    for i, (animation_class, description) in enumerate(animations, 1):
        print(f"\n📹 Rendering {i}/{len(animations)}: {animation_class}")
        print(f"   {description}")
        
        try:
            cmd = ["manim", "-q", "m", "main.py", animation_class]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"   ✅ Successfully rendered {animation_class}")
            else:
                print(f"   ❌ Failed to render {animation_class}")
                print(f"   Error: {result.stderr}")
                
        except Exception as e:
            print(f"   💥 Exception while rendering {animation_class}: {e}")
    
    print("\n🎉 Animation rendering complete!")
    print("📁 Check the 'media' folder for generated videos")

def main():
    """Main entry point for the animation suite."""
    if len(sys.argv) > 1 and sys.argv[1] == "--render-all":
        render_all_animations()
    else:
        print("🎓 Simple LLMs Educational Animation Suite")
        print("\nAvailable animations:")
        print("  • BasicNeuralNetwork - Fundamental neural network concepts")
        print("  • WeightVisualization - Weight importance demonstration")
        print("  • RecurrentNeuralNetwork - RNNs and memory")
        print("  • RNNProblems - RNN limitations")
        print("  • AttentionMechanism - The attention breakthrough")
        print("  • TransformerArchitecture - Complete transformer")
        print("  • LLMOverview - Complete LLM pipeline")
        print("  • LLMCapabilities - What LLMs can accomplish")
        print("\nUsage:")
        print("  manim main.py <AnimationName>")
        print("  python main.py --render-all")
        print("\nFor detailed scripts and concepts, see the 'materials/' folder")

if __name__ == "__main__":
    main()