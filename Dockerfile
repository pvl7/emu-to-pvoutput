FROM faucet/python3:latest
LABEL Pavel Lu "email@pavel.lu"

WORKDIR /opt/emu-to-pvoutput

# copy the dependencies file to the working directory
COPY emu-requirements.txt .

# install dependencies
RUN pip3 install -r emu-requirements.txt

# copy the content of the local src directory to the working directory
COPY rainforest-to-pvoutput.py .
COPY startup.sh .

ENTRYPOINT ["sh", "/opt/emu-to-pvoutput/startup.sh"]
