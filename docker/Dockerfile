FROM debian:11-slim AS get-mcbe-sever

ARG MCBE_SERVER_ZIP_PATH

RUN apt update && apt install -y curl unzip \
  # get server
  && curl -Lo server.zip ${MCBE_SERVER_ZIP_PATH} \
  && unzip -d bedrock server.zip


FROM debian:11-slim AS runner

COPY --from=get-mcbe-sever bedrock bedrock

RUN apt update \
  && apt install -y vim git gh curl tmux \
  && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/bin/bash", "-c"]
WORKDIR /bedrock
CMD [ "./run.sh" ]
