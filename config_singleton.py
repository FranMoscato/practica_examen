import yaml,os

class SingletonMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ConfigClass(metaclass=SingletonMeta):
    def load_config_data(self,file_name):
        current_dir = os.getcwd()
        folder_path = os.path.join(current_dir,file_name)
        with open(folder_path, "r") as f:
            config = yaml.safe_load(f)

        # Acceder a los valores
        self.local_fix = float(config['parameters']['local_fix'])
        self.national_fix = float(config['parameters']['national_fix'])
        self.international_fix = float(config['parameters']['international_fix'])
        self.local_var = float(config['parameters']['local_var'])
        self.national_var = float(config['parameters']['national_var'])
        self.international_var = float(config['parameters']['international_var'])


if __name__ == "__main__":
    # The client code.
    # Agg esto porque no quiero romper nada

    s1 = ConfigClass()
    s2 = ConfigClass()

    if id(s1) == id(s2):
        print("Singleton works, both variables contain the same instance.")
    else:
        print("Singleton failed, variables contain different instances.")

    s1.load_config_data("cnfig.yml")
    