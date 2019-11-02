# Dockerfile for a Jupyter notebook with bash-kernel.
# We needed to set up a specific Dockerfile because
# the standard binderhub procedures lead to a container that
# does not allow to include man-pages of Unix-commands.
# Those we want to have.

# Dockerfile maintained by Oliver Cordes & Thomas Erben

FROM buildpack-deps:bionic

# avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Set up locales properly
RUN apt-get -qq update && \
    apt-get -qq install --yes --no-install-recommends locales > /dev/null && \
    apt-get -qq purge && \
    apt-get -qq clean && \
    rm -rf /var/lib/apt/lists/*

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

# Use bash as default shell, rather than sh
ENV SHELL /bin/bash

# Set up users; main user is annika; other users on the
# docker are oliver and thomas
ENV NB_USER annika
#ENV NB_UID 1000
ENV USER ${NB_USER}
ENV HOME /home/${NB_USER}

RUN adduser --disabled-password \
    --ingroup users \
    --gecos "Default user" \
    --uid 1000 \
    ${NB_USER}

RUN adduser --disabled-password \
    --ingroup users \
    --gecos "Default user" \
    --uid 1001 \
    oliver

RUN adduser --disabled-password \
    --ingroup users \
    --gecos "Default user" \
    --uid  1002 \
    thomas

RUN wget --quiet -O - https://deb.nodesource.com/gpgkey/nodesource.gpg.key |  apt-key add - && \
    DISTRO="bionic" && \
    echo "deb https://deb.nodesource.com/node_10.x $DISTRO main" >> /etc/apt/sources.list.d/nodesource.list && \
    echo "deb-src https://deb.nodesource.com/node_10.x $DISTRO main" >> /etc/apt/sources.list.d/nodesource.list

# Base package installs are not super interesting to users, so hide their outputs
# If install fails for some reason, errors will still be printed
RUN apt-get -qq update && \
    apt-get -qq install --yes --no-install-recommends \
       less \
       nodejs \
       unzip \
       > /dev/null && \
    apt-get -qq purge && \
    apt-get -qq clean && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 8888

# Environment variables required for build
ENV APP_BASE /srv
ENV NPM_DIR ${APP_BASE}/npm
ENV NPM_CONFIG_GLOBALCONFIG ${NPM_DIR}/npmrc
ENV CONDA_DIR ${APP_BASE}/conda
ENV NB_PYTHON_PREFIX ${CONDA_DIR}/envs/notebook
ENV KERNEL_PYTHON_PREFIX ${NB_PYTHON_PREFIX}

# Special case PATH
ENV PATH ${NB_PYTHON_PREFIX}/bin:${CONDA_DIR}/bin:${NPM_DIR}/bin:${PATH}

# If scripts required during build are present, copy them
COPY binder/install-miniconda.bash /tmp/install-miniconda.bash
COPY binder/activate-conda.sh /etc/profile.d/activate-conda.sh
COPY binder/environment.frozen.yml /tmp/environment.yml

RUN mkdir -p ${NPM_DIR} && \
chown -R ${NB_USER}:users ${NPM_DIR}

USER ${NB_USER}
RUN npm config --global set prefix ${NPM_DIR}

USER root
RUN bash /tmp/install-miniconda.bash && \
rm /tmp/install-miniconda.bash /tmp/environment.yml



# Allow target path repo is cloned to be configurable
ARG REPO_DIR=${HOME}
ENV REPO_DIR ${REPO_DIR}
WORKDIR ${REPO_DIR}

# We want to allow two things:
#   1. If there's a .local/bin directory in the repo, things there
#      should automatically be in path
#   2. postBuild and users should be able to install things into ~/.local/bin
#      and have them be automatically in path
#
# The XDG standard suggests ~/.local/bin as the path for local user-specific
# installs. See https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
ENV PATH ${HOME}/.local/bin:${REPO_DIR}/.local/bin:${PATH}

# Copy and chown stuff. This doubles the size of the repo, because
# you can't actually copy as USER, only as root! Thanks, Docker!
USER root
COPY . ${REPO_DIR}
RUN chown -R ${NB_USER}:users ${REPO_DIR}

# fix the BUG in Ubuntu bionic image
RUN sed -i '/path-exclude=\/usr\/share\/man\/*/c\#path-exclude=\/usr\/share\/man\/*' /etc/dpkg/dpkg.cfg.d/excludes && \
  apt-get -qq update && \
  apt-get install --yes --no-install-recommends man manpages-posix && \
  dpkg -l | grep ^ii | cut -d' ' -f3 | xargs apt-get install -y --reinstall && \
  apt-get -qq purge && \
  apt-get -qq clean


# Run assemble scripts! These will actually build the specification
# in the repository into the image.
RUN test -f binder/apt.txt && apt-get -qq update && \
  apt-get install --yes --no-install-recommends `cat binder/apt.txt` && \
  apt-get -qq purge && \
  apt-get -qq clean && \
  rm -rf /var/lib/apt/lists/*

# setup the bash_calysto kernel. It is only available via pip
# but not from conda:
RUN test -f binder/requirements.txt && \
  pip install --no-cache-dir -r binder/requirements.txt

# uncomment the following line if you want to use bash_kernel
# instead of calysto_bash
# RUN python3 -m bash_kernel.install

# Add start script
# Add entrypoint
COPY binder/repo2docker-entrypoint /usr/local/bin/repo2docker-entrypoint
RUN chmod 755 /usr/local/bin/repo2docker-entrypoint

# We always want containers to run as non-root but as NB_USER:
USER ${NB_USER}:users

# remove unnecessary files within the docker:
RUN rm -rf binder
RUN rm -rf figuren-tikz-skripte
RUN rm -rf .git
RUN rm -rf tools
RUN rm README.md
RUN rm LICENSE.md
RUM rm AUTHORS.md

# modify .bashrc to immediately modify .bash_history after
# each command:
RUN echo "" >> .bashrc
RUN echo "shopt -s histappend" >> .bashrc
RUN echo 'PROMPT_COMMAND="history -a;$PROMPT_COMMAND"' >> .bashrc

ENTRYPOINT ["/usr/local/bin/repo2docker-entrypoint"]

# Specify the default command to run
CMD ["jupyter", "notebook", "--ip", "0.0.0.0"]
