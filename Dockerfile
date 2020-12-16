FROM faucet/python3:latest
MAINTAINER Pavel Lu "email@pavel.lu"

WORKDIR /rainforest

# copy the dependencies file to the working directory
COPY emu-requirements.txt .

# install dependencies
RUN pip3 install -r emu-requirements.txt

# copy the content of the local src directory to the working directory
COPY rainforest-to-pvoutput.py .
COPY startup.sh .

ENTRYPOINT ["sh", "/rainforest/startup.sh"]
