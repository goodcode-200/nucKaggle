FROM django:1.9.1-python3
COPY nuckaggle/requirement.txt /tmp/
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirement.txt
WORKDIR /usr/src/