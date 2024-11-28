# Use an Ubuntu base image
FROM ubuntu:20.04

# Set environment variables
ENV HADOOP_VERSION=3.3.6
ENV HADOOP_HOME=/usr/local/hadoop
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# Install necessary tools
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    openssh-server \
    wget \
    curl \
    vim && \
    mkdir /var/run/sshd && \
    echo 'root:root' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    service ssh start

# Download and install Hadoop
RUN wget https://downloads.apache.org/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz && \
    tar -xzf hadoop-$HADOOP_VERSION.tar.gz && \
    mv hadoop-$HADOOP_VERSION /usr/local/hadoop && \
    rm hadoop-$HADOOP_VERSION.tar.gz

# Configure environment variables for Hadoop
ENV PATH=$PATH:$JAVA_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Setup SSH for Hadoop
RUN ssh-keygen -t rsa -f /root/.ssh/id_rsa -q -N "" && \
    cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys

# Expose necessary ports
EXPOSE 50070 8088 8020 9000 9864 9866

# Start SSH service
CMD ["/usr/sbin/sshd", "-D"]
