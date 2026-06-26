import test_package.module_b
import test_package.module_a
from test_package.module_a import Module_a, module_a_fuc, module_var_a

def main():
        print(test_package.module_a.Module_a())
        print(test_package.module_a.module_var_a)
        test_package.module_a.module_a_fuc()
        print(test_package.module_b.Module_b())
        print(test_package.module_b.module_var_b)
        test_package.module_b.module_b_fuc()

        print(Module_a())
        print(module_var_a)
        module_a_fuc()


if __name__ == "__main__":
        main()
