// begin test/test_pointers.c

#include <malloc.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "pointers.h"


// Test that allocate_integer() returns a valid pointer.
static int test_allocate_integer_valid_pointer() {
    int *ptr = allocate_integer(10);
    if (ptr == NULL) {
        fprintf(stderr, "Test failed: allocate_integer() returned NULL\n");
        return 1; // Indicate failure
    }
    free(ptr);
    return 0; // Indicate success
}


// Test that allocate_integer() allocates the correct amount of memory.
static int test_allocate_integer_correct_size() {
    int *ptr = allocate_integer(10);
    size_t usable_size = malloc_usable_size(ptr);
    if (usable_size < sizeof(int)) {
        fprintf(stderr, "Test failed: Insufficient memory allocated\n");
        return 1;
    }
    free(ptr);
    return 0;
}


// Test that allocate_integer() sets the value of the allocated integer.
static int test_allocate_integer_set_value() {
    int *ptr = allocate_integer(10);
    if (*ptr!= 10) {
        fprintf(stderr, "Test failed: Incorrect value set in allocated memory\n");
        return 1;
    }
    free(ptr);
    return 0;
}


// Test that deallocate_integer() frees the allocated memory.
// Note: It's still difficult to directly test memory freeing.
static int test_deallocate_integer_frees_memory() {
    int *ptr = allocate_integer(10);
    deallocate_integer(ptr);
    // Add any indirect checks or assertions if possible
    return 0;
}


int main(int argc, char **argv) {
    if (argc!= 2) {
        int failed_tests = 0;
        failed_tests += test_allocate_integer_valid_pointer();
        failed_tests += test_allocate_integer_correct_size();
        failed_tests += test_allocate_integer_set_value();
        failed_tests += test_deallocate_integer_frees_memory();
        
        if (failed_tests > 0) {
            fprintf(stderr, "%d tests failed\n", failed_tests);
            return failed_tests;
        }
    }
    else {
        const char *test_function_name = argv[1];

        if (strcmp(test_function_name, "test_allocate_integer_valid_pointer") == 0) {
            return test_allocate_integer_valid_pointer();
        } else if (strcmp(test_function_name, "test_allocate_integer_correct_size") == 0) {
            return test_allocate_integer_correct_size();
        } else if (strcmp(test_function_name, "test_allocate_integer_set_value") == 0) {
            return test_allocate_integer_set_value();
        } else if (strcmp(test_function_name, "test_deallocate_integer_frees_memory") == 0) {
            return test_deallocate_integer_frees_memory();
        } else {
            fprintf(stderr, "Invalid test function name: %s\n", test_function_name);
            return 1;
        }
    }
}

// end test/test_pointers.c
