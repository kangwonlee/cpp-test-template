# begin Dockerfile

FROM ghcr.io/kangwonlee/edu-base-cpp:89c465c

WORKDIR /tests/

RUN mkdir -p /tests/

COPY tests/* /tests/

# To install additional modules for this particular assignment,
#   please uncomment the following lines after adding them to requirements.txt
# COPY ./requirements.txt /app/requirements.txt
# RUN uv pip install --system --requirement /app/requirements.txt \
#     && rm /app/requirements.txt

RUN python3 -c "import pytest; import requests; import glob; files = glob.glob('/tests/test_*.py'); print('Found', len(files), 'files:', files); assert files, 'No files in /tests/!'" \
      && clang-format --version

WORKDIR /app/

# end Dockerfile
