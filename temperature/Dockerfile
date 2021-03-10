FROM balenalib/raspberrypi3-64:buster

RUN apt-get update && \
     apt-get install -y \
     ruby wget vim && \
     apt-get clean && \
     rm -rf /var/lib/apt/lists/*

RUN gem install bundler -v 2.1.4 --without test

WORKDIR /app

COPY Gemfile /app/Gemfile
COPY Gemfile.lock /app/Gemfile.lock
RUN bundle install

COPY sensor_read.rb /app

RUN useradd -ms /bin/bash weather
RUN chown -R weather:weather /app
USER weather

CMD [ "bundle", "exec", "ruby", "sensor_read.rb" ]
