# Environment for the FireAndStructure notebook (Python 3.12 + geospatial packages from conda-forge).
# The data are not included; mount a local Data/ folder when running the container (see README).
FROM mambaorg/micromamba:2.9.0-debian12-slim

# Install the packages from environment.yml into the base environment, which the image activates by default
COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yml /tmp/environment.yml
RUN micromamba install -y -n base -f /tmp/environment.yml && \
    micromamba clean --all --yes

# Copy the notebook and helper modules
WORKDIR /home/mambauser/FireAndStructure
COPY --chown=$MAMBA_USER:$MAMBA_USER Data_Exploration.ipynb node_summaries.py landcover.py risk_correlations.py README.md LICENSE ./

# Start Jupyter on port 8888; the login link (with token) is printed in the container log
EXPOSE 8888
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser"]
