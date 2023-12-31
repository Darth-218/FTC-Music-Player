#include "stdlib.h"

int main() {
  int exit_code;
  exit_code = system("./.venv/bin/python3 ./main.py");
  return exit_code;
}
