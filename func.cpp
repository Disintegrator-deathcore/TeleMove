#define WIN_API __declspec(dllexport)
#include <iostream>
#include <vector>
#include <filesystem>

namespace fs = std::filesystem;

extern "C" WIN_API void read_dir(const char* path){
    fs::path p {path};
    std::cout << "parent_path: " << p.parent_path() << std::endl;
    std::cout << "extension: " << p.extension() << std::endl;
    std::cout << "filename: " << p.filename() << std::endl;
    std::cout << "root_name: " << p.root_name() << std::endl;
    std::cout << "has_relative_path: " << p.has_relative_path() << std::endl;
    std::cout << "has_root_directory: " << p.has_root_directory() << std::endl;
}

