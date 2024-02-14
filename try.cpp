#include <windows.h>
#include <iostream>
#include <vector>

int main() {
    std::wstring path = L"C:/programming/*";
    HANDLE hFindFile;
    WIN32_FIND_DATAW fd;
    std::vector<std::wstring> list_files;

    hFindFile = FindFirstFileW(path.c_str(), &fd);

    if (hFindFile != INVALID_HANDLE_VALUE){
        list_files.push_back(fd.cFileName);

        while (FindNextFileW(hFindFile, &fd)){
            list_files.push_back(fd.cFileName);
        }
        FindClose(hFindFile);
    }

    for (const auto& file : list_files) {
        std::wcout << file << std::endl;
    }

    return 0;
}
