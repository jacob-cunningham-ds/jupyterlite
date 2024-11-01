import numpy as np
import os

def mag(fov, h):
    '''
    Returns the magnification given the sensor size and 
    field of view.
    '''
    for param_name, param in {'fov': fov, 'h': h}.items():
        if not isinstance(param, (float, int, np.ndarray)):
            raise ValueError(f"{param_name} must be a float, int, or ndarray, got {type(param).__name__}")
    if fov == 0:
        raise ZeroDivisionError("FOV cannot be zero, as this would cause division by zero.")
    m = h / fov
    return m


def decay(mult, r, source='point'):
    '''
    Returns the decay for a given multiplier, distance, and
    given source. kwarg source may be \'point\' or \'line\'. 
    The default is \'point\'.
    '''
    for param_name, param in {'mult': mult, 'r': r}.items():
        if not isinstance(param, (float, int, np.ndarray)):
            raise ValueError(f"{param_name} must be a float, int or ndarray, got {type(param).__name__}")
    match source:
        case 'point':
            x = 1 / r**2
        case 'line':
            x = 1 / r
        case _:
            raise ValueError(f"Source must be specified as 'point' or 'line', got {source}.")
    d = mult * x 
    return d


def life(resistance, rate):
    '''
    Returns the time given the resistance and the rate.
    '''
    for param_name, param in {'resistance': resistance, 'rate': rate}.items():
        if not isinstance(param, (float, int, np.ndarray)):
            raise ValueError(f"{param_name} must be a float, int, or ndarray, got {type(param).__name__}")
    if rate == 0:
        raise ZeroDivisionError("Rate cannot be zero, as this would cause division by zero.")
    time = resistance / rate
    return time


def working_distance(mag, image_track_length):
    '''
    Returns the object track length (aka working distance)
    given the magnification and image track length. Assumes
    thin lens.
    '''
    for param_name, param in {'mag': mag, 'image_track_length': image_track_length}.items():
        if not isinstance(param, (float, int, np.ndarray)):
            raise ValueError(f"{param_name} must be a float, int, or ndarray, got {type(param).__name__}")
    if mag == 0:
        raise ZeroDivisionError("Mag cannot be zero, as this would cause division by zero.")
    wd = image_track_length / mag
    return wd


def focal_length(do, di):
    '''
    Returns the focal length required for a given
    object distance and image distance. Assumes thin
    lens.
    '''
    for param_name, param in {'do': do, 'di': di}.items():
        if not isinstance(param, (float, int, np.ndarray)):
            raise ValueError(f"{param_name} must be a float, int, or ndarray, got {type(param).__name__}")
    if do == 0 or di == 0:
        raise ZeroDivisionError
    f = (1 / do + 1 / di)**(-1)
    return f

def input_helper(prompt):
    while True:
        value = input(prompt)
        try:
            value = float(value)
            return value
        except ValueError:
           print(f"Input must be a float or int, got {type(value).__name__}")

def source_helper():
    while True:
        value = input("Enter the source type ('point' or 'line'): ").lower()
        match value:
            case 'point' | 'line':
                return value
            case _:
                print(f"Input must be 'point' or 'line', got {value}")
                

def main():
    os.system('cls')
    while True:
        # get user input
        fov = input_helper("Enter the desired FOV: ")
        h = input_helper("Enter the sensor size: ")
        s_max = input_helper("Enter the space envelope: ")
        resistance = input_helper("Enter the resistance: ")
        rate_resistance = input_helper("Enter the rate resistance: ")
        mult = input_helper("Enter the multiplier: ")
        r = input_helper("Enter the radius: ")
        source = source_helper()
        itl = input_helper("Enter the image track length: ") # TODO add error handling for itl > s_max

        # givens dictionary
        givens_dict = {
            'FOV': fov,
            'Sensor Size': h,
            'Space': s_max,
            'Resistance': resistance,
            'Rate Resistance': rate_resistance,
            'Multiplier': mult,
            'Radius': r,
            'Source': source,
            'Image Track Length': itl}
        
        # do calculations
        m = mag(fov, h)
        decay_rate = decay(mult, r, source)
        rate_pass = rate_resistance > decay_rate
        life_expectancy = life(resistance, decay_rate)
        wd = working_distance(m, itl)
        f = focal_length(wd, itl)

        # results dictionary
        results_dict = {
            'Magnification': m,
            'Decay Rate': decay_rate,
            'Passes Rate?': rate_pass,
            'Life': life_expectancy,
            'Working Distance': wd,
            'Focal Length': f}

        # Output Summary
        print(" ")
        print("*" * 50)
        print("GIVENS")
        print("-" * 50)
        for key, value in givens_dict.items():
            print(f"{key}: {value}")
        print("-" * 50)
        print("RESULTS")
        print("-" * 50)
        for key, value in results_dict.items():
            print(f"{key}: {value}")
        print("*" * 50)

        # Prompt for loop
        print(" ")
        while True:
            again_prompt = input("Perform another run (Y/N)?: ").lower()
            match again_prompt:
                case 'y':
                    break
                case 'n':
                    return
                case _:
                    print(f"Input must be 'Y' or 'N', got {again_prompt}.")

if __name__ == '__main__':
    main()
            
        
        
        




















