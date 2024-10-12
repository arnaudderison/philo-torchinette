import subprocess
import time
import sys
import os
import signal

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ORANGE = '\033[38;5;208m'

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_torch():
    torch = f'''
{Colors.YELLOW}           /|
        /\\/ |/\\
        \\  ^   | /\\  /\\
  (\\/\\  / ^   /\\/  )/^ )
   \\  \\/^ /\\       ^  /
    )^       ^ \\     (
   (   ^   ^      ^\\  )
    \\___\\/____/______/{Colors.ENDC}
    {Colors.ORANGE}[________________]
     |              |
     |     {Colors.RED}//\\\\{Colors.ORANGE}     |
     |    {Colors.RED}<<{Colors.YELLOW}(){Colors.RED}>{Colors.ORANGE}    |
     |     {Colors.RED}\\\\/{Colors.YELLOW}/{Colors.ORANGE}     |
      \\____________/
          |    |
          |    |
          |    |
          |    |
          |    |
          |    |
          |    |{Colors.ENDC}

{Colors.BOLD}{Colors.ORANGE}aderison alias TheTorch...{Colors.ENDC}
    '''
    print(torch)

def print_colored(text, color):
    print(f"{color}{text}{Colors.ENDC}")

def print_result(success, message):
    emoji = "✅" if success else "❌"
    color = Colors.OKGREEN if success else Colors.FAIL
    print_colored(f"{emoji} {message}", color)

def check_norm():
    result = subprocess.run(["norminette"], capture_output=True, text=True)
    success = "Error" not in result.stdout
    message = "Norm check passed" if success else "Code does not comply with the norm"
    print_result(success, message)
    return success

def compile_project():
    result = subprocess.run(["make"], capture_output=True, text=True)
    success = result.returncode == 0
    message = "Project compiled successfully" if success else "Compilation failed"
    print_result(success, message)
    return success

def run_test(test_number, command, expected, timeout=60):
    print_colored(f"\nTest {test_number}: {command}", Colors.BOLD)
    try:
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, preexec_fn=os.setsid)
        stdout, stderr = process.communicate(timeout=timeout)
        
        if process.returncode != 0:
            print_result(False, f"Program terminated with an error (code {process.returncode})")
            return False
        
    except subprocess.TimeoutExpired:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        print_result(False, "Program did not finish within the time limit")
        return False
    except Exception as e:
        print_result(False, f"An error occurred: {str(e)}")
        return False

    counts = {
        'deaths': stdout.lower().count("died"),
        'meals': stdout.lower().count("is eating"),
        'sleeps': stdout.lower().count("is sleeping"),
        'thinks': stdout.lower().count("is thinking")
    }

    success = all(counts[key] == expected[key] for key in expected)
    
    if success:
        print_result(True, "All counters match the expected values")
    else:
        print_result(False, "Some counters do not match the expected values")
        print("\nDetails:")
        for key in expected:
            status = "OK" if counts[key] == expected[key] else "ERROR"
            color = Colors.OKGREEN if counts[key] == expected[key] else Colors.FAIL
            print_colored(f"  {key.capitalize():8} : {counts[key]:3} (actual) vs {expected[key]:3} (expected) - {status}", color)
    
    return success

def run_segfault_test(command, description):
    print_colored(f"\n{description}: {command}", Colors.BOLD)
    try:
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, preexec_fn=os.setsid)
        stdout, stderr = process.communicate(timeout=5)
        
        if process.returncode < 0:
            print_result(True, f"Program terminated with signal {-process.returncode}")
            return True
        elif process.returncode > 0:
            print_result(True, f"Program terminated with an error (code {process.returncode})")
            return True
        else:
            print_result(False, "Program terminated normally when an error was expected")
            return False
        
    except subprocess.TimeoutExpired:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        print_result(False, "Program did not finish within the time limit")
        return False
    except Exception as e:
        print_result(True, f"An error occurred: {str(e)}")
        return True

def main():
    clear_terminal()
    print_torch()
    print_colored("🧠 Tester for Philosopher Project 🍽", Colors.HEADER)
    time.sleep(2)

    norm_success = check_norm()
    compile_success = compile_project()

    if not (norm_success and compile_success):
        print_colored("\n⚠️ Warning: Norm check failed or compilation failed.", Colors.WARNING)
        print_colored("Tests will still be executed, but results may be affected.", Colors.WARNING)

    tests = [
        ("1", "./philo 1 800 200 200", {'deaths': 1, 'meals': 0, 'sleeps': 0, 'thinks': 0}),
        ("2", "./philo 5 800 200 200 7", {'deaths': 0, 'meals': 35, 'sleeps': 35, 'thinks': 35}),
        ("3", "./philo 4 410 200 200 20", {'deaths': 0, 'meals': 80, 'sleeps': 80, 'thinks': 80}),
        ("4", "./philo 2 125 60 60 100", {'deaths': 0, 'meals': 200, 'sleeps': 200, 'thinks': 200}),
        ("5", "./philo 5 800 211 600", {'deaths': 1, 'meals': 5, 'sleeps': 5, 'thinks': 0}),
    ]

    segfault_tests = [
        ("./philo 0 800 200 200", "Test with 0 philosophers"),
        ("./philo -1 800 200 200", "Test with a negative number of philosophers"),
        ("./philo 5 -800 200 200", "Test with a negative time"),
        ("./philo 5 800 200 200 0", "Test with 0 meals"),
        ("./philo", "Test without arguments"),
        ("./philo 5 800 200", "Test with too few arguments"),
        ("./philo 5 800 200 200 7 10", "Test with too many arguments"),
        ("./philo 2147483648 800 200 200", "Test with a number of philosophers that's too large"),
    ]

    print_colored("\n🧪 Functional Tests", Colors.BOLD)
    functional_successes = sum(run_test(*test) for test in tests)

    print_colored("\n💥 CRASH Tests", Colors.BOLD)
    segfault_successes = sum(run_segfault_test(*test) for test in segfault_tests)

    total_tests = len(tests) + len(segfault_tests)
    total_successes = functional_successes + segfault_successes

    print_colored(f"\n📊 Final Results: {total_successes}/{total_tests} tests passed", Colors.BOLD)
    if total_successes == total_tests:
        print_colored("🎉 All tests passed!", Colors.OKGREEN)
    elif total_successes == 0:
        print_colored("💔 All tests failed.", Colors.FAIL)
    else:
        print_colored("🤔 Some tests failed.", Colors.WARNING)

if __name__ == "__main__":
    main()