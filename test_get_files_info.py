from functions.get_files_info import get_files_info
print("Current:")
print(get_files_info("calculator", "."))
print("\npkg")
print(get_files_info("calculator", "pkg"))
print("\nbin")
print(get_files_info("calculator", "/bin"))
print("\n../")
print(get_files_info("calculator", "../"))
