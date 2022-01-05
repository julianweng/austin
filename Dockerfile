ARG BASE_CONTAINER=jupyter/base-notebook:python-3.8.6
FROM $BASE_CONTAINER

LABEL author="Julian Weng"
USER root

RUN pip3 install --upgrade pip==20.2
RUN conda install ujson==1.35 PyTorch==1.8.0 -y
RUN pip3 install transformers==4.8.2 PyDictionary bs4 lxml mathparse discord click==7.1.1
RUN pip3 install rasa-x==0.39.3 --extra-index-url https://pypi.rasa.com/simple
RUN pip3 install spacy==3.0.6
RUN pip3 install sentence-transformers==2.1.0
RUN pip3 install sympy==1.9
RUN pip3 install pandas==1.3.4
RUN spacy download en_core_web_md;

# Switch back to jovyan to avoid accidental container runs as root
USER $NB_UID