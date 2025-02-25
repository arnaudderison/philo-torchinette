# 🍽️ Tester for the Philosopher Project

![tester](./images/torch.png)
![License](https://img.shields.io/badge/license-MIT-orange)

## 📜 Description
This tester is designed to verify the proper functioning of your implementation of the Philosopher project from 42 school. It performs a series of functional tests and crash tests to ensure that your program meets the subject requirements.

## ✨ Features
- 📏 Norm check (norminette)
- 🛠️ Project compilation
- 🧪 Functional tests with various configurations
- 💥 Crash tests to verify error handling
- 🌈 Colorful and clear display of results

## 🔧 Prerequisites
- 🐍 Python 3.x
- 🔨 Make
- 📐 Norminette (installed on 42 machines)

## 📥 Installation
1. Clone this repository or copy the `philo_tester.py` file into your Philosopher project directory.

## 🚀 Usage
1. Ensure that your Makefile and source files are in the same directory as the tester.
2. Run the tester with the following command:
   ```
   python3 philo_tester.py
   ```

## 🔬 Test Details

### 🧪 Functional Tests
The tester runs a series of tests with different configurations:
1. 1️⃣ philosopher, 800ms to die, 200ms to eat, 200ms to sleep
2. 5️⃣ philosophers, 800ms to die, 200ms to eat, 200ms to sleep, 7 meals each
3. 4️⃣ philosophers, 410ms to die, 200ms to eat, 200ms to sleep, 20 meals each
4. 2️⃣ philosophers, 125ms to die, 60ms to eat, 60ms to sleep, 100 meals each
5. 5️⃣ philosophers, 800ms to die, 211ms to eat, 600ms to sleep

### 💥 Crash Tests
The tester also checks error handling with edge cases:
- 0️⃣ 0 philosopher
- ➖ Negative number of philosophers
- ⏰ Negative time
- 🍽️ 0 meals
- 🚫 No arguments
- 📉 Too few arguments
- 📈 Too many arguments
- 🔢 Number of philosophers too large

## 📊 Interpreting Results
- ✅ indicates a passed test
- ❌ indicates a failed test
- Details of failures are displayed to help you debug

### Example output:
```
🧠 Tester for Philosopher Project 🍽
✅ Norm check passed
✅ Project compiled successfully

🧪 Functional Tests
Test 1: ./philo 1 800 200 200
✅ All counters match the expected values

Test 2: ./philo 5 800 200 200 7
✅ All counters match the expected values

...

💥 CRASH Tests
Test with 0 philosophers: ./philo 0 800 200 200
✅ Program terminated with an error (code 1)

...

📊 Final Results: 13/13 tests passed
🎉 All tests passed!
```

## 📝 Notes
- ⚠️ The tester first checks the norm and compilation. Even if these steps fail, the tests will be executed.
- 🎭 Crash tests are designed to fail under certain conditions, which is normal and expected.

## 🤝 Contribution
Feel free to suggest improvements or report issues by opening an issue on the project repository.

## 👤 Author
This tester was created by aderison, aka TheTorch, to assist 42 students with their Philosopher project.

---

💡 **Tip:** Run the tester regularly during your development to quickly detect potential issues!

