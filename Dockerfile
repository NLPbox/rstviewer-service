
FROM nlpbox/rstviewer:2018-05-31-2

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip && \
    pip3 install hug sh

WORKDIR /opt/rstviewer_service
ADD rstviewer_hug_api.py /opt/rstviewer_service/
EXPOSE 8000

# RUN pip3 install pudb bpython # used only for debugging

ENTRYPOINT ["hug"]
CMD ["-f", "rstviewer_hug_api.py"]
