# begin Dockerfile

FROM ghcr.io/kangwonlee/edu-base-cpp:9208e69

WORKDIR /tests/

RUN mkdir -p /tests/

COPY tests/* /tests/

RUN python3 -c "import pytest; import requests; import glob; files = glob.glob('/tests/test_*.py'); print('Found', len(files), 'files:', files); assert files, 'No files in /tests/!'" \
      && clang-format --version

WORKDIR /app/

# end Dockerfile
