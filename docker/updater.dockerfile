FROM alpine:latest
RUN apk add --no-cache bash bind-tools
COPY dns-updater.sh /dns-updater.sh
RUN chmod +x /dns-updater.sh
CMD ["/dns-updater.sh"]
