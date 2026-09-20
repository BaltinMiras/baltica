# Using *args and **kwargs

def show_info(*args, **kwargs):
    print("Arguments:", args)
    print("Keyword arguments:", kwargs)


show_info("Alice", 25, city="Almaty", country="Kazakhstan")
