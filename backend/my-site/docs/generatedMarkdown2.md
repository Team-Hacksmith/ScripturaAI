```cpp
#include <iostream>
#include <chrono>
#include <thread>
#include <mutex>
#include <vector>

std::mutex vecMutex;

void add_to_vector(std::vector<int> &numbers, int value)
{
    std::lock_guard<std::mutex> guard(vecMutex);
    numbers.push_back(value);
}

void print_vector(const std::vector<int> &numbers)
{
    std::lock_guard<std::mutex> guard(vecMutex);
    for (const auto &ae : numbers)
        std::cout << ae << " ";
    std::cout << "\n";
}

int main()
{
    std::vector<int> numbers;
    std::thread t1(add_to_vector, std::ref(numbers), 1);
    std::thread t2(add_to_vector, std::ref(numbers), 2);
    t1.join();
    t2.join();
    std::thread t3(print_vector, std::ref(numbers));
    t3.join();
    return 0;
}
```

This code demonstrates multithreading in C++ using the `std::thread` class and a mutex to protect shared data.

- A mutex (mutual exclusion) is a synchronization primitive that ensures that only one thread can access a shared resource at a time.
- The `vecMutex` mutex is used to protect the `numbers` vector from concurrent access by multiple threads.
- The `add_to_vector` function adds a value to the `numbers` vector, and the `print_vector` function prints the contents of the vector.
- In the `main` function, two threads (`t1` and `t2`) are created to concurrently add values to the `numbers` vector.
- After the first two threads have finished, a third thread (`t3`) is created to print the contents of the vector.
- The `join` method is used to wait for each thread to finish before proceeding to the next thread.

This code demonstrates how to use multithreading to perform tasks concurrently, and how to use a mutex to protect shared data from concurrent access.