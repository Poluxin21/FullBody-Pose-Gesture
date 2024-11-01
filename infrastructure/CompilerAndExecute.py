import subprocess
import os

class CppCompiler:
    def __init__(self, cpp_file, executable, include_dir, lib_name):
        self.cpp_file = cpp_file
        self.executable = executable
        self.include_dir = include_dir
        self.lib_name = lib_name

    def compile_and_run(self):
        compile_process = subprocess.run(
            ["g++", self.cpp_file, "-o", self.executable, "-I", self.include_dir, f"-l{self.lib_name}"],
            check=True
        )

        if compile_process.returncode == 0:
            print("Compilação de main.cpp concluída com sucesso.")
            driver_process = subprocess.Popen([f"./{self.executable}"])
            driver_process.wait()
        else:
            print("Erro na compilação de main.cpp.")