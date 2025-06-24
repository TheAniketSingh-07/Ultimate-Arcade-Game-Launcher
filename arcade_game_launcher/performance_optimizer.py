#!/usr/bin/env python3
"""
Performance Optimizer for Game Launcher
Automatically detects and fixes common performance issues
"""

import os
import sys
import json
import psutil
import platform
from typing import Dict, List, Tuple

class PerformanceOptimizer:
    """Analyzes system and optimizes launcher performance"""
    
    def __init__(self):
        self.system_info = self.get_system_info()
        self.recommendations = []
        self.config_path = "performance_config.json"
    
    def get_system_info(self) -> Dict:
        """Gather system information"""
        return {
            "cpu_count": psutil.cpu_count(),
            "memory_gb": psutil.virtual_memory().total / (1024**3),
            "platform": platform.system(),
            "python_version": sys.version_info[:2],
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent
        }
    
    def analyze_performance(self) -> List[str]:
        """Analyze system and provide recommendations"""
        recommendations = []
        
        # CPU Analysis
        if self.system_info["cpu_count"] < 4:
            recommendations.append("LOW_CPU: Reduce target FPS to 60")
            recommendations.append("LOW_CPU: Disable smooth animations")
        
        # Memory Analysis
        if self.system_info["memory_gb"] < 4:
            recommendations.append("LOW_MEMORY: Reduce cache size")
            recommendations.append("LOW_MEMORY: Disable surface caching")
        
        # Current Load Analysis
        if self.system_info["cpu_percent"] > 80:
            recommendations.append("HIGH_CPU_LOAD: Lower FPS target")
        
        if self.system_info["memory_percent"] > 80:
            recommendations.append("HIGH_MEMORY_LOAD: Enable memory management")
        
        # Platform Specific
        if self.system_info["platform"] == "Windows":
            recommendations.append("WINDOWS: Enable hardware acceleration")
        elif self.system_info["platform"] == "Linux":
            recommendations.append("LINUX: Check for graphics drivers")
        
        return recommendations
    
    def load_config(self) -> Dict:
        """Load current configuration"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self.get_default_config()
    
    def get_default_config(self) -> Dict:
        """Get default configuration"""
        return {
            "display": {
                "width": 1200,
                "height": 800,
                "target_fps": 120,
                "vsync": True,
                "hardware_acceleration": True
            },
            "performance": {
                "cache_text_surfaces": True,
                "cache_size_limit": 1000,
                "smooth_scrolling": True,
                "animation_quality": "high"
            }
        }
    
    def optimize_config(self, config: Dict) -> Dict:
        """Apply optimizations to configuration"""
        recommendations = self.analyze_performance()
        
        for rec in recommendations:
            if "LOW_CPU" in rec:
                if "Reduce target FPS" in rec:
                    config["display"]["target_fps"] = 60
                elif "Disable smooth animations" in rec:
                    config["performance"]["animation_quality"] = "low"
            
            elif "LOW_MEMORY" in rec:
                if "Reduce cache size" in rec:
                    config["performance"]["cache_size_limit"] = 500
                elif "Disable surface caching" in rec:
                    config["performance"]["cache_text_surfaces"] = False
            
            elif "HIGH_CPU_LOAD" in rec:
                config["display"]["target_fps"] = min(60, config["display"]["target_fps"])
            
            elif "HIGH_MEMORY_LOAD" in rec:
                config["performance"]["memory_management"] = True
            
            elif "WINDOWS" in rec and "hardware acceleration" in rec:
                config["display"]["hardware_acceleration"] = True
        
        return config
    
    def save_config(self, config: Dict):
        """Save optimized configuration"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"✅ Configuration saved to {self.config_path}")
        except Exception as e:
            print(f"❌ Failed to save config: {e}")
    
    def print_system_info(self):
        """Print system information"""
        print("🖥️  System Information:")
        print(f"   Platform: {self.system_info['platform']}")
        print(f"   CPU Cores: {self.system_info['cpu_count']}")
        print(f"   Memory: {self.system_info['memory_gb']:.1f} GB")
        print(f"   Python: {'.'.join(map(str, self.system_info['python_version']))}")
        print(f"   CPU Usage: {self.system_info['cpu_percent']:.1f}%")
        print(f"   Memory Usage: {self.system_info['memory_percent']:.1f}%")
    
    def print_recommendations(self, recommendations: List[str]):
        """Print optimization recommendations"""
        if not recommendations:
            print("✅ No optimizations needed - system looks good!")
            return
        
        print("\n🔧 Performance Recommendations:")
        for rec in recommendations:
            print(f"   • {rec.split(': ', 1)[1] if ': ' in rec else rec}")
    
    def run_optimization(self):
        """Run full optimization process"""
        print("🚀 Performance Optimizer for Game Launcher")
        print("=" * 50)
        
        # Show system info
        self.print_system_info()
        
        # Analyze performance
        recommendations = self.analyze_performance()
        self.print_recommendations(recommendations)
        
        # Load and optimize config
        config = self.load_config()
        optimized_config = self.optimize_config(config)
        
        # Show changes
        if config != optimized_config:
            print("\n⚙️  Configuration Changes:")
            self.show_config_diff(config, optimized_config)
            
            # Save optimized config
            self.save_config(optimized_config)
        else:
            print("\n✅ Configuration is already optimized!")
        
        print("\n🎮 Optimization complete! Restart the launcher to apply changes.")
    
    def show_config_diff(self, old_config: Dict, new_config: Dict):
        """Show configuration differences"""
        def compare_dict(old_dict, new_dict, prefix=""):
            for key, new_value in new_dict.items():
                old_value = old_dict.get(key)
                current_key = f"{prefix}.{key}" if prefix else key
                
                if isinstance(new_value, dict) and isinstance(old_value, dict):
                    compare_dict(old_value, new_value, current_key)
                elif old_value != new_value:
                    print(f"   {current_key}: {old_value} → {new_value}")
        
        compare_dict(old_config, new_config)

def main():
    """Main function"""
    try:
        optimizer = PerformanceOptimizer()
        optimizer.run_optimization()
    except ImportError as e:
        if "psutil" in str(e):
            print("Installing psutil for system analysis...")
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
            print("Please run the optimizer again.")
        else:
            print(f"Import error: {e}")
    except Exception as e:
        print(f"Optimization error: {e}")

if __name__ == "__main__":
    main()
