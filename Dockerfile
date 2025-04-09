FROM quay.io/astronomer/astro-runtime:12.7.0

# install soda into a virtual environment
RUN python -m venv soda_venv && source soda_venv/bin/activate && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir soda-core-redshift && deactivate

# install pandas into a virtual environment
RUN python -m venv pandas_venv && source pandas_venv/bin/activate && \
    pip install --no-cache-dir requests && \
    pip install --no-cache-dir pandas && deactivate


# install s3 dependencies into a virtual environment
RUN python -m venv aws_venv && source aws_venv/bin/activate && \
    pip install --no-cache-dir s3fs && deactivate

# install dbt-redishift dependencies into a virtual environment
RUN python -m venv dbt_venv && source dbt_venv/bin/activate && \
    pip install --no-cache-dir dbt-core && \
    pip install --no-cache-dir dbt-redshift && deactivate


